#!/usr/bin/env python3
import sys
import os
import json
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer
from nnsight import LanguageModel
from functools import partial
from tqdm import tqdm

# Add the parent directory to the path so we can import from codetrace
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codetrace.parsing_utils import get_model_fim, prepare_fim_prompt

def load_example():
    """Load a simplified security example for testing."""
    with open("security/simplified_security_examples.json", "r") as f:
        examples = json.load(f)
    return examples[0]  # Just use the first example

def tokenize_prompt(tokenizer, fim_obj, prompt):
    """Tokenize a prompt for the model."""
    try:
        if fim_obj.placeholder in prompt and not fim_obj._is_fim(prompt):
            return prepare_fim_prompt(tokenizer, fim_obj, prompt)
        elif fim_obj._is_fim(prompt):
            return prompt
        else:
            return prompt
    except Exception as e:
        print(f"Error in tokenize_prompt: {e}")
        return prompt

def generate_without_steering(model, tokenizer, prompt, max_tokens=20):
    """Generate text without steering using nnsight."""
    print("Generating without steering...")
    
    # Encode the prompt to get its length
    encoded_prompt = tokenizer.encode(prompt)
    
    with model.trace() as tracer:
        with tracer.invoke(prompt) as invoker:
            # Use invoker.inputs[0] for the model inputs
            outputs = model.generate(
                inputs=invoker.inputs[0],
                max_new_tokens=max_tokens,
                do_sample=True,
                temperature=0.7,
                top_p=0.9
            )
            
            # Get the generated text
            generated_ids = outputs.value[0].tolist()
            # Decode only the new tokens
            generated_text = tokenizer.decode(generated_ids[len(encoded_prompt):], skip_special_tokens=True)
    
    return generated_text

def generate_with_steering(model, tokenizer, prompt, layer_idx, steering_tensor, max_tokens=20):
    """Generate text with steering at a specific layer using nnsight."""
    print(f"Generating with steering at layer {layer_idx}...")
    
    # For token-by-token generation with steering
    completion = ""
    current_prompt = prompt
    
    for i in range(max_tokens):
        try:
            with model.trace() as tracer:
                # Set up a hook to modify the hidden states at the specified layer
                layer = model.model.layers[layer_idx]
                
                # Define our modification function
                @tracer.module(layer)
                def modify_hidden_states(self, module_inputs):
                    # Run the module normally first
                    result = self._original_forward(*module_inputs)
                    
                    # Get the hidden states (first element of the result tuple)
                    hidden_states = result[0]
                    
                    # Modify the hidden states of the last token
                    batch_size, seq_len, hidden_dim = hidden_states.shape
                    
                    # Create a mask for the last token
                    last_token_mask = torch.zeros((batch_size, seq_len, 1), 
                                                  dtype=torch.bool, 
                                                  device=hidden_states.device)
                    last_token_mask[:, -1] = True
                    
                    # Apply the steering tensor to the last token
                    # The steering tensor should be shape [1, hidden_dim]
                    steering_vector = steering_tensor[1, layer_idx].to(hidden_states.device)
                    
                    # Reshape steering vector to match the hidden states
                    steering_vector = steering_vector.view(1, 1, -1)
                    
                    # Add the steering vector to the hidden states of the last token
                    modified_hidden_states = hidden_states.clone()
                    
                    # Use broadcasting to add the steering vector only to the last token
                    modified_hidden_states = torch.where(
                        last_token_mask.expand_as(hidden_states),
                        hidden_states + steering_vector, 
                        hidden_states
                    )
                    
                    # Return the modified hidden states and the rest of the tuple
                    modified_result = (modified_hidden_states,) + result[1:]
                    return modified_result
                
                with tracer.invoke(current_prompt) as invoker:
                    # Get the logits for the last token
                    logits = model.lm_head.output[0, -1]
                    
                    # Apply temperature and top-p sampling
                    logits = logits / 0.7  # temperature
                    
                    # Apply top-p (nucleus) sampling
                    sorted_logits, sorted_indices = torch.sort(logits, descending=True)
                    cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)
                    
                    # Remove tokens with cumulative probability above the threshold
                    sorted_indices_to_remove = cumulative_probs > 0.9  # top_p
                    sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
                    sorted_indices_to_remove[..., 0] = 0
                    
                    # Set logits for removed indices to negative infinity
                    indices_to_remove = sorted_indices[sorted_indices_to_remove]
                    logits_cpu = logits.cpu().clone()
                    logits_cpu[indices_to_remove] = float('-inf')
                    
                    # Sample from the filtered distribution
                    probs = F.softmax(logits_cpu, dim=-1)
                    next_token_id = torch.multinomial(probs, num_samples=1).item()
                    
                    # Decode the token
                    next_token = tokenizer.decode([next_token_id], skip_special_tokens=True)
            
            if not next_token:
                next_token = " "  # Prevent empty token issues
                
            print(f"Token {i+1}: '{next_token}'")
            completion += next_token
            current_prompt += next_token
            
            # Check for stopping conditions
            if next_token.strip() == "" or len(completion) > 500:
                break
                
        except Exception as e:
            print(f"Error generating token {i+1}: {e}")
            break
    
    return completion

def main():
    # Initialize tokenizer and model
    model_name = "bigcode/starcoderbase-1b"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Initialize model with nnsight
    print("Initializing model with nnsight...")
    model = LanguageModel(model_name, device_map="auto")
    fim_obj = get_model_fim(model_name)
    
    # Load example and prepare prompt
    example = load_example()
    prompt = tokenize_prompt(tokenizer, fim_obj, example["fim_program"])
    
    # Print the prompt and expected completion
    print(f"\nPrompt: {prompt[:100]}...")
    print(f"Expected: {example['fim_type'][:100]}...")
    
    # Generate without steering
    try:
        completion_without_steering = generate_without_steering(model, tokenizer, prompt)
        print(f"Generated without steering: {completion_without_steering[:100]}...")
    except Exception as e:
        print(f"Error generating without steering: {e}")
        completion_without_steering = "Error: " + str(e)
    
    # Load the steering tensor
    steering_tensor_path = "security_steering_results_simple/cached_steering_tensor.pt"
    try:
        print(f"Loading steering tensor from {steering_tensor_path}...")
        steering_tensor = torch.load(steering_tensor_path)
        print(f"Steering tensor shape: {steering_tensor.shape}")
        
        # Try with steering at a specific layer
        layer_idx = 10  # Use layer 10 for steering
        completion_with_steering = generate_with_steering(
            model, tokenizer, prompt, layer_idx, steering_tensor
        )
        print(f"Generated with steering (layer {layer_idx}): {completion_with_steering[:100]}...")
        
    except Exception as e:
        print(f"Error with steering tensor: {e}")
        import traceback
        traceback.print_exc()
    
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
            "method": f"steering_layer{layer_idx}",
            "prompt": prompt,
            "expected": example["fim_type"],
            "generated": completion_with_steering
        })
    
    with open("security/nnsight_steering_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\nResults saved to security/nnsight_steering_results.json")

if __name__ == "__main__":
    main() 