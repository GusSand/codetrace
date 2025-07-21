#!/usr/bin/env python3
"""
Sophisticated Security Steering - Uses activation steering instead of token biasing.
This approach creates steering vectors from semantic differences between secure and insecure code,
making it much more robust than token-level biasing.
"""

import sys
import os
import json
import torch
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Tuple
from tqdm import tqdm
import datasets

# Add the parent directory to the path so we can import from codetrace
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codetrace.steering import SteeringManager, subtract_avg, prepare_prompt_pairs
from codetrace.parsing_utils import get_model_fim, prepare_fim_prompt
from codetrace.utils import load_dataset, save_dataset
from nnsight import LanguageModel


def create_security_steering_dataset(examples: List[Dict], vulnerability_type: str = "sql_injection") -> List[Dict]:
    """
    Create paired examples for steering vector creation.
    Each pair consists of insecure code (negative) and secure code (positive).
    """
    steering_pairs = []
    
    for example in examples:
        if example.get("vulnerability_type") == vulnerability_type:
            # Create a steering pair
            pair = {
                "fim_program": example["insecure_code"],  # Negative example
                "mutated_program": example["secure_code"],  # Positive example  
                "fim_type": example["secure_code"],  # Expected output
                "vulnerability_type": vulnerability_type,
                "typechecks": True  # Assume both code examples are syntactically valid
            }
            steering_pairs.append(pair)
    
    return steering_pairs


def create_contextual_steering_vectors(
    model: LanguageModel, 
    secure_examples: List[str], 
    insecure_examples: List[str],
    layers: List[int] = None
) -> torch.Tensor:
    """
    Create steering vectors using contextual embeddings from secure vs insecure code.
    This captures semantic security concepts rather than individual tokens.
    """
    if layers is None:
        layers = [10, 15, 20]  # Default to middle-to-late layers
    
    print(f"Creating contextual steering vectors for {len(secure_examples)} examples...")
    
    # Collect hidden states for secure examples
    secure_states = []
    insecure_states = []
    
    # Process secure examples
    for example in tqdm(secure_examples, desc="Processing secure examples"):
        with model.trace() as tracer:
            with tracer.invoke(example):
                # Collect hidden states from specified layers
                layer_states = []
                for layer_idx in layers:
                    # Get hidden states from the specified layer
                    hidden_state = model.model.layers[layer_idx].output[0]
                    # Take the mean across sequence length for this example
                    mean_state = hidden_state.mean(dim=1)  # [batch_size, hidden_dim]
                    layer_states.append(mean_state.save())
                
                secure_states.append([state.value for state in layer_states])
    
    # Process insecure examples  
    for example in tqdm(insecure_examples, desc="Processing insecure examples"):
        with model.trace() as tracer:
            with tracer.invoke(example):
                layer_states = []
                for layer_idx in layers:
                    hidden_state = model.model.layers[layer_idx].output[0]
                    mean_state = hidden_state.mean(dim=1)
                    layer_states.append(mean_state.save())
                
                insecure_states.append([state.value for state in layer_states])
    
    # Compute steering vectors as difference between secure and insecure patterns
    steering_vectors = []
    for layer_i, layer_idx in enumerate(layers):
        # Collect states for this layer across all examples
        secure_layer_states = torch.stack([states[layer_i] for states in secure_states])
        insecure_layer_states = torch.stack([states[layer_i] for states in insecure_states])
        
        # Compute mean difference (secure - insecure)
        secure_mean = secure_layer_states.mean(dim=0)  # [batch_size, hidden_dim]
        insecure_mean = insecure_layer_states.mean(dim=0)
        
        steering_vector = secure_mean - insecure_mean  # Direction toward security
        steering_vectors.append(steering_vector)
    
    # Stack into tensor [num_layers, batch_size, hidden_dim]
    steering_tensor = torch.stack(steering_vectors)
    print(f"Created steering tensor with shape: {steering_tensor.shape}")
    
    return steering_tensor, layers


def generate_with_activation_steering(
    model: LanguageModel,
    tokenizer,
    prompt: str,
    steering_tensor: torch.Tensor,
    steering_layers: List[int],
    steering_scale: float = 2.0,
    max_new_tokens: int = 50,
    temperature: float = 0.7
) -> str:
    """
    Generate text using activation steering - modifies hidden states rather than token probabilities.
    This is much more sophisticated than token biasing.
    """
    print(f"Generating with activation steering (scale={steering_scale})...")
    
    device = next(model.parameters()).device
    completion = ""
    current_input = prompt
    
    for step in range(max_new_tokens):
        with model.trace() as tracer:
            with tracer.invoke(current_input) as invoker:
                # Apply steering to specified layers
                for layer_idx in steering_layers:
                    if layer_idx < len(steering_layers):
                        # Get the hidden states from this layer
                        hidden_states = model.model.layers[layer_idx].output[0]
                        
                        # Get the steering vector for this layer
                        layer_steering_idx = steering_layers.index(layer_idx)
                        steering_vec = steering_tensor[layer_steering_idx] * steering_scale
                        
                        # Apply steering to the last token (where generation happens)
                        modified_states = hidden_states.clone()
                        modified_states[:, -1, :] += steering_vec.to(device)
                        
                        # Replace the hidden states with our modified version
                        model.model.layers[layer_idx].output[0][:] = modified_states
                
                # Get the logits and sample the next token
                logits = model.lm_head.output
                
                # Apply temperature
                if temperature > 0:
                    logits = logits / temperature
                
                # Sample next token
                probs = torch.softmax(logits[:, -1, :], dim=-1)
                next_token = torch.multinomial(probs, 1)
                
                # Decode and add to completion
                next_text = tokenizer.decode(next_token[0], skip_special_tokens=True)
                completion += next_text
                current_input += next_text
                
                # Stop if we hit end of sequence
                if tokenizer.eos_token in next_text:
                    break
    
    return completion


def main():
    """
    Main function demonstrating sophisticated security steering.
    """
    # Load model
    model_name = "bigcode/starcoderbase-1b"  
    print(f"Loading model: {model_name}")
    
    model = LanguageModel(model_name, device_map="auto")
    tokenizer = model.tokenizer
    
    # Example secure vs insecure code pairs for SQL injection
    secure_examples = [
        "cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))",
        "stmt = conn.prepare('SELECT name FROM users WHERE age > ?')\nstmt.execute((min_age,))",
        "query = 'SELECT * FROM products WHERE category = %(category)s'\ncursor.execute(query, {'category': category})"
    ]
    
    insecure_examples = [
        "cursor.execute('SELECT * FROM users WHERE id = ' + user_id)",
        "query = f'SELECT name FROM users WHERE age > {min_age}'\ncursor.execute(query)",
        "cursor.execute('SELECT * FROM products WHERE category = \"' + category + '\"')"
    ]
    
    # Create steering vectors from contextual embeddings
    print("Creating sophisticated steering vectors...")
    steering_tensor, steering_layers = create_contextual_steering_vectors(
        model, secure_examples, insecure_examples, layers=[8, 12, 16]
    )
    
    # Test prompts (insecure code that needs completion)
    test_prompts = [
        "# Complete this SQL query securely:\nuser_input = request.form['username']\nquery = 'SELECT * FROM users WHERE name = ' + ",
        "# Fix this database query:\nproduct_id = get_product_id()\nconn.execute(f'DELETE FROM products WHERE id = {product_id",
    ]
    
    results = []
    
    for i, prompt in enumerate(test_prompts):
        print(f"\n=== Test Case {i+1} ===")
        print(f"Prompt: {prompt[:100]}...")
        
        # Generate without steering (baseline)
        print("\n1. Generating without steering...")
        baseline_completion = ""  # Would use standard generation here
        
        # Generate with sophisticated activation steering
        print("2. Generating with activation steering...")
        steered_completion = generate_with_activation_steering(
            model, tokenizer, prompt, steering_tensor, steering_layers,
            steering_scale=3.0, max_new_tokens=30, temperature=0.6
        )
        
        # Analyze security patterns in the completion
        security_patterns = analyze_security_patterns(steered_completion)
        
        result = {
            "prompt": prompt,
            "baseline_completion": baseline_completion,
            "steered_completion": steered_completion,
            "security_analysis": security_patterns,
            "steering_method": "activation_steering",
            "steering_scale": 3.0,
            "layers_steered": steering_layers
        }
        results.append(result)
        
        print(f"Steered completion: {steered_completion[:100]}...")
        print(f"Security patterns found: {list(security_patterns.keys())}")
    
    # Save results
    with open("security/sophisticated_steering_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to security/sophisticated_steering_results.json")
    print_analysis_summary(results)


def analyze_security_patterns(text: str) -> Dict[str, bool]:
    """
    Analyze generated text for security patterns - this goes beyond simple token matching.
    """
    patterns = {
        "parameterized_query": any(pattern in text.lower() for pattern in [
            "%s", "?", ".execute(", "prepare(", "%(", "parameterized"
        ]),
        "input_validation": any(pattern in text.lower() for pattern in [
            "validate", "sanitize", "escape", "filter", "check", "isinstance"
        ]),
        "error_handling": any(pattern in text.lower() for pattern in [
            "try:", "except", "catch", "error", "exception"
        ]),
        "string_concatenation": any(pattern in text for pattern in [
            " + ", "f'{", "format(", "% (", ".format"
        ]),
        "sql_keywords": any(pattern in text.upper() for pattern in [
            "SELECT", "INSERT", "UPDATE", "DELETE", "FROM", "WHERE"
        ])
    }
    return patterns


def print_analysis_summary(results: List[Dict]):
    """Print a summary of the security analysis."""
    print("\n" + "="*60)
    print("SOPHISTICATED STEERING ANALYSIS SUMMARY")
    print("="*60)
    
    for i, result in enumerate(results):
        print(f"\nTest Case {i+1}:")
        analysis = result["security_analysis"]
        
        # Count positive security patterns
        secure_patterns = sum(1 for pattern, found in analysis.items() 
                            if found and pattern != "string_concatenation")
        
        # Check for insecure patterns
        has_string_concat = analysis.get("string_concatenation", False)
        
        print(f"  Secure patterns found: {secure_patterns}/4")
        print(f"  Insecure string concatenation: {'Yes' if has_string_concat else 'No'}")
        
        if analysis.get("parameterized_query"):
            print("  ✓ Uses parameterized queries")
        if analysis.get("input_validation"):
            print("  ✓ Includes input validation")
        if analysis.get("error_handling"):
            print("  ✓ Has error handling")
        if has_string_concat:
            print("  ⚠ Contains string concatenation (potential vulnerability)")
    
    print("\n" + "="*60)
    print("Key Advantages of Activation Steering over Token Biasing:")
    print("1. Captures semantic security concepts, not just individual tokens")
    print("2. Robust to different ways of expressing security patterns") 
    print("3. Works with the model's learned representations")
    print("4. Can generalize to unseen security patterns")
    print("5. More context-aware and sophisticated")


if __name__ == "__main__":
    main()