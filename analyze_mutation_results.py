import json
import sys
from pprint import pprint

# Load the results
with open('data/mutation_robustness_results.json', 'r') as f:
    data = json.load(f)

# Print summary statistics
print(f"Total examples: {len(data)}")
print(f"Examples with all mutations successful: {sum(1 for ex in data if all(m.get('success', False) for m in ex.get('mutations', [])))}")
print(f"Examples with at least one failed mutation: {sum(1 for ex in data if any(not m.get('success', True) for m in ex.get('mutations', [])))}")
print(f"Average mutations per example: {sum(len(ex.get('mutations', [])) for ex in data)/len(data):.2f}")

# Calculate exact match statistics
total_mutations = sum(len(ex.get('mutations', [])) for ex in data)
exact_matches = sum(sum(1 for m in ex.get('mutations', []) 
                      if m.get('completion') == ex.get('original_completion'))
                   for ex in data)
print(f"Total mutations: {total_mutations}")
print(f"Exact matches with original completion: {exact_matches} ({exact_matches/total_mutations*100:.2f}%)")

# Count examples by number of exact matches
match_counts = {}
for ex in data:
    matches = sum(1 for m in ex.get('mutations', []) 
                 if m.get('completion') == ex.get('original_completion'))
    total = len(ex.get('mutations', []))
    key = f"{matches}/{total}"
    match_counts[key] = match_counts.get(key, 0) + 1

print("\nExamples by match ratio:")
for key in sorted(match_counts.keys()):
    print(f"  {key} matches: {match_counts[key]} examples")

# Print details of a specific example
if len(sys.argv) > 1:
    example_idx = int(sys.argv[1])
    if 0 <= example_idx < len(data):
        example = data[example_idx]
        print("\nExample Details:")
        print(f"Example ID: {example.get('example_id')}")
        print(f"FIM Type: {example.get('fim_type')}")
        print(f"Original Success: {example.get('original_success')}")
        print(f"Original Completion: {repr(example.get('original_completion'))}")
        
        print("\nMutations:")
        for i, mutation in enumerate(example.get('mutations', [])):
            print(f"\nMutation {i+1}:")
            print(f"  Success: {mutation.get('success')}")
            print(f"  Completion: {repr(mutation.get('completion'))}")
            
            # Check if completions match
            if example.get('original_completion') == mutation.get('completion'):
                print("  Result: EXACT MATCH with original")
            else:
                print("  Result: DIFFERENT from original")
    else:
        print(f"Example index {example_idx} out of range (0-{len(data)-1})")
else:
    # If no example specified, print the first 3 examples
    for i in range(min(3, len(data))):
        example = data[i]
        print(f"\nExample {i}:")
        print(f"  FIM Type: {example.get('fim_type')}")
        print(f"  Original Completion: {repr(example.get('original_completion'))[:50]}...")
        print(f"  Number of Mutations: {len(example.get('mutations', []))}")
        
        # Count matches
        matches = sum(1 for m in example.get('mutations', []) 
                     if m.get('completion') == example.get('original_completion'))
        print(f"  Mutations with exact match: {matches}/{len(example.get('mutations', []))}") 