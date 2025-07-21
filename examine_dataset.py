#!/usr/bin/env python3
import json
import sys
from collections import Counter
import re

def examine_dataset(file_path):
    """Examine a mutation dataset and print information about its size and structure."""
    print(f"Examining dataset: {file_path}")
    
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    print(f"Number of examples: {len(data)}")
    
    # Check if mutations exist
    mutation_counts = Counter()
    
    # Check for mutation types
    mutation_types_found = False
    
    # Look for evidence of mutation types in the code
    var_renames = 0
    type_renames = 0
    annotation_deletions = 0
    
    for example in data:
        mutations = example.get('mutations', [])
        mutation_counts[len(mutations)] += 1
        
        # Check for mutation_types field
        for mutation in mutations:
            if 'mutation_types' in mutation:
                mutation_types_found = True
                break
        
        # Check original vs mutated code for evidence of mutations
        original_code = example.get('fim_program', '')
        mutated_code = example.get('mutated_program', '')
        
        if original_code and mutated_code:
            # Check for variable renames (look for __tmp variables)
            if re.search(r'__tmp\d+', mutated_code):
                var_renames += 1
            
            # Check for type renames (look for TypeAlias declarations)
            if re.search(r'TypeAlias', mutated_code) and not re.search(r'TypeAlias', original_code):
                type_renames += 1
            
            # Check for annotation deletions (look for missing type annotations)
            original_annotations = len(re.findall(r':\s*[A-Za-z0-9_\[\]\'\"]+', original_code))
            mutated_annotations = len(re.findall(r':\s*[A-Za-z0-9_\[\]\'\"]+', mutated_code))
            if mutated_annotations < original_annotations:
                annotation_deletions += 1
    
    print(f"Mutation counts: {dict(mutation_counts)}")
    print(f"Mutation_types field found: {mutation_types_found}")
    print(f"Evidence of mutations:")
    print(f"  Variable renames: {var_renames}")
    print(f"  Type renames: {type_renames}")
    print(f"  Annotation deletions: {annotation_deletions}")
    
    # Print a sample example
    if data:
        print("\nSample example:")
        example = data[0]
        print(f"  Example ID: {example.get('example_id')}")
        print(f"  FIM Type: {example.get('fim_type')}")
        
        # Print mutations
        mutations = example.get('mutations', [])
        if mutations:
            print(f"  Number of mutations: {len(mutations)}")
            print(f"  First mutation:")
            mutation = mutations[0]
            for key, value in mutation.items():
                if key not in ['original_code', 'mutated_code', 'prompt']:
                    print(f"    {key}: {value}")
        
        # Print original vs mutated code for the first example
        original_code = example.get('fim_program', '')
        mutated_code = example.get('mutated_program', '')
        
        if original_code and mutated_code:
            # Find a short section with differences
            original_lines = original_code.split('\n')
            mutated_lines = mutated_code.split('\n')
            
            print("\n  Code comparison (first 10 lines with differences):")
            diff_count = 0
            for i in range(min(len(original_lines), len(mutated_lines))):
                if original_lines[i] != mutated_lines[i]:
                    print(f"    Original: {original_lines[i]}")
                    print(f"    Mutated:  {mutated_lines[i]}")
                    print()
                    diff_count += 1
                    if diff_count >= 10:
                        break

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python examine_dataset.py <dataset_file>")
        sys.exit(1)
    
    examine_dataset(sys.argv[1]) 