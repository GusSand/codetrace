#!/usr/bin/env python3
import datasets
from pathlib import Path
import pandas as pd
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import Terminal256Formatter
from pygments.token import Token
from pygments.lexer import inherit
import json
import sys
from pprint import pprint
import os
from collections import Counter

class FIMPythonLexer(PythonLexer):
    """Custom lexer that highlights FIM tags and code"""
    tokens = {
        'root': [
            (r'<prefix>|</prefix>|<suffix>|</suffix>|<middle>|</middle>', Token.Generic.Prompt),  # Red tags
            inherit,
        ]
    }

def format_fim_parts(program: str) -> str:
    """Format the program showing FIM structure inline with highlighted tags."""
    # Split into prefix, middle, suffix based on <FILL>
    parts = program.split('<FILL>')
    if len(parts) != 2:
        return "Error: Could not find <FILL> token"
    
    prefix, suffix = parts
    
    # Construct the FIM format with tags
    fim_format = f"<prefix>{prefix.rstrip()}</prefix> <middle>TYPE</middle> <suffix>{suffix.lstrip()}</suffix>"
    
    # Highlight the entire thing including tags
    return highlight(fim_format, FIMPythonLexer(), Terminal256Formatter(style='monokai'))

# Load the dataset
ds = datasets.load_from_disk('starcoder1_fim_completions')

# Convert to pandas for easier analysis
df = ds.to_pandas()

# Print overall statistics
print("\nOverall Statistics:")
print("-" * 50)
print(f"Total examples: {len(df)}")
print(f"Correct predictions: {df['correct'].sum()}")
print(f"Accuracy: {df['correct'].mean()*100:.2f}%")

# Print some example predictions
print("\nExample Predictions:")
print("-" * 50)
for i, row in df.iterrows():
    print(f"\nExample {i+1}:")
    print("Program context (FIM structure):")
    print("-" * 20)
    print(format_fim_parts(row['fim_program']))
    print("\nType prediction:")
    print("-" * 20)
    print(f"Expected type:   {row['fim_type']}")
    print(f"Generated type:  {row['generated_text']}")
    print(f"Correct:         {row['correct']}")
    print("=" * 50)

# Analyze error patterns
print("\nError Analysis:")
print("-" * 50)
incorrect_df = df[~df['correct']]
if len(incorrect_df) > 0:
    print("\nIncorrect Predictions:")
    for i, row in incorrect_df.iterrows():
        print(f"\nMisprediction {i+1}:")
        print("Program context (FIM structure):")
        print("-" * 20)
        print(format_fim_parts(row['fim_program']))
        print("\nType prediction:")
        print("-" * 20)
        print(f"Expected type:   {row['fim_type']}")
        print(f"Generated type:  {row['generated_text']}")
        print("=" * 50)

# Load the results
with open('data/mutation_robustness_results.json', 'r') as f:
    data = json.load(f)

# Print summary statistics
print(f"Total examples: {len(data)}")
print(f"Examples with all mutations successful: {sum(1 for ex in data if all(m.get('success', False) for m in ex.get('mutations', [])))}")
print(f"Examples with at least one failed mutation: {sum(1 for ex in data if any(not m.get('success', True) for m in ex.get('mutations', [])))}")
print(f"Average mutations per example: {sum(len(ex.get('mutations', [])) for ex in data)/len(data):.2f}")

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

        print(f"  Mutations with exact match: {matches}/{len(example.get('mutations', []))}") 