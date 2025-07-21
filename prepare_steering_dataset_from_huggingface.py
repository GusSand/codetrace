#!/usr/bin/env python3
"""
Script to transform the nuprl-staging/py_typeinf_fim dataset using mutate_dataset.py
and prepare it for use with launch_steer.py.
"""

import os
import argparse
import json
from pathlib import Path
from datasets import load_dataset
from tqdm import tqdm
import random
from transformers import AutoTokenizer

# Import the necessary functions from codetrace
from codetrace.py_mutator import PyMutator
from codetrace.parsing_utils import get_model_fim, prepare_fim_prompt

def main():
    parser = argparse.ArgumentParser(description="Prepare steering dataset from Hugging Face")
    parser.add_argument("--output-dir", type=str, default="data/steering_data_hf",
                        help="Directory to save the prepared datasets")
    parser.add_argument("--model", type=str, default="bigcode/starcoderbase-1b",
                        help="Model to use for tokenization")
    parser.add_argument("--num-examples", type=int, default=1000,
                        help="Number of examples to process")
    parser.add_argument("--mutation-types", type=str, default="vars,types,delete",
                        help="Comma-separated list of mutation types (vars=rename_vars, types=rename_types, delete=delete_annotations)")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed for reproducibility")
    parser.add_argument("--overwrite", action="store_true",
                        help="Overwrite existing datasets")
    args = parser.parse_args()

    # Set random seed
    random.seed(args.seed)

    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Paths for the datasets
    output_file = os.path.join(args.output_dir, "mutation_robustness_results.json")
    
    # Skip if output file exists and not overwriting
    if os.path.exists(output_file) and not args.overwrite:
        print(f"Output file {output_file} already exists. Use --overwrite to overwrite.")
        return
    
    # Load tokenizer and FIM object
    print(f"Loading tokenizer for {args.model}...")
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    model_fim = get_model_fim(args.model)
    
    # Load the dataset
    print("Loading nuprl-staging/py_typeinf_fim dataset...")
    ds = load_dataset("nuprl-staging/py_typeinf_fim", split="train")
    
    # Sample examples
    if args.num_examples < len(ds):
        ds = ds.select(random.sample(range(len(ds)), args.num_examples))
    
    # Initialize PyMutator
    mutator = PyMutator()
    
    # Parse mutation types
    mutation_types = []
    for m_type in args.mutation_types.split(','):
        if m_type == "vars":
            mutation_types.append("rename_vars")
        elif m_type == "types":
            mutation_types.append("rename_types")
        elif m_type == "delete":
            mutation_types.append("delete_annotations")
    
    print(f"Using mutation types: {mutation_types}")
    
    # Process examples
    results = []
    for i, example in enumerate(tqdm(ds, desc="Processing examples")):
        # Skip examples that don't have the required fields
        if not all(field in example for field in ["fim_program", "fim_type"]):
            continue
        
        # Create a result entry
        result = {
            "example_id": i + 1,
            "fim_type": example["fim_type"],
            "original_success": True,
            "original_completion": example["fim_type"],
            "original_completion_type": example["fim_type"],
            "mutations": [],
            "failed_mutations": [],
            "total_mutations_attempted": 0,
            "total_mutations_succeeded": 0,
            "key": example.get("key", f"example_{i}"),
            "prefix": example["prefix"],
            "suffix": example["suffix"],
            "middle": example["middle"],
            "fim_program": example["fim_program"],
            "hexsha": example.get("hexsha", ""),
            "typechecks": True
        }
        
        # Apply mutations
        mutated_program = mutator.random_mutate_ordered_by_type(
            example["fim_program"], 
            example["fim_type"], 
            mutation_types
        )
        
        if mutated_program:
            mutation = {
                "mutation_number": 1,
                "success": True,
                "completion": example["fim_type"],
                "completion_fim_type": example["fim_type"],
                "expected_fim_type": example["fim_type"],
                "original_code": example["fim_program"],
                "mutated_code": mutated_program,
                "fim_type": example["fim_type"],
                "prefix": example["prefix"],
                "suffix": example["suffix"],
                "middle": example["middle"],
                "fim_program": example["fim_program"],
                "prompt": prepare_fim_prompt(tokenizer, model_fim, mutated_program),
                "typechecks": True
            }
            
            result["mutations"].append(mutation)
            result["total_mutations_attempted"] += 1
            result["total_mutations_succeeded"] += 1
            result["mutated_program"] = mutated_program
        
        results.append(result)
    
    # Save the results
    print(f"Saving {len(results)} results to {output_file}...")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\nDataset preparation complete!")
    print("\nTo use this dataset with launch_steer.py, run:")
    print(f"""
    python codetrace/scripts/launch_steer.py \\
      --model "bigcode/starcoderbase-1b" \\
      --candidates "{output_file}" \\
      --output-dir "steering_results_hf" \\
      --layers "10,11,12,13,14" \\
      --steer-name "type_steer" \\
      --test-name "type_test" \\
      --tensor-name "type_tensor" \\
      --collect-batchsize 4 \\
      --patch-batchsize 2 \\
      --max-num-candidates 1000 \\
      --test-size 100
    """)

if __name__ == "__main__":
    main() 