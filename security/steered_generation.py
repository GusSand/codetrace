#!/usr/bin/env python3
import sys
import os
import json
import torch
from transformers import AutoTokenizer
from nnsight import LanguageModel
from functools import partial
import itertools as it
from typing import List, Dict, Any, Callable, Optional, Union
import datasets
from pathlib import Path
from tqdm import tqdm

# Add the parent directory to the path so we can import from codetrace
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codetrace.parsing_utils import STARCODER_FIM, fim_placeholder, prepare_fim_prompt, get_model_fim
from codetrace.utils import apply_reduction, masked_fill, mask_target_idx

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

def token_mask_fn(hidden_states, tokens):
    """Function to create a mask for the last token."""
    return mask_target_idx(hidden_states, indices=[-1])

def generate_steered_completion(
    model, 
    tokenizer, 
    prompt: str, 
    steering_tensor: Optional[Dict[int, torch.Tensor]] = None, 
    layers_to_steer: Optional[List[int]] = None, 
    max_new_tokens: int = 50,
    steering_scale: float = 1.0
) -> str:
    """
    Generate a completion with steered generation using nnsight.
    
    Args:
        model: The language model (nnsight LanguageModel)
        tokenizer: The tokenizer
        prompt: The prompt to complete
        steering_tensor: Dictionary mapping layer indices to steering tensors
        layers_to_steer: List of layer indices to apply steering to
        max_new_tokens: Maximum number of tokens to generate
        steering_scale: Scaling factor for the steering tensor
        
    Returns:
        The generated completion
    """
    # Record the original prompt length
    prompt_tokens = tokenizer.encode(prompt)
    original_length = len(prompt_tokens)
    
    # Apply steering during generation
    generated_text = ""
    current_text = prompt
    
    for _ in tqdm(range(max_new_tokens), desc="Generating tokens"):
        # Use nnsight to trace through the model and apply steering
        with model.trace() as tracer:
            # Set up hooks to apply steering
            if steering_tensor is not None and layers_to_steer is not None:
                # Define a patch function to apply during forward pass
                def apply_patch(hidden_states, layer_idx):
                    if layer_idx in layers_to_steer and layer_idx in steering_tensor:
                        # Get the mask for the last token
                        mask = token_mask_fn(hidden_states, None)
                        
                        # Apply steering to the hidden states
                        layer_tensor = steering_tensor[layer_idx].to(hidden_states.device)
                        
                        # Scale the steering tensor
                        scaled_tensor = layer_tensor * steering_scale
                        
                        # Apply the steering
                        return masked_fill(hidden_states, mask, scaled_tensor)
                    return hidden_states
                
                # Register hooks for each layer
                for layer_idx in layers_to_steer:
                    if layer_idx in steering_tensor:
                        tracer.hooks.modify_at(
                            f"model.layers.{layer_idx}.output[0]",
                            partial(apply_patch, layer_idx=layer_idx)
                        )
            
            # Generate the next token
            with tracer.invoke(current_text) as invoker:
                outputs = model.generate(
                    inputs=invoker.inputs[0],
                    max_new_tokens=1,
                    do_sample=False
                )
                output = tokenizer.decode(outputs[0][len(prompt_tokens):], skip_special_tokens=True)
        
        # Get the generated token
        new_token = output
        generated_text += new_token
        current_text += new_token
        
        # Check for end conditions (max length, EOS token, etc.)
        if tokenizer.eos_token in new_token or len(new_token.strip()) == 0:
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
    
    # Prepare prompts
    prompts = []
    for example in examples:
        # Format the prompt
        formatted_prompt = modified_tokenize(tokenizer, STARCODER_FIM, example["fim_program"])
        prompts.append((formatted_prompt, example))
    
    # Load the steering tensors if they exist
    steering_tensors = {}
    tensor_paths = [
        "simplified_security_results/security_tensor_layer7.pt",  # Layer 7 tensor from simplified examples
        "security_steering_results/security_tensor.pt"            # Original layer 10 tensor
    ]
    
    for tensor_path in tensor_paths:
        if os.path.exists(tensor_path):
            try:
                tensor = torch.load(tensor_path)
                tensor_name = os.path.basename(tensor_path).replace(".pt", "")
                steering_tensors[tensor_name] = tensor
                print(f"Loaded steering tensor from {tensor_path}")
            except Exception as e:
                print(f"Error loading steering tensor from {tensor_path}: {e}")
    
    # Dictionary to store results for different scenarios
    all_results = []
    
    # Test with a smaller subset first
    test_prompts = prompts[:1]  # Just use the first example for testing
    
    # Generate without steering first
    print("\nGenerating without steering...")
    for i, (prompt, example) in enumerate(test_prompts):
        print(f"\nGenerating completion {i+1}/{len(test_prompts)} without steering...")
        completion = generate_steered_completion(
            model, tokenizer, prompt,
            max_new_tokens=20  # Reduce tokens for testing
        )
        
        result = {
            "example_id": i,
            "prompt": prompt,
            "expected": example["fim_type"],
            "generated": completion,
            "method": "no_steering"
        }
        all_results.append(result)
        
        # Print the result for this example
        print(f"\nPrompt: {prompt[:100]}...")
        print(f"Expected: {example['fim_type'][:100]}...")
        print(f"Generated: {completion[:100]}...")
    
    # Generate with layer 7 steering if available
    if "security_tensor_layer7" in steering_tensors:
        print("\nGenerating with layer 7 steering...")
        for i, (prompt, example) in enumerate(test_prompts):
            print(f"\nGenerating completion {i+1}/{len(test_prompts)} with layer 7 steering...")
            
            # Prepare the layer-specific steering tensor
            layer_tensor = {7: steering_tensors["security_tensor_layer7"][7]}
            
            completion = generate_steered_completion(
                model, tokenizer, prompt,
                steering_tensor=layer_tensor,
                layers_to_steer=[7],
                max_new_tokens=20,  # Reduce tokens for testing
                steering_scale=1.0
            )
            
            result = {
                "example_id": i,
                "prompt": prompt,
                "expected": example["fim_type"],
                "generated": completion,
                "method": "layer7_steering"
            }
            all_results.append(result)
            
            # Print the result for this example
            print(f"\nPrompt: {prompt[:100]}...")
            print(f"Expected: {example['fim_type'][:100]}...")
            print(f"Generated: {completion[:100]}...")
    
    # Save the results
    with open("security/steered_generation_results.json", "w") as f:
        json.dump(all_results, f, indent=2)
    
    print("\nResults saved to security/steered_generation_results.json")
    
    # Print a summary of the results
    print("\n=== RESULTS SUMMARY ===\n")
    methods = set(result["method"] for result in all_results)
    
    for method in methods:
        method_results = [r for r in all_results if r["method"] == method]
        
        # Count exact matches
        exact_matches = 0
        for result in method_results:
            if result["expected"] == result["generated"]:
                exact_matches += 1
        
        print(f"Method: {method}")
        print(f"Exact matches: {exact_matches}/{len(method_results)} ({exact_matches/len(method_results)*100:.1f}%)")
        
        # Check for partial matches
        partial_matches = 0
        for result in method_results:
            if any(line.strip() in result["generated"] for line in result["expected"].split("\n") if len(line.strip()) > 10):
                partial_matches += 1
        
        print(f"Partial matches: {partial_matches}/{len(method_results)} ({partial_matches/len(method_results)*100:.1f}%)\n")

if __name__ == "__main__":
    main() 