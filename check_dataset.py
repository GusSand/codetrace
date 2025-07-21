#!/usr/bin/env python3
import json
import sys

def check_dataset(file_path):
    """Check the structure of a dataset."""
    print(f"Checking dataset: {file_path}")
    
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    print(f"Number of examples: {len(data)}")
    print(f"First example ID: {data[0].get('example_id')}")
    print(f"Last example ID: {data[-1].get('example_id')}")
    
    # Check mutations
    mutations_count = sum(1 for ex in data if ex.get('mutations'))
    print(f"Examples with mutations: {mutations_count}")
    
    # Check mutated_program field
    mutated_program_count = sum(1 for ex in data if ex.get('mutated_program'))
    print(f"Examples with mutated_program: {mutated_program_count}")
    
    # Print a sample of FIM types
    fim_types = [ex.get('fim_type') for ex in data[:10]]
    print(f"Sample FIM types: {fim_types}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_dataset.py <dataset_file>")
        sys.exit(1)
    
    check_dataset(sys.argv[1]) 