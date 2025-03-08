#!/usr/bin/env python3
import json
import argparse
import difflib
from typing import Dict, List, Any, Tuple

def find_diff(vulnerable_code: str, secure_code: str) -> Tuple[str, str]:
    """
    Find the difference between vulnerable and secure code.
    Returns a tuple of (vulnerable_context, security_fix)
    """
    # Simple diff - this could be improved for more complex cases
    vulnerable_lines = vulnerable_code.splitlines()
    secure_lines = secure_code.splitlines()
    
    # Use difflib to find differences
    diff = list(difflib.unified_diff(
        vulnerable_lines,
        secure_lines,
        n=0,  # No context lines
        lineterm=''
    ))
    
    # For now, let's just use the whole secure code as the fix
    # A more sophisticated approach would isolate just the changed lines
    security_fix = secure_code
    
    return vulnerable_code, security_fix

def adapt_security_dataset(input_file: str, output_file: str):
    """
    Adapt the security steering dataset to match the format expected by the steering pipeline.
    
    For security vulnerabilities, we'll:
    1. Present the vulnerable code
    2. Add "// The secure version of this code is:" transition
    3. Place <FILL> token for the model to generate the fixed code
    """
    print(f"Reading security dataset from {input_file}...")
    with open(input_file, 'r') as f:
        security_data = json.load(f)
    
    adapted_data = []
    
    for idx, example in enumerate(security_data):
        # Extract the code part from the prompt (remove the "Security review" prefix)
        prompt_text = example['prompt']
        vulnerable_code = prompt_text.replace("Security review of this code:\n\n", "")
        secure_code = example['mutated_program']
        
        # Identify the vulnerable context and security fix
        context, fix = find_diff(vulnerable_code, secure_code)
        
        # Create a FIM-style example
        adapted_example = {
            # Fields required by the steering pipeline
            "fim_program": context + "\n\n// The secure version of this code is:\n<FILL>",
            "fim_type": fix,
            
            # Preserve original fields
            "original_prompt": example['prompt'],
            "original_completion": example['completion'],
            "original_vulnerable_code": vulnerable_code,
            "original_secure_code": secure_code,
            
            # Preserve metadata
            "cwe": example.get('cwe', ""),
            "vulnerability_type": example.get('vulnerability_type', ""),
            "source": example.get('source', ""),
            "idx": idx,
        }
        
        # Add additional fields if present
        for key, value in example.items():
            if key not in adapted_example and key not in ['prompt', 'completion', 'mutated_program']:
                adapted_example[key] = value
        
        adapted_data.append(adapted_example)
    
    print(f"Adapted {len(adapted_data)} examples.")
    
    # Save the adapted dataset
    print(f"Saving adapted dataset to {output_file}...")
    with open(output_file, 'w') as f:
        json.dump(adapted_data, f, indent=2)
    
    print("Done!")

def main():
    parser = argparse.ArgumentParser(description='Adapt security steering dataset for the FIM steering pipeline')
    parser.add_argument('--input_file', type=str, default='./security_steering_data.json',
                      help='Input security steering dataset file')
    parser.add_argument('--output_file', type=str, default='./security_steering_data_fim.json',
                      help='Output file for the adapted dataset')
    args = parser.parse_args()
    
    adapt_security_dataset(args.input_file, args.output_file)

if __name__ == "__main__":
    main() 