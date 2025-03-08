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
    security_bias_factor: float = 3.0
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
        
    Returns:
        The generated completion
    """
    # Define security-focused code patterns with balanced bias
    security_patterns = {
        # SQL parameterized query patterns
        "WHERE name = %s": security_bias_factor * 3.0,
        "WHERE user = %s": security_bias_factor * 3.0,
        "WHERE id = %s": security_bias_factor * 3.0,
        "execute_query": security_bias_factor * 2.5,
        "cursor.execute": security_bias_factor * 2.5,
        
        # Common SQL parameterized patterns
        "params": security_bias_factor * 2.0,
        "parameters": security_bias_factor * 2.0,
        "VALUES (%s": security_bias_factor * 2.0,
        "query = ": security_bias_factor * 1.5,
        
        # Security validation patterns
        "validate": security_bias_factor * 1.5,
        "sanitize": security_bias_factor * 1.5,
        "escape": security_bias_factor * 1.5,
        
        # Individual security tokens with lower bias
        "%s": security_bias_factor * 1.0,
        "?": security_bias_factor * 1.0,
        "prepared": security_bias_factor * 1.0,
        "statement": security_bias_factor * 1.0,
        "SELECT": security_bias_factor * 0.5,
        "FROM": security_bias_factor * 0.5,
        "WHERE": security_bias_factor * 0.5
    }
    
    # Add security code examples as conditioning
    security_examples = [
        'query = "SELECT * FROM users WHERE name = %s"',
        'cursor.execute(query, (user_input,))',
        'params = [user_input]',
        'return execute_query(query, params)'
    ]
    
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
    model.to(device)
    
    # Encode the prompt
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    
    # Generate tokens one by one
    generated_ids = inputs.input_ids
    generated_text = ""
    
    # First token conditioning - try to start with "def" or other good patterns
    start_pattern_bias = {
        "def": 2.0,
        "query": 2.0
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
            
            # Add extra bias for the first token
            if i == 0:
                for pattern, bias in start_pattern_bias.items():
                    for token_id in tokenizer.encode(" " + pattern, add_special_tokens=False):
                        if token_id < logits.shape[1]:
                            logits[:, token_id] += bias * security_bias_factor
            
            # Apply dynamic bias based on context
            current_text = generated_text.lower()
            
            # If we're starting to write a SQL query, boost parameterized query tokens
            if "query" in current_text and "=" in current_text and len(generated_text) < 50:
                for pattern in ["%s", "?", "param"]:
                    for token_id in tokenizer.encode(" " + pattern, add_special_tokens=False):
                        if token_id < logits.shape[1]:
                            logits[:, token_id] += security_bias_factor * 2.0
            
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
            inputs = tokenizer(prompt + generated_text, return_tensors="pt").to(device)
            
            # Check for stopping conditions
            if tokenizer.eos_token in new_token or len(generated_text) > 500:
                break
    
    return generated_text

def main():
    # Load the simplified security examples
    with open("security/simplified_security_examples.json", "r") as f:
        examples = json.load(f)
    
    # Initialize tokenizer and model
    model_name = "bigcode/starcoderbase-1b"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    fim_obj = get_model_fim(model_name)
    
    # Get the first example and prepare prompt
    example = examples[0]
    prompt = modified_tokenize(tokenizer, fim_obj, example["fim_program"])
    
    print(f"\nPrompt: {prompt[:100]}...")
    print(f"Expected: {example['fim_type'][:100]}...")
    
    # Generate with balanced security bias
    print("\nGenerating with balanced security bias...")
    security_completion = generate_with_security_bias(
        model, tokenizer, prompt,
        max_new_tokens=40,
        security_bias_factor=3.0,
        temperature=0.8
    )
    print(f"Generated with security bias: {security_completion[:200]}...")
    
    # Generate without bias for comparison
    print("\nGenerating without bias...")
    normal_completion = generate_with_security_bias(
        model, tokenizer, prompt,
        max_new_tokens=40,
        security_bias_factor=0.0  # No bias
    )
    print(f"Generated without bias: {normal_completion[:200]}...")
    
    # Save the results
    results = [
        {
            "method": "balanced_security_bias",
            "prompt": prompt,
            "expected": example["fim_type"],
            "generated": security_completion
        },
        {
            "method": "no_bias",
            "prompt": prompt,
            "expected": example["fim_type"],
            "generated": normal_completion
        }
    ]
    
    with open("security/balanced_steering_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\nResults saved to security/balanced_steering_results.json")
    
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
    
    # Detailed comparison with expected output
    print("\n=== COMPARING WITH EXPECTED OUTPUT ===\n")
    
    # Expected solution
    expected_lines = example["fim_type"].split("\n")
    expected_key_elements = [
        "query = ",
        "SELECT",
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
    
    # Print final recommendations
    print("\n=== RECOMMENDATIONS ===\n")
    print("1. Try with a larger model like StarCoder-7B for better results")
    print("2. Consider fine-tuning a model specifically for security-aware code generation")
    print("3. Explore retrieval-augmented generation with security examples")
    print("4. For production use, combine this approach with static analysis tools")
    print("5. Future work should focus on proper integration with nnsight for true token-by-token steering")

if __name__ == "__main__":
    main() 