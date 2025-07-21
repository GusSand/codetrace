#!/usr/bin/env python3
import os
import json
import argparse
import random
import numpy as np
from difflib import SequenceMatcher
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def normalize_code(code):
    """Basic code normalization to improve matching."""
    return code.replace("\n", " ").replace("\t", " ").lower()

def calculate_similarity(code1, code2):
    """Calculate similarity between two code snippets."""
    # Using both sequence matcher and TF-IDF for better matching
    seq_sim = SequenceMatcher(None, normalize_code(code1), normalize_code(code2)).ratio()
    
    # TF-IDF based similarity
    try:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([code1, code2])
        cos_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return (seq_sim + cos_sim) / 2
    except:
        return seq_sim  # Fallback to sequence matcher if TF-IDF fails

def find_best_match(target_code, candidates, threshold=0.5):
    """Find the best matching code from candidates."""
    best_match = None
    best_score = 0
    
    for idx, code in candidates:
        similarity = calculate_similarity(target_code, code)
        if similarity > best_score and similarity >= threshold:
            best_score = similarity
            best_match = (idx, code, similarity)
    
    return best_match

def load_jsonl(file_path):
    """Load data from a jsonl file."""
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def prepare_security_steering_dataset(input_path, output_path, num_examples=1000, similarity_threshold=0.6, random_seed=42):
    """Prepare dataset for security steering by pairing vulnerable and safe code."""
    random.seed(random_seed)
    np.random.seed(random_seed)
    
    # Load datasets
    train_data = load_jsonl(os.path.join(input_path, 'train.jsonl'))
    valid_data = load_jsonl(os.path.join(input_path, 'valid.jsonl'))
    test_data = load_jsonl(os.path.join(input_path, 'test.jsonl'))
    
    # Combine all data
    all_data = train_data + valid_data + test_data
    print(f"Loaded {len(all_data)} examples in total")
    
    # Separate vulnerable and secure code
    vulnerable_examples = [(idx, item) for idx, item in enumerate(all_data) if item['target'] == 1]
    secure_examples = [(idx, item) for idx, item in enumerate(all_data) if item['target'] == 0]
    
    print(f"Found {len(vulnerable_examples)} vulnerable examples and {len(secure_examples)} secure examples")
    
    # Group examples by project (to prioritize matching within the same project)
    project_to_examples = {}
    for idx, item in enumerate(all_data):
        project = item['project']
        if project not in project_to_examples:
            project_to_examples[project] = {'vulnerable': [], 'secure': []}
        
        if item['target'] == 1:
            project_to_examples[project]['vulnerable'].append((idx, item))
        else:
            project_to_examples[project]['secure'].append((idx, item))
    
    # Create pairs
    paired_examples = []
    skipped_examples = 0
    
    # First, try to match within projects
    for project, examples in project_to_examples.items():
        print(f"Processing project: {project}")
        vulnerable_codes = [(idx, item['func']) for idx, item in examples['vulnerable']]
        secure_codes = [(idx, item['func']) for idx, item in examples['secure']]
        
        for v_idx, v_item in examples['vulnerable']:
            vulnerable_code = v_item['func']
            
            # Try to find a matching secure code
            matched = find_best_match(vulnerable_code, secure_codes, similarity_threshold)
            
            if matched:
                s_idx, secure_code, similarity = matched
                paired_examples.append({
                    'vulnerable_code': vulnerable_code,
                    'secure_code': secure_code,
                    'vulnerable_idx': v_idx,
                    'secure_idx': s_idx,
                    'similarity': similarity,
                    'project': project
                })
                
                # Remove the matched secure code to avoid duplicates
                secure_codes = [(idx, code) for idx, code in secure_codes if idx != s_idx]
            else:
                skipped_examples += 1
    
    print(f"Created {len(paired_examples)} pairs within projects")
    print(f"Skipped {skipped_examples} vulnerable examples that couldn't be matched")
    
    # If we need more examples, try cross-project matching for remaining examples
    if len(paired_examples) < num_examples:
        all_secure_codes = [(idx, item['func']) for idx, item in secure_examples]
        
        for v_idx, v_item in vulnerable_examples:
            # Skip if this vulnerable example is already paired
            if any(pair['vulnerable_idx'] == v_idx for pair in paired_examples):
                continue
                
            vulnerable_code = v_item['func']
            matched = find_best_match(vulnerable_code, all_secure_codes, similarity_threshold)
            
            if matched:
                s_idx, secure_code, similarity = matched
                paired_examples.append({
                    'vulnerable_code': vulnerable_code,
                    'secure_code': secure_code,
                    'vulnerable_idx': v_idx,
                    'secure_idx': s_idx,
                    'similarity': similarity,
                    'project': v_item['project'] + '-cross'
                })
                
                # Remove matched secure code
                all_secure_codes = [(idx, code) for idx, code in all_secure_codes if idx != s_idx]
                
                # Break if we have enough examples
                if len(paired_examples) >= num_examples:
                    break
    
    print(f"Created {len(paired_examples)} pairs in total after cross-project matching")
    
    # Sort by similarity
    paired_examples.sort(key=lambda x: x['similarity'], reverse=True)
    
    # Take top examples
    final_examples = paired_examples[:num_examples]
    
    # Format for steering
    steering_examples = []
    for pair in final_examples:
        steering_examples.append({
            'code': pair['vulnerable_code'],
            'mutated_program': pair['secure_code'],
            'typechecks': True
        })
    
    # Save dataset
    os.makedirs(output_path, exist_ok=True)
    output_file = os.path.join(output_path, 'security_steering_dataset.json')
    
    with open(output_file, 'w') as f:
        json.dump(steering_examples, f, indent=2)
    
    print(f"Saved {len(steering_examples)} examples to {output_file}")
    
    # Create a samples file to inspect some pairs
    samples_file = os.path.join(output_path, 'sample_pairs.json')
    with open(samples_file, 'w') as f:
        json.dump(random.sample(final_examples, min(10, len(final_examples))), f, indent=2)
    
    print(f"Saved sample pairs to {samples_file} for inspection")
    
    return output_file

def main():
    parser = argparse.ArgumentParser(description='Prepare security steering dataset from CodeXGLUE defect detection dataset')
    parser.add_argument('--input-path', type=str, default='datasets/codexglue/CodeXGLUE/Code-Code/Defect-detection/dataset',
                        help='Path to the CodeXGLUE dataset directory containing jsonl files')
    parser.add_argument('--output-path', type=str, default='data/security_steering_data',
                        help='Path to save the prepared steering dataset')
    parser.add_argument('--num-examples', type=int, default=1000,
                        help='Number of examples to include in the dataset')
    parser.add_argument('--similarity-threshold', type=float, default=0.6,
                        help='Minimum similarity threshold for pairing (0-1)')
    parser.add_argument('--random-seed', type=int, default=42,
                        help='Random seed for reproducibility')
    
    args = parser.parse_args()
    
    output_file = prepare_security_steering_dataset(
        args.input_path,
        args.output_path,
        args.num_examples,
        args.similarity_threshold,
        args.random_seed
    )
    
    print("\nDataset preparation complete!")
    print(f"To use this dataset with launch_steer.py, run:")
    print(f"python launch_steer.py --model bigcode/starcoderbase-1b --candidates {output_file} " +
          f"--output-dir steering_results_security --layers 10-14 --steer-batch 10 --test-batch 10")

if __name__ == "__main__":
    main() 