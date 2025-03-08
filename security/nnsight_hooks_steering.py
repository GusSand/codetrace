#!/usr/bin/env python3
import sys
import os
import json
import torch
from transformers import AutoTokenizer
from nnsight import LanguageModel
from functools import partial
from typing import List, Dict, Any, Optional, Union
from tqdm import tqdm

# Add the parent directory to the path so we can import from codetrace
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codetrace.parsing_utils import get_model_fim, prepare_fim_prompt
from codetrace.utils import masked_fill, mask_target_idx

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

def token_mask_fn(hidden_states):
    """Function to create a mask for the last token."""
    # Create a mask where only the last token is True
    batch_size, seq_len = hidden_states.shape[:2]
    mask = torch.zeros((batch_size, seq_len), dtype=torch.bool, device=hidden_states.device)
    mask[:, -1] = True
    
    # Expand to match the hidden states dimensions
    expanded_mask = mask.unsqueeze(-1).expand(-1, -1, hidden_states.shape[-1])
    return expanded_mask

def generate_steered_completion(
    model, 
    tokenizer, 
    prompt: str, 
    steering_tensor: Optional[torch.Tensor] = None, 
    layers_to_steer: Optional[List[int]] = None, 
    max_new_tokens: int = 20,
    steering_scale: float = 1.0,
    temperature: float = 0.7,
    top_p: float = 0.9
) -> str:
    """
    Generate a completion with steered generation using nnsight.
    
    Args:
        model: The language model (nnsight LanguageModel)
        tokenizer: The tokenizer
        prompt: The prompt to complete
        steering_tensor: Tensor containing steering vectors for each layer
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
    
    for i in tqdm(range(max_new_tokens), desc="Generating tokens"):
        # Use nnsight to trace through the model and apply steering
        with model.trace() as tracer:
            # Set up hooks to apply steering
            if steering_tensor is not None and layers_to_steer is not None:
                # Define a patch function to apply during forward pass
                def apply_patch(hidden_states, layer_idx):
                    # Get the mask for the last token
                    mask = token_mask_fn(hidden_states)
                    
                    # Apply steering to the hidden states
                    # Steering tensor is shape [3, 24, 1, 2048]
                    layer_tensor = steering_tensor[1, layer_idx].to(hidden_states.device)
                    
                    # Reshape to match the required dimensions
                    layer_tensor = layer_tensor.view(1, 1, -1)
                    
                    # Scale the steering tensor
                    scaled_tensor = layer_tensor * steering_scale
                    
                    # Apply the steering by adding the tensor to the hidden states
                    # where the mask is True (for the last token)
                    patched_hidden_states = torch.where(
                        mask,
                        hidden_states + scaled_tensor,  # Add the steering tensor
                        hidden_states  # Keep original for other tokens
                    )
                    
                    return patched_hidden_states
                
                # Register hooks for each layer
                for layer_idx in layers_to_steer:
                    tracer.hooks.modify_at(
                        f"model.layers.{layer_idx}.output[0]",
                        partial(apply_patch, layer_idx=layer_idx)
                    )
            
            # Generate the next token with temperature and top-p sampling
            with tracer.invoke(current_text) as invoker:
                # Get the input_ids
                input_ids = invoker.inputs[0]["input_ids"]
                
                # Generate a single token
                outputs = model.generate(
                    inputs=invoker.inputs[0],
                    max_new_tokens=1,
                    do_sample=True,
                    temperature=temperature,
                    top_p=top_p
                )
                
                # Get the new token and decode it
                generated_token_ids = outputs.value[0, len(input_ids[0]):].tolist()
                new_token = tokenizer.decode(generated_token_ids, skip_special_tokens=True)
        
        # If empty token, try again with a space
        if not new_token or len(new_token.strip()) == 0:
            new_token = " "
            
        print(f"Token {i+1}: '{new_token}'")
        generated_text += new_token
        current_text += new_token
        
        # Check for end conditions
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
    
    # Initialize model with nnsight
    print("Initializing model with nnsight...")
    model = LanguageModel(model_name, device_map="auto")
    fim_obj = get_model_fim(model_name)
    
    # Prepare the prompt from the first example
    example = examples[0]  # Just use the first example
    prompt = modified_tokenize(tokenizer, fim_obj, example["fim_program"])
    
    print(f"\nPrompt: {prompt[:100]}...")
    print(f"Expected: {example['fim_type'][:100]}...")
    
    # Try generating without steering
    print("\nGenerating without steering...")
    try:
        completion_without_steering = generate_steered_completion(
            model, tokenizer, prompt,
            max_new_tokens=20
        )
        print(f"Generated without steering: {completion_without_steering[:100]}...")
    except Exception as e:
        print(f"Error generating without steering: {e}")
        import traceback
        traceback.print_exc()
        completion_without_steering = "Error: " + str(e)
    
    # Try with steering
    print("\nLoading steering tensor...")
    steering_tensor_path = "security_steering_results_simple/cached_steering_tensor.pt"
    try:
        steering_tensor = torch.load(steering_tensor_path)
        print(f"Loaded steering tensor with shape: {steering_tensor.shape}")
        
        # Generate with steering at layer 10
        print("\nGenerating with steering at layer 10...")
        completion_with_steering = generate_steered_completion(
            model, tokenizer, prompt,
            steering_tensor=steering_tensor,
            layers_to_steer=[10],
            steering_scale=1.0,
            max_new_tokens=20
        )
        print(f"Generated with steering: {completion_with_steering[:100]}...")
    except Exception as e:
        print(f"Error with steering: {e}")
        import traceback
        traceback.print_exc()
        completion_with_steering = "Error: " + str(e)
    
    # Save the results
    results = [
        {
            "method": "no_steering",
            "prompt": prompt,
            "expected": example["fim_type"],
            "generated": completion_without_steering
        }
    ]
    
    if 'completion_with_steering' in locals():
        results.append({
            "method": "steering_layer10",
            "prompt": prompt,
            "expected": example["fim_type"],
            "generated": completion_with_steering
        })
    
    with open("security/nnsight_hooks_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\nResults saved to security/nnsight_hooks_results.json")
    
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