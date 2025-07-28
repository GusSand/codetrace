#!/usr/bin/env python3
"""
Monitor the completion generation progress
"""

import json
import time
import os
import subprocess
from datetime import datetime
import sys

def monitor_generation():
    """Monitor generation progress"""
    print("="*60)
    print("COMPLETION GENERATION MONITOR")
    print("="*60)
    
    # Find the latest progress file
    progress_files = [f for f in os.listdir('.') if f.startswith('completion_progress_') and f.endswith('.json')]
    if not progress_files:
        print("No progress file found yet. Waiting for generation to start...")
        return
    
    progress_file = max(progress_files)  # Get the latest
    log_file = "generate_completions_25x.log"
    
    last_update_time = 0
    last_total_generated = 0
    stall_counter = 0
    
    while True:
        try:
            # Check if process is still running
            result = subprocess.run(['pgrep', '-f', 'generate_completions_25x.py'], 
                                  capture_output=True, text=True)
            
            if not result.stdout.strip():
                print("\n⚠️  Generation process not found!")
                
                # Check if it completed
                if os.path.exists(progress_file):
                    with open(progress_file, 'r') as f:
                        progress = json.load(f)
                    if progress.get('total_generated', 0) > 0:
                        print("Generation may have completed. Check the log file.")
                    else:
                        print("Generation process died. Check the log for errors.")
                break
            
            # Read progress
            if os.path.exists(progress_file):
                with open(progress_file, 'r') as f:
                    progress = json.load(f)
                
                completed = len(progress.get('completed_scenarios', []))
                total_generated = progress.get('total_generated', 0)
                valid_programs = progress.get('valid_programs', 0)
                compilable = progress.get('compilable_programs', 0)
                timestamp = progress.get('timestamp', 'Unknown')
                
                # Check for stalls
                current_time = os.path.getmtime(progress_file)
                if current_time == last_update_time and total_generated == last_total_generated:
                    stall_counter += 1
                    if stall_counter > 5:  # No update for 5 minutes
                        print(f"\n⚠️  WARNING: No progress for {stall_counter} minutes!")
                else:
                    stall_counter = 0
                    last_update_time = current_time
                    last_total_generated = total_generated
                
                # Display progress
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Progress Update:")
                print(f"  Scenarios completed: {completed}")
                print(f"  Total completions: {total_generated}")
                if total_generated > 0:
                    print(f"  Valid programs: {valid_programs} ({valid_programs/total_generated*100:.1f}%)")
                    print(f"  Compilable: {compilable} ({compilable/total_generated*100:.1f}%)")
                print(f"  Last update: {timestamp}")
                
                # Estimate completion
                if completed > 0:
                    avg_per_scenario = total_generated / completed
                    estimated_total = 89 * 25  # 89 scenarios * 25 completions
                    progress_pct = total_generated / estimated_total * 100
                    print(f"  Overall progress: ~{progress_pct:.1f}%")
            
            # Show recent log entries
            if os.path.exists(log_file):
                print("\nRecent activity:")
                # Get last 5 lines that show progress
                result = subprocess.run(
                    ['tail', '-20', log_file],
                    capture_output=True,
                    text=True
                )
                lines = result.stdout.strip().split('\n')
                for line in lines[-5:]:
                    if any(keyword in line for keyword in ['Completed', 'Starting scenario', 'Progress:', 'Generated in']):
                        print(f"  {line.split(' - ', 1)[-1][:100]}")
            
            # Check for errors
            if os.path.exists(log_file):
                result = subprocess.run(
                    ['grep', '-c', 'ERROR', log_file],
                    capture_output=True,
                    text=True
                )
                error_count = int(result.stdout.strip() or 0)
                if error_count > 0:
                    print(f"\n⚠️  Found {error_count} errors in log")
                    # Show last error
                    result = subprocess.run(
                        ['grep', 'ERROR', log_file],
                        capture_output=True,
                        text=True
                    )
                    if result.stdout:
                        last_error = result.stdout.strip().split('\n')[-1]
                        print(f"  Last error: {last_error[:150]}")
            
            print("-" * 60)
            
        except Exception as e:
            print(f"Monitor error: {e}")
        
        # Wait 60 seconds before next check
        time.sleep(60)
    
    print("\nMonitoring stopped.")

if __name__ == "__main__":
    monitor_generation()