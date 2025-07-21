#!/usr/bin/env python3
import json
import os
import time
import sys
from datetime import datetime, timedelta

def format_time(seconds):
    """Format time in seconds to a readable format."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{int(minutes)}m {int(seconds)}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"

def monitor_progress(results_file, interval=30):
    """Monitor the progress of mutation robustness testing."""
    print(f"Monitoring progress of {results_file}...")
    print(f"Will check every {interval} seconds.")
    print("Press Ctrl+C to stop monitoring.")
    
    start_time = time.time()
    last_count = 0
    
    try:
        while True:
            try:
                if not os.path.exists(results_file):
                    print(f"Results file {results_file} not found. Waiting...")
                    time.sleep(interval)
                    continue
                
                with open(results_file, 'r') as f:
                    results = json.load(f)
                
                # Calculate statistics
                num_examples = len(results)
                total_mutations = sum(r.get("total_mutations_attempted", 0) for r in results)
                exact_matches = sum(sum(1 for m in r.get("mutations", []) if m.get("exact_match", False)) for r in results)
                
                # Count failed mutations
                failed_examples = sum(1 for r in results if len(r.get("failed_mutations", [])) > 0)
                total_failures = sum(len(r.get("failed_mutations", [])) for r in results)
                
                # Calculate speed
                elapsed_time = time.time() - start_time
                examples_per_second = num_examples / elapsed_time if elapsed_time > 0 else 0
                
                # Estimate remaining time
                if num_examples > last_count and examples_per_second > 0:
                    # Assuming we're targeting 100 examples (from the command)
                    remaining_examples = 100 - num_examples
                    estimated_remaining_time = remaining_examples / examples_per_second
                    eta = format_time(estimated_remaining_time)
                else:
                    eta = "unknown"
                
                # Print progress
                print("\n" + "="*80)
                print(f"Progress update at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:")
                print(f"Processed examples: {num_examples}")
                print(f"Total mutations: {total_mutations}")
                
                # Fix the f-string formatting errors
                exact_match_pct = exact_matches/total_mutations*100 if total_mutations > 0 else 0
                print(f"Exact matches: {exact_matches} ({exact_match_pct:.2f}%)")
                
                failed_pct = failed_examples/num_examples*100 if num_examples > 0 else 0
                print(f"Examples with failures: {failed_examples} ({failed_pct:.2f}%)")
                
                print(f"Total failed mutations: {total_failures}")
                print(f"Elapsed time: {format_time(elapsed_time)}")
                print(f"Estimated remaining time: {eta}")
                print(f"Processing speed: {examples_per_second:.2f} examples/second")
                print("="*80)
                
                last_count = num_examples
                
                # Sleep for the specified interval
                time.sleep(interval)
                
            except json.JSONDecodeError:
                print(f"Error reading results file. It may be in the process of being written. Retrying in {interval} seconds...")
                time.sleep(interval)
                
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python monitor_progress.py <results_file> [interval_seconds]")
        sys.exit(1)
    
    results_file = sys.argv[1]
    interval = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    
    monitor_progress(results_file, interval) 