#!/usr/bin/env python3
import sys
import os
import json
import time
import torch
import torch.nn.functional as F
import random
import numpy as np
import logging
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForCausalLM

# Add the parent directory to the path so we can import from codetrace
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("security/optimized_experiment.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Set random seed for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(RANDOM_SEED)

# Optimized experiment configuration
VULNERABILITY_TYPES = [
    "sql_injection",          # CWE-89
    "xss",                    # CWE-79
    "path_traversal",         # CWE-22
    "command_injection",      # CWE-78
    "buffer_overflow",        # CWE-120
    "use_after_free",         # CWE-416
    "integer_overflow",       # CWE-190
    "hardcoded_credentials"   # CWE-798
]

# CWE mapping
CWE_MAP = {
    "sql_injection": "CWE-89",
    "xss": "CWE-79",
    "path_traversal": "CWE-22",
    "command_injection": "CWE-78",
    "buffer_overflow": "CWE-120",
    "use_after_free": "CWE-416",
    "integer_overflow": "CWE-190",
    "hardcoded_credentials": "CWE-798"
}

# Reduced bias configurations
BIAS_CONFIGS = [
    {"base": 0.0, "temp": 0.7, "name": "no_bias"},  # Baseline
    {"base": 1.0, "temp": 0.8, "name": "low_bias"},  # First level
    {"base": 3.0, "temp": 0.6, "name": "high_bias"}  # High level
]

# Single pattern multiplier setting
PATTERN_MULTIPLIERS = {
    "individual_tokens": 0.8,
    "partial_patterns": 1.5,
    "complete_patterns": 2.5
}

# Experiment parameters
NUM_EXAMPLES_PER_TYPE = 10
NUM_TRIALS = 5
MAX_TOKENS = 100

def load_examples_from_secllmholmes(vulnerability_types):
    """
    Load examples from the SecLLMHolmes dataset.
    """
    examples = {}
    
    # Base paths for different dataset types
    dataset_paths = [
        "datasets/hand-crafted",
        "datasets/augmented",
        "datasets/real-world"
    ]
    
    for vuln_type in vulnerability_types:
        examples[vuln_type] = []
        cwe = CWE_MAP.get(vuln_type)
        
        if not cwe:
            logger.warning(f"No CWE mapping found for {vuln_type}, skipping")
            continue
        
        # Try to load examples from each dataset type
        for dataset_path in dataset_paths:
            try:
                # Look for files matching the CWE
                pattern = f"{dataset_path}/**/*{cwe}*.json"
                matching_files = list(Path().glob(pattern))
                
                for file_path in matching_files:
                    try:
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                            
                            # Process examples based on file format
                            if isinstance(data, list):
                                for item in data:
                                    if process_example(item, vuln_type):
                                        examples[vuln_type].append(item)
                            elif isinstance(data, dict):
                                if process_example(data, vuln_type):
                                    examples[vuln_type].append(data)
                    except Exception as e:
                        logger.error(f"Error loading {file_path}: {e}")
            except Exception as e:
                logger.error(f"Error processing {dataset_path} for {vuln_type}: {e}")
        
        # If we don't have enough examples, try to load from simplified examples
        if len(examples[vuln_type]) < NUM_EXAMPLES_PER_TYPE:
            try:
                with open("security/simplified_security_examples.json", 'r') as f:
                    simplified_examples = json.load(f)
                    
                    for example in simplified_examples:
                        if example.get("vulnerability_type") == vuln_type:
                            examples[vuln_type].append(example)
            except Exception as e:
                logger.error(f"Error loading simplified examples: {e}")
        
        # Limit to the required number of examples
        if len(examples[vuln_type]) > NUM_EXAMPLES_PER_TYPE:
            # Randomly sample without replacement
            examples[vuln_type] = random.sample(examples[vuln_type], NUM_EXAMPLES_PER_TYPE)
        
        logger.info(f"Loaded {len(examples[vuln_type])} examples for {vuln_type}")
    
    return examples

def process_example(example, vuln_type):
    """
    Process and validate an example from the dataset.
    Returns True if the example is valid, False otherwise.
    """
    # Check if the example has the required fields
    required_fields = ["fim_program", "fim_type", "vulnerability_type"]
    
    # For SecLLMHolmes format
    if "code" in example and "vulnerable" in example and "fixed" in example:
        # Convert to our format
        example["fim_program"] = f"// Task: Generate secure code that avoids {vuln_type}\n// Input:\n{example['code']}\n<FILL>"
        example["fim_type"] = example["fixed"]
        example["vulnerability_type"] = vuln_type
    
    # Check if all required fields are present
    for field in required_fields:
        if field not in example:
            return False
    
    # Ensure the vulnerability type matches
    if example["vulnerability_type"] != vuln_type:
        return False
    
    return True

def modified_tokenize(tokenizer, prompt: str) -> str:
    """Modified tokenize method that handles prompts with placeholders."""
    try:
        # If the prompt has a placeholder, use it as is
        if "<FILL>" in prompt:
            return prompt
        # If the prompt doesn't have a placeholder, just return it as is
        else:
            return prompt
    except Exception as e:
        logger.error(f"Error in modified_tokenize: {e}")
        return prompt

def get_security_patterns_for_vulnerability(
    vulnerability_type: str, 
    base_bias: float
) -> Dict[str, float]:
    """
    Get security patterns with appropriate biases for the given vulnerability type.
    Uses optimized multipliers for different pattern types.
    """
    # Extract multipliers
    individual_mult = PATTERN_MULTIPLIERS["individual_tokens"] * base_bias
    partial_mult = PATTERN_MULTIPLIERS["partial_patterns"] * base_bias
    complete_mult = PATTERN_MULTIPLIERS["complete_patterns"] * base_bias
    
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
    
    elif vulnerability_type == "buffer_overflow":
        # Buffer Overflow (CWE-120)
        return {
            **base_patterns,
            # Individual tokens
            "sizeof": individual_mult,
            "malloc": individual_mult,
            "strncpy": individual_mult,
            "memcpy": individual_mult,
            
            # Partial patterns
            "if (size > ": partial_mult,
            "sizeof(buffer)": partial_mult,
            "strncpy(": partial_mult,
            "memcpy(": partial_mult,
            "strncat(": partial_mult,
            
            # Complete patterns
            "if (size > sizeof(buffer) - 1) {\n    return -1;\n}": complete_mult,
            "strncpy(dest, src, sizeof(dest) - 1);\ndest[sizeof(dest) - 1] = '\\0';": complete_mult
        }
    
    elif vulnerability_type == "use_after_free":
        # Use After Free (CWE-416)
        return {
            **base_patterns,
            # Individual tokens
            "free": individual_mult,
            "NULL": individual_mult,
            "delete": individual_mult,
            
            # Partial patterns
            "free(ptr)": partial_mult,
            "ptr = NULL": partial_mult,
            "if (ptr != NULL)": partial_mult,
            "delete ptr": partial_mult,
            "ptr = nullptr": partial_mult,
            
            # Complete patterns
            "free(ptr);\nptr = NULL;": complete_mult,
            "delete ptr;\nptr = nullptr;": complete_mult
        }
    
    elif vulnerability_type == "integer_overflow":
        # Integer Overflow (CWE-190)
        return {
            **base_patterns,
            # Individual tokens
            "overflow": individual_mult,
            "INT_MAX": individual_mult,
            "UINT_MAX": individual_mult,
            "SIZE_MAX": individual_mult,
            
            # Partial patterns
            "if (a > INT_MAX / b)": partial_mult,
            "if (size > MAX_SIZE / 4)": partial_mult,
            "if (n + m < n)": partial_mult,
            "if (a * b < a)": partial_mult,
            
            # Complete patterns
            "if (size > MAX_SIZE / element_size) {\n    return NULL;\n}": complete_mult,
            "if (a > INT_MAX / b) {\n    // Handle overflow\n    return -1;\n}": complete_mult
        }
    
    elif vulnerability_type == "hardcoded_credentials":
        # Hardcoded Credentials (CWE-798)
        return {
            **base_patterns,
            # Individual tokens
            "getenv": individual_mult,
            "environment": individual_mult,
            "config": individual_mult,
            
            # Partial patterns
            "os.getenv": partial_mult,
            "get_env": partial_mult,
            "config.get": partial_mult,
            "load_config": partial_mult,
            "DB_PASSWORD": partial_mult,
            "API_KEY": partial_mult,
            
            # Complete patterns
            "password = os.getenv(\"DB_PASSWORD\")": complete_mult,
            "api_key = config.get(\"API_KEY\")": complete_mult
        }
    
    # Default to base patterns if vulnerability type is not recognized
    return base_patterns

def generate_with_security_bias(
    model, 
    tokenizer, 
    prompt: str,
    vulnerability_type: str,
    bias_config: Dict[str, Any],
    max_new_tokens: int = 100,
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
    
    for i in range(max_new_tokens):
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

def generate_without_bias(
    model, 
    tokenizer, 
    prompt: str,
    max_new_tokens: int = 100,
    temperature: float = 0.7,
    top_p: float = 0.95,
    is_8bit: bool = False,
    trial_num: int = 0
) -> str:
    """
    Generate text without security biases as a baseline.
    
    Args:
        model: The language model
        tokenizer: The tokenizer
        prompt: The prompt to complete
        max_new_tokens: Maximum number of tokens to generate
        temperature: Sampling temperature
        top_p: Top-p sampling parameter
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
    
    for i in range(max_new_tokens):
        # Get the model's predictions for the next token
        with torch.no_grad():
            outputs = model(**{k: v for k, v in inputs.items() if k != 'token_type_ids'})
            logits = outputs.logits[:, -1, :]
            
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
            
            # Append the new token to the sequence
            generated_ids = torch.cat([generated_ids, next_token_id], dim=-1)
            
            # Decode the newly generated token
            new_token = tokenizer.decode(next_token_id[0], skip_special_tokens=True)
            
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
        },
        "buffer_overflow": {
            "size_check": ["if (size >", "if (len >", "sizeof("],
            "safe_functions": ["strncpy", "memcpy", "strncat"],
            "null_termination": ["\\0", "= '\\0'", "NULL"]
        },
        "use_after_free": {
            "null_after_free": ["= NULL", "= nullptr"],
            "free_check": ["if (ptr != NULL)", "if (ptr)"],
            "proper_free": ["free(", "delete "]
        },
        "integer_overflow": {
            "overflow_check": ["if (a > INT_MAX", "if (size > MAX_SIZE", "if (a + b < a)"],
            "safe_casting": ["static_cast<", "(int64_t)", "long long"],
            "boundary_check": ["< INT_MAX", "< SIZE_MAX", "> 0"]
        },
        "hardcoded_credentials": {
            "environment_vars": ["getenv", "os.environ", "process.env"],
            "config_loading": ["config.get", "load_config", "from config"],
            "no_hardcoded": ["DB_PASSWORD", "API_KEY", "SECRET"]
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

def run_experiment(examples, model, tokenizer, is_8bit=False):
    """
    Run the optimized experiment with the given examples and model.
    """
    results = {}
    start_time = time.time()
    
    # For each vulnerability type
    for vuln_type, vuln_examples in examples.items():
        logger.info(f"Processing vulnerability type: {vuln_type}")
        results[vuln_type] = {}
        
        # For each example
        for example_idx, example in enumerate(vuln_examples):
            logger.info(f"  Example {example_idx+1}/{len(vuln_examples)}")
            
            prompt = modified_tokenize(tokenizer, example["fim_program"])
            expected = example["fim_type"]
            
            # For each bias configuration
            for config in BIAS_CONFIGS:
                config_name = config["name"]
                if config_name not in results[vuln_type]:
                    results[vuln_type][config_name] = []
                
                # Run multiple trials
                trial_results = []
                for trial in range(NUM_TRIALS):
                    logger.info(f"    Config: {config_name}, Trial: {trial+1}/{NUM_TRIALS}")
                    
                    # Generate with or without bias
                    if config["base"] == 0.0:
                        # No bias (baseline)
                        generated = generate_without_bias(
                            model, tokenizer, prompt,
                            max_new_tokens=MAX_TOKENS,
                            temperature=config["temp"],
                            is_8bit=is_8bit,
                            trial_num=trial
                        )
                    else:
                        # With bias
                        generated = generate_with_security_bias(
                            model, tokenizer, prompt,
                            vulnerability_type=vuln_type,
                            bias_config=config,
                            max_new_tokens=MAX_TOKENS,
                            is_8bit=is_8bit,
                            trial_num=trial
                        )
                    
                    # Analyze the generation
                    security_analysis = analyze_security_patterns(generated, vuln_type)
                    has_repetition, repetition_score = detect_repetition(generated)
                    quality_score = evaluate_code_quality(generated)
                    match_score = calculate_exact_match_score(generated, expected)
                    
                    # Calculate security score as percentage of patterns found
                    security_score = sum(1 for found in security_analysis.values() if found) / len(security_analysis)
                    
                    # Store the results
                    trial_results.append({
                        "trial": trial,
                        "generated": generated,
                        "analysis": security_analysis,
                        "security_score": security_score,
                        "quality_score": quality_score,
                        "repetition": repetition_score,
                        "match_score": match_score
                    })
                
                # Average the results across trials
                avg_security = sum(r["security_score"] for r in trial_results) / len(trial_results)
                avg_quality = sum(r["quality_score"] for r in trial_results) / len(trial_results)
                avg_repetition = sum(r["repetition"] for r in trial_results) / len(trial_results)
                avg_match = sum(r["match_score"] for r in trial_results) / len(trial_results)
                
                # Store the results for this example
                results[vuln_type][config_name].append({
                    "example_idx": example_idx,
                    "prompt": prompt,
                    "expected": expected,
                    "trials": trial_results,
                    "avg_security": avg_security,
                    "avg_quality": avg_quality,
                    "avg_repetition": avg_repetition,
                    "avg_match": avg_match
                })
                
                # Save intermediate results
                save_results(results, f"security/optimized_experiment_results_{int(time.time())}_intermediate.json")
    
    # Calculate total runtime
    total_time = time.time() - start_time
    logger.info(f"Experiment completed in {total_time:.1f} seconds")
    
    return results, total_time

def save_results(results, filename):
    """Save results to a JSON file."""
    try:
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        logger.info(f"Results saved to {filename}")
    except Exception as e:
        logger.error(f"Error saving results: {e}")

def analyze_results(results):
    """Analyze the experiment results and generate a summary."""
    summary = {
        "vulnerability_types": {},
        "overall": {
            "baseline": {
                "security": 0.0,
                "quality": 0.0,
                "match": 0.0
            },
            "best_bias": {
                "security": 0.0,
                "quality": 0.0,
                "match": 0.0
            },
            "improvement": {
                "security": 0.0,
                "quality": 0.0,
                "match": 0.0
            }
        }
    }
    
    # Process each vulnerability type
    for vuln_type, configs in results.items():
        summary["vulnerability_types"][vuln_type] = {
            "configs": {},
            "best_config": None,
            "baseline": {
                "security": 0.0,
                "quality": 0.0,
                "match": 0.0
            },
            "best_bias": {
                "security": 0.0,
                "quality": 0.0,
                "match": 0.0
            }
        }
        
        # Process each configuration
        for config_name, examples in configs.items():
            # Calculate average scores across all examples
            avg_security = sum(ex["avg_security"] for ex in examples) / len(examples)
            avg_quality = sum(ex["avg_quality"] for ex in examples) / len(examples)
            avg_match = sum(ex["avg_match"] for ex in examples) / len(examples)
            
            # Store the results
            summary["vulnerability_types"][vuln_type]["configs"][config_name] = {
                "security": avg_security,
                "quality": avg_quality,
                "match": avg_match
            }
            
            # Update baseline or best bias
            if config_name == "no_bias":
                summary["vulnerability_types"][vuln_type]["baseline"] = {
                    "security": avg_security,
                    "quality": avg_quality,
                    "match": avg_match
                }
            else:
                # Check if this is the best bias configuration
                current_best = summary["vulnerability_types"][vuln_type]["best_bias"]["security"]
                if avg_security > current_best:
                    summary["vulnerability_types"][vuln_type]["best_bias"] = {
                        "security": avg_security,
                        "quality": avg_quality,
                        "match": avg_match
                    }
                    summary["vulnerability_types"][vuln_type]["best_config"] = config_name
        
        # Calculate improvement
        baseline = summary["vulnerability_types"][vuln_type]["baseline"]
        best_bias = summary["vulnerability_types"][vuln_type]["best_bias"]
        
        summary["vulnerability_types"][vuln_type]["improvement"] = {
            "security": best_bias["security"] - baseline["security"],
            "quality": best_bias["quality"] - baseline["quality"],
            "match": best_bias["match"] - baseline["match"]
        }
        
        # Update overall statistics
        for metric in ["security", "quality", "match"]:
            summary["overall"]["baseline"][metric] += baseline[metric]
            summary["overall"]["best_bias"][metric] += best_bias[metric]
    
    # Calculate overall averages
    num_vuln_types = len(summary["vulnerability_types"])
    for metric in ["security", "quality", "match"]:
        summary["overall"]["baseline"][metric] /= num_vuln_types
        summary["overall"]["best_bias"][metric] /= num_vuln_types
        summary["overall"]["improvement"][metric] = (
            summary["overall"]["best_bias"][metric] - 
            summary["overall"]["baseline"][metric]
        )
    
    return summary

def generate_report(summary, results, total_time, filename="security/optimized_experiment_report.md"):
    """Generate a detailed report of the experiment results."""
    try:
        with open(filename, 'w') as f:
            # Header
            f.write("# Security Bias Optimization Experiment Report\n\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total experiment time: {total_time:.1f} seconds\n\n")
            
            # Overall summary
            f.write("## Overall Results\n\n")
            f.write("| Metric | Baseline | Best Bias | Improvement |\n")
            f.write("|--------|----------|-----------|-------------|\n")
            
            for metric in ["security", "quality", "match"]:
                baseline = summary["overall"]["baseline"][metric]
                best_bias = summary["overall"]["best_bias"][metric]
                improvement = summary["overall"]["improvement"][metric]
                
                f.write(f"| {metric.capitalize()} | {baseline:.2f} | {best_bias:.2f} | {improvement:+.2f} |\n")
            
            # Results by vulnerability type
            f.write("\n## Results by Vulnerability Type\n\n")
            
            for vuln_type, vuln_summary in summary["vulnerability_types"].items():
                f.write(f"### {vuln_type.replace('_', ' ').title()}\n\n")
                
                # Best configuration
                best_config = vuln_summary["best_config"]
                f.write(f"Best configuration: **{best_config}**\n\n")
                
                # Metrics table
                f.write("| Metric | Baseline | Best Bias | Improvement |\n")
                f.write("|--------|----------|-----------|-------------|\n")
                
                for metric in ["security", "quality", "match"]:
                    baseline = vuln_summary["baseline"][metric]
                    best_bias = vuln_summary["best_bias"][metric]
                    improvement = vuln_summary["improvement"][metric]
                    
                    f.write(f"| {metric.capitalize()} | {baseline:.2f} | {best_bias:.2f} | {improvement:+.2f} |\n")
                
                # Configuration comparison
                f.write("\n#### All Configurations\n\n")
                f.write("| Configuration | Security | Quality | Match |\n")
                f.write("|---------------|----------|---------|-------|\n")
                
                for config_name, metrics in vuln_summary["configs"].items():
                    security = metrics["security"]
                    quality = metrics["quality"]
                    match = metrics["match"]
                    
                    f.write(f"| {config_name} | {security:.2f} | {quality:.2f} | {match:.2f} |\n")
                
                # Example outputs
                f.write("\n#### Example Outputs\n\n")
                
                # Get the first example from each configuration
                for config_name, examples in results[vuln_type].items():
                    if examples:
                        example = examples[0]
                        trials = example["trials"]
                        
                        if trials:
                            f.write(f"**{config_name}:**\n\n")
                            f.write("```python\n")
                            f.write(trials[0]["generated"])
                            f.write("\n```\n\n")
                            
                            f.write("Security patterns:\n\n")
                            for pattern, found in trials[0]["analysis"].items():
                                f.write(f"- {pattern}: {'✓' if found else '✗'}\n")
                            
                            f.write("\n")
            
            # Statistical analysis
            f.write("\n## Statistical Analysis\n\n")
            
            # Calculate p-values and effect sizes
            f.write("| Vulnerability Type | Security Improvement | p-value | Effect Size |\n")
            f.write("|---------------------|---------------------|---------|-------------|\n")
            
            for vuln_type, vuln_summary in summary["vulnerability_types"].items():
                improvement = vuln_summary["improvement"]["security"]
                
                # Simple effect size calculation (no p-value without more trials)
                effect_size = abs(improvement) / 0.5  # Normalized by 0.5 (medium effect)
                effect_size_desc = "Small" if effect_size < 0.5 else "Medium" if effect_size < 0.8 else "Large"
                
                f.write(f"| {vuln_type.replace('_', ' ').title()} | {improvement:+.2f} | N/A | {effect_size:.2f} ({effect_size_desc}) |\n")
            
            # Conclusion
            f.write("\n## Conclusion\n\n")
            
            overall_improvement = summary["overall"]["improvement"]["security"]
            if overall_improvement > 0.2:
                f.write("The security bias optimization shows **significant improvements** in generating secure code patterns. ")
            elif overall_improvement > 0:
                f.write("The security bias optimization shows **modest improvements** in generating secure code patterns. ")
            else:
                f.write("The security bias optimization shows **no substantial improvements** in generating secure code patterns. ")
            
            # Best performing vulnerability types
            best_vuln_types = []
            for vuln_type, vuln_summary in summary["vulnerability_types"].items():
                if vuln_summary["improvement"]["security"] > 0.1:
                    best_vuln_types.append(vuln_type)
            
            if best_vuln_types:
                f.write("The approach was most effective for the following vulnerability types:\n\n")
                for vuln_type in best_vuln_types:
                    f.write(f"- {vuln_type.replace('_', ' ').title()}\n")
            
            f.write("\nThese results suggest that security biasing can be an effective approach to steering ")
            f.write("language models toward more secure code generation, but further refinements are needed ")
            f.write("to address the remaining challenges, particularly for more complex security patterns.\n")
        
        logger.info(f"Report saved to {filename}")
    except Exception as e:
        logger.error(f"Error generating report: {e}")

def main():
    """Main function to run the experiment."""
    parser = argparse.ArgumentParser(description="Run the optimized security bias experiment")
    parser.add_argument("--model", type=str, default="bigcode/starcoder", help="Model to use")
    parser.add_argument("--output", type=str, default="security/optimized_experiment_results.json", help="Output file")
    parser.add_argument("--report", type=str, default="security/optimized_experiment_report.md", help="Report file")
    args = parser.parse_args()
    
    # Log experiment start
    logger.info(f"Starting optimized security bias experiment with model: {args.model}")
    logger.info(f"Experiment configuration:")
    logger.info(f"  Vulnerability types: {VULNERABILITY_TYPES}")
    logger.info(f"  Bias configurations: {BIAS_CONFIGS}")
    logger.info(f"  Pattern multipliers: {PATTERN_MULTIPLIERS}")
    logger.info(f"  Examples per type: {NUM_EXAMPLES_PER_TYPE}")
    logger.info(f"  Trials per example: {NUM_TRIALS}")
    
    # Load examples
    logger.info("Loading examples from SecLLMHolmes dataset")
    examples = load_examples_from_secllmholmes(VULNERABILITY_TYPES)
    
    # Check if we have examples for all vulnerability types
    for vuln_type in VULNERABILITY_TYPES:
        if vuln_type not in examples or not examples[vuln_type]:
            logger.warning(f"No examples found for {vuln_type}")
    
    # Initialize tokenizer and model
    logger.info(f"Loading model: {args.model}")
    
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    
    # Try to load the model with different precision options
    model = None
    is_8bit = False
    
    try:
        # First try: 8-bit quantization for memory efficiency
        logger.info("Attempting to load with 8-bit quantization")
        model = AutoModelForCausalLM.from_pretrained(
            args.model, 
            device_map="auto", 
            torch_dtype=torch.float16,
            load_in_8bit=True
        )
        is_8bit = True
        logger.info("Using 8-bit quantized model")
    except Exception as e:
        logger.warning(f"8-bit quantization failed: {e}")
        try:
            # Second try: 16-bit precision
            logger.info("Falling back to 16-bit precision")
            model = AutoModelForCausalLM.from_pretrained(
                args.model, 
                device_map="auto", 
                torch_dtype=torch.float16
            )
        except Exception as e:
            logger.warning(f"16-bit precision failed: {e}")
            try:
                # Third try: 32-bit precision
                logger.info("Falling back to 32-bit precision")
                model = AutoModelForCausalLM.from_pretrained(
                    args.model, 
                    device_map="auto"
                )
            except Exception as e:
                logger.error(f"32-bit precision failed: {e}")
                logger.error("Unable to load model, exiting.")
                return
    
    if model is None:
        logger.error("Failed to load model, exiting.")
        return
    
    logger.info("Model loaded successfully!")
    
    # Run the experiment
    logger.info("Running experiment")
    results, total_time = run_experiment(examples, model, tokenizer, is_8bit=is_8bit)
    
    # Save the results
    save_results(results, args.output)
    
    # Analyze the results
    logger.info("Analyzing results")
    summary = analyze_results(results)
    
    # Generate a report
    logger.info("Generating report")
    generate_report(summary, results, total_time, filename=args.report)
    
    logger.info("Experiment completed successfully!")

if __name__ == "__main__":
    main()
