#!/usr/bin/env python3
import json
from scipy.stats import binomtest
import sys
import logging
import time
from tqdm import tqdm

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

def count_json_objects(filename):
    """Quick count of JSON objects by counting opening braces"""
    count = 0
    file_size = 0
    with open(filename, 'rb') as f:
        # Get file size
        f.seek(0, 2)  # Seek to end
        file_size = f.tell()
        f.seek(0)  # Back to start
        
        # Count objects
        in_string = False
        escape_next = False
        for chunk in iter(lambda: f.read(1024*1024), b''):  # Read 1MB at a time
            for byte in chunk:
                char = chr(byte)
                if escape_next:
                    escape_next = False
                elif char == '\\':
                    escape_next = True
                elif char == '"':
                    in_string = not in_string
                elif not in_string and char == '{':
                    count += 1
    return count, file_size

def stream_json(filename, total_objects=None, file_size=None):
    """Stream JSON array elements to reduce memory usage"""
    bytes_processed = 0
    start_time = time.time()
    objects_processed = 0
    
    with open(filename, 'r') as f:
        content = f.read(1)  # Read first character
        bytes_processed += 1
        if content != '[':
            raise ValueError("Expected JSON array")
            
        content = ""
        depth = 0
        in_string = False
        escape_next = False
        
        while True:
            char = f.read(1)
            if not char:  # EOF
                break
                
            bytes_processed += 1
            
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
                    objects_processed += 1
                    elapsed_time = time.time() - start_time
                    if elapsed_time > 0:
                        speed = objects_processed / elapsed_time
                        
                        # Calculate progress
                        if total_objects:
                            percent_objects = (objects_processed / total_objects) * 100
                        else:
                            percent_objects = 0
                            
                        if file_size:
                            percent_bytes = (bytes_processed / file_size) * 100
                        else:
                            percent_bytes = 0
                            
                        if objects_processed % 10 == 0:  # Update every 10 objects
                            log_info(f"Progress: {percent_bytes:.1f}% of file ({bytes_processed}/{file_size} bytes), "
                                   f"{percent_objects:.1f}% of objects ({objects_processed}/{total_objects}), "
                                   f"Speed: {speed:.1f} examples/sec")
                    
                    # Yield the parsed object
                    if content.strip().endswith('},'):
                        yield json.loads(content.strip()[:-1])
                    else:
                        yield json.loads(content.strip())
                    content = ""

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

def analyze_type_predictions(results_file):
    log_info(f"\nAnalyzing results from {results_file}")
    
    # Get total count for progress tracking
    log_info("Counting total objects (this may take a minute)...")
    total_objects, file_size = count_json_objects(results_file)
    log_info(f"Found {total_objects} objects in {file_size/1024/1024/1024:.1f}GB file")
    
    log_info("\nSteering Effectiveness Analysis:")
    log_info("-" * 50 + "\n")
    
    # Initialize counters
    total_correct_before = 0
    total_correct_after = 0
    total_examples = 0
    start_time = time.time()
    
    # Process results one at a time
    try:
        for result in stream_json(results_file, total_objects, file_size):
            correct_before, correct_after, count = process_result(result)
            
            # Update totals
            total_correct_before += correct_before
            total_correct_after += correct_after
            total_examples += count
            
            # Log intermediate results every 50 examples
            if total_examples > 0 and total_examples % 50 == 0:
                elapsed_time = time.time() - start_time
                speed = total_examples / elapsed_time if elapsed_time > 0 else 0
                
                accuracy_before = total_correct_before / total_examples
                accuracy_after = total_correct_after / total_examples
                
                log_info(f"\nIntermediate Results (after {total_examples} examples, {speed:.1f} examples/sec):")
                log_info(f"Correct before: {total_correct_before}/{total_examples} ({accuracy_before:.2%})")
                log_info(f"Correct after: {total_correct_after}/{total_examples} ({accuracy_after:.2%})")
    
    except Exception as e:
        log_info(f"Error processing results: {str(e)}")
        raise
    
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
    results_file = "data/steering_results/steering_results.json"
    analyze_type_predictions(results_file)

if __name__ == "__main__":
    main() 