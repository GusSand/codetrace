#!/usr/bin/env python3
import sys
import os
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from functools import partial
import itertools as it
from typing import List, Dict, Any, Callable

# Add the parent directory to the path so we can import from codetrace
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codetrace.parsing_utils import STARCODER_FIM, fim_placeholder, prepare_fim_prompt
from codetrace.steering import prepare_prompt_pairs

def tokenize(tokenizer, fim_obj, prompt: str) -> str:
    """Mimic the tokenize method in SteeringManager."""
    try:
        return prepare_fim_prompt(tokenizer, fim_obj, prompt)
    except Exception as e:
        print(f"Error in tokenize: {e}")
        # If the prompt doesn't have a placeholder, it's probably a mutated program
        # Let's try to handle it differently
        if fim_obj.placeholder not in prompt:
            print("Prompt doesn't have a placeholder, treating as regular text")
            return prompt
        raise e

def custom_prepare_prompt_pairs(data: List[Dict[str, Any]], format_fn: Callable[[str], str]) -> List[str]:
    """Custom version of prepare_prompt_pairs that handles errors."""
    result = []
    for x in data:
        try:
            fim_program_formatted = format_fn(x["fim_program"])
            result.append(fim_program_formatted)
        except Exception as e:
            print(f"Error formatting fim_program: {e}")
        
        try:
            mutated_program_formatted = format_fn(x["mutated_program"])
            result.append(mutated_program_formatted)
        except Exception as e:
            print(f"Error formatting mutated_program: {e}")
            # If the mutated program doesn't have a placeholder, just use it as is
            if STARCODER_FIM.placeholder not in x["mutated_program"]:
                print("Using mutated_program as is")
                result.append(x["mutated_program"])
    
    return result

def main():
    # Load the security examples
    with open("security/security_steering_examples.json", "r") as f:
        examples = json.load(f)
    
    # Initialize tokenizer
    tokenizer = AutoTokenizer.from_pretrained("bigcode/starcoderbase-1b")
    
    # Test with a simple example
    print("\nTesting with a simple example:")
    simple_example = {
        "fim_program": "This is a test with <FILL> in the middle",
        "mutated_program": "This is a test with placeholder in the middle",
        "prefix": "This is a test with ",
        "suffix": " in the middle",
        "middle": "placeholder"
    }
    
    # Create a format function that mimics the tokenize method
    format_fn = partial(tokenize, tokenizer, STARCODER_FIM)
    
    try:
        # Try to tokenize the simple fim_program
        tokenized_fim = tokenize(tokenizer, STARCODER_FIM, simple_example['fim_program'])
        print(f"Tokenized simple fim_program: {tokenized_fim}")
        
        # Try to tokenize the simple mutated_program
        tokenized_mutated = tokenize(tokenizer, STARCODER_FIM, simple_example['mutated_program'])
        print(f"Tokenized simple mutated_program: {tokenized_mutated}")
        
        # Try our custom prepare_prompt_pairs for the simple example
        prompt_pairs = custom_prepare_prompt_pairs([simple_example], format_fn)
        print(f"Number of prompt pairs: {len(prompt_pairs)}")
        if len(prompt_pairs) >= 1:
            print(f"First prompt in pair: {prompt_pairs[0]}")
        if len(prompt_pairs) >= 2:
            print(f"Second prompt in pair: {prompt_pairs[1]}")
    except Exception as e:
        print(f"Error with simple example: {e}")
    
    # Test with a real security example
    print("\nTesting with a real security example:")
    example = examples[0]
    
    try:
        # Try our custom prepare_prompt_pairs for the real example
        prompt_pairs = custom_prepare_prompt_pairs([example], format_fn)
        print(f"Number of prompt pairs: {len(prompt_pairs)}")
        if len(prompt_pairs) >= 1:
            print(f"First prompt in pair: {prompt_pairs[0][:100]}...")
        if len(prompt_pairs) >= 2:
            print(f"Second prompt in pair: {prompt_pairs[1][:100]}...")
    except Exception as e:
        print(f"Error with real example: {e}")
    
    # Let's look at the steering.py file to understand how it handles mutated programs
    print("\nAnalyzing how steering.py handles mutated programs:")
    
    # Check if the mutated program has a placeholder
    for i, example in enumerate(examples[:3]):
        print(f"\nExample {i}:")
        print(f"fim_program has placeholder: {STARCODER_FIM.placeholder in example['fim_program']}")
        print(f"mutated_program has placeholder: {STARCODER_FIM.placeholder in example['mutated_program']}")
        
        # Check if the mutated program is already in FIM format
        print(f"fim_program is in FIM format: {STARCODER_FIM._is_fim(example['fim_program'])}")
        print(f"mutated_program is in FIM format: {STARCODER_FIM._is_fim(example['mutated_program'])}")
        
        # Check if the mutated program is in placeholder format
        print(f"fim_program is in placeholder format: {STARCODER_FIM._is_placeholder(example['fim_program'])}")
        print(f"mutated_program is in placeholder format: {STARCODER_FIM._is_placeholder(example['mutated_program'])}")

if __name__ == "__main__":
    main() 