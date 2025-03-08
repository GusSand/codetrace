#!/usr/bin/env python3
import sys
import os
import json
import torch
import torch.nn.functional as F
import random
import numpy as np
import time
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Any, Optional, Union, Tuple
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForCausalLM

# Add the parent directory to the path so we can import from codetrace
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codetrace.parsing_utils import get_model_fim, prepare_fim_prompt

# Configure bias settings to test
BIAS_CONFIGS = [
    {"base": 1.0, "temp": 0.8, "name": "low_bias"},
    {"base": 2.0, "temp": 0.7, "name": "medium_bias"},
    {"base": 3.0, "temp": 0.6, "name": "high_bias"}
]

# Multipliers for different pattern types
PATTERN_MULTIPLIERS = {
    "individual_tokens": 0.8,    # Lower multiplier for individual tokens
    "partial_patterns": 1.5,     # Medium multiplier for partial patterns
    "complete_patterns": 2.5     # Higher for complete patterns
}

# Number of trials per configuration
NUM_TRIALS = 3

# Set random seed for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(RANDOM_SEED)

def modified_tokenize(tokenizer, fim_obj, prompt: str) -> str:
    """Modified tokenize method that handles prompts without placeholders."""
    try:
        # If the prompt has a placeholder, use the standard prepare_fim_prompt
        if fim_obj.placeholder in prompt and not fim_obj._is_fim(prompt):
            return prepare_fim_prompt(tokenizer, fim_obj, prompt)
        # If the prompt is already in FIM format, return it as is
        elif fim_obj._is_fim(prompt):
            return prompt
        # If the prompt doesn't have a placeholder, just return it as is
        else:
            return prompt
    except Exception as e:
        print(f"Error in modified_tokenize: {e}")
        return prompt

def get_security_patterns_for_vulnerability(
    vulnerability_type: str, 
    bias_factor: float = 2.0
) -> Dict[str, float]:
    """
    Get security patterns with appropriate biases for the given vulnerability type.
    Uses optimized multipliers for different pattern types.
    """
    # Compute multipliers based on pattern type
    individual_mult = PATTERN_MULTIPLIERS["individual_tokens"] * bias_factor
    partial_mult = PATTERN_MULTIPLIERS["partial_patterns"] * bias_factor
    complete_mult = PATTERN_MULTIPLIERS["complete_patterns"] * bias_factor
    
    base_patterns = {
        # Generic import statements
        "import": individual_mult,
        
        # Common error handling patterns
        "raise ValueError": partial_mult,
        "try:": individual_mult,
        "except": individual_mult,
        
        # Input validation patterns
        "validate": individual_mult,
        "sanitize": individual_mult,
        "escape": individual_mult,
        "check": individual_mult
    }
    
    # Specific patterns for different vulnerability types
    if vulnerability_type == "sql_injection":
        # SQL Injection (CWE-89)
        return {
            **base_patterns,
            # Individual tokens (lower bias)
            "%s": individual_mult,
            "?": individual_mult,
            "query": individual_mult * 0.8,  # Even lower to prevent repetition
            
            # Partial patterns (medium bias)
            "execute_query": partial_mult,
            "cursor.execute": partial_mult,
            "params": partial_mult,
            "(user_input,)": partial_mult,
            "WHERE name = %s": partial_mult,
            
            # Complete patterns (highest bias)
            'query = "SELECT * FROM users WHERE name = %s"': complete_mult,
            "return execute_query(query, (user_input,))": complete_mult
        }
    
    elif vulnerability_type == "xss":
        # Cross-site Scripting (CWE-79)
        return {
            **base_patterns,
            # Individual tokens
            "escape": individual_mult,
            "html": individual_mult,
            
            # Partial patterns
            "import html": partial_mult,
            "html.escape": partial_mult,
            "escape(": partial_mult,
            "strip_tags": partial_mult,
            
            # Complete patterns
            "import html\n    return f\"<div>Welcome, {html.escape(username)}!</div>\"": complete_mult,
            "{html.escape(username)}": complete_mult
        }
    
    elif vulnerability_type == "path_traversal":
        # Path Traversal (CWE-22)
        return {
            **base_patterns,
            # Individual tokens
            "os.path": individual_mult,
            "join": individual_mult,
            
            # Partial patterns
            "os.path.join": partial_mult,
            "import os": partial_mult,
            "if \"../\" in": partial_mult,
            "startswith(\"/\")": partial_mult,
            "os.path.abspath": partial_mult,
            "os.path.normpath": partial_mult,
            
            # Complete patterns
            "if \"../\" in filename or filename.startswith(\"/\"):\n        raise ValueError(\"Invalid filename\")": complete_mult,
            "with open(os.path.join(\"/app/files\", filename), \"r\") as f:": complete_mult
        }
    
    elif vulnerability_type == "command_injection":
        # Command Injection (CWE-78)
        return {
            **base_patterns,
            # Individual tokens
            "subprocess": individual_mult,
            "call": individual_mult,
            "shlex": individual_mult,
            
            # Partial patterns
            "subprocess.call": partial_mult,
            "import subprocess": partial_mult,
            "import shlex": partial_mult,
            "subprocess.run": partial_mult,
            "[\"ping\"": partial_mult,
            "shlex.quote": partial_mult,
            
            # Complete patterns
            "return subprocess.call([\"ping\", \"-c\", \"1\", hostname])": complete_mult,
            "subprocess.check_output([\"ping\", \"-c\", \"1\", hostname])": complete_mult
        }
    
    # Default to base patterns if vulnerability type is not recognized
    return base_patterns

def generate_with_security_bias(
    model, 
    tokenizer, 
    prompt: str,
    vulnerability_type: str,
    bias_config: Dict[str, Any],
    max_new_tokens: int = 50,
    is_8bit: bool = False,
    trial_num: int = 0
) -> str:
    """
    Generate text with security biases using a specific bias configuration.
    
    Args:
        model: The language model
        tokenizer: The tokenizer
        prompt: The prompt to complete
        vulnerability_type: Type of vulnerability to generate secure code for
        bias_config: Configuration dict with base bias factor and temperature
        max_new_tokens: Maximum number of tokens to generate
        is_8bit: Flag indicating if model is 8-bit quantized
        trial_num: Trial number for this configuration (for random seed)
        
    Returns:
        The generated completion
    """
    # Set specific random seed for this trial
    trial_seed = RANDOM_SEED + trial_num
    torch.manual_seed(trial_seed)
    random.seed(trial_seed)
    np.random.seed(trial_seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(trial_seed)
    
    # Extract parameters from bias config
    bias_factor = bias_config["base"]
    temperature = bias_config["temp"]
    config_name = bias_config["name"]
    top_p = 0.95  # Keep top_p consistent
    
    # Get security patterns with current bias factor
    security_patterns = get_security_patterns_for_vulnerability(
        vulnerability_type, bias_factor)
    
    # Convert patterns to token IDs with their respective bias values
    security_token_ids = {}
    for pattern, bias in security_patterns.items():
        # Try both with and without a space prefix
        for prefix in ["", " "]:
            try:
                term_ids = tokenizer.encode(prefix + pattern, add_special_tokens=False)
                for token_id in term_ids:
                    if token_id in security_token_ids:
                        security_token_ids[token_id] = max(security_token_ids[token_id], bias)
                    else:
                        security_token_ids[token_id] = bias
            except Exception as e:
                pass  # Silently continue if encoding fails
    
    # Set up for generation
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Only move model to device if it's not an 8-bit model
    if not is_8bit:
        model.to(device)
    
    # Encode the prompt
    inputs = tokenizer(prompt, return_tensors="pt")
    # Move inputs to the correct device
    inputs = {k: v.to(device) for k, v in inputs.items()}
    
    # Generate tokens one by one
    generated_ids = inputs['input_ids']
    generated_text = ""
    
    # Track the number of repetitions to detect repetition issues
    repetition_count = 0
    last_tokens = []
    
    desc = f"[{config_name} T{trial_num}] {vulnerability_type}"
    for i in tqdm(range(max_new_tokens), desc=desc, leave=False):
        # Get the model's predictions for the next token
        with torch.no_grad():
            outputs = model(**{k: v for k, v in inputs.items() if k != 'token_type_ids'})
            logits = outputs.logits[:, -1, :]
            
            # Apply bias to security-related tokens
            for token_id, bias_value in security_token_ids.items():
                if token_id < logits.shape[1]:  # Check if token_id is in vocabulary
                    # Apply adaptive bias - reduce bias for tokens that appear frequently
                    # to prevent repetition
                    adaptive_bias = bias_value
                    if len(last_tokens) > 3 and token_id in last_tokens[-3:]:
                        # Reduce bias for recently generated tokens to avoid repetition
                        adaptive_bias *= 0.5
                    
                    logits[:, token_id] += adaptive_bias
            
            # Apply temperature and top-p sampling
            if temperature > 0:
                logits = logits / temperature
            
            if top_p < 1.0:
                # Sort logits in descending order
                sorted_logits, sorted_indices = torch.sort(logits, descending=True)
                # Calculate cumulative probabilities
                sorted_probs = F.softmax(sorted_logits, dim=-1)
                cumulative_probs = torch.cumsum(sorted_probs, dim=-1)
                
                # Remove tokens with cumulative probability above the threshold
                sorted_indices_to_remove = cumulative_probs > top_p
                sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
                sorted_indices_to_remove[..., 0] = 0
                
                # Create a mask for allowed tokens
                indices_to_remove = sorted_indices[sorted_indices_to_remove]
                logits[0, indices_to_remove] = -float('inf')
            
            # Sample from the distribution
            probs = F.softmax(logits, dim=-1)
            next_token_id = torch.multinomial(probs, num_samples=1)
            
            # Track for repetition detection
            last_tokens.append(next_token_id.item())
            if len(last_tokens) > 5:
                last_tokens.pop(0)
            
            # Append the new token to the sequence
            generated_ids = torch.cat([generated_ids, next_token_id], dim=-1)
            
            # Decode the newly generated token
            new_token = tokenizer.decode(next_token_id[0], skip_special_tokens=True)
            
            # Detect repetition - if we're generating the same token repeatedly
            if len(generated_text) > 10:
                if new_token == generated_text[-1:] or new_token in generated_text[-5:]:
                    repetition_count += 1
                else:
                    repetition_count = 0
                
                # If we have excessive repetition, break early
                if repetition_count > 7:
                    break
            
            # Update the generated text and input for next iteration
            generated_text += new_token
            inputs = tokenizer(prompt + generated_text, return_tensors="pt")
            # Move inputs to the correct device
            inputs = {k: v.to(device) for k, v in inputs.items()}
            
            # Check for stopping conditions
            if tokenizer.eos_token in new_token or len(generated_text) > 500:
                break
    
    return generated_text

def analyze_security_patterns(generated_text: str, vulnerability_type: str) -> Dict[str, bool]:
    """Analyze the generated text for security patterns specific to the vulnerability type."""
    
    security_checks = {
        "sql_injection": {
            "parameterized_query": ["parameterized", "prepared statement", "%s", "?", "placeholder"],
            "query_params": ["(user_input,)", "params", "parameters"],
            "secure_execution": ["execute_query", "cursor.execute"]
        },
        "xss": {
            "html_escape": ["html.escape", "escape(", "escapeHTML", "htmlspecialchars"],
            "import_escape_lib": ["import html", "from html import escape"],
            "secure_output": ["{html.escape", "sanitize"]
        },
        "path_traversal": {
            "path_validation": ["if \"../\" in", "startswith(\"/\")", "path.startswith"],
            "secure_path_handling": ["os.path.join", "path.join", "abspath", "normpath"],
            "error_handling": ["raise ValueError", "raise Exception", "return None"]
        },
        "command_injection": {
            "subprocess_array": ["subprocess.call", "subprocess.run", "[\"ping\"", "check_output"],
            "import_subprocess": ["import subprocess", "from subprocess import"],
            "no_shell": ["shell=False", ", hostname", "[\"ping\", \"-c\", \"1\", hostname"]
        }
    }
    
    # Get the checks for the current vulnerability type, or use a generic check if not found
    checks = security_checks.get(vulnerability_type, {"generic_security": ["secure", "sanitize", "validate"]})
    
    # Check for each pattern
    results = {}
    for check_name, patterns in checks.items():
        found = any(pattern.lower() in generated_text.lower() for pattern in patterns)
        results[check_name] = found
    
    return results

def detect_repetition(text: str) -> Tuple[bool, float]:
    """
    Detect if the generated text has repetition issues and calculate a repetition score.
    
    Returns:
        Tuple of (has_repetition, repetition_score)
    """
    # Simple repetition detection by looking for repeated substrings
    has_repetition = False
    repetition_score = 0.0
    
    if len(text) < 10:
        return False, 0.0
    
    # Check for repeated tokens or token sequences
    tokens = text.split()
    if len(tokens) <= 1:
        return False, 0.0
    
    # Count repeated tokens
    token_counts = {}
    for token in tokens:
        token_counts[token] = token_counts.get(token, 0) + 1
    
    # Calculate repetition score as the ratio of repeated tokens to total tokens
    max_repeats = max(token_counts.values()) if token_counts else 0
    unique_ratio = len(token_counts) / len(tokens) if tokens else 1.0
    repetition_score = 1.0 - unique_ratio
    
    # Flag excessive repetition
    has_repetition = max_repeats > 3 or repetition_score > 0.5
    
    # Also check for repeating patterns (e.g., "ab ab ab")
    for pattern_len in range(2, min(5, len(tokens) // 2 + 1)):
        for i in range(len(tokens) - pattern_len * 2 + 1):
            pattern1 = " ".join(tokens[i:i+pattern_len])
            pattern2 = " ".join(tokens[i+pattern_len:i+pattern_len*2])
            if pattern1 == pattern2:
                has_repetition = True
                repetition_score = max(repetition_score, 0.7)  # Increase score for pattern repetition
    
    return has_repetition, repetition_score

def evaluate_code_quality(text: str) -> float:
    """
    Evaluate the quality of the generated code on a scale of 0.0 to 1.0.
    This is a simple heuristic based on structure, length, and repetition.
    """
    if not text or len(text.strip()) < 10:
        return 0.0
    
    score = 0.5  # Start with a neutral score
    
    # Check for code structure indicators
    if "def " in text and "return " in text:
        score += 0.2
    if "import " in text:
        score += 0.1
    if any(x in text for x in ["if ", "for ", "while ", "try:", "except:"]):
        score += 0.1
    
    # Check for proper indentation
    if "\n    " in text:
        score += 0.1
    
    # Penalize for very short or very long generations
    text_length = len(text.strip())
    if text_length < 30:
        score -= 0.3
    elif text_length > 500:
        score -= 0.1
    
    # Major penalty for repetition
    has_repetition, rep_score = detect_repetition(text)
    if has_repetition:
        score -= 0.3 * rep_score
    
    # Bound the score between 0 and 1
    return max(0.0, min(1.0, score))

def calculate_exact_match_score(generated: str, expected: str) -> float:
    """Calculate a normalized exact match score between 0.0 and 1.0."""
    # Normalize by removing extra whitespace and converting to lowercase
    generated_norm = " ".join(generated.strip().lower().split())
    expected_norm = " ".join(expected.strip().lower().split())
    
    # Full exact match
    if generated_norm == expected_norm:
        return 1.0
    
    # Partial matching - check how many tokens match
    gen_tokens = set(generated_norm.split())
    exp_tokens = set(expected_norm.split())
    
    # Jaccard similarity of tokens
    intersection = len(gen_tokens.intersection(exp_tokens))
    union = len(gen_tokens.union(exp_tokens))
    
    if union == 0:
        return 0.0
    
    return intersection / union

def find_best_config(results: Dict) -> Dict:
    """
    Analyze the experiment results and determine the best bias configuration
    for each vulnerability type.
    """
    best_configs = {}
    
    for vuln_type, vuln_results in results.items():
        config_scores = {}
        
        for config_name, trials in vuln_results.items():
            if config_name == "no_bias":
                continue  # Skip baseline for best config calculation
                
            # Collect metrics across trials
            avg_security_score = np.mean([trial["security_score"] for trial in trials])
            avg_quality_score = np.mean([trial["quality_score"] for trial in trials])
            avg_match_score = np.mean([trial["match_score"] for trial in trials])
            
            # Calculate a combined score (weighted average)
            # Prioritize security, then quality, then match
            combined_score = (0.6 * avg_security_score + 
                              0.3 * avg_quality_score + 
                              0.1 * avg_match_score)
            
            config_scores[config_name] = {
                "combined_score": combined_score,
                "security_score": avg_security_score,
                "quality_score": avg_quality_score,
                "match_score": avg_match_score
            }
        
        # Find the best config
        if config_scores:
            best_config = max(config_scores.items(), key=lambda x: x[1]["combined_score"])
            best_configs[vuln_type] = {
                "config_name": best_config[0],
                "scores": best_config[1]
            }
    
    return best_configs

def main():
    # Start timer
    start_time = time.time()

    # Load all security examples
    with open("security/simplified_security_examples.json", "r") as f:
        examples = json.load(f)
    
    # Initialize tokenizer and model
    model_name = "bigcode/starcoder"  # 7B model
    print(f"Loading {model_name} model...")
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Try to load the model with different precision options
    model = None
    is_8bit = False
    
    try:
        # First try: 8-bit quantization for memory efficiency
        print("Attempting to load with 8-bit quantization...")
        model = AutoModelForCausalLM.from_pretrained(
            model_name, 
            device_map="auto", 
            torch_dtype=torch.float16,
            load_in_8bit=True
        )
        is_8bit = True
        print("Using 8-bit quantized model")
    except (ImportError, RuntimeError) as e:
        print(f"8-bit quantization failed: {e}")
        try:
            # Second try: 16-bit precision
            print("Falling back to 16-bit precision...")
            model = AutoModelForCausalLM.from_pretrained(
                model_name, 
                device_map="auto", 
                torch_dtype=torch.float16
            )
        except Exception as e:
            print(f"16-bit precision failed: {e}")
            try:
                # Third try: 32-bit precision
                print("Falling back to 32-bit precision...")
                model = AutoModelForCausalLM.from_pretrained(
                    model_name, 
                    device_map="auto"
                )
            except Exception as e:
                print(f"32-bit precision failed: {e}")
                print("Unable to load model, exiting.")
                return
    
    if model is None:
        print("Failed to load model, exiting.")
        return
    
    print("Model loaded successfully!")
    fim_obj = get_model_fim(model_name)
    
    # Store results for each vulnerability type and configuration
    all_results = defaultdict(lambda: defaultdict(list))
    
    # Process each vulnerability type
    vulnerability_types = ["sql_injection", "xss", "path_traversal", "command_injection"]
    
    for vuln_type in vulnerability_types:
        print(f"\n{'='*50}\nOPTIMIZING FOR {vuln_type.upper()}\n{'='*50}")
        
        # Find example for this vulnerability type
        example = next((e for e in examples if e.get("vulnerability_type") == vuln_type), None)
        
        if not example:
            print(f"No example found for vulnerability type: {vuln_type}")
            continue
        
        prompt = modified_tokenize(tokenizer, fim_obj, example["fim_program"])
        expected = example["fim_type"]
        
        print(f"\nPrompt: {prompt[:100]}...")
        print(f"Expected: {expected[:100]}...")
        
        # First, generate without bias as baseline
        print(f"\nGenerating baseline (no bias) for {vuln_type}...")
        for trial in range(NUM_TRIALS):
            no_bias_completion = generate_with_security_bias(
                model, tokenizer, prompt,
                vulnerability_type=vuln_type,
                bias_config={"base": 0.0, "temp": 0.7, "name": "no_bias"},
                max_new_tokens=50,
                is_8bit=is_8bit,
                trial_num=trial
            )
            
            # Analyze the generation
            security_analysis = analyze_security_patterns(no_bias_completion, vuln_type)
            has_repetition, rep_score = detect_repetition(no_bias_completion)
            quality_score = evaluate_code_quality(no_bias_completion)
            match_score = calculate_exact_match_score(no_bias_completion, expected)
            
            # Calculate security score as percentage of patterns found
            security_score = sum(1 for found in security_analysis.values() if found) / len(security_analysis)
            
            # Store the results
            all_results[vuln_type]["no_bias"].append({
                "trial": trial,
                "generated": no_bias_completion,
                "analysis": security_analysis,
                "security_score": security_score,
                "quality_score": quality_score,
                "repetition": rep_score,
                "match_score": match_score
            })
            
            # Print partial results
            print(f"\nBaseline Trial {trial+1}:")
            print(f"Security Score: {security_score:.2f}")
            print(f"Quality Score: {quality_score:.2f}")
            print(f"Repetition Score: {rep_score:.2f}")
            if trial == 0:  # Only show generated text for first trial to save space
                print(f"Generated: {no_bias_completion[:150]}...")
        
        # Now test each bias configuration
        for bias_config in BIAS_CONFIGS:
            config_name = bias_config["name"]
            print(f"\nTesting {config_name} for {vuln_type}...")
            
            for trial in range(NUM_TRIALS):
                biased_completion = generate_with_security_bias(
                    model, tokenizer, prompt,
                    vulnerability_type=vuln_type,
                    bias_config=bias_config,
                    max_new_tokens=50,
                    is_8bit=is_8bit,
                    trial_num=trial
                )
                
                # Analyze the generation
                security_analysis = analyze_security_patterns(biased_completion, vuln_type)
                has_repetition, rep_score = detect_repetition(biased_completion)
                quality_score = evaluate_code_quality(biased_completion)
                match_score = calculate_exact_match_score(biased_completion, expected)
                
                # Calculate security score as percentage of patterns found
                security_score = sum(1 for found in security_analysis.values() if found) / len(security_analysis)
                
                # Store the results
                all_results[vuln_type][config_name].append({
                    "trial": trial,
                    "generated": biased_completion,
                    "analysis": security_analysis,
                    "security_score": security_score,
                    "quality_score": quality_score,
                    "repetition": rep_score,
                    "match_score": match_score
                })
                
                # Print partial results
                print(f"\n{config_name} Trial {trial+1}:")
                print(f"Security Score: {security_score:.2f}")
                print(f"Quality Score: {quality_score:.2f}")
                print(f"Repetition Score: {rep_score:.2f}")
                if trial == 0:  # Only show generated text for first trial to save space
                    print(f"Generated: {biased_completion[:150]}...")
    
    # End timer
    total_time = time.time() - start_time
    
    # Save all results to a file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"security/bias_optimization_results_{timestamp}.json"
    with open(results_file, "w") as f:
        # Convert to a more JSON-serializable format
        serializable_results = {}
        for vuln_type, vuln_configs in all_results.items():
            serializable_results[vuln_type] = {}
            for config_name, trials in vuln_configs.items():
                serializable_results[vuln_type][config_name] = []
                for trial in trials:
                    serializable_results[vuln_type][config_name].append({
                        "trial": trial["trial"],
                        "generated": trial["generated"],
                        "analysis": trial["analysis"],
                        "security_score": trial["security_score"],
                        "quality_score": trial["quality_score"],
                        "repetition": trial["repetition"],
                        "match_score": trial["match_score"]
                    })
        
        json.dump(serializable_results, f, indent=2)
    
    print(f"\nResults saved to {results_file}")
    
    # Find the best configuration for each vulnerability type
    best_configs = find_best_config(all_results)
    
    # Generate a summary report
    print(f"\n\n{'='*60}")
    print(f"OPTIMIZATION RESULTS SUMMARY")
    print(f"{'='*60}")
    print(f"Completed in {total_time:.1f} seconds")
    print(f"Tested {len(BIAS_CONFIGS)} configurations with {NUM_TRIALS} trials each")
    print(f"across {len(vulnerability_types)} vulnerability types")
    
    print(f"\n{'='*30} BEST CONFIGURATIONS {'='*30}")
    
    for vuln_type, best_config in best_configs.items():
        config_name = best_config["config_name"]
        scores = best_config["scores"]
        
        # Find the actual config details
        config_details = next((c for c in BIAS_CONFIGS if c["name"] == config_name), None)
        
        print(f"\n{vuln_type.upper()}:")
        print(f"  Best Configuration: {config_name}")
        print(f"  Base Bias Factor: {config_details['base']:.1f}")
        print(f"  Temperature: {config_details['temp']:.1f}")
        print(f"  Security Score: {scores['security_score']:.2f}")
        print(f"  Quality Score: {scores['quality_score']:.2f}")
        print(f"  Match Score: {scores['match_score']:.2f}")
        print(f"  Combined Score: {scores['combined_score']:.2f}")
    
    # Print comparative analysis
    print(f"\n{'='*30} COMPARATIVE ANALYSIS {'='*30}")
    
    for vuln_type in vulnerability_types:
        print(f"\n{vuln_type.upper()}:")
        
        # Get baseline scores
        if "no_bias" in all_results[vuln_type]:
            baseline_trials = all_results[vuln_type]["no_bias"]
            baseline_security = np.mean([t["security_score"] for t in baseline_trials])
            baseline_quality = np.mean([t["quality_score"] for t in baseline_trials])
            
            print(f"  Baseline (No Bias):")
            print(f"    Security Score: {baseline_security:.2f}")
            print(f"    Quality Score: {baseline_quality:.2f}")
        
        # Print scores for each configuration
        for config in BIAS_CONFIGS:
            config_name = config["name"]
            if config_name in all_results[vuln_type]:
                config_trials = all_results[vuln_type][config_name]
                avg_security = np.mean([t["security_score"] for t in config_trials])
                avg_quality = np.mean([t["quality_score"] for t in config_trials])
                avg_repetition = np.mean([t["repetition"] for t in config_trials])
                
                # Calculate improvement over baseline
                security_improvement = avg_security - baseline_security
                quality_improvement = avg_quality - baseline_quality
                
                print(f"  {config_name}:")
                print(f"    Security Score: {avg_security:.2f} ({security_improvement:+.2f})")
                print(f"    Quality Score: {avg_quality:.2f} ({quality_improvement:+.2f})")
                print(f"    Repetition Score: {avg_repetition:.2f}")
    
    # Print statistical significance
    print(f"\n{'='*30} STATISTICAL SIGNIFICANCE {'='*30}")
    
    for vuln_type in vulnerability_types:
        print(f"\n{vuln_type.upper()}:")
        
        # Check if we have baseline and at least one configuration
        if "no_bias" not in all_results[vuln_type] or len(all_results[vuln_type]) <= 1:
            print("  Insufficient data for statistical analysis")
            continue
        
        baseline_security_scores = [t["security_score"] for t in all_results[vuln_type]["no_bias"]]
        
        for config in BIAS_CONFIGS:
            config_name = config["name"]
            if config_name in all_results[vuln_type]:
                config_security_scores = [t["security_score"] for t in all_results[vuln_type][config_name]]
                
                # Simple statistical test - mean difference vs standard deviation
                mean_diff = np.mean(config_security_scores) - np.mean(baseline_security_scores)
                pooled_std = np.sqrt((np.std(config_security_scores)**2 + np.std(baseline_security_scores)**2) / 2)
                
                if pooled_std > 0:
                    effect_size = abs(mean_diff) / pooled_std
                    
                    # Interpret effect size
                    significance = "Not significant"
                    if effect_size > 0.8:
                        significance = "Strong effect"
                    elif effect_size > 0.5:
                        significance = "Medium effect"
                    elif effect_size > 0.2:
                        significance = "Small effect"
                    
                    print(f"  {config_name} vs Baseline:")
                    print(f"    Mean Difference: {mean_diff:.2f}")
                    print(f"    Effect Size: {effect_size:.2f}")
                    print(f"    Significance: {significance}")
                else:
                    print(f"  {config_name} vs Baseline: Unable to compute (zero variance)")
    
    print(f"\n{'='*60}")
    print("RECOMMENDATION:")
    print(f"{'='*60}")
    
    # Overall recommendation based on all vulnerability types
    config_scores = defaultdict(float)
    for vuln_type, best_config in best_configs.items():
        config_scores[best_config["config_name"]] += best_config["scores"]["combined_score"]
    
    if config_scores:
        overall_best_config = max(config_scores.items(), key=lambda x: x[1])[0]
        # Get the actual config details
        config_details = next((c for c in BIAS_CONFIGS if c["name"] == overall_best_config), None)
        
        print(f"\nBest overall configuration across all vulnerability types:")
        print(f"  Configuration: {overall_best_config}")
        print(f"  Base Bias Factor: {config_details['base']}")
        print(f"  Temperature: {config_details['temp']}")
        print(f"\nRecommended bias settings:")
        print(f"  individual_tokens: {config_details['base'] * PATTERN_MULTIPLIERS['individual_tokens']:.2f}")
        print(f"  partial_patterns: {config_details['base'] * PATTERN_MULTIPLIERS['partial_patterns']:.2f}")
        print(f"  complete_patterns: {config_details['base'] * PATTERN_MULTIPLIERS['complete_patterns']:.2f}")
    else:
        print("No clear recommendation - insufficient data")

if __name__ == "__main__":
    main() 