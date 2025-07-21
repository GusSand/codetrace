#!/usr/bin/env python3
import datasets
import argparse
import random
import traceback
from tqdm import tqdm
from pathlib import Path
from codetrace.py_mutator import PyMutator

def apply_mutations(program, fim_type, mutation_types):
    """Apply mutations to a program."""
    try:
        # Create a PyMutator instance without arguments
        mutator = PyMutator()
        
        # Apply mutations based on the specified types
        if "vars" in mutation_types:
            program = mutator.random_mutate(program, fim_type, ["rename_vars"])
        
        if "types" in mutation_types:
            program = mutator.random_mutate(program, fim_type, ["rename_types"])
            
        if "delete_annotations" in mutation_types:
            program = mutator.random_mutate(program, fim_type, ["delete_annotations"])
        
        return program, True
    except Exception as e:
        print(f"Mutation error: {str(e)}")
        print(traceback.format_exc())
        return program, False

def create_mutated_dataset(input_path, output_path, mutation_types, max_samples=None, seed=42):
    """Create a mutated version of the dataset."""
    # Set random seed for reproducibility
    random.seed(seed)
    
    # Load the dataset
    print(f"Loading dataset from {input_path}...")
    dataset = datasets.load_from_disk(input_path)
    
    # Limit the number of samples if specified
    if max_samples and max_samples < len(dataset):
        dataset = dataset.select(range(max_samples))
    
    print(f"Dataset loaded with {len(dataset)} examples")
    print(f"Applying mutations: {', '.join(mutation_types)}")
    
    # Create a PyMutator instance for testing
    mutator = PyMutator()
    
    # Test on the first example
    print("Testing mutation on first example...")
    test_example = dataset[0]
    test_program = test_example["fim_program"]
    test_type = test_example["fim_type"]
    
    try:
        if "vars" in mutation_types:
            test_result = mutator.random_mutate(test_program, test_type, ["rename_vars"])
            print("Variable renaming test successful!")
            print(f"Original: {test_program[:100]}...")
            print(f"Mutated: {test_result[:100]}...")
    except Exception as e:
        print(f"Test mutation failed: {str(e)}")
        print(traceback.format_exc())
    
    # Apply mutations to the dataset
    print("Applying mutations to dataset...")
    
    # Track statistics
    successful_mutations = 0
    total_mutations = 0
    
    def process_example(example):
        nonlocal successful_mutations, total_mutations
        
        program = example["fim_program"]
        fim_type = example["fim_type"]
        
        # Apply mutations
        mutated_program, success = apply_mutations(program, fim_type, mutation_types)
        
        # Update statistics
        if success and mutated_program != program:
            successful_mutations += 1
            total_mutations += 1
            example["original_program"] = program
            example["mutated_program"] = mutated_program
        
        return example
    
    # Apply mutations to all examples
    mutated_dataset = dataset.map(process_example)
    
    print(f"Successfully mutated {successful_mutations}/{len(mutated_dataset)} examples")
    print(f"Average mutations per example: {total_mutations/len(mutated_dataset):.2f}")
    
    # Save the mutated dataset if any mutations were successful
    if successful_mutations > 0:
        # Create the output directory if it doesn't exist
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Save the dataset
        mutated_dataset.save_to_disk(output_path)
        print(f"Mutated dataset saved to {output_path}")
        
        # Print a sample mutation
        sample_idx = random.randint(0, len(mutated_dataset) - 1)
        sample = mutated_dataset[sample_idx]
        if "mutated_program" in sample:
            print("\nSample mutation:")
            print(f"Original: {sample['original_program'][:200]}...")
            print(f"Mutated: {sample['mutated_program'][:200]}...")
    else:
        print("No examples were successfully mutated. Dataset not saved.")
    
    # Print mutation summary
    print("\nMutation Summary:")
    print(f"Total examples: {len(mutated_dataset)}")
    print(f"Successfully mutated: {successful_mutations} ({successful_mutations/len(mutated_dataset):.2%})")
    print(f"Failed mutations: {len(mutated_dataset) - successful_mutations}")
    print(f"Average mutations per example: {total_mutations/len(mutated_dataset):.2f}")

def main():
    parser = argparse.ArgumentParser(description="Create a mutated version of a type inference dataset")
    parser.add_argument("--input-path", type=str, default="starcoder1_fim_completions",
                        help="Path to the input dataset")
    parser.add_argument("--output-path", type=str, default="starcoder1_fim_completions_mutated",
                        help="Path to save the mutated dataset")
    parser.add_argument("--mutation-types", type=str, nargs="+", 
                        choices=["vars", "types", "delete_annotations"],
                        default=["vars"],
                        help="Types of mutations to apply")
    parser.add_argument("--max-samples", type=int, default=None,
                        help="Maximum number of samples to process")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed for reproducibility")
    args = parser.parse_args()
    
    create_mutated_dataset(
        args.input_path,
        args.output_path,
        args.mutation_types,
        args.max_samples,
        args.seed
    )

if __name__ == "__main__":
    main() 