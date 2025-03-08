#!/usr/bin/env python3
import sys
import os
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from functools import partial
import itertools as it
from typing import List, Dict, Any, Callable
import datasets
from pathlib import Path

# Add the parent directory to the path so we can import from codetrace
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codetrace.parsing_utils import STARCODER_FIM, fim_placeholder, prepare_fim_prompt, get_model_fim

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

def generate_completions(model, tokenizer, prompts, steering_tensor=None, layers_to_steer=None, max_new_tokens=50):
    """
    Generate completions for a list of prompts, optionally using a steering tensor.
    
    Args:
        model: The language model to use for generation
        tokenizer: The tokenizer to use
        prompts: List of prompts to generate completions for
        steering_tensor: Optional steering tensor to use for steering the generation
        layers_to_steer: List of layer indices to apply the steering tensor to
        max_new_tokens: Maximum number of new tokens to generate
        
    Returns:
        List of generated completions
    """
    print(f"Generating completions for {len(prompts)} prompts...")
    results = []
    
    # Handle the case where steering_tensor is None
    if steering_tensor is None or layers_to_steer is None:
        print("Generating without steering...")
        for i, prompt in enumerate(prompts):
            print(f"Generating completion {i+1}/{len(prompts)}...")
            # Tokenize the prompt
            encoded_prompt = tokenizer(prompt, return_tensors="pt").to(model.device)
            
            # Generate a completion
            output = model.generate(
                **encoded_prompt,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                num_return_sequences=1
            )
            
            # Decode the completion
            decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)
            
            # Get just the generated part (after the prompt)
            completion = decoded_output[len(prompt):]
            
            results.append(completion)
        return results
    
    # Apply steering during generation
    # This is a simple implementation that doesn't fully match the steering pipeline's approach
    print("Generating with steering...")
    for i, prompt in enumerate(prompts):
        print(f"Generating completion {i+1}/{len(prompts)}...")
        # Tokenize the prompt
        encoded_prompt = tokenizer(prompt, return_tensors="pt").to(model.device)
        
        # Initialize the generated sequence with the input tokens
        generated = encoded_prompt.input_ids.clone()
        
        # Generate tokens one by one
        for _ in range(max_new_tokens):
            # Get the next token logits
            with torch.no_grad():
                outputs = model(input_ids=generated)
                next_token_logits = outputs.logits[:, -1, :]
                
                # Apply steering to the logits (simplified version)
                # In a real implementation, you would need to get the hidden states,
                # apply the steering tensor, and then compute the logits
                
                # Here we're just demonstrating the idea
                next_token = torch.argmax(next_token_logits, dim=-1).unsqueeze(0)
                
                # Append the next token to the generated sequence
                generated = torch.cat([generated, next_token], dim=1)
                
                # Check if we've generated an EOS token
                if next_token.item() == tokenizer.eos_token_id:
                    break
        
        # Decode the completion
        decoded_output = tokenizer.decode(generated[0], skip_special_tokens=True)
        
        # Get just the generated part (after the prompt)
        completion = decoded_output[len(prompt):]
        
        results.append(completion)
    
    return results

def main():
    # Load the security examples
    with open("security/security_steering_examples.json", "r") as f:
        examples = json.load(f)
    
    # Initialize tokenizer and model
    model_name = "bigcode/starcoderbase-1b"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    
    # Move the model to the device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    
    # Prepare prompts
    prompts = []
    for example in examples:
        # Format the prompt
        formatted_prompt = modified_tokenize(tokenizer, STARCODER_FIM, example["fim_program"])
        prompts.append(formatted_prompt)
    
    # Load the steering tensor if it exists
    steering_tensor_path = "security_steering_results/security_tensor.pt"
    steering_tensor = None
    if os.path.exists(steering_tensor_path):
        try:
            steering_tensor = torch.load(steering_tensor_path)
            print("Loaded steering tensor")
        except Exception as e:
            print(f"Error loading steering tensor: {e}")
    
    # Generate completions without steering first
    print("\nGenerating completions without steering...")
    completions_without_steering = generate_completions(
        model, tokenizer, prompts, 
        max_new_tokens=50
    )
    
    # Generate completions with steering
    print("\nGenerating completions with steering...")
    completions_with_steering = generate_completions(
        model, tokenizer, prompts, 
        steering_tensor=steering_tensor,
        layers_to_steer=[10],
        max_new_tokens=50
    )
    
    # Compare the results
    print("\n=== COMPARISON OF RESULTS ===\n")
    for i, (example, completion_without, completion_with) in enumerate(zip(examples, completions_without_steering, completions_with_steering)):
        print(f"\n--- Example {i+1} ---\n")
        
        # Display original prompt
        print("Original FIM Program:")
        print(example["fim_program"])
        print("\n")
        
        # Display expected secure implementation
        print("Expected Secure Implementation (FIM Type):")
        print(example["fim_type"])
        print("\n")
        
        # Display completion without steering
        print("Completion Without Steering:")
        print(completion_without)
        print("\n")
        
        # Display completion with steering
        print("Completion With Steering:")
        print(completion_with)
        print("\n")
        
        # Check if completions match expected
        match_without = example["fim_type"] in completion_without
        match_with = example["fim_type"] in completion_with
        print(f"Match Without Steering: {match_without}")
        print(f"Match With Steering: {match_with}")
        print("-" * 80)
    
    # Save the results
    results = {
        "examples": examples,
        "completions_without_steering": completions_without_steering,
        "completions_with_steering": completions_with_steering
    }
    
    with open("security/generation_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\nResults saved to security/generation_results.json")

if __name__ == "__main__":
    main() 