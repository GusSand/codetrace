#!/usr/bin/env python3
import sys
import os
import json
import torch
from transformers import AutoTokenizer
from nnsight import LanguageModel
from pathlib import Path
from functools import partial

# Add the parent directory to the path so we can import from codetrace
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def generate_with_steering(model, tokenizer, prompt, steering_tensor, layers_to_steer, max_new_tokens=50, steering_scale=1.0):
    """Generate text with steering applied to specific layers."""
    # Record the original prompt length
    prompt_tokens = tokenizer.encode(prompt)
    original_length = len(prompt_tokens)
    
    # Apply steering during generation
    generated_text = ""
    current_text = prompt
    
    for _ in range(max_new_tokens):
        # Use nnsight to trace through the model and apply steering
        with model.trace() as tracer:
            # Set up hooks to apply steering
            def apply_patch(hidden_states, layer_idx):
                if layer_idx in layers_to_steer:
                    # Get the steering tensor for this layer
                    layer_tensor = steering_tensor[layer_idx].to(hidden_states.device)
                    # Scale the steering tensor
                    scaled_tensor = layer_tensor * steering_scale
                    # Apply the steering to the last token
                    hidden_states[:, -1] += scaled_tensor
                return hidden_states
            
            # Register hooks for each layer
            for layer_idx in layers_to_steer:
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
        
        # Check for end conditions
        if tokenizer.eos_token in new_token or len(new_token.strip()) == 0:
            break
    
    return generated_text

def main():
    # Load the steering tensor
    steering_tensor_path = Path("security_steering_results/security_tensor.pt")
    if not steering_tensor_path.exists():
        print("Error: Steering tensor not found. Please run modified_steering.py first.")
        return
    
    steering_tensor = torch.load(steering_tensor_path)
    print(f"Loaded steering tensor with shape: {steering_tensor.shape}")
    
    # Initialize model and tokenizer
    model_name = "bigcode/starcoderbase-7b"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = LanguageModel(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto",
        use_auth_token=True
    )
    
    # Test prompt
    test_prompt = "Write a function that queries a database for a user by name. The function should take a username as input and return the user's data."
    
    # Generate without steering
    print("\nGenerating without steering...")
    with model.trace() as tracer:
        with tracer.invoke(test_prompt) as invoker:
            outputs = model.generate(
                inputs=invoker.inputs[0],
                max_new_tokens=100,
                do_sample=False
            )
    no_steering_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"Output without steering:\n{no_steering_output}\n")
    
    # Generate with steering
    print("\nGenerating with steering...")
    # Choose some layers to steer (e.g., middle layers)
    layers_to_steer = list(range(20, 30))  # Middle layers
    steering_scale = 1.0
    
    steered_output = generate_with_steering(
        model=model,
        tokenizer=tokenizer,
        prompt=test_prompt,
        steering_tensor=steering_tensor,
        layers_to_steer=layers_to_steer,
        max_new_tokens=100,
        steering_scale=steering_scale
    )
    print(f"Output with steering:\n{steered_output}\n")

if __name__ == "__main__":
    main() 