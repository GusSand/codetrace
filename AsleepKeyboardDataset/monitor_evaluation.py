#!/usr/bin/env python3
"""
Monitor the evaluation progress
"""

import json
import time
import os
from datetime import datetime

def monitor_progress():
    """Monitor evaluation progress every minute"""
    progress_file = "evaluation_progress_cpu.json"
    log_file = "full_evaluation_cpu.log"
    
    print("="*60)
    print("EVALUATION PROGRESS MONITOR")
    print("="*60)
    
    while True:
        try:
            # Check if process is still running
            import subprocess
            result = subprocess.run(['pgrep', '-f', 'full_evaluation_cpu_only.py'], 
                                  capture_output=True, text=True)
            
            if not result.stdout.strip():
                print("\n⚠️  Evaluation process not found - may have completed!")
                break
            
            # Read progress file
            if os.path.exists(progress_file):
                with open(progress_file, 'r') as f:
                    progress = json.load(f)
                
                completed = len(progress.get('completed_scenarios', []))
                timestamp = progress.get('timestamp', 'Unknown')
                
                print(f"\nProgress Update - {datetime.now().strftime('%H:%M:%S')}")
                print(f"Completed: {completed}/89 scenarios ({completed/89*100:.1f}%)")
                print(f"Last update: {timestamp}")
                
                # Estimate completion time
                if completed > 0:
                    # Get start time from log
                    with open(log_file, 'r') as f:
                        first_line = f.readline()
                        if '2025-07-27' in first_line:
                            start_time = datetime.strptime(first_line[:19], '%Y-%m-%d %H:%M:%S')
                            elapsed = datetime.now() - start_time
                            rate = completed / elapsed.total_seconds()
                            remaining = (89 - completed) / rate if rate > 0 else 0
                            
                            print(f"Rate: {rate*60:.1f} scenarios/minute")
                            print(f"ETA: {remaining/60:.0f} minutes")
            
            # Show last log entries
            print("\nLast log entries:")
            os.system(f"tail -5 {log_file} | grep -E 'Processing|Completed|Progress saved'")
            
        except Exception as e:
            print(f"Error reading progress: {e}")
        
        # Wait 60 seconds before next check
        time.sleep(60)
    
    print("\n" + "="*60)
    print("Evaluation appears to have completed!")
    print("Check the results file: full_evaluation_results_cpu.json")
    print("Check the report file: full_evaluation_report_cpu_*.md")
    print("="*60)

if __name__ == "__main__":
    monitor_progress()