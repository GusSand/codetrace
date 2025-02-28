#!/usr/bin/env python3
import datasets
from collections import defaultdict
from typing import Dict, List, Tuple
import re

def categorize_type(type_str: str) -> str:
    """Categorize the type into broader categories."""
    if type_str in ['str', 'String']:
        return 'string'
    elif type_str in ['int', 'float', 'number']:
        return 'numeric'
    elif type_str in ['dict', 'Dict']:
        return 'dictionary'
    elif type_str in ['list', 'List', 'Tuple', 'tuple']:
        return 'sequence'
    elif 'Optional' in type_str:
        return 'optional'
    elif type_str in ['bool', 'boolean']:
        return 'boolean'
    elif type_str in ['DataFrame']:
        return 'dataframe'
    else:
        return 'other'

def analyze_context(program: str) -> List[str]:
    """Analyze the context in which the type appears."""
    contexts = []
    
    # Check for function parameters
    if re.search(r'def\s+\w+\s*\([^)]*<FILL>[^)]*\)', program):
        contexts.append('function_parameter')
    
    # Check for return type hints
    if '->' in program:
        contexts.append('return_type')
        
    # Check for class methods
    if 'class' in program and 'def' in program:
        contexts.append('class_method')
        
    # Check for docstrings
    if '"""' in program or "'''" in program:
        contexts.append('documented')
        
    # Check for type annotations in variable assignments
    if re.search(r'\w+\s*:\s*<FILL>', program):
        contexts.append('variable_annotation')
    
    return contexts or ['other']

def main():
    # Load the dataset
    ds = datasets.load_from_disk('starcoder1_fim_completions')
    
    # Initialize counters
    type_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
    context_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
    
    # Analyze each example
    for example in ds:
        expected_type = example['fim_type']
        generated_type = example['generated_text']
        program = example['fim_program']
        
        # Analyze by type category
        type_category = categorize_type(expected_type)
        type_stats[type_category]['total'] += 1
        if example['correct']:
            type_stats[type_category]['correct'] += 1
            
        # Analyze by context
        contexts = analyze_context(program)
        for context in contexts:
            context_stats[context]['total'] += 1
            if example['correct']:
                context_stats[context]['correct'] += 1
    
    # Print results
    print("\nAccuracy by Type Category:")
    print("-" * 50)
    for category, stats in sorted(type_stats.items()):
        accuracy = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
        print(f"{category:15} {accuracy:6.2f}% ({stats['correct']}/{stats['total']})")
    
    print("\nAccuracy by Context:")
    print("-" * 50)
    for context, stats in sorted(context_stats.items()):
        accuracy = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
        print(f"{context:20} {accuracy:6.2f}% ({stats['correct']}/{stats['total']})")

if __name__ == '__main__':
    main() 