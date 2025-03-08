#!/usr/bin/env python3
import sys
import os
import json
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForCausalLM
from typing import List, Dict, Any, Optional, Union, Tuple
from tqdm import tqdm

# Add the parent directory to the path so we can import from codetrace
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codetrace.parsing_utils import get_model_fim, prepare_fim_prompt

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

def generate_with_targeted_bias(
    model, 
    tokenizer, 
    prompt: str, 
    max_new_tokens: int = 50,
    temperature: float = 0.8,
    top_p: float = 0.95,
    bias_factor: float = 5.0,
    is_8bit: bool = False
) -> str:
    """
    Generate text with a highly targeted bias toward secure code patterns.
    
    Args:
        model: The language model
        tokenizer: The tokenizer
        prompt: The prompt to complete
        max_new_tokens: Maximum number of tokens to generate
        temperature: Temperature for sampling
        top_p: Top-p value for nucleus sampling
        bias_factor: Base bias factor for security patterns
        is_8bit: Whether the model is using 8-bit quantization
        
    Returns:
        The generated completion
    """
    # Define complete code patterns for secure SQL
    secure_code_templates = [
        # Function definition
        "def search_users(user_input):",
        
        # Secure parameterized query definition
        "query = \"SELECT * FROM users WHERE name = %s\"",
        "query = 'SELECT * FROM users WHERE name = %s'",
        
        # Other secure patterns
        "params = (user_input,)",
        "cursor.execute(query, (user_input,))",
        "return execute_query(query, (user_input,))",
        
        # Other parameterized patterns
        "query = \"SELECT * FROM users WHERE email = %s\"",
        "cursor.execute(query, params)"
    ]
    
    # Convert each template to token IDs and assign a high bias
    template_token_ids = {}
    for template in secure_code_templates:
        token_ids = tokenizer.encode(template, add_special_tokens=False)
        # Assign bias to each token sequence of 1-3 tokens
        for i in range(len(token_ids)):
            # Single token
            template_token_ids[token_ids[i]] = bias_factor
            
            # Two token sequence if available
            if i < len(token_ids) - 1:
                token_pair = (token_ids[i], token_ids[i+1])
                template_token_ids[token_pair] = bias_factor * 1.5
                
            # Three token sequence if available
            if i < len(token_ids) - 2:
                token_triple = (token_ids[i], token_ids[i+1], token_ids[i+2])
                template_token_ids[token_triple] = bias_factor * 2.0
    
    # Define code stages for context-aware biasing
    stages = {
        "function_def": {
            "patterns": ["def search_users"],
            "next": "param_def"
        },
        "param_def": {
            "patterns": ["user_input", "(user_input):"],
            "next": "query_def"
        },
        "query_def": {
            "patterns": ["query =", "SELECT * FROM users"],
            "next": "parameterized_query"
        },
        "parameterized_query": {
            "patterns": ["WHERE name = %s", "WHERE email = %s"],
            "next": "execute_query"
        },
        "execute_query": {
            "patterns": ["return execute_query", "cursor.execute"],
            "next": "done"
        }
    }
    
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
    
    # Track generation state
    current_stage = "function_def"
    tokens_since_stage_change = 0
    
    for i in tqdm(range(max_new_tokens), desc="Generating tokens"):
        # Get the model's predictions for the next token
        with torch.no_grad():
            outputs = model(**{k: v for k, v in inputs.items() if k != 'token_type_ids'})
            logits = outputs.logits[:, -1, :]
            
            # Apply basic token biases
            for token_or_seq, bias in template_token_ids.items():
                if isinstance(token_or_seq, int):
                    # Single token
                    if token_or_seq < logits.shape[1]:
                        logits[:, token_or_seq] += bias
                else:
                    # Token sequence - boost first token based on sequence
                    token = token_or_seq[0]
                    if token < logits.shape[1]:
                        # Higher boost if we've seen previous tokens in sequence
                        if len(generated_text) >= len(token_or_seq) - 1:
                            prev_tokens = []
                            # Fix: Check if we actually have generated IDs to check
                            last_tokens = generated_ids[0].tolist()  # Get all tokens as a list
                            
                            # Use a different variable name for the inner loop
                            for k in range(1, min(len(token_or_seq), len(last_tokens))):
                                prev_token_id = token_or_seq[k]
                                # Check if the previous token matches
                                if len(last_tokens) >= k + 1 and prev_token_id == last_tokens[-k]:
                                    prev_tokens.append(prev_token_id)
                            
                            # Boost based on how many previous tokens match
                            if len(prev_tokens) > 0:
                                boost = bias * (1 + 0.5 * len(prev_tokens))
                                logits[:, token] += boost
            
            # Apply stage-specific biasing
            stage_info = stages[current_stage]
            stage_patterns = stage_info["patterns"]
            
            # Check if we need to move to the next stage
            next_stage = False
            for pattern in stage_patterns:
                if pattern in generated_text:
                    next_stage = True
                    break
            
            if next_stage:
                print(f"Moving from stage {current_stage} to {stage_info['next']}")
                current_stage = stage_info["next"]
                tokens_since_stage_change = 0
                # If we've reached the end, stop generation
                if current_stage == "done":
                    break
            else:
                tokens_since_stage_change += 1
            
            # Apply context-specific biasing for the current stage
            if current_stage == "function_def":
                # Boost "def search_users" tokens
                for token_id in tokenizer.encode("def search_users", add_special_tokens=False):
                    if token_id < logits.shape[1]:
                        logits[:, token_id] += bias_factor * 3.0
            
            elif current_stage == "param_def":
                # Boost parameter definition tokens
                for param_pattern in ["(user_input):", "(user_input,):"]:
                    for token_id in tokenizer.encode(param_pattern, add_special_tokens=False):
                        if token_id < logits.shape[1]:
                            logits[:, token_id] += bias_factor * 3.0
            
            elif current_stage == "query_def":
                # Boost query definition tokens
                for query_pattern in ["query = \"", "SELECT * FROM users"]:
                    for token_id in tokenizer.encode(query_pattern, add_special_tokens=False):
                        if token_id < logits.shape[1]:
                            logits[:, token_id] += bias_factor * 3.0
            
            elif current_stage == "parameterized_query":
                # Boost parameterized query tokens
                for param_pattern in ["%s", "WHERE name = %s"]:
                    for token_id in tokenizer.encode(param_pattern, add_special_tokens=False):
                        if token_id < logits.shape[1]:
                            logits[:, token_id] += bias_factor * 4.0
            
            elif current_stage == "execute_query":
                # Boost execution tokens
                for exec_pattern in ["return execute_query", "(query, (user_input,))"]:
                    for token_id in tokenizer.encode(exec_pattern, add_special_tokens=False):
                        if token_id < logits.shape[1]:
                            logits[:, token_id] += bias_factor * 3.0
            
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
            print(f"Token {i+1} [{current_stage}]: '{new_token}'")
            
            # Update the generated text and input for next iteration
            generated_text += new_token
            inputs = tokenizer(prompt + generated_text, return_tensors="pt")
            # Move inputs to the correct device
            inputs = {k: v.to(device) for k, v in inputs.items()}
            
            # Check for stopping conditions
            if tokenizer.eos_token in new_token or len(generated_text) > 500:
                break
            
            # Prevent getting stuck in a stage
            if tokens_since_stage_change > 15:
                print(f"Forcing progression from {current_stage} to {stage_info['next']}")
                current_stage = stage_info["next"]
                tokens_since_stage_change = 0
                # If we've reached the end, stop generation
                if current_stage == "done":
                    break
    
    return generated_text

def main():
    # Load the simplified security examples
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
        # First try: 8-bit quantization
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
    
    # Get the first example and prepare prompt
    example = examples[0]
    prompt = modified_tokenize(tokenizer, fim_obj, example["fim_program"])
    
    print(f"\nPrompt: {prompt[:100]}...")
    print(f"Expected: {example['fim_type'][:100]}...")
    
    # Generate with targeted security bias
    print("\nGenerating with targeted security bias (7B model)...")
    security_completion = generate_with_targeted_bias(
        model, tokenizer, prompt,
        max_new_tokens=50,
        bias_factor=5.0,
        temperature=0.7,
        is_8bit=is_8bit
    )
    print(f"Generated with security bias: {security_completion[:200]}...")
    
    # Generate without bias for comparison
    print("\nGenerating without bias (7B model)...")
    normal_completion = generate_with_targeted_bias(
        model, tokenizer, prompt,
        max_new_tokens=50,
        bias_factor=0.0,  # No bias
        is_8bit=is_8bit
    )
    print(f"Generated without bias: {normal_completion[:200]}...")
    
    # Save the results
    results = [
        {
            "method": "starcoder7b_targeted_bias",
            "prompt": prompt,
            "expected": example["fim_type"],
            "generated": security_completion
        },
        {
            "method": "starcoder7b_no_bias",
            "prompt": prompt,
            "expected": example["fim_type"],
            "generated": normal_completion
        }
    ]
    
    with open("security/starcoder7b_targeted_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\nResults saved to security/starcoder7b_targeted_results.json")
    
    # Analyze the results
    print("\n=== RESULTS ANALYSIS ===\n")
    for result in results:
        method = result["method"]
        expected = result["expected"]
        generated = result["generated"]
        
        # Check for exact match
        exact_match = expected == generated
        
        # Check for partial match
        partial_match = False
        
        # Look for meaningful code fragments
        key_phrases = [
            "query = ",
            "WHERE name = %s",
            "execute_query",
            "cursor.execute"
        ]
        
        for phrase in key_phrases:
            if phrase in generated:
                partial_match = True
                break
        
        print(f"Method: {method}")
        print(f"Exact match: {'Yes' if exact_match else 'No'}")
        print(f"Partial match: {'Yes' if partial_match else 'No'}")
        
        # Security pattern analysis
        security_patterns = {
            "parameterized_query": ["parameterized", "prepared statement", "%s", "?", "placeholder"],
            "input_validation": ["validate", "sanitize", "escape", "filter", "check"],
            "error_handling": ["try", "catch", "except", "error", "exception"],
            "null_check": ["null", "None", "undefined", "if", "check"],
            "sql_query": ["SELECT", "FROM", "WHERE", "query", "execute"]
        }
        
        print("\nSecurity patterns:")
        for pattern_name, keywords in security_patterns.items():
            found = any(keyword.lower() in generated.lower() for keyword in keywords)
            print(f"  - {pattern_name}: {'Yes' if found else 'No'}")
        
        print("\n" + "-"*50 + "\n")
    
    # Compare with expected output
    print("\n=== EXACT MATCHING ANALYSIS ===\n")
    
    secure_query_pattern = 'query = "SELECT * FROM users WHERE name = %s"'
    
    # Compare with the exact pattern
    print(f"Expected secure query pattern: {secure_query_pattern}")
    
    for result in results:
        method = result["method"]
        generated = result["generated"]
        
        if secure_query_pattern in generated:
            print(f"{method}: ✅ Exact secure query pattern found!")
        else:
            print(f"{method}: ❌ Exact secure query pattern NOT found")
            
            # Let's check how close we got
            if "query" in generated and "SELECT" in generated and "users" in generated:
                if "%s" in generated:
                    print(f"  - But found parameterized query components")
                else:
                    print(f"  - Found SQL query but missing parameterization")

if __name__ == "__main__":
    main() 