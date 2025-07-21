#!/usr/bin/env python3
import json
import sys
import os

def examine_early_stop(results_file, num_examples=5):
    """Examine why examples stopped before reaching 10 mutations."""
    if not os.path.exists(results_file):
        print(f"Results file {results_file} not found.")
        return
    
    with open(results_file, 'r') as f:
        data = json.load(f)
    
    # Find examples that stopped early
    early_stop = [r for r in data if len(r['mutations']) < 10]
    
    print(f"Found {len(early_stop)} examples that stopped before 10 mutations.")
    
    # Examine a subset of early stopping examples
    for i, example in enumerate(early_stop[:num_examples]):
        example_id = example["example_id"]
        mutation_count = len(example["mutations"])
        
        print(f"\n{'='*80}")
        print(f"Example {example_id} stopped at {mutation_count} mutations")
        
        if mutation_count > 0:
            last_mutation = example["mutations"][-1]
            print(f"\nLast mutation (#{last_mutation['mutation_number']}):")
            print(f"  Success: {last_mutation.get('success', False)}")
            print(f"  Exact match: {last_mutation.get('exact_match', False)}")
            
            # Check if there's a pattern in the code that might cause issues
            original_code = last_mutation.get("original_code", "")
            mutated_code = last_mutation.get("mutated_code", "")
            
            if original_code and mutated_code:
                # Check if the mutation is too large
                original_lines = original_code.split("\n")
                mutated_lines = mutated_code.split("\n")
                
                print(f"\nOriginal code: {len(original_lines)} lines, {len(original_code)} chars")
                print(f"Mutated code: {len(mutated_lines)} lines, {len(mutated_code)} chars")
                
                # Check for specific patterns that might cause issues
                if "__tmp" in mutated_code:
                    tmp_vars = set()
                    for line in mutated_code.split("\n"):
                        if "__tmp" in line:
                            for word in line.split():
                                if word.startswith("__tmp"):
                                    tmp_vars.add(word.strip(",:()[]{}"))
                    
                    print(f"\nFound {len(tmp_vars)} temporary variables in mutated code:")
                    for var in sorted(tmp_vars)[:10]:  # Show at most 10
                        print(f"  - {var}")
                    
                    if len(tmp_vars) > 10:
                        print(f"  ... and {len(tmp_vars) - 10} more")
            
            # Check if the next mutation attempt would be on a very different program
            if mutation_count > 1:
                prev_mutation = example["mutations"][-2]
                prev_mutated_code = prev_mutation.get("mutated_code", "")
                
                if prev_mutated_code and mutated_code:
                    similarity = len(set(prev_mutated_code.split()) & set(mutated_code.split())) / len(set(prev_mutated_code.split() + mutated_code.split()))
                    print(f"\nSimilarity to previous mutation: {similarity:.2f}")
        else:
            print("No mutations were applied to this example.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python examine_early_stop.py <results_file> [num_examples]")
        sys.exit(1)
    
    results_file = sys.argv[1]
    num_examples = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    examine_early_stop(results_file, num_examples) 