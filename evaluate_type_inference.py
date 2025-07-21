import datasets
import argparse
import json
import os
import sys
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Union, Optional
from pathlib import Path
import random
import traceback
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import hf_hub_download

# Import FIM utility if available in the codebase
try:
    from codetrace.parsing_utils import STARCODER_FIM, fim_placeholder
except ImportError:
    print("Warning: Could not import STARCODER_FIM from codetrace. Using placeholder implementation.")
    # Placeholder implementation
    class FimObj:
        def __init__(self):
            self.placeholder = "<FILL>"
            
        def fim_to_placeholder(self, program: str) -> str:
            # Basic implementation to convert FIM format to placeholder format
            if "<fim_prefix>" in program and "<fim_suffix>" in program:
                prefix = program.split("<fim_prefix>")[1].split("<fim_suffix>")[0]
                suffix = program.split("<fim_suffix>")[1].split("<fim_middle>")[0]
                return f"{prefix}<FILL>{suffix}"
            return program
            
        def placeholder_to_fim(self, program: str) -> str:
            # Basic implementation to convert placeholder format to FIM format
            if self.placeholder in program:
                parts = program.split(self.placeholder)
                if len(parts) == 2:
                    prefix, suffix = parts
                    return f"<fim_prefix>{prefix}<fim_suffix>{suffix}<fim_middle>"
            return program
    
    STARCODER_FIM = FimObj()
    fim_placeholder = "<FILL>"

def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate type inference on original vs. mutated code examples")
    parser.add_argument("--original-dataset", type=str, required=True, 
                      help="Path to the original dataset")
    parser.add_argument("--mutated-dataset", type=str, required=True, 
                      help="Path to the mutated dataset")
    parser.add_argument("--output-dir", type=str, default="type_inference_results",
                      help="Directory to save results")
    parser.add_argument("--model-id", type=str, default="bigcode/starcoderbase-1b",
                      help="Model ID to use for inference")
    parser.add_argument("--num-examples", type=int, default=100,
                      help="Number of examples to evaluate (set to -1 for all)")
    parser.add_argument("--device", type=str, default="cpu",
                      help="Device to run model on (cpu or cuda)")
    parser.add_argument("--seed", type=int, default=42,
                      help="Random seed for reproducibility")
    return parser.parse_args()

def load_datasets(original_path: str, mutated_path: str, num_examples: int, seed: int):
    """Load and process the original and mutated datasets."""
    print(f"Loading original dataset from {original_path}")
    original_ds = datasets.load_from_disk(original_path)
    
    print(f"Loading mutated dataset from {mutated_path}")
    mutated_ds = datasets.load_from_disk(mutated_path)
    
    print(f"Original dataset size: {len(original_ds)}")
    print(f"Mutated dataset size: {len(mutated_ds)}")
    
    # If specified, take a random sample
    if num_examples > 0 and num_examples < len(original_ds):
        random.seed(seed)
        indices = random.sample(range(len(original_ds)), num_examples)
        original_ds = original_ds.select(indices)
        mutated_ds = mutated_ds.select(indices)
        print(f"Sampled {num_examples} examples for evaluation")
    
    return original_ds, mutated_ds

def load_model_and_tokenizer(model_id: str, device: str):
    """Load the model and tokenizer."""
    print(f"Loading model and tokenizer from {model_id}")
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype="auto", device_map=device)
        return model, tokenizer
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

def generate_completions(model, tokenizer, programs: List[str], max_new_tokens: int = 20):
    """Generate completions for the programs."""
    completions = []
    
    for program in tqdm(programs, desc="Generating completions"):
        try:
            inputs = tokenizer(program, return_tensors="pt").to(model.device)
            outputs = model.generate(
                inputs.input_ids,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id
            )
            
            # Get just the newly generated tokens
            new_tokens = outputs[0, inputs.input_ids.shape[1]:]
            completion = tokenizer.decode(new_tokens, skip_special_tokens=True)
            completions.append(completion)
        except Exception as e:
            print(f"Error generating completion: {str(e)}")
            completions.append("")
    
    return completions

def evaluate_type_accuracy(
    expected_types: List[str],
    generated_types: List[str]
) -> Dict[str, Any]:
    """Evaluate the accuracy of type inference."""
    results = {
        "total": len(expected_types),
        "correct": 0,
        "incorrect": 0,
        "empty": 0
    }
    
    for i, (expected, generated) in enumerate(zip(expected_types, generated_types)):
        if not generated or generated.strip() == "":
            results["empty"] += 1
        elif expected.strip() == generated.strip():
            results["correct"] += 1
        else:
            results["incorrect"] += 1
    
    results["accuracy"] = results["correct"] / results["total"] if results["total"] > 0 else 0
    return results

def categorize_type(type_str: str) -> str:
    """Categorize the type into broader categories."""
    if type_str in ['str', 'String']:
        return 'string'
    elif type_str in ['int', 'float', 'number']:
        return 'numeric'
    elif type_str in ['dict', 'Dict']:
        return 'dictionary'
    elif type_str in ['list', 'List', 'Tuple', 'tuple']:
        return 'sequence'
    elif 'Optional' in type_str:
        return 'optional'
    elif type_str in ['bool', 'boolean']:
        return 'boolean'
    elif type_str in ['DataFrame']:
        return 'dataframe'
    else:
        return 'other'

def analyze_results_by_type(
    expected_types: List[str],
    generated_original: List[str],
    generated_mutated: List[str]
) -> Dict[str, Dict[str, Any]]:
    """Analyze results broken down by type category."""
    type_categories = {}
    
    for i, (expected, orig_gen, mut_gen) in enumerate(zip(expected_types, generated_original, generated_mutated)):
        category = categorize_type(expected)
        if category not in type_categories:
            type_categories[category] = {
                "total": 0,
                "original_correct": 0,
                "mutated_correct": 0
            }
        
        type_categories[category]["total"] += 1
        if expected.strip() == orig_gen.strip():
            type_categories[category]["original_correct"] += 1
        if expected.strip() == mut_gen.strip():
            type_categories[category]["mutated_correct"] += 1
    
    # Calculate accuracies
    for category in type_categories:
        stats = type_categories[category]
        stats["original_accuracy"] = stats["original_correct"] / stats["total"] if stats["total"] > 0 else 0
        stats["mutated_accuracy"] = stats["mutated_correct"] / stats["total"] if stats["total"] > 0 else 0
        stats["accuracy_drop"] = stats["original_accuracy"] - stats["mutated_accuracy"]
    
    return type_categories

def main():
    args = parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Load datasets
    original_ds, mutated_ds = load_datasets(
        args.original_dataset, 
        args.mutated_dataset, 
        args.num_examples, 
        args.seed
    )
    
    # Load model and tokenizer
    model, tokenizer = load_model_and_tokenizer(args.model_id, args.device)
    
    # Extract programs from datasets
    original_programs = [ex["fim_program"] for ex in original_ds]
    mutated_programs = [ex["fim_program"] for ex in mutated_ds]
    expected_types = [ex["fim_type"] for ex in original_ds]
    
    # Generate completions for both datasets
    print("\nGenerating completions for original programs...")
    original_completions = generate_completions(model, tokenizer, original_programs)
    
    print("\nGenerating completions for mutated programs...")
    mutated_completions = generate_completions(model, tokenizer, mutated_programs)
    
    # Evaluate results
    print("\nEvaluating results...")
    original_results = evaluate_type_accuracy(expected_types, original_completions)
    mutated_results = evaluate_type_accuracy(expected_types, mutated_completions)
    
    # Analyze results by type category
    type_analysis = analyze_results_by_type(expected_types, original_completions, mutated_completions)
    
    # Calculate overall accuracy drop
    accuracy_drop = original_results["accuracy"] - mutated_results["accuracy"]
    
    # Print and save results
    print("\n===== RESULTS =====")
    print(f"Original dataset accuracy: {original_results['accuracy']:.4f}")
    print(f"Mutated dataset accuracy: {mutated_results['accuracy']:.4f}")
    print(f"Accuracy drop: {accuracy_drop:.4f} ({accuracy_drop / original_results['accuracy'] * 100:.2f}%)")
    
    print("\nAccuracy by Type Category:")
    print("-" * 80)
    print(f"{'Type Category':<15} {'Original':<10} {'Mutated':<10} {'Drop':<10} {'Sample Count':<15}")
    print("-" * 80)
    
    for category, stats in sorted(type_analysis.items()):
        print(f"{category:<15} {stats['original_accuracy']:.4f}     {stats['mutated_accuracy']:.4f}     {stats['accuracy_drop']:.4f}     {stats['total']}")
    
    # Save detailed results to file
    results = {
        "summary": {
            "original_accuracy": original_results["accuracy"],
            "mutated_accuracy": mutated_results["accuracy"],
            "accuracy_drop": accuracy_drop,
            "accuracy_drop_percentage": accuracy_drop / original_results["accuracy"] * 100 if original_results["accuracy"] > 0 else 0,
            "total_examples": len(original_programs)
        },
        "original_results": original_results,
        "mutated_results": mutated_results,
        "type_analysis": type_analysis
    }
    
    results_file = os.path.join(args.output_dir, "type_inference_results.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Save a few examples to examine
    examples = []
    for i in range(min(10, len(original_ds))):
        examples.append({
            "original_program": original_programs[i],
            "mutated_program": mutated_programs[i],
            "expected_type": expected_types[i],
            "original_completion": original_completions[i],
            "mutated_completion": mutated_completions[i],
            "original_correct": expected_types[i].strip() == original_completions[i].strip(),
            "mutated_correct": expected_types[i].strip() == mutated_completions[i].strip()
        })
    
    examples_file = os.path.join(args.output_dir, "example_completions.json")
    with open(examples_file, 'w') as f:
        json.dump(examples, f, indent=2)
    
    print(f"\nResults saved to {results_file}")
    print(f"Example completions saved to {examples_file}")

if __name__ == "__main__":
    main() 