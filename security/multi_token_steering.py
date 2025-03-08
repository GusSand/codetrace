#!/usr/bin/env python3
import sys
import os
import json
import torch
import torch.nn.functional as F
import numpy as np
from transformers import AutoTokenizer, AutoModelForCausalLM
from nnsight import LanguageModel
from functools import partial
import itertools as it
from typing import List, Dict, Any, Callable, Optional, Union
from pathlib import Path
from tqdm import tqdm

# Add the parent directory to the path so we can import from codetrace
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codetrace.parsing_utils import STARCODER_FIM, get_model_fim, prepare_fim_prompt
from codetrace.utils import mask_target_idx, masked_fill

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

def token_mask_fn(input_ids):
    """Function to create a mask for the last token."""
    batch_size, seq_len = input_ids.shape
    mask = torch.zeros((batch_size, seq_len), dtype=torch.bool, device=input_ids.device)
    mask[:, -1] = True
    return mask

def generate_token_with_steering(
    model, 
    tokenizer, 
    prompt: str, 
    steering_tensor: torch.Tensor,
    layer_idx: int,
    steering_scale: float = 1.0,
    top_p: float = 0.95,
    temperature: float = 0.7
) -> str:
    """
    Generate a single token with steering using nnsight hooks.
    """
    with model.trace() as tracer:
        # Define a function to apply steering
        def apply_steering(hidden_states):
            # Get the mask for the last token
            mask = token_mask_fn(hidden_states)
            # Expand mask to match hidden state dimensions
            expanded_mask = mask.unsqueeze(-1).expand(-1, -1, hidden_states.shape[-1])
            
            # Apply steering to the last token's hidden states
            if steering_tensor is not None:
                # We know steering_tensor is shape [3, 24, 1, 2048], we need to get the right layer
                layer_tensor = steering_tensor[1, layer_idx].to(hidden_states.device)
                
                # Scale the steering tensor
                scaled_tensor = layer_tensor * steering_scale
                
                # Apply the steering using masked_fill function
                patched_hidden_states = hidden_states.clone()
                patched_hidden_states = torch.where(
                    expanded_mask,
                    hidden_states + scaled_tensor,  # Add steering vector to the hidden states
                    hidden_states  # Keep original hidden states for non-target tokens
                )
                return patched_hidden_states
            
            return hidden_states
        
        # Register hook at the specific layer
        tracer.hooks.modify_at(
            f"model.layers.{layer_idx}.output[0]",
            apply_steering
        )
        
        # Generate the next token
        with tracer.invoke(prompt) as invoker:
            # Get the logits for the last token
            logits = model.lm_head.output[0, -1]
            
            # Apply temperature
            if temperature > 0:
                logits = logits / temperature
            
            # Apply top-p sampling
            if top_p < 1.0:
                sorted_logits, sorted_indices = torch.sort(logits, descending=True)
                cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)
                
                # Remove tokens with cumulative probability above the threshold
                sorted_indices_to_remove = cumulative_probs > top_p
                # Shift the indices to the right to keep also the first token above the threshold
                sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
                sorted_indices_to_remove[..., 0] = 0
                
                indices_to_remove = sorted_indices[sorted_indices_to_remove]
                logits[indices_to_remove] = -float("Inf")
            
            # Sample from the distribution
            probs = F.softmax(logits, dim=-1)
            next_token = torch.multinomial(probs, num_samples=1)
            
            # Decode the token
            next_token_text = tokenizer.decode([next_token.item()], skip_special_tokens=True)
    
    return next_token_text

def generate_steered_completion(
    model, 
    tokenizer, 
    prompt: str, 
    steering_tensor: Optional[torch.Tensor] = None,
    layer_idx: int = 10,
    max_new_tokens: int = 20,
    steering_scale: float = 1.0,
    top_p: float = 0.95,
    temperature: float = 0.7
) -> str:
    """
    Generate a completion with token-by-token steered generation.
    """
    generated_text = ""
    current_prompt = prompt
    
    for i in range(max_new_tokens):
        print(f"\nGenerating token {i+1}...")
        token = generate_token_with_steering(
            model, 
            tokenizer, 
            current_prompt, 
            steering_tensor,
            layer_idx,
            steering_scale,
            top_p,
            temperature
        )
        
        if not token:
            token = " "  # Prevent empty token issues
            
        print(f"Generated token: '{token}'")
        generated_text += token
        current_prompt += token
        print(f"Current completion: '{generated_text}'")
        
        # Check for completion conditions
        if tokenizer.eos_token in token or token.strip() == "":
            break
    
    return generated_text

def main():
    # Load the simplified security examples
    with open("security/simplified_security_examples.json", "r") as f:
        examples = json.load(f)
    
    # Initialize tokenizer and model
    model_name = "bigcode/starcoderbase-1b"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Initialize model with nnsight
    print("Initializing model with nnsight...")
    model = LanguageModel(model_name, device_map="auto")
    fim_obj = get_model_fim(model_name)
    
    # Generate without steering first
    print("\nGenerating without steering...")
    results_without_steering = []
    
    # Just use the first example for testing
    example = examples[0]
    prompt = modified_tokenize(tokenizer, fim_obj, example["fim_program"])
    
    # Generate without steering using the regular model.generate
    try:
        with model.trace() as tracer:
            encoded_prompt = tokenizer.encode(prompt, return_tensors="pt")
            encoded_prompt_len = len(encoded_prompt[0])
            
            with tracer.invoke(prompt) as invoker:
                # Get the input_ids from the invoker
                input_ids = invoker.inputs[0]["input_ids"]
                
                # Generate text with standard parameters
                outputs = model.generate(
                    inputs=invoker.inputs[0],
                    max_new_tokens=20,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.95,
                    pad_token_id=None  # Use None for open-end generation
                )
                
                # Extract the generated tokens and decode them
                output_ids = outputs.value[0]
                completion_without_steering = tokenizer.decode(output_ids[encoded_prompt_len:], skip_special_tokens=True)
    except Exception as e:
        print(f"Error generating without steering: {e}")
        completion_without_steering = "Error: " + str(e)
    
    results_without_steering.append({
        "prompt": prompt,
        "expected": example["fim_type"],
        "generated": completion_without_steering,
        "method": "no_steering"
    })
    
    print(f"\nPrompt: {prompt[:100]}...")
    print(f"Expected: {example['fim_type'][:100]}...")
    print(f"Generated without steering: {completion_without_steering[:100]}...")
    
    # Load the steering tensor
    steering_tensor_path = "security_steering_results_simple/cached_steering_tensor.pt"
    
    # Generate with steering
    print("\nSimulating multi-token steering with cached steering tensor...")
    try:
        steering_tensor = torch.load(steering_tensor_path)
        print(f"Loaded steering tensor from {steering_tensor_path}")
        print(f"Steering tensor shape: {steering_tensor.shape}")
        
        # Use layer index 10 for steering
        layer_idx = 10
        print(f"Using layer index {layer_idx} for steering")
        
        # Generate text with steering
        completion_with_steering = generate_steered_completion(
            model, 
            tokenizer, 
            prompt, 
            steering_tensor=steering_tensor,
            layer_idx=layer_idx,
            max_new_tokens=20,
            steering_scale=1.0,
            top_p=0.95,
            temperature=0.7
        )
        
        results_with_steering = {
            "prompt": prompt,
            "expected": example["fim_type"],
            "generated": completion_with_steering,
            "method": f"multi_token_steering_layer{layer_idx}"
        }
        
        print(f"\nPrompt: {prompt[:100]}...")
        print(f"Expected: {example['fim_type'][:100]}...")
        print(f"Generated with steering (layer {layer_idx}): {completion_with_steering[:100]}...")
        
    except Exception as e:
        print(f"Error with steering tensor: {e}")
        results_with_steering = {
            "prompt": prompt,
            "expected": example["fim_type"],
            "generated": "Error: " + str(e),
            "method": "multi_token_steering_error"
        }
    
    # Generate with a security bias approach (without using the steering tensor)
    print("\nSimulating multi-token steering with security bias...")
    
    # Define security-relevant tokens (a simplified approach)
    security_tokens = [
        "parameterized", "prepared", "statement", "escape", "validate", 
        "sanitize", "filter", "check", "secure", "query", "injection",
        "bound", "limit", "transaction"
    ]
    
    # Convert to token IDs
    security_token_ids = []
    for token in security_tokens:
        ids = tokenizer.encode(" " + token, add_special_tokens=False)
        security_token_ids.extend(ids)
    
    def generate_with_security_bias(
        model, 
        tokenizer, 
        prompt: str, 
        security_token_ids: List[int],
        security_bias: float = 1.0,
        max_new_tokens: int = 20,
        top_p: float = 0.95,
        temperature: float = 0.7
    ) -> str:
        generated_text = ""
        current_prompt = prompt
        
        for i in range(max_new_tokens):
            print(f"\nGenerating token {i+1} with security bias...")
            
            # Forward pass through the model to get logits
            with model.trace() as tracer:
                with tracer.invoke(current_prompt) as invoker:
                    # Get logits for the last token
                    logits = model.lm_head.output[0, -1]
                    
                    # Apply bias to security-relevant tokens
                    for token_id in security_token_ids:
                        if token_id < logits.shape[0]:  # Check if token_id is in vocabulary
                            logits[token_id] += security_bias
                    
                    # Apply temperature
                    if temperature > 0:
                        logits = logits / temperature
                    
                    # Apply top-p sampling
                    if top_p < 1.0:
                        sorted_logits, sorted_indices = torch.sort(logits, descending=True)
                        cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)
                        
                        # Remove tokens with cumulative probability above the threshold
                        sorted_indices_to_remove = cumulative_probs > top_p
                        # Shift the indices to the right to keep also the first token above the threshold
                        sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
                        sorted_indices_to_remove[..., 0] = 0
                        
                        indices_to_remove = sorted_indices[sorted_indices_to_remove]
                        logits[indices_to_remove] = -float("Inf")
                    
                    # Sample from the distribution
                    probs = F.softmax(logits, dim=-1)
                    next_token = torch.multinomial(probs, num_samples=1)
                    
                    # Decode the token
                    next_token_text = tokenizer.decode([next_token.item()], skip_special_tokens=True)
            
            if not next_token_text:
                next_token_text = " "  # Prevent empty token issues
                
            print(f"Generated token: '{next_token_text}'")
            generated_text += next_token_text
            current_prompt += next_token_text
            print(f"Current completion: '{generated_text}'")
            
            # Check for completion conditions
            if tokenizer.eos_token in next_token_text or next_token_text.strip() == "":
                break
        
        return generated_text
    
    # Generate with security bias
    completion_with_security_bias = generate_with_security_bias(
        model, 
        tokenizer, 
        prompt, 
        security_token_ids,
        security_bias=5.0,  # Higher bias for security tokens
        max_new_tokens=20,
        top_p=0.95,
        temperature=0.7
    )
    
    results_with_security_bias = {
        "prompt": prompt,
        "expected": example["fim_type"],
        "generated": completion_with_security_bias,
        "method": "security_biased_sampling"
    }
    
    print(f"\nPrompt: {prompt[:100]}...")
    print(f"Expected: {example['fim_type'][:100]}...")
    print(f"Generated with security bias: {completion_with_security_bias[:100]}...")
    
    # Combine and save all results
    all_results = [results_without_steering, results_with_steering, results_with_security_bias]
    
    with open("security/multi_token_steering_results.json", "w") as f:
        json.dump(all_results, f, indent=2)
    
    print("\nResults saved to security/multi_token_steering_results.json")
    
    # Analyze and print results summary
    print("\n=== RESULTS SUMMARY ===\n")
    
    for result in all_results:
        # Handle both single result object and list of results
        if isinstance(result, list):
            results_to_check = result
        else:
            results_to_check = [result]
            
        for method_result in results_to_check:
            method = method_result["method"]
            expected = method_result["expected"]
            generated = method_result["generated"]
            
            # Count exact matches
            exact_match = expected == generated
            
            # Check for partial matches (at least one line with >10 chars matches)
            partial_match = False
            expected_lines = expected.split("\n")
            generated_lines = generated.split("\n")
            
            for e_line in expected_lines:
                if len(e_line.strip()) > 10:
                    for g_line in generated_lines:
                        if e_line.strip() in g_line:
                            partial_match = True
                            break
                    if partial_match:
                        break
            
            print(f"\nMethod: {method}")
            print(f"Exact matches: {1 if exact_match else 0}/1 ({100 if exact_match else 0.0}%)")
            print(f"Partial matches: {1 if partial_match else 0}/1 ({100 if partial_match else 0.0}%)")
    
    # Perform security pattern analysis
    print("\n\n=== SECURITY PATTERN ANALYSIS ===\n")
    
    security_patterns = {
        "parameterized_query": ["parameterized", "prepared statement", "%s", "?", "placeholder"],
        "input_validation": ["validate", "sanitize", "escape", "filter", "check"],
        "error_handling": ["try", "catch", "except", "error", "exception"],
        "null_check": ["null", "None", "undefined", "if", "check"],
        "authentication": ["auth", "login", "password", "token", "session"]
    }
    
    for result in all_results:
        # Handle both single result object and list of results
        if isinstance(result, list):
            results_to_check = result
        else:
            results_to_check = [result]
            
        for method_result in results_to_check:
            method = method_result["method"]
            generated = method_result["generated"]
            
            print(f"\nMethod: {method}")
            
            for pattern_name, pattern_keywords in security_patterns.items():
                pattern_found = any(keyword in generated.lower() for keyword in pattern_keywords)
                print(f"  - {pattern_name}: {'Found' if pattern_found else 'Not found'}")
    
    # Print next steps
    print("\n\n=== NEXT STEPS ===\n")
    print("1. Try with a larger model like StarCoder-7B")
    print("2. Consider fine-tuning a model specifically for security-aware code generation")
    print("3. Explore other approaches like retrieval-augmented generation")
    print("4. Develop a proper nnsight integration for true token-by-token steering")

if __name__ == "__main__":
    main() 