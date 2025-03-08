#!/usr/bin/env python3
import json
import sys
import difflib

def main():
    with open('security_steering_data.json', 'r') as f:
        data = json.load(f)
    
    print(f"Total examples: {len(data)}")
    print("\nFunction names:")
    for i, example in enumerate(data):
        print(f"Example {i}: {example['function_name']} (similarity: {example['similarity']:.4f})")
    
    # Show differences for each example
    for i, example in enumerate(data):
        print(f"\n\n=== Example {i}: {example['function_name']} ===")
        
        # Extract code from prompt (removing the "Security review of this code:" prefix)
        vuln_code = example['prompt'].replace("Security review of this code:\n\n", "")
        secure_code = example['mutated_program']
        
        # Generate diff
        diff = list(difflib.unified_diff(
            vuln_code.splitlines(),
            secure_code.splitlines(),
            fromfile='Vulnerable',
            tofile='Secure',
            lineterm=''
        ))
        
        # Print diff if there are differences
        if len(diff) > 0:
            print("Differences found:")
            for line in diff[:20]:  # Limit to first 20 lines of diff
                print(line)
            if len(diff) > 20:
                print(f"... and {len(diff) - 20} more lines")
        else:
            print("No differences found (identical code)")

if __name__ == "__main__":
    main() 