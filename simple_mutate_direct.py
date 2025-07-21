import datasets
import argparse
import os
import sys
import traceback
from codetrace.py_mutator import PyMutator
from codetrace.parsing_utils import STARCODER_FIM, fim_placeholder, get_captures
from codetrace.py_mutator import PY_VARIABLE_DECLARATION_QUERY

def process_example(example, mutator, debug=False):
    try:
        if debug:
            print(f"Original program: {example['fim_program']}")
            print(f"FIM type: {example['fim_type']}")
        
        # Check if we're working with FIM format
        program = example['fim_program']
        
        # First, check if the program is in FIM format
        if "<fim_prefix>" in program and "<fim_suffix>" in program and "<fim_middle>" in program:
            # Convert FIM format to placeholder format
            program_with_placeholder = STARCODER_FIM.fim_to_placeholder(program)
            if debug:
                print(f"Program with placeholder: {program_with_placeholder}")
        else:
            # Already in placeholder format or not FIM format
            program_with_placeholder = program
            if debug:
                print("Program not in FIM format, using as is")
        
        # Check if the placeholder exists in the program
        if fim_placeholder not in program_with_placeholder:
            if debug:
                print(f"Program does not contain placeholder '{fim_placeholder}'")
            # Try to add placeholder at the end as a fallback
            program_with_placeholder = program + " " + fim_placeholder
            if debug:
                print(f"Added placeholder to end: {program_with_placeholder}")
        
        # Apply mutations
        mutation_types = ["vars"]
        if debug:
            print(f"Applying mutation types: {mutation_types}")
        
        # Replace placeholder to prevent tree-sitter errors
        program_with_placeholder = mutator.replace_placeholder(program_with_placeholder)
        if debug:
            print(f"Program after replace_placeholder: {program_with_placeholder[:50]}...")
        
        # Get variable captures directly using get_captures
        var_captures = get_captures(program_with_placeholder, PY_VARIABLE_DECLARATION_QUERY, "py", "id")
        if debug:
            print(f"Variable renaming opportunities: {len(var_captures)}")
            for i, var in enumerate(var_captures[:5]):  # Show first 5 for debugging
                print(f"  Var {i}: {var.text.decode('utf-8')} at {var.start_byte}-{var.end_byte}")
        
        # Generate mutations
        mutations = []
        if var_captures:
            var_mutations = mutator.rename_vars(var_captures)
            mutations.extend(var_mutations)
            if debug:
                print(f"Generated {len(var_mutations)} variable mutations")
        
        # If no mutations were created, return None
        if not mutations:
            if debug:
                print("No mutations were created")
            return None
        
        # Apply the mutations
        try:
            mutated_program = mutator.apply_mutations(program_with_placeholder, mutations)
            if debug:
                print(f"Mutated program: {mutated_program[:50]}...")  # Show beginning of mutated program
            
            # Convert mutation objects to serializable dict format
            serializable_mutations = []
            for mut in mutations:
                serializable_mutations.append({
                    'start_byte': mut.location.start_byte,
                    'end_byte': mut.location.end_byte,
                    'replacement': mut.byte_replacement.decode('utf-8') if isinstance(mut.byte_replacement, bytes) else mut.byte_replacement,
                    'prefix': mut.prefix.decode('utf-8') if mut.prefix and isinstance(mut.prefix, bytes) else mut.prefix
                })
            
            # Convert back to FIM format if original was in FIM format
            if "<fim_prefix>" in program and "<fim_suffix>" in program and "<fim_middle>" in program:
                mutated_program_fim = STARCODER_FIM.placeholder_to_fim(mutated_program)
                if debug:
                    print(f"Mutated program in FIM format: {mutated_program_fim[:50]}...")
                
                # Create a new example with all the original fields plus the mutated program
                mutated_example = dict(example)
                mutated_example["original_program"] = example["fim_program"]
                mutated_example["fim_program"] = mutated_program_fim
                mutated_example["mutations_info"] = serializable_mutations
                return mutated_example
            else:
                # Create a new example with all the original fields plus the mutated program
                mutated_example = dict(example)
                mutated_example["original_program"] = example["fim_program"]
                mutated_example["fim_program"] = mutated_program
                mutated_example["mutations_info"] = serializable_mutations
                return mutated_example
        except Exception as e:
            if debug:
                print(f"Error applying mutations: {str(e)}")
                traceback.print_exc()
            return None
    except Exception as e:
        if debug:
            print(f"Error processing example: {str(e)}")
            traceback.print_exc()
        return None

def main():
    parser = argparse.ArgumentParser(description="Test PyMutator directly on a dataset")
    parser.add_argument("--input-path", required=True, help="Path to the input dataset")
    parser.add_argument("--output-path", help="Path to save the mutated dataset")
    parser.add_argument("--example-index", type=int, default=0, help="Index of example to test")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--num-examples", type=int, help="Number of examples to process (default: all)")
    args = parser.parse_args()
    
    print(f"Loading dataset from {args.input_path}")
    dataset = datasets.load_from_disk(args.input_path)
    print(f"Dataset loaded with {len(dataset)} examples")
    print(f"Dataset columns: {dataset.column_names}")
    
    # Create the mutator
    mutator = PyMutator()
    
    # Process a single example for testing
    if args.debug:
        print(f"\nTesting example at index {args.example_index}")
        example = dataset[args.example_index]
        result = process_example(example, mutator, debug=True)
        if result:
            print("Mutation successful!")
        else:
            print("Mutation failed!")
    
    # Determine number of examples to process
    num_examples = args.num_examples if args.num_examples else len(dataset)
    if args.debug:
        # Limit to 10 examples in debug mode
        num_examples = min(10, num_examples)
    
    print(f"Processing {num_examples} examples...")
    successful = 0
    mutated_examples = []
    
    for i in range(num_examples):
        if i % 10 == 0:
            print(f"\nProcessing example {i}/{num_examples}")
        example = dataset[i]
        result = process_example(example, mutator, debug=args.debug)
        if result:
            successful += 1
            mutated_examples.append(result)
    
    print(f"Successfully mutated {successful}/{num_examples} examples")
    
    # Save the mutated dataset if output path is provided
    if args.output_path and mutated_examples:
        print(f"Saving {len(mutated_examples)} mutated examples to {args.output_path}")
        mutated_dataset = datasets.Dataset.from_list(mutated_examples)
        mutated_dataset.save_to_disk(args.output_path)
        print("Dataset saved successfully")
    elif mutated_examples:
        print("No output path provided, skipping dataset save")
    else:
        print("No examples were successfully mutated. Skipping dataset save.")

if __name__ == "__main__":
    main() 