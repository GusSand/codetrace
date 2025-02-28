#!/usr/bin/env python3
import datasets
from pathlib import Path
import pandas as pd
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import Terminal256Formatter
from pygments.token import Token
from pygments.lexer import inherit

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