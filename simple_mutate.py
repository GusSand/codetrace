import datasets
from codetrace.py_mutator import PyMutator
import argparse
from tqdm import tqdm
import random
import traceback
import os
import hashlib

def apply_mutations(mutator, program, fim_type, mutation_types):
    """Apply specified mutations to a program"""
    try:
        if program is None:
            print("Program is None, skipping mutations")
            return None
            
        print(f"Program starts with: {program[:50]}...")
        print(f"FIM type: {fim_type}")
        print(f"Mutation types: {mutation_types}")
        
        mutated_program = program
        
        if "vars" in mutation_types:
            print("Applying variable renaming...")
            try:
                mutated_program = mutator.random_mutate(mutated_program, fim_type, ["rename_vars"])
                if mutated_program is None:
                    print("Variable renaming returned None, using original program")
                    mutated_program = program
            except Exception as e:
                print(f"Error in variable renaming: {str(e)}")
                print(f"Traceback: {traceback.format_exc()}")
                # Continue with original program
        
        if "types" in mutation_types:
            print("Applying type renaming...")
            try:
                temp_program = mutator.random_mutate(mutated_program, fim_type, ["rename_types"])
                if temp_program is not None:
                    mutated_program = temp_program
                else:
                    print("Type renaming returned None, keeping previous version")
            except Exception as e:
                print(f"Error in type renaming: {str(e)}")
                print(f"Traceback: {traceback.format_exc()}")
                # Continue with current program
            
        if "delete" in mutation_types:
            print("Applying annotation deletion...")
            try:
                temp_program = mutator.random_mutate(mutated_program, fim_type, ["delete_annotations"])
                if temp_program is not None:
                    mutated_program = temp_program
                else:
                    print("Annotation deletion returned None, keeping previous version")
            except Exception as e:
                print(f"Error in annotation deletion: {str(e)}")
                print(f"Traceback: {traceback.format_exc()}")
                # Continue with current program
            
        return mutated_program
    except Exception as e:
        print(f"Error applying mutations: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Apply mutations to a dataset using PyMutator directly")
    parser.add_argument("--input-path", type=str, required=True, help="Path to the input dataset")
    parser.add_argument("--output-path", type=str, required=True, help="Path to save the mutated dataset")
    parser.add_argument("--save-files", type=str, help="Directory to save individual mutated files")
    parser.add_argument("--mutation-types", type=str, nargs="+", choices=["vars", "types", "delete"], 
                        default=["vars"], help="Types of mutations to apply")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--debug", action="store_true", help="Enable verbose debug output")
    args = parser.parse_args()
    
    random.seed(args.seed)
    
    # Create directory for individual files if specified
    if args.save_files:
        os.makedirs(args.save_files, exist_ok=True)
        print(f"Will save individual files to {args.save_files}")
    
    print(f"Loading dataset from {args.input_path}...")
    ds = datasets.load_from_disk(args.input_path)
    
    print(f"Dataset has {len(ds)} examples with columns: {ds.column_names}")
    print(f"First example fim_type: {ds[0]['fim_type']}")
    print(f"Applying mutations: {', '.join(args.mutation_types)}...")
    
    # Try mutation on a test example to verify the setup works
    test_example = ds[0]
    print("\nTesting mutation on first example:")
    mutator = PyMutator()
    
    # Process just the first example for testing
    test_result = apply_mutations(mutator, test_example["fim_program"], test_example["fim_type"], args.mutation_types)
    if test_result:
        print("Test mutation successful!")
        print(f"Original starts with: {test_example['fim_program'][:100]}...")
        print(f"Mutated starts with: {test_result[:100]}...")
    else:
        print("Test mutation failed. Please check the error messages above.")

    print("\nProcessing full dataset...")
    def process_example(example):
        try:
            if args.debug:
                print(f"\nProcessing example with type: {example['fim_type']}")
            
            # Check if fim_program exists and is not None
            if "fim_program" not in example or example["fim_program"] is None:
                print(f"Example missing fim_program field or it's None, skipping")
                return example
            
            mutated_program = apply_mutations(
                mutator, 
                example["fim_program"],
                example["fim_type"],
                args.mutation_types
            )
            
            if mutated_program:
                example["mutated_program"] = mutated_program
                # If we want to keep track of which mutations were applied
                example["applied_mutations"] = args.mutation_types
                
                # Save individual file if requested
                if args.save_files and mutated_program:
                    # Create a unique filename based on content hash
                    file_hash = hashlib.md5(mutated_program.encode()).hexdigest()[:10]
                    file_type = example["fim_type"].replace("/", "_").replace("<", "").replace(">", "")
                    filename = f"{file_hash}_{file_type}.py"
                    file_path = os.path.join(args.save_files, filename)
                    
                    with open(file_path, "w") as f:
                        f.write(mutated_program)
                    
                    # Store the file path in the example
                    example["mutated_file_path"] = file_path
            else:
                # If mutation failed but we still have the original program, 
                # we can optionally use it as is
                print("Mutation failed, keeping original program")
                example["mutated_program"] = example["fim_program"]
                example["applied_mutations"] = []
            
            return example
        except Exception as e:
            print(f"Error processing example: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            return example
    
    # Process just a few examples if debugging
    if args.debug:
        print("Debug mode: processing only 5 examples")
        mutated_ds = ds.select(range(min(5, len(ds)))).map(process_example)
    else:
        mutated_ds = ds.map(process_example)
    
    # Check how many examples were successfully mutated
    successful = sum(1 for ex in mutated_ds if "mutated_program" in ex)
    fully_mutated = sum(1 for ex in mutated_ds if "mutated_program" in ex and 
                        "applied_mutations" in ex and len(ex["applied_mutations"]) == len(args.mutation_types))
    fallback_to_original = sum(1 for ex in mutated_ds if "mutated_program" in ex and 
                              "applied_mutations" in ex and len(ex["applied_mutations"]) == 0)
    
    print(f"Successfully processed {successful}/{len(mutated_ds)} examples")
    print(f"Fully mutated: {fully_mutated}")
    print(f"Fallback to original: {fallback_to_original}")
    print(f"Partially mutated: {successful - fully_mutated - fallback_to_original}")
    
    if successful > 0:
        print(f"Saving mutated dataset to {args.output_path}...")
        mutated_ds.save_to_disk(args.output_path)
        print("Mutation complete!")
        
        if args.save_files:
            files_saved = sum(1 for ex in mutated_ds if "mutated_file_path" in ex)
            print(f"Saved {files_saved} individual files to {args.save_files}")
        
        # Print a sample of mutations for verification
        idx = random.randint(0, successful-1)
        examples_with_mutations = [i for i, ex in enumerate(mutated_ds) if "mutated_program" in ex]
        if examples_with_mutations:
            sample_idx = examples_with_mutations[idx % len(examples_with_mutations)]
            sample = mutated_ds[sample_idx]
            print("\nSample mutation:")
            print("Original program:")
            print(sample["fim_program"][:300] + "..." if len(sample["fim_program"]) > 300 else sample["fim_program"])
            print("\nMutated program:")
            print(sample["mutated_program"][:300] + "..." if len(sample["mutated_program"]) > 300 else sample["mutated_program"])
    else:
        print("No examples were successfully mutated. Skipping dataset save.")

if __name__ == "__main__":
    main() 