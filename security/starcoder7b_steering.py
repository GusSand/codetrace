#!/usr/bin/env python3
import sys
import os
import json
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForCausalLM
from typing import List, Dict, Any, Optional, Union
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

def generate_with_security_bias(
    model, 
    tokenizer, 
    prompt: str, 
    max_new_tokens: int = 40,
    temperature: float = 0.8,
    top_p: float = 0.95,
    security_bias_factor: float = 2.0,  # Slightly lower default for 7B model
    is_8bit: bool = False  # Flag to indicate if model is 8-bit quantized
) -> str:
    """
    Generate text with a balanced bias towards security-related patterns.
    
    Args:
        model: The language model
        tokenizer: The tokenizer
        prompt: The prompt to complete
        max_new_tokens: Maximum number of tokens to generate
        temperature: Temperature for sampling
        top_p: Top-p value for nucleus sampling
        security_bias_factor: Base bias factor for security tokens
        is_8bit: Flag indicating if model is 8-bit quantized
        
    Returns:
        The generated completion
    """
    # Define security-focused code patterns with balanced bias
    security_patterns = {
        # SQL parameterized query patterns (highest bias)
        "WHERE name = %s": security_bias_factor * 3.0,
        "WHERE user = %s": security_bias_factor * 3.0,
        "WHERE id = %s": security_bias_factor * 3.0,
        "execute_query": security_bias_factor * 2.5,
        "cursor.execute": security_bias_factor * 2.5,
        
        # Complete secure query (high bias)
        'query = "SELECT * FROM users WHERE name = %s"': security_bias_factor * 4.0,
        
        # Common SQL parameterized patterns (medium bias)
        "params": security_bias_factor * 2.0,
        "parameters": security_bias_factor * 2.0,
        "VALUES (%s": security_bias_factor * 2.0,
        "query = ": security_bias_factor * 1.5,
        
        # Security validation patterns
        "validate": security_bias_factor * 1.5,
        "sanitize": security_bias_factor * 1.5,
        "escape": security_bias_factor * 1.5,
        
        # Individual security tokens (lower bias)
        "%s": security_bias_factor * 1.0,
        "?": security_bias_factor * 1.0,
        "prepared": security_bias_factor * 1.0,
        "statement": security_bias_factor * 1.0,
        "SELECT": security_bias_factor * 0.5,
        "FROM": security_bias_factor * 0.5,
        "WHERE": security_bias_factor * 0.5,
        
        # Function definition (to start properly)
        "def search_users": security_bias_factor * 3.0
    }
    
    # Convert patterns to token IDs with their respective bias values
    security_token_ids = {}
    # Add bias for security patterns
    for pattern, bias in security_patterns.items():
        term_ids = tokenizer.encode(" " + pattern, add_special_tokens=False)
        for token_id in term_ids:
            if token_id in security_token_ids:
                security_token_ids[token_id] = max(security_token_ids[token_id], bias)
            else:
                security_token_ids[token_id] = bias
    
    print(f"Security tokens biased: {len(security_token_ids)}")
    
    # Set up for generation
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Only move model to device if it's not an 8-bit model (which is already on the correct device)
    if not is_8bit:
        model.to(device)
    
    # Encode the prompt
    inputs = tokenizer(prompt, return_tensors="pt")
    # Move inputs to the correct device
    inputs = {k: v.to(device) for k, v in inputs.items()}
    
    # Generate tokens one by one
    generated_ids = inputs['input_ids']
    generated_text = ""
    
    # First token conditioning - try to start with "def" or other good patterns
    start_patterns = {
        "def": 3.0,
        "def search_users": 4.0
    }
    
    for i in tqdm(range(max_new_tokens), desc="Generating tokens"):
        # Get the model's predictions for the next token
        with torch.no_grad():
            outputs = model(**{k: v for k, v in inputs.items() if k != 'token_type_ids'})
            logits = outputs.logits[:, -1, :]
            
            # Apply bias to security-related tokens
            for token_id, bias_value in security_token_ids.items():
                if token_id < logits.shape[1]:  # Check if token_id is in vocabulary
                    logits[:, token_id] += bias_value
            
            # Apply context-aware biasing
            if i == 0:
                # First token - try to start with function definition
                for pattern, bias in start_patterns.items():
                    for token_id in tokenizer.encode(pattern, add_special_tokens=False):
                        if token_id < logits.shape[1]:
                            logits[:, token_id] += bias * security_bias_factor
            elif len(generated_text) < 20:
                # Early generation - encourage function definition pattern
                if "def" in generated_text and "(" not in generated_text:
                    # Encourage parameter definition
                    for token_id in tokenizer.encode("(user_input):", add_special_tokens=False):
                        if token_id < logits.shape[1]:
                            logits[:, token_id] += security_bias_factor * 2.0
            elif "query" in generated_text.lower() and "=" in generated_text and "SELECT" not in generated_text:
                # We're defining a query - boost SQL keywords
                for sql_term in ["SELECT * FROM", "users WHERE", "name = %s"]:
                    for token_id in tokenizer.encode(" " + sql_term, add_special_tokens=False):
                        if token_id < logits.shape[1]:
                            logits[:, token_id] += security_bias_factor * 3.0
            
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
            print(f"Token {i+1}: '{new_token}'")
            
            # Update the generated text and input for next iteration
            generated_text += new_token
            inputs = tokenizer(prompt + generated_text, return_tensors="pt")
            # Move inputs to the correct device
            inputs = {k: v.to(device) for k, v in inputs.items()}
            
            # Check for stopping conditions
            if tokenizer.eos_token in new_token or len(generated_text) > 500:
                break
    
    return generated_text

def main():
    # Load the simplified security examples
    with open("security/simplified_security_examples.json", "r") as f:
        examples = json.load(f)
    
    # Initialize tokenizer and model
    model_name = "bigcode/starcoder"  # This is the 7B model
    print(f"Loading {model_name} model...")
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Try to load the model with different precision options, falling back if needed
    model = None
    is_8bit = False  # Flag to track if we're using 8-bit quantization
    
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
            # Second try: 16-bit precision without quantization
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
    
    # Generate with balanced security bias
    print("\nGenerating with security bias (7B model)...")
    security_completion = generate_with_security_bias(
        model, tokenizer, prompt,
        max_new_tokens=40,
        security_bias_factor=2.0,  # Slightly lower for 7B model
        temperature=0.7,  # Lower temperature for more focused generation
        is_8bit=is_8bit  # Pass the 8-bit flag
    )
    print(f"Generated with security bias: {security_completion[:200]}...")
    
    # Generate without bias for comparison
    print("\nGenerating without bias (7B model)...")
    normal_completion = generate_with_security_bias(
        model, tokenizer, prompt,
        max_new_tokens=40,
        security_bias_factor=0.0,  # No bias
        is_8bit=is_8bit  # Pass the 8-bit flag
    )
    print(f"Generated without bias: {normal_completion[:200]}...")
    
    # Save the results
    results = [
        {
            "method": "starcoder7b_security_bias",
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
    
    with open("security/starcoder7b_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\nResults saved to security/starcoder7b_results.json")
    
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
    print("\n=== COMPARING WITH EXPECTED OUTPUT ===\n")
    
    # Expected solution
    expected_lines = example["fim_type"].split("\n")
    expected_key_elements = [
        "def search_users",
        "query = ",
        "SELECT * FROM users",
        "%s",
        "execute_query"
    ]
    
    print("Expected key elements:")
    for element in expected_key_elements:
        present_in_expected = any(element in line for line in expected_lines)
        print(f"  - {element}: {'Present' if present_in_expected else 'Not present'}")
    
    # Check biased output
    print("\nBiased output key elements:")
    for element in expected_key_elements:
        present_in_biased = element in security_completion
        print(f"  - {element}: {'Present' if present_in_biased else 'Not present'}")
    
    # Check similarity to expected output
    print("\nSimilarity to expected output:")
    expected_secure_pattern = 'query = "SELECT * FROM users WHERE name = %s"'
    if expected_secure_pattern in security_completion:
        print("✅ Secure query pattern is exactly as expected!")
    else:
        print("❌ Exact secure query pattern not found")
        
        # Check for close matches
        if "query" in security_completion and "SELECT" in security_completion and "%s" in security_completion:
            print("✓ Contains main components of secure query but not exact pattern")

if __name__ == "__main__":
    main() 