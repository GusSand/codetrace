#!/usr/bin/env python3
import json
from scipy.stats import binomtest
import sys
import logging
import time
import os
from concurrent.futures import ProcessPoolExecutor
from glob import glob

# Set up logging with immediate flush
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/analyze_steering.log', mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)

def log_info(msg):
    logging.info(msg)
    for handler in logging.getLogger().handlers:
        handler.flush()

def process_result(result):
    """Process a single result and return statistics"""
    if '<FILL>' not in result.get('original_program', ''):
        return 0, 0, 0
        
    # Extract the expected type from the original program
    type_start = result['original_program'].find('<FILL>')
    context_before = result['original_program'][:type_start].strip()
    last_colon = context_before.rfind(':')
    if last_colon == -1:
        return 0, 0, 0
        
    expected_type = context_before[last_colon+1:].strip()
    
    # Compare predictions directly
    original_pred = result.get('original_prediction', '')
    mutated_pred = result.get('mutated_prediction', '')
    
    correct_before = 1 if expected_type.lower() in original_pred.lower() else 0
    correct_after = 1 if expected_type.lower() in mutated_pred.lower() else 0
            
    return correct_before, correct_after, 1

def process_chunk(chunk_file):
    """Process a single chunk file and return aggregated statistics"""
    total_correct_before = 0
    total_correct_after = 0
    total_examples = 0
    
    try:
        with open(chunk_file, 'r') as f:
            results = json.load(f)
            
        for result in results:
            correct_before, correct_after, count = process_result(result)
            total_correct_before += correct_before
            total_correct_after += correct_after
            total_examples += count
            
    except Exception as e:
        print(f"Error processing chunk {chunk_file}: {str(e)}")
        return 0, 0, 0
        
    return total_correct_before, total_correct_after, total_examples

def analyze_chunks(chunks_dir):
    log_info(f"\nAnalyzing chunks from {chunks_dir}")
    log_info("\nSteering Effectiveness Analysis:")
    log_info("-" * 50 + "\n")
    
    # Get list of chunk files
    chunk_files = sorted(glob(os.path.join(chunks_dir, "chunk_*.json")))
    if not chunk_files:
        log_info("No chunk files found!")
        return
        
    log_info(f"Found {len(chunk_files)} chunks to process")
    
    # Initialize counters
    total_correct_before = 0
    total_correct_after = 0
    total_examples = 0
    start_time = time.time()
    chunks_processed = 0
    
    # Process chunks in parallel
    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_chunk, chunk_file) for chunk_file in chunk_files]
        
        for future in futures:
            correct_before, correct_after, count = future.result()
            total_correct_before += correct_before
            total_correct_after += correct_after
            total_examples += count
            chunks_processed += 1
            
            # Log progress
            if chunks_processed % 5 == 0:  # Update every 5 chunks
                elapsed_time = time.time() - start_time
                chunks_per_sec = chunks_processed / elapsed_time if elapsed_time > 0 else 0
                
                if total_examples > 0:
                    accuracy_before = total_correct_before / total_examples
                    accuracy_after = total_correct_after / total_examples
                    
                    log_info(f"\nProgress: {chunks_processed}/{len(chunk_files)} chunks ({chunks_per_sec:.1f} chunks/sec)")
                    log_info(f"Intermediate Results (after {total_examples} examples):")
                    log_info(f"Correct before: {total_correct_before}/{total_examples} ({accuracy_before:.2%})")
                    log_info(f"Correct after: {total_correct_after}/{total_examples} ({accuracy_after:.2%})")
    
    if total_examples == 0:
        log_info("No valid results found for analysis")
        return
        
    # Calculate final statistics
    accuracy_before = total_correct_before / total_examples
    accuracy_after = total_correct_after / total_examples
    
    elapsed_time = time.time() - start_time
    final_speed = total_examples / elapsed_time if elapsed_time > 0 else 0
    
    log_info(f"\nFinal Results (processed at {final_speed:.1f} examples/sec):")
    log_info(f"Total examples analyzed: {total_examples}")
    log_info(f"Correct type predictions before steering: {total_correct_before}/{total_examples} ({accuracy_before:.2%})")
    log_info(f"Correct type predictions after steering: {total_correct_after}/{total_examples} ({accuracy_after:.2%})")
    
    # Statistical significance test
    if total_examples > 0:
        binom_test = binomtest(total_correct_after, total_examples, p=accuracy_before)
        log_info(f"\nStatistical Analysis:")
        log_info(f"p-value: {binom_test.pvalue:.6f}")
        log_info(f"Significant at p < 0.05: {binom_test.pvalue < 0.05}")

def main():
    chunks_dir = "data/steering_results/chunks"
    analyze_chunks(chunks_dir)

if __name__ == "__main__":
    main() 