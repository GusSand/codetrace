#!/usr/bin/env python3
import json
import os
import datasets
import random
from pathlib import Path

def create_steering_candidates(original_ds_path, mutated_ds_path, output_file, num_candidates=5):
    """Create steering candidates manually for testing."""
    print(f"Loading original dataset from {original_ds_path}")
    original_ds = datasets.load_from_disk(original_ds_path)
    
    print(f"Loading mutated dataset from {mutated_ds_path}")
    mutated_ds = datasets.load_from_disk(mutated_ds_path)
    
    # For demonstration purposes, we'll create candidates from the first few examples
    candidates = []
    
    # Get a few examples from the dataset
    for i in range(min(num_candidates, len(original_ds))):
        original_example = original_ds[i]
        mutated_example = mutated_ds[i]
        
        # Create a candidate with the necessary fields
        candidate = {
            "index": i,
            "original_program": original_example["fim_program"],
            "expected_type": original_example["fim_type"],
            "category": "string" if "str" in original_example["fim_type"] else 
                       "numeric" if any(t in original_example["fim_type"] for t in ["int", "float", "number"]) else
                       "flexible" if any(t in original_example["fim_type"] for t in ["Any", "Optional"]) else
                       "other",
            "contexts": ["function", "assignment", "return_type"],
            "generated_type_original": "",  # Simulating an incorrect prediction
            "generated_type_mutated": "",   # Simulating an incorrect prediction
            "original_correct": False,
            "mutated_correct": False
        }
        
        candidates.append(candidate)
    
    # Save the candidates
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(candidates, f, indent=2)
    
    print(f"Created {len(candidates)} steering candidates and saved to {output_file}")
    return candidates

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Create steering candidates manually for testing")
    parser.add_argument("--original-dataset", type=str, default="starcoder1_fim_completions",
                        help="Path to the original dataset")
    parser.add_argument("--mutated-dataset", type=str, default="starcoder1_fim_completions_mutated",
                        help="Path to the mutated dataset")
    parser.add_argument("--output-file", type=str, default="type_inference_results/steering_candidates.json",
                        help="Path to save the steering candidates")
    parser.add_argument("--num-candidates", type=int, default=5,
                        help="Number of steering candidates to create")
    args = parser.parse_args()
    
    create_steering_candidates(
        args.original_dataset,
        args.mutated_dataset,
        args.output_file,
        args.num_candidates
    )

if __name__ == "__main__":
    main() 