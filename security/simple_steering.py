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
    max_new_tokens: int = 20,
    temperature: float = 0.7,
    top_p: float = 0.9,
    security_bias: float = 5.0
) -> str:
    """
    Generate text with a bias towards security-related tokens.
    
    Args:
        model: The language model
        tokenizer: The tokenizer
        prompt: The prompt to complete
        max_new_tokens: Maximum number of tokens to generate
        temperature: Temperature for sampling
        top_p: Top-p value for nucleus sampling
        security_bias: Bias factor for security-related tokens
        
    Returns:
        The generated completion
    """
    # Define security-relevant terms
    security_terms = [
        "%s",            # Parameterized query
        "?",             # Another placeholder
        "parameterized", 
        "prepared",
        "statement",
        "sanitize",
        "escape",
        "check",
        "validate",
        "secure",
        "input",
        "filter"
    ]
    
    # Convert terms to token IDs
    security_token_ids = []
    for term in security_terms:
        term_ids = tokenizer.encode(" " + term, add_special_tokens=False)
        security_token_ids.extend(term_ids)
    
    print(f"Security token ids: {security_token_ids[:10]}...")
    
    # Set up for generation
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    
    # Encode the prompt
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    input_length = inputs.input_ids.shape[1]
    
    # Generate tokens one by one
    generated_ids = inputs.input_ids
    generated_text = ""
    
    for i in tqdm(range(max_new_tokens), desc="Generating tokens"):
        # Get the model's predictions for the next token
        with torch.no_grad():
            outputs = model(**{k: v for k, v in inputs.items() if k != 'token_type_ids'})
            logits = outputs.logits[:, -1, :]
            
            # Apply bias to security-related tokens
            for token_id in security_token_ids:
                if token_id < logits.shape[1]:  # Check if token_id is in vocabulary
                    logits[:, token_id] += security_bias
            
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
                # Shift indices to keep first token above threshold
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
    
    # Generate with security bias
    print("\nGenerating with security bias...")
    security_completion = generate_with_security_bias(
        model, tokenizer, prompt,
        max_new_tokens=20,
        security_bias=5.0
    )
    print(f"Generated with security bias: {security_completion[:100]}...")
    
    # Generate without bias for comparison
    print("\nGenerating without bias...")
    normal_completion = generate_with_security_bias(
        model, tokenizer, prompt,
        max_new_tokens=20,
        security_bias=0.0  # No bias
    )
    print(f"Generated without bias: {normal_completion[:100]}...")
    
    # Save the results
    results = [
        {
            "method": "security_bias",
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
    
    with open("security/simple_steering_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\nResults saved to security/simple_steering_results.json")
    
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
        for line in expected.split("\n"):
            if len(line.strip()) > 10 and line.strip() in generated:
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
            "authentication": ["auth", "login", "password", "token", "session"]
        }
        
        print("\nSecurity patterns:")
        for pattern_name, keywords in security_patterns.items():
            found = any(keyword.lower() in generated.lower() for keyword in keywords)
            print(f"  - {pattern_name}: {'Yes' if found else 'No'}")
        
        print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    main() 