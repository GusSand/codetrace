#!/usr/bin/env python3
import datasets
import argparse
import json
import os
import torch
import random
from pathlib import Path
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer
import numpy as np

def load_model_and_tokenizer(model_id):
    """Load the model and tokenizer."""
    print(f"Loading model and tokenizer from {model_id}")
    
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto",
        torch_dtype=torch.float16,
        trust_remote_code=True
    )
    
    return model, tokenizer

def extract_type_from_program(program):
    """
    Extract the context for type inference from the program.
    For FIM format with <FILL> placeholder, extract the surrounding context.
    """
    if '<FILL>' not in program:
        return program
    
    # Split by <FILL> placeholder to get prefix and suffix
    parts = program.split('<FILL>')
    if len(parts) != 2:
        return program
    
    prefix, suffix = parts
    # Return the context without the placeholder
    context = prefix.rstrip() + suffix.lstrip()
    return context

def create_steering_vectors(model, tokenizer, candidates):
    """Create steering vectors based on candidates."""
    print(f"Creating steering vectors for {len(candidates)} examples...")
    
    steering_vectors = []
    
    for candidate in tqdm(candidates, desc="Creating steering vectors"):
        # Get the program and expected type
        program = candidate['original_program']
        expected_type = candidate['expected_type']
        
        # Extract prompt for type inference
        prompt = extract_type_from_program(program)
        
        # Tokenize
        inputs = tokenizer(prompt, return_tensors="pt")
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        
        # Run a forward pass to get embeddings for the expected result
        with torch.no_grad():
            outputs_expected = model(
                inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                output_hidden_states=True
            )
        
        # Create a steering vector using the last hidden state
        # This is a simplified approach - more sophisticated methods could be used
        last_hidden_state = outputs_expected.hidden_states[-1][0]
        
        # Create a steering vector based on the expected type
        # We'll use this to guide generation towards the correct type
        steering_vector = {
            'index': candidate['index'],
            'program': program,
            'expected_type': expected_type,
            'category': candidate['category'],
            'contexts': candidate['contexts'],
            'generated_original': candidate['generated_type_original'],
            'generated_mutated': candidate['generated_type_mutated'],
            # Store the last hidden state tensor
            'vector': last_hidden_state.mean(dim=0).cpu().numpy().tolist()
        }
        
        steering_vectors.append(steering_vector)
    
    return steering_vectors

def apply_steering_vector(model, hidden_states, steering_vector, strength=0.5):
    """Apply a steering vector to model hidden states during generation."""
    # Convert steering vector to tensor and move to device
    vector = torch.tensor(steering_vector['vector'], 
                          dtype=hidden_states.dtype, 
                          device=hidden_states.device)
    
    # Reshape for broadcasting
    vector = vector.view(1, 1, -1)
    
    # Apply the steering vector with a scaling factor
    steered_states = hidden_states + strength * vector
    
    return steered_states

def run_steered_completions(candidates, steering_vectors, model, tokenizer, output_path, strength=0.5):
    """Run completions with steering vectors."""
    print(f"Running steered completions on {len(candidates)} examples with strength {strength}...")
    
    results = []
    
    for i, candidate in enumerate(tqdm(candidates, desc="Running steered completions")):
        # Get the program and steering vector
        program = candidate['original_program']
        expected_type = candidate['expected_type']
        steering_vector = steering_vectors[i]
        
        # Extract prompt for type inference
        prompt = extract_type_from_program(program)
        
        # Tokenize
        inputs = tokenizer(prompt, return_tensors="pt")
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        
        # Hook function to apply steering
        hooks = []
        
        def hook_fn(module, input, output):
            # Modify the last hidden state with the steering vector
            modified_output = apply_steering_vector(
                model, output[0], steering_vector, strength
            )
            return (modified_output,) + output[1:]
        
        # Register hooks on the model's layers (simplified approach)
        # In a real implementation, you might want to target specific layers
        for name, module in model.named_modules():
            if name.endswith('output'):
                hook = module.register_forward_hook(hook_fn)
                hooks.append(hook)
        
        # Generate completion with steering
        try:
            with torch.no_grad():
                outputs = model.generate(
                    inputs["input_ids"],
                    attention_mask=inputs["attention_mask"],
                    max_new_tokens=10,
                    do_sample=False,
                    pad_token_id=tokenizer.eos_token_id
                )
            
            # Get only the newly generated tokens
            generated_tokens = outputs[0, inputs["input_ids"].shape[1]:]
            generated_type = tokenizer.decode(generated_tokens, skip_special_tokens=True)
            
            # Remove whitespace and newlines for cleaner comparison
            generated_type = generated_type.strip()
            
            # Check if prediction is correct
            is_correct = (generated_type.strip() == expected_type.strip())
            
            result = {
                'index': candidate['index'],
                'program': program,
                'expected_type': expected_type,
                'category': candidate['category'],
                'original_generated': candidate['generated_type_original'],
                'mutated_generated': candidate['generated_type_mutated'],
                'steered_generated': generated_type,
                'original_correct': False,  # From candidate selection criteria
                'mutated_correct': False,   # From candidate selection criteria
                'steered_correct': is_correct
            }
            
            results.append(result)
            
        except Exception as e:
            print(f"Error in steered completion for example {i}: {str(e)}")
            result = {
                'index': candidate['index'],
                'program': program,
                'expected_type': expected_type,
                'category': candidate['category'],
                'original_generated': candidate['generated_type_original'],
                'mutated_generated': candidate['generated_type_mutated'],
                'steered_generated': "ERROR",
                'original_correct': False,
                'mutated_correct': False,
                'steered_correct': False,
                'error': str(e)
            }
            results.append(result)
        
        # Remove all hooks
        for hook in hooks:
            hook.remove()
    
    # Calculate accuracy
    correct_count = sum(1 for r in results if r['steered_correct'])
    accuracy = correct_count / len(results) if results else 0
    
    print(f"Steered completions: {correct_count}/{len(results)} correct ({accuracy:.2%})")
    
    # Create a concise results summary
    summary = {
        'steering_strength': strength,
        'examples_count': len(results),
        'correct_count': correct_count,
        'accuracy': accuracy,
        'results': results
    }
    
    # Save results
    os.makedirs(output_path, exist_ok=True)
    output_file = os.path.join(output_path, f"steered_results_strength_{strength:.2f}.json")
    with open(output_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"Results saved to {output_file}")
    
    return summary

def main():
    parser = argparse.ArgumentParser(description="Run completions with steering vectors")
    parser.add_argument("--candidates-file", type=str, required=True,
                        help="Path to steering candidates JSON file")
    parser.add_argument("--model-id", type=str, default="bigcode/starcoderbase-1b",
                        help="Model ID to use for completions")
    parser.add_argument("--output-dir", type=str, default="steering_results",
                        help="Directory to save steered results")
    parser.add_argument("--max-examples", type=int, default=10,
                        help="Maximum number of examples to process")
    parser.add_argument("--strength", type=float, default=0.5,
                        help="Strength of the steering vector (0.0 to 1.0)")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed for reproducibility")
    args = parser.parse_args()
    
    # Set random seed
    random.seed(args.seed)
    torch.manual_seed(args.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)
    
    # Load candidates
    if not os.path.exists(args.candidates_file):
        print(f"Candidates file not found: {args.candidates_file}")
        print("Please run analyze_type_inference_results.py first")
        return
    
    with open(args.candidates_file, 'r') as f:
        candidates = json.load(f)
    
    # Limit number of examples if needed
    if args.max_examples and args.max_examples < len(candidates):
        candidates = candidates[:args.max_examples]
    
    print(f"Loaded {len(candidates)} candidates for steering")
    
    # Load model and tokenizer
    model, tokenizer = load_model_and_tokenizer(args.model_id)
    
    # Create steering vectors
    steering_vectors = create_steering_vectors(model, tokenizer, candidates)
    
    # Create steering vectors directory
    vectors_dir = os.path.join(args.output_dir, "vectors")
    os.makedirs(vectors_dir, exist_ok=True)
    vectors_file = os.path.join(vectors_dir, "steering_vectors.json")
    
    # Save vectors (without the actual vector data, which is too large)
    vectors_summary = [
        {k: v for k, v in sv.items() if k != 'vector'} 
        for sv in steering_vectors
    ]
    with open(vectors_file, 'w') as f:
        json.dump(vectors_summary, f, indent=2)
    
    print(f"Steering vector info saved to {vectors_file}")
    
    # Run completions with steering
    results = run_steered_completions(
        candidates, 
        steering_vectors, 
        model, 
        tokenizer, 
        args.output_dir,
        args.strength
    )
    
    # Print final summary
    print("\n===== STEERING RESULTS =====")
    print(f"Original accuracy: 0.0% (0/{len(candidates)})")  # By selection criteria
    print(f"Steered accuracy: {results['accuracy']*100:.2f}% ({results['correct_count']}/{results['examples_count']})")
    print(f"Improvement: {results['accuracy']*100:.2f}%")
    
    # Print example comparisons
    print("\nExample Comparisons:")
    for i, result in enumerate(results['results'][:3]):
        print(f"\nExample {i+1} (Category: {result['category']}):")
        print(f"Expected type: {result['expected_type']}")
        print(f"Original generated: {result['original_generated']} (Correct: {result['original_correct']})")
        print(f"Steered generated: {result['steered_generated']} (Correct: {result['steered_correct']})")

if __name__ == "__main__":
    main() 