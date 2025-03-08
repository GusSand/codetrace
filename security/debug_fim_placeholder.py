#!/usr/bin/env python3
import sys
import os
import torch
from transformers import AutoTokenizer

# Add the parent directory to the path so we can import from codetrace
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codetrace.parsing_utils import STARCODER_FIM, fim_placeholder

def test_placeholder_format(prompt):
    """Test if a prompt is in the correct FIM placeholder format."""
    print(f"\nTesting prompt: {prompt}")
    try:
        # Check if the placeholder is in the prompt
        print(f"Placeholder in prompt: {STARCODER_FIM.placeholder in prompt}")
        
        # Check if the prompt is already in FIM format
        is_fim = STARCODER_FIM._is_fim(prompt)
        print(f"Is already in FIM format: {is_fim}")
        
        # Check if the prompt is in placeholder format
        is_placeholder = STARCODER_FIM._is_placeholder(prompt)
        print(f"Is in placeholder format: {is_placeholder}")
        
        # Try to convert to FIM format
        if is_placeholder and not is_fim:
            fim_prompt = STARCODER_FIM.placeholder_to_fim(prompt)
            print(f"Successfully converted to FIM format: {fim_prompt}")
            return True
        else:
            print("Failed to convert to FIM format")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    # Test various placeholder formats
    test_cases = [
        # Basic test with placeholder in the middle
        "This is a test with <FILL> in the middle",
        
        # Test with placeholder at the beginning
        "<FILL> at the beginning",
        
        # Test with placeholder at the end
        "At the end <FILL>",
        
        # Test with multiple placeholders
        "Multiple <FILL> placeholders <FILL>",
        
        # Test with no placeholder
        "No placeholder here",
        
        # Test with FIM format already
        "<fim_prefix>prefix<fim_suffix>suffix<fim_middle>middle",
        
        # Test with code-like format
        "def function(): <FILL> return result",
        
        # Test with our security example format
        "// Security task: Replace vulnerable code with secure implementation\n// Vulnerability: sql_injection (CWE-89)\n\ndef search_users(user_input): <FILL>     query = \"SELECT * FROM users WHERE name = '\" + user_input + \"'\"\n    return execute_query(query)"
    ]
    
    results = []
    for test_case in test_cases:
        result = test_placeholder_format(test_case)
        results.append(result)
    
    print("\nSummary:")
    for i, (test_case, result) in enumerate(zip(test_cases, results)):
        print(f"Test case {i+1}: {'Success' if result else 'Failure'}")
        
    # Now let's try to fix our security example format
    print("\nTrying to fix our security example format:")
    security_example = "// Security task: Replace vulnerable code with secure implementation\n// Vulnerability: sql_injection (CWE-89)\n\ndef search_users(user_input): <FILL>     query = \"SELECT * FROM users WHERE name = '\" + user_input + \"'\"\n    return execute_query(query)"
    
    # Try splitting by the placeholder and reconstructing
    parts = security_example.split("<FILL>")
    if len(parts) == 2:
        prefix = parts[0]
        suffix = parts[1]
        print(f"Prefix: {prefix}")
        print(f"Suffix: {suffix}")
        
        # Try reconstructing with the placeholder
        reconstructed = prefix + "<FILL>" + suffix
        print(f"Reconstructed: {reconstructed}")
        test_placeholder_format(reconstructed)
    
if __name__ == "__main__":
    main() 