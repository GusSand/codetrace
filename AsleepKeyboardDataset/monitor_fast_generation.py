#!/usr/bin/env python3
"""Monitor fast generation progress"""

import os
import json
import time
from datetime import datetime
import glob

def monitor():
    print("Monitoring completion generation...")
    print("="*60)
    
    while True:
        # Find checkpoint files
        checkpoints = glob.glob("checkpoint_*.json")
        if checkpoints:
            latest_checkpoint = max(checkpoints)
            with open(latest_checkpoint, 'r') as f:
                data = json.load(f)
                completed = data.get('completed', [])
            
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}]")
            print(f"Completed scenarios: {len(completed)}/89 ({len(completed)/89*100:.1f}%)")
            if completed:
                print(f"Last completed: {completed[-1]}")
                print(f"Estimated completions: {len(completed) * 25}")
        
        # Check output file size
        output_files = glob.glob("completions_dow_starcoder_*.jsonl")
        if output_files:
            for f in output_files:
                size = os.path.getsize(f)
                lines = sum(1 for _ in open(f))
                print(f"Output file: {f}")
                print(f"  Size: {size/1024/1024:.1f} MB")
                print(f"  Completions: {lines}")
        
        # Check log
        if os.path.exists("completions_generation.log"):
            # Get last few non-empty lines
            with open("completions_generation.log", 'r') as f:
                lines = f.readlines()
                recent = [l.strip() for l in lines[-10:] if l.strip()]
                if recent:
                    print("\nRecent log entries:")
                    for line in recent[-3:]:
                        if len(line) > 100:
                            print(f"  {line[:100]}...")
                        else:
                            print(f"  {line}")
        
        print("-"*60)
        time.sleep(30)

if __name__ == "__main__":
    monitor()