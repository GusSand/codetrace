#!/usr/bin/env python3
import json
import argparse
import os
import re
import difflib
from collections import defaultdict
import time
from typing import List, Dict, Any, Tuple
from tqdm import tqdm

def extract_function_name(func_code: str) -> str:
    """Extract the function name from the code."""
    # Try to match common function declarations like:
    # static int function_name(...) or void function_name(...) etc.
    match = re.search(r'(?:static\s+)?(?:[a-zA-Z0-9_]+\s+)+([a-zA-Z0-9_]+)\s*\(', func_code)
    if match:
        return match.group(1)
    return ""

def load_jsonl(file_path: str) -> List[Dict]:
    """Load data from a jsonl file."""
    data = []
    print(f"Loading data from {file_path}...")
    with open(file_path, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    print(f"Loaded {len(data)} examples from {file_path}")
    return data

def normalize_code(code: str) -> str:
    """Normalize code by removing whitespace, comments, etc."""
    # Remove comments
    code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    # Remove whitespace
    code = re.sub(r'\s+', ' ', code)
    return code.strip()

def calculate_similarity(code1: str, code2: str) -> float:
    """Calculate similarity between two code snippets using difflib."""
    normalized_code1 = normalize_code(code1)
    normalized_code2 = normalize_code(code2)
    
    # Use difflib's SequenceMatcher to calculate similarity
    similarity = difflib.SequenceMatcher(None, normalized_code1, normalized_code2).ratio()
    return similarity

def find_secure_counterparts(vulnerable_examples: List[Dict], secure_examples: List[Dict], 
                            similarity_threshold: float = 0.3) -> List[Dict]:
    """
    For each vulnerable example, find a similar secure example from the same project
    with the same function name when possible.
    """
    pairs = []
    
    # Extract function names for all examples
    print("Extracting function names for all examples...")
    for example in tqdm(vulnerable_examples):
        example['function_name'] = extract_function_name(example['func'])
    
    for example in tqdm(secure_examples):
        example['function_name'] = extract_function_name(example['func'])
    
    # Group secure examples by project and function name
    print("Grouping secure examples by project and function name...")
    secure_by_project = defaultdict(list)
    secure_by_project_and_func = defaultdict(list)
    
    for example in secure_examples:
        project = example['project']
        secure_by_project[project].append(example)
        
        if example['function_name']:
            key = (project, example['function_name'])
            secure_by_project_and_func[key].append(example)
    
    # For each vulnerable example, find a similar secure counterpart
    print("Finding secure counterparts for vulnerable examples...")
    for vuln_example in tqdm(vulnerable_examples):
        project = vuln_example['project']
        function_name = vuln_example['function_name']
        
        best_match = None
        best_similarity = 0
        same_function = False
        
        # First try to find a secure version with the same function name
        if function_name:
            key = (project, function_name)
            if key in secure_by_project_and_func:
                for secure_example in secure_by_project_and_func[key]:
                    similarity = calculate_similarity(vuln_example['func'], secure_example['func'])
                    if similarity > best_similarity and similarity >= similarity_threshold:
                        best_similarity = similarity
                        best_match = secure_example
                        same_function = True
        
        # If no match with same function name, try any function from the same project
        if not best_match and project in secure_by_project:
            for secure_example in secure_by_project[project][:50]:  # Limit to 50 to keep it efficient
                similarity = calculate_similarity(vuln_example['func'], secure_example['func'])
                if similarity > best_similarity and similarity >= similarity_threshold:
                    best_similarity = similarity
                    best_match = secure_example
                    same_function = (function_name and secure_example['function_name'] == function_name)
        
        if best_match:
            pair = {
                'vulnerable': vuln_example,
                'secure': best_match,
                'similarity': best_similarity,
                'same_function': same_function
            }
            pairs.append(pair)
    
    # Sort by same_function (True first) and then by similarity (highest first)
    def sort_key(pair):
        # Convert boolean to int (True=1, False=0) for proper sorting
        return (1 if pair['same_function'] else 0, pair['similarity'])
    
    pairs.sort(key=sort_key, reverse=True)
    
    print(f"Found {len(pairs)} pairs with secure counterparts")
    print(f"- {sum(1 for p in pairs if p['same_function'])} pairs with matching function names")
    print(f"- {sum(1 for p in pairs if not p['same_function'])} pairs with different function names")
    
    return pairs

def prepare_steering_data(pairs: List[Dict], num_pairs: int = 10) -> List[Dict]:
    """
    Prepare the steering data from pairs of vulnerable and secure code.
    """
    # Select top pairs based on prioritizing same function matches
    selected_pairs = pairs[:num_pairs]
    
    steering_data = []
    function_names_used = set()
    
    for idx, pair in enumerate(selected_pairs):
        vuln_code = pair['vulnerable']['func']
        secure_code = pair['secure']['func']
        vuln_func_name = pair['vulnerable'].get('function_name', '')
        secure_func_name = pair['secure'].get('function_name', '')
        project = pair['vulnerable']['project']
        similarity = pair['similarity']
        
        # Track function names used
        if vuln_func_name:
            function_names_used.add(vuln_func_name)
        
        # Create steering example - for security we want to steer AWAY from vulnerable code
        # and TOWARD secure code
        steering_example = {
            "prompt": f"Security review of this code:\n\n{vuln_code}",
            "completion": "This code contains security vulnerabilities.",
            "mutated_program": secure_code,
            "project": project,
            "function_name": vuln_func_name,
            "vulnerability_type": "general",  # Could be more specific with proper analysis
            "similarity": similarity,
            "same_function": pair['same_function'],
            "idx": idx,
            "typechecks": True  # Assuming all examples typecheck
        }
        
        steering_data.append(steering_example)
    
    # Print statistics about the dataset
    same_function_count = sum(1 for example in steering_data if example["same_function"])
    print(f"\nSteering data preparation complete.")
    print(f"Total examples: {len(steering_data)}")
    print(f"Examples with matching function names: {same_function_count}")
    print(f"Examples with different function names: {len(steering_data) - same_function_count}")
    print(f"Distinct functions found: {len(function_names_used)}")
    
    if function_names_used:
        print("\nFunctions with matching pairs:")
        for func_name in sorted(function_names_used):
            pairs_with_func = sum(1 for ex in steering_data if ex["function_name"] == func_name)
            print(f"- {func_name}: {pairs_with_func} pair(s)")
    
    return steering_data

def main():
    parser = argparse.ArgumentParser(description='Prepare security steering dataset')
    parser.add_argument('--dataset_file', type=str, 
                      default='../datasets/codexglue/CodeXGLUE/Code-Code/Defect-detection/dataset/test.jsonl',
                      help='Path to the dataset file')
    parser.add_argument('--output_file', type=str, default='./security_steering_data.json',
                      help='Output file for the steering dataset')
    parser.add_argument('--num_pairs', type=int, default=10,
                      help='Number of pairs to include in the steering dataset')
    parser.add_argument('--similarity_threshold', type=float, default=0.3,
                      help='Minimum similarity threshold')
    args = parser.parse_args()
    
    # Load dataset
    data = load_jsonl(args.dataset_file)
    
    # Separate secure and vulnerable examples
    secure_examples = [example for example in data if example['target'] == 0]
    vulnerable_examples = [example for example in data if example['target'] == 1]
    
    print(f"Dataset statistics:")
    print(f"- Total examples: {len(data)}")
    print(f"- Secure examples (target=0): {len(secure_examples)}")
    print(f"- Vulnerable examples (target=1): {len(vulnerable_examples)}")
    
    # Find similar pairs
    pairs = find_secure_counterparts(vulnerable_examples, secure_examples, args.similarity_threshold)
    
    # Prepare steering data
    steering_data = prepare_steering_data(pairs, args.num_pairs)
    
    # Save the steering data
    with open(args.output_file, 'w') as f:
        json.dump(steering_data, f, indent=2)
    
    print(f"Saved steering data to {args.output_file}")
    print("\nTo run the steering process, use:")
    print(f"python3 -m steering.run_steering --model bigcode/starcoderbase-1b \\\n"
          f"--output_dir security_steering_results \\\n"
          f"--test_split {args.dataset_file} \\\n"
          f"--test_steer_batch_size 32 \\\n"
          f"--test_batch_size 32 \\\n"
          f"--steering_file {args.output_file}")

if __name__ == "__main__":
    main() 