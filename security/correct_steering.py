#!/usr/bin/env python3
import sys
import os
import json
import torch
import numpy as np
from pathlib import Path
from tqdm import tqdm
from transformers import AutoTokenizer
from nnsight import LanguageModel
import nnsight

# Add the parent directory to the path so we can import from codetrace
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codetrace.parsing_utils import get_model_fim, prepare_fim_prompt
from codetrace.utils import mask_target_idx, masked_fill, get_lm_layers

def modified_tokenize(tokenizer, fim_obj, prompt: str) -> str:
    """Modified tokenize method that handles prompts without placeholders."""
    try:
        # If the prompt has a placeholder, use the standard prepare_fim_prompt
        if fim_obj.placeholder in prompt and not fim_obj._is_fim(prompt):
            return prepare_fim_prompt(tokenizer, fim_obj, prompt)
        elif fim_obj._is_fim(prompt):
            return prompt
        else:
            return prompt
    except Exception as e:
        print(f"Error in modified_tokenize: {e}")
        return prompt

def generate_without_steering(model, tokenizer, prompt, max_tokens=20):
    """Generate text without steering using nnsight's direct model.generate approach."""
    print("Generating without steering...")
    
    # Get prompt length for trimming later
    prompt_tokens = tokenizer.encode(prompt)
    prompt_length = len(prompt_tokens)
    
    with model.trace() as tracer:
        with tracer.invoke(prompt) as invoker:
            # Generate with standard settings
            outputs = model.generate(
                inputs=invoker.inputs[0], 
                max_new_tokens=max_tokens,
                do_sample=True,
                temperature=0.7,
                top_p=0.9
            )
            
            # Get the output IDs and decode them
            output_ids = outputs.value[0].tolist()
            generated_text = tokenizer.decode(output_ids[prompt_length:], skip_special_tokens=True)
    
    return generated_text

def generate_with_steering(model, tokenizer, prompt, steering_tensor, layers_to_steer=[10], steering_scale=1.0, max_tokens=20):
    """Generate text token-by-token with steering using the pattern from steering.py."""
    print(f"Generating with steering at layers {layers_to_steer}...")
    
    completion = ""
    current_prompt = prompt
    
    for i in range(max_tokens):
        with model.trace() as tracer:
            with tracer.invoke(current_prompt) as invoker:
                # Iterate through transformer layers
                hidden_states = []
                
                # Apply steering to specified layers
                for layer in range(len(get_lm_layers(model))):
                    # Get the hidden states from the current layer
                    hs = get_lm_layers(model)[layer].output[0]
                    
                    # Apply steering if this is a layer we want to steer
                    if layer in layers_to_steer:
                        # Create mask for the last token
                        mask = torch.zeros_like(hs[:, :, 0], dtype=torch.bool)
                        mask[:, -1] = True  # Select only the last token
                        mask = mask.unsqueeze(-1).expand(-1, -1, hs.shape[-1])
                        
                        # Get the right slice of the steering tensor for this layer
                        # Assuming steering_tensor shape is [3, 24, 1, 2048]
                        layer_tensor = steering_tensor[1, layer].to(hs.device)
                        
                        # Scale the steering tensor
                        scaled_tensor = layer_tensor * steering_scale
                        
                        # Reshape to match hidden state dimensions
                        scaled_tensor = scaled_tensor.view(1, 1, -1)
                        
                        # Apply steering by adding the tensor to the last token's hidden states
                        patched_hs = hs.clone()
                        patched_hs = torch.where(mask, hs + scaled_tensor, hs)
                        
                        # Replace the original hidden states with the patched version
                        for prompt_idx in range(hs.shape[0]):
                            get_lm_layers(model)[layer].output[0][prompt_idx,:,:] = patched_hs[prompt_idx,:,:]
                
                # Get logits for the last token
                logits = model.lm_head.output[0, -1]
                
                # Apply temperature and sampling
                probs = torch.nn.functional.softmax(logits / 0.7, dim=-1)
                next_token = torch.multinomial(probs.cpu(), num_samples=1).item()
                
                # Decode the token
                next_token_text = tokenizer.decode([next_token])
                
            # Add the new token to our completion
            if not next_token_text or next_token_text.isspace():
                # If we get an empty token, try a different approach
                next_token_text = " "
            
            print(f"Generated token {i+1}: '{next_token_text}'")
            completion += next_token_text
            current_prompt += next_token_text
            
            # Check for stopping conditions
            if len(completion) > 500 or tokenizer.eos_token in next_token_text:
                break
    
    return completion

def main():
    # Initialize model and tokenizer
    model_name = "bigcode/starcoderbase-1b"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Initialize model with nnsight
    print("Initializing model with nnsight...")
    model = LanguageModel(model_name, device_map="auto")
    
    # Load example and format prompt
    with open("security/simplified_security_examples.json", "r") as f:
        examples = json.load(f)
    
    example = examples[0]  # Use first example
    fim_obj = get_model_fim(model_name)
    prompt = modified_tokenize(tokenizer, fim_obj, example["fim_program"])
    
    print(f"\nPrompt: {prompt[:100]}...")
    print(f"Expected completion: {example['fim_type'][:100]}...")
    
    # Generate without steering
    try:
        completion_without_steering = generate_without_steering(model, tokenizer, prompt)
        print(f"Generated without steering: {completion_without_steering[:100]}...")
    except Exception as e:
        print(f"Error generating without steering: {e}")
        import traceback
        traceback.print_exc()
        completion_without_steering = "Error: " + str(e)
    
    # Load steering tensor
    steering_tensor_path = "security_steering_results_simple/cached_steering_tensor.pt"
    try:
        print(f"Loading steering tensor from {steering_tensor_path}...")
        steering_tensor = torch.load(steering_tensor_path)
        print(f"Steering tensor shape: {steering_tensor.shape}")
        
        # Generate with steering
        layers_to_steer = [10]  # Use layer 10
        completion_with_steering = generate_with_steering(
            model, tokenizer, prompt, steering_tensor,
            layers_to_steer=layers_to_steer,
            steering_scale=1.0
        )
        print(f"Generated with steering: {completion_with_steering[:100]}...")
    except Exception as e:
        print(f"Error with steering tensor: {e}")
        import traceback
        traceback.print_exc()
        completion_with_steering = "Error: " + str(e)
    
    # Save results
    results = [
        {
            "method": "no_steering",
            "prompt": prompt,
            "expected": example["fim_type"],
            "generated": completion_without_steering
        },
        {
            "method": f"steering_layers{layers_to_steer}",
            "prompt": prompt,
            "expected": example["fim_type"],
            "generated": completion_with_steering
        }
    ]
    
    with open("security/correct_steering_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\nResults saved to security/correct_steering_results.json")
    
    # Analyze results
    print("\n=== RESULTS ANALYSIS ===\n")
    
    for result in results:
        method = result["method"]
        expected = result["expected"]
        generated = result["generated"]
        
        # Count exact matches
        exact_match = expected == generated
        
        # Check for partial matches
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
        
        print(f"Method: {method}")
        print(f"Exact matches: {1 if exact_match else 0}/1 ({100 if exact_match else 0.0}%)")
        print(f"Partial matches: {1 if partial_match else 0}/1 ({100 if partial_match else 0.0}%)")
        
        # Check for security patterns
        security_patterns = {
            "parameterized_query": ["parameterized", "prepared statement", "%s", "?", "placeholder"],
            "input_validation": ["validate", "sanitize", "escape", "filter", "check"],
            "error_handling": ["try", "catch", "except", "error", "exception"],
            "null_check": ["null", "None", "undefined", "if", "check"],
            "authentication": ["auth", "login", "password", "token", "session"]
        }
        
        print("\nSecurity patterns found:")
        for pattern_name, keywords in security_patterns.items():
            found = any(keyword.lower() in generated.lower() for keyword in keywords)
            print(f"  - {pattern_name}: {'Yes' if found else 'No'}")
        
        print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    main() 