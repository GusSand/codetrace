#!/usr/bin/env python3
import json
import os
from tqdm import tqdm
import sys

def estimate_object_size(obj_str):
    """Estimate the size of a JSON object in MB"""
    return sys.getsizeof(obj_str) / (1024 * 1024)  # Convert bytes to MB

def stream_and_split(input_file, output_dir, target_chunk_size_mb=100):
    """Split a large JSON array file into chunks targeting a specific size in MB"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Initialize counters and buffers
    current_chunk = []
    current_chunk_size = 0
    chunk_number = 0
    in_string = False
    escape_next = False
    content = ""
    depth = 0
    total_size = 0
    total_objects = 0
    
    print(f"Splitting {input_file} into chunks targeting {target_chunk_size_mb}MB each...")
    
    with open(input_file, 'r') as f:
        # Skip initial [
        char = f.read(1)
        if char != '[':
            raise ValueError("Expected JSON array")
            
        while True:
            char = f.read(1)
            if not char:  # EOF
                break
                
            if escape_next:
                escape_next = False
            elif char == '\\':
                escape_next = True
            elif char == '"' and not escape_next:
                in_string = not in_string
            elif not in_string:
                if char == '{':
                    depth += 1
                elif char == '}':
                    depth -= 1
                    
            content += char
            
            if depth == 0 and content.strip():
                if content.strip().endswith('},') or content.strip().endswith('}'):
                    # Clean up the content
                    if content.strip().endswith(','):
                        obj_str = content.strip()[:-1]
                    else:
                        obj_str = content.strip()
                    
                    # Check object size
                    obj_size_mb = estimate_object_size(obj_str)
                    total_size += obj_size_mb
                    total_objects += 1
                    
                    # Parse and store object
                    try:
                        obj = json.loads(obj_str)
                        current_chunk.append(obj)
                        current_chunk_size += obj_size_mb
                        
                        # Print size statistics for first few objects
                        if total_objects <= 5:
                            print(f"Object {total_objects} size: {obj_size_mb:.2f}MB")
                            
                    except json.JSONDecodeError as e:
                        print(f"Error parsing object: {e}")
                        print(f"Problematic content: {obj_str[:100]}...")
                        continue
                        
                    content = ""
                    
                    # If chunk exceeds target size, write it out
                    if current_chunk_size >= target_chunk_size_mb:
                        output_file = os.path.join(output_dir, f'chunk_{chunk_number:04d}.json')
                        with open(output_file, 'w') as out:
                            json.dump(current_chunk, out)
                        print(f"Wrote chunk {chunk_number} to {output_file} ({current_chunk_size:.2f}MB, {len(current_chunk)} objects)")
                        current_chunk = []
                        current_chunk_size = 0
                        chunk_number += 1
    
    # Write final chunk if not empty
    if current_chunk:
        output_file = os.path.join(output_dir, f'chunk_{chunk_number:04d}.json')
        with open(output_file, 'w') as out:
            json.dump(current_chunk, out)
        print(f"Wrote final chunk {chunk_number} to {output_file} ({current_chunk_size:.2f}MB, {len(current_chunk)} objects)")
    
    # Print final statistics
    print("\nFinal Statistics:")
    print(f"Total objects processed: {total_objects}")
    print(f"Total size: {total_size:.2f}MB")
    print(f"Average object size: {(total_size/total_objects):.2f}MB")
    print(f"Total chunks created: {chunk_number + 1}")
    print(f"Average chunk size: {(total_size/(chunk_number + 1)):.2f}MB")

def main():
    input_file = "data/steering_results/steering_results.json"
    output_dir = "data/steering_results/chunks"
    target_chunk_size_mb = 10  # Start with smaller chunks (10MB) to analyze sizes
    
    stream_and_split(input_file, output_dir, target_chunk_size_mb)
    print("Splitting complete!")

if __name__ == "__main__":
    main() 