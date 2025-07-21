#!/usr/bin/env python3
import datasets
import argparse
from pathlib import Path
import random
import torch
import os
import json
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer

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

def run_completions(dataset, model, tokenizer, output_path, max_samples=None):
    """Run type inference completions on a dataset."""
    if max_samples and max_samples < len(dataset):
        # Sample a subset for quicker testing
        indices = random.sample(range(len(dataset)), max_samples)
        dataset = dataset.select(indices)
    
    print(f"Running completions on {len(dataset)} examples")
    
    results = []
    correct_count = 0
    
    for i, example in enumerate(tqdm(dataset, desc="Generating completions")):
        try:
            # Get the program and expected type
            program = example["fim_program"]
            expected_type = example["fim_type"]
            
            # Extract prompt for type inference
            prompt = extract_type_from_program(program)
            
            # Tokenize
            inputs = tokenizer(prompt, return_tensors="pt")
            inputs = {k: v.to(model.device) for k, v in inputs.items()}
            
            # Generate completion
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
            if is_correct:
                correct_count += 1
            
            # Store result
            result = {
                "index": i,
                "program": program,
                "expected_type": expected_type,
                "generated_type": generated_type,
                "is_correct": is_correct
            }
            
            results.append(result)
            
            # Print debug info for the first few examples
            if i < 3:
                print(f"\nExample {i+1}:")
                print(f"Expected type: {expected_type}")
                print(f"Generated type: {generated_type}")
                print(f"Correct: {is_correct}")
            
        except Exception as e:
            print(f"Error processing example {i}: {str(e)}")
            result = {
                "index": i,
                "program": example["fim_program"],
                "expected_type": example["fim_type"],
                "generated_type": "ERROR",
                "is_correct": False,
                "error": str(e)
            }
            results.append(result)
    
    # Calculate accuracy
    accuracy = correct_count / len(dataset) if dataset else 0
    
    print(f"Completions: {correct_count}/{len(dataset)} correct ({accuracy:.2%})")
    
    # Create a results summary
    summary = {
        "dataset_size": len(dataset),
        "correct_count": correct_count,
        "accuracy": accuracy,
        "results": results
    }
    
    # Save results
    os.makedirs(output_path, exist_ok=True)
    output_file = os.path.join(output_path, "inference_results.json")
    with open(output_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"Results saved to {output_file}")
    
    # Save example predictions for easier analysis
    examples_file = os.path.join(output_path, "example_predictions.json")
    with open(examples_file, 'w') as f:
        json.dump(results[:10], f, indent=2)
    
    # Convert results to dataset format for easier processing
    result_ds = dataset.map(
        lambda example, idx: {
            "generated_type": results[idx]["generated_type"] if idx < len(results) else "ERROR",
            "is_correct": results[idx]["is_correct"] if idx < len(results) else False
        },
        with_indices=True
    )
    
    # Save as dataset
    result_ds.save_to_disk(output_path)
    
    return result_ds

def main():
    parser = argparse.ArgumentParser(description="Run type inference completions on datasets")
    parser.add_argument("--original-dataset", type=str, default="starcoder1_fim_completions",
                        help="Path to the original dataset")
    parser.add_argument("--mutated-dataset", type=str, default="starcoder1_fim_completions_mutated",
                        help="Path to the mutated dataset")
    parser.add_argument("--model-id", type=str, default="bigcode/starcoderbase-1b",
                        help="Model ID to use for completions")
    parser.add_argument("--original-output", type=str, default="starcoder1_fim_completions_results",
                        help="Path to save original dataset results")
    parser.add_argument("--mutated-output", type=str, default="starcoder1_fim_completions_mutated_results",
                        help="Path to save mutated dataset results")
    parser.add_argument("--max-samples", type=int, default=None,
                        help="Maximum number of samples to process")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed for reproducibility")
    args = parser.parse_args()
    
    # Set random seed
    random.seed(args.seed)
    torch.manual_seed(args.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)
    
    # Load model and tokenizer
    model, tokenizer = load_model_and_tokenizer(args.model_id)
    
    # Create output directories
    for path in [args.original_output, args.mutated_output]:
        os.makedirs(path, exist_ok=True)
    
    # Check if we need to run original dataset
    if os.path.exists(args.original_output) and len(os.listdir(args.original_output)) > 0:
        print(f"Original dataset results already exist at {args.original_output}")
        original_ds = datasets.load_from_disk(args.original_output)
    else:
        # Load and run original dataset
        print(f"Loading original dataset from {args.original_dataset}")
        original_ds = datasets.load_from_disk(args.original_dataset)
        original_ds = run_completions(
            original_ds, model, tokenizer, args.original_output, args.max_samples
        )
    
    # Check if we need to run mutated dataset
    if os.path.exists(args.mutated_output) and len(os.listdir(args.mutated_output)) > 0:
        print(f"Mutated dataset results already exist at {args.mutated_output}")
        mutated_ds = datasets.load_from_disk(args.mutated_output)
    else:
        # Load and run mutated dataset
        print(f"Loading mutated dataset from {args.mutated_dataset}")
        mutated_ds = datasets.load_from_disk(args.mutated_dataset)
        mutated_ds = run_completions(
            mutated_ds, model, tokenizer, args.mutated_output, args.max_samples
        )
    
    print("Completions finished for both datasets")

if __name__ == "__main__":
    main() 