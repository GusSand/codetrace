#!/usr/bin/env python3
import json
import os
import re
import difflib
from collections import defaultdict
import argparse
from typing import List, Dict, Tuple, Set
import time
from tqdm import tqdm  # For progress bars

def load_jsonl(file_path: str) -> List[Dict]:
    """Load data from a jsonl file."""
    data = []
    print(f"Loading data from {file_path}...")
    with open(file_path, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    print(f"Loaded {len(data)} examples from {file_path}")
    return data

def extract_function_name(func_code: str) -> str:
    """Extract the function name from the code."""
    # Try to match common function declarations like:
    # static int function_name(...) or void function_name(...) etc.
    match = re.search(r'(?:static\s+)?(?:[a-zA-Z0-9_]+\s+)+([a-zA-Z0-9_]+)\s*\(', func_code)
    if match:
        return match.group(1)
    return ""

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

def find_similar_pairs_by_function(secure_examples: List[Dict], vulnerable_examples: List[Dict], 
                      num_pairs: int = 10, similarity_threshold: float = 0.4) -> List[Tuple[Dict, Dict, float]]:
    """
    Find pairs of similar code between secure and vulnerable examples,
    prioritizing matches from the same project with the same function name.
    """
    pairs = []
    
    # Extract function names for all examples
    print("Extracting function names...")
    for example in secure_examples:
        example['function_name'] = extract_function_name(example['func'])
    
    for example in vulnerable_examples:
        example['function_name'] = extract_function_name(example['func'])
    
    # Group examples by project and function name
    print("Grouping examples by project and function name...")
    secure_by_project_and_func = defaultdict(list)
    for example in secure_examples:
        if example['function_name']:  # Only include examples where we could extract a function name
            key = (example['project'], example['function_name'])
            secure_by_project_and_func[key].append(example)
    
    vulnerable_by_project_and_func = defaultdict(list)
    for example in vulnerable_examples:
        if example['function_name']:  # Only include examples where we could extract a function name
            key = (example['project'], example['function_name'])
            vulnerable_by_project_and_func[key].append(example)
    
    # Find matching project-function combinations
    common_keys = set(secure_by_project_and_func.keys()).intersection(
        set(vulnerable_by_project_and_func.keys()))
    
    print(f"Found {len(common_keys)} project-function combinations with both secure and vulnerable examples")
    
    # For each common project-function, find the best matching pair
    for key in tqdm(common_keys, desc="Finding pairs by function name"):
        project, func_name = key
        secure_list = secure_by_project_and_func[key]
        vulnerable_list = vulnerable_by_project_and_func[key]
        
        best_pair = None
        best_similarity = 0
        
        # Compare each secure example to each vulnerable example
        for secure_ex in secure_list:
            for vulnerable_ex in vulnerable_list:
                similarity = calculate_similarity(secure_ex['func'], vulnerable_ex['func'])
                
                if similarity > best_similarity and similarity >= similarity_threshold:
                    best_similarity = similarity
                    best_pair = (vulnerable_ex, secure_ex, similarity)
        
        if best_pair:
            pairs.append(best_pair)
            print(f"Found pair with function '{func_name}' in project '{project}' (similarity: {best_similarity:.2f})")
            
            # Break if we have enough pairs
            if len(pairs) >= num_pairs:
                print(f"Reached target of {num_pairs} pairs, stopping search")
                break
    
    # If we don't have enough pairs, fall back to the original similarity-based approach
    if len(pairs) < num_pairs:
        print(f"Only found {len(pairs)} pairs by function name, searching for more...")
        remaining_pairs_needed = num_pairs - len(pairs)
        
        # Exclude examples that are already in pairs
        used_secure_examples = {ex['idx'] for _, ex, _ in pairs}
        used_vulnerable_examples = {ex['idx'] for ex, _, _ in pairs}
        
        filtered_secure = [ex for ex in secure_examples if ex['idx'] not in used_secure_examples]
        filtered_vulnerable = [ex for ex in vulnerable_examples if ex['idx'] not in used_vulnerable_examples]
        
        # Find additional pairs based on similarity
        additional_pairs = find_similar_pairs_by_similarity(
            filtered_secure, filtered_vulnerable, remaining_pairs_needed, similarity_threshold)
        
        pairs.extend(additional_pairs)
    
    # Sort by similarity (highest first)
    pairs.sort(key=lambda x: x[2], reverse=True)
    return pairs[:num_pairs]

def find_similar_pairs_by_similarity(secure_examples: List[Dict], vulnerable_examples: List[Dict], 
                           num_pairs: int = 10, similarity_threshold: float = 0.4) -> List[Tuple[Dict, Dict, float]]:
    """Find pairs of similar code between secure and vulnerable examples based on code similarity."""
    pairs = []
    
    # Group examples by project for more relevant comparisons
    secure_by_project = defaultdict(list)
    for example in secure_examples:
        secure_by_project[example['project']].append(example)
    
    # For each vulnerable example, find the most similar secure example from the same project
    print(f"Searching for {num_pairs} similar pairs (threshold: {similarity_threshold})...")
    start_time = time.time()
    
    # Use tqdm for progress tracking
    for i, vuln_example in enumerate(tqdm(vulnerable_examples[:500], 
                                        desc="Finding pairs by similarity")):
        project = vuln_example['project']
        
        # Status update every 50 examples
        if i > 0 and i % 50 == 0:
            elapsed = time.time() - start_time
            avg_time_per_example = elapsed / i
            remaining_examples = min(500, len(vulnerable_examples)) - i
            estimated_time = avg_time_per_example * remaining_examples
            print(f"Processed {i}/500 examples. "
                 f"Found {len(pairs)}/{num_pairs} pairs. "
                 f"Est. time remaining: {estimated_time:.2f} seconds")
        
        # Skip if no secure examples from the same project
        if project not in secure_by_project or not secure_by_project[project]:
            continue
        
        best_match = None
        best_similarity = 0
        
        # Only check a limited number of secure examples per project to speed things up
        for secure_example in secure_by_project[project][:50]:
            similarity = calculate_similarity(vuln_example['func'], secure_example['func'])
            
            if similarity > best_similarity and similarity >= similarity_threshold:
                best_similarity = similarity
                best_match = secure_example
        
        if best_match:
            pairs.append((vuln_example, best_match, best_similarity))
            
            # Remove the matched secure example to avoid duplicates
            secure_by_project[project].remove(best_match)
            
            print(f"Found pair #{len(pairs)} by similarity: {vuln_example['project']} (similarity: {best_similarity:.2f})")
        
        # Break if we have enough pairs
        if len(pairs) >= num_pairs:
            print(f"Reached target of {num_pairs} pairs, stopping search")
            break
    
    return pairs

def find_similar_pairs(secure_examples: List[Dict], vulnerable_examples: List[Dict], 
                      num_pairs: int = 10, similarity_threshold: float = 0.4) -> List[Tuple[Dict, Dict, float]]:
    """
    Find pairs of similar code between secure and vulnerable examples.
    First tries to find pairs with the same function name, then falls back to general similarity.
    """
    return find_similar_pairs_by_function(secure_examples, vulnerable_examples, 
                                         num_pairs, similarity_threshold)

def main():
    parser = argparse.ArgumentParser(description='Find similar code pairs between secure and vulnerable examples')
    parser.add_argument('--dataset_dir', type=str, default='../datasets/codexglue/CodeXGLUE/Code-Code/Defect-detection/dataset',
                        help='Directory containing the dataset files')
    parser.add_argument('--output_dir', type=str, default='../security',
                        help='Directory to save the output')
    parser.add_argument('--num_pairs', type=int, default=10,
                        help='Number of pairs to find')
    parser.add_argument('--similarity_threshold', type=float, default=0.4,
                        help='Minimum similarity threshold')
    parser.add_argument('--limit', type=int, default=1000, 
                        help='Limit number of examples to process for faster results')
    parser.add_argument('--use_train', action='store_true',
                        help='Use training data instead of test data')
    args = parser.parse_args()
    
    print(f"Starting code pair search with settings:")
    print(f"- Dataset directory: {args.dataset_dir}")
    print(f"- Output directory: {args.output_dir}")
    print(f"- Number of pairs to find: {args.num_pairs}")
    print(f"- Similarity threshold: {args.similarity_threshold}")
    print(f"- Processing limit: {args.limit} examples")
    print(f"- Using {'training' if args.use_train else 'test'} data")
    
    # Load the dataset
    data_file = 'train.jsonl' if args.use_train else 'test.jsonl'
    data = load_jsonl(os.path.join(args.dataset_dir, data_file))
    
    # Separate secure and vulnerable examples
    secure_examples = [example for example in data if example['target'] == 0]
    vulnerable_examples = [example for example in data if example['target'] == 1]
    
    print(f"Separated examples:")
    print(f"- Secure examples: {len(secure_examples)}")
    print(f"- Vulnerable examples: {len(vulnerable_examples)}")
    
    # Find similar pairs
    start_time = time.time()
    pairs = find_similar_pairs(secure_examples, vulnerable_examples, args.num_pairs, args.similarity_threshold)
    elapsed_time = time.time() - start_time
    
    # Save the pairs
    output_file = os.path.join(args.output_dir, 'similar_code_pairs.json')
    with open(output_file, 'w') as f:
        json.dump([{
            'vulnerable': {
                'project': vuln['project'],
                'commit_id': vuln['commit_id'],
                'func': vuln['func'],
                'function_name': vuln.get('function_name', ''),
                'idx': vuln['idx']
            },
            'secure': {
                'project': secure['project'],
                'commit_id': secure['commit_id'],
                'func': secure['func'],
                'function_name': secure.get('function_name', ''),
                'idx': secure['idx']
            },
            'same_function': vuln.get('function_name', '') == secure.get('function_name', '') and vuln.get('function_name', '') != '',
            'similarity': similarity
        } for vuln, secure, similarity in pairs], f, indent=2)
    
    print(f"\nResults:")
    print(f"- Found {len(pairs)} similar pairs")
    print(f"- Processing time: {elapsed_time:.2f} seconds")
    print(f"- Saved pairs to {output_file}")
    
    # Print a summary of the pairs
    same_function_count = sum(1 for vuln, secure, _ in pairs if 
                              vuln.get('function_name', '') == secure.get('function_name', '') and 
                              vuln.get('function_name', '') != '')
    print(f"- Pairs with same function name: {same_function_count}")
    
    for i, (vuln, secure, similarity) in enumerate(pairs):
        same_func = (vuln.get('function_name', '') == secure.get('function_name', '') and 
                     vuln.get('function_name', '') != '')
        print(f"\nPair {i+1} (Similarity: {similarity:.2f}, Same function: {same_func}):")
        func_name = vuln.get('function_name', 'unknown')
        print(f"Function name: {func_name}")
        print(f"Vulnerable example from {vuln['project']} (idx: {vuln['idx']})")
        print(f"Secure example from {secure['project']} (idx: {secure['idx']})")
        
        # Print the first few lines of each function
        vuln_lines = vuln['func'].split('\n')[:3]
        secure_lines = secure['func'].split('\n')[:3]
        
        print("Vulnerable function (first 3 lines):")
        print('\n'.join(vuln_lines))
        print("...")
        
        print("Secure function (first 3 lines):")
        print('\n'.join(secure_lines))
        print("...")

if __name__ == "__main__":
    main()