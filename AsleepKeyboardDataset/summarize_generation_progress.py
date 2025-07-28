#!/usr/bin/env python3
"""Summarize generation progress"""

import json
import glob
from collections import defaultdict
from datetime import datetime

def summarize():
    # Find completion files
    files = glob.glob("completions_dow_starcoder_*.jsonl")
    if not files:
        print("No completion files found")
        return
    
    latest_file = max(files)
    print(f"Analyzing: {latest_file}")
    print("="*60)
    
    # Count completions by scenario
    by_scenario = defaultdict(int)
    by_cwe = defaultdict(int)
    total = 0
    
    with open(latest_file, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                scenario_id = data['scenario_id']
                by_scenario[scenario_id] += 1
                
                # Extract CWE
                cwe = scenario_id.split('/')[1].split('-')[0] + '-' + scenario_id.split('/')[1].split('-')[1]
                by_cwe[cwe] += 1
                total += 1
            except:
                pass
    
    print(f"Total completions: {total}")
    print(f"Scenarios completed: {len(by_scenario)}")
    print(f"Expected total: {len(by_scenario) * 25}")
    
    # Check if all scenarios have 25 completions
    incomplete = [(s, c) for s, c in by_scenario.items() if c != 25]
    if incomplete:
        print(f"\nIncomplete scenarios ({len(incomplete)}):")
        for s, c in incomplete[:5]:
            print(f"  {s}: {c}/25")
    
    print(f"\nCompletions by CWE:")
    for cwe, count in sorted(by_cwe.items()):
        print(f"  {cwe}: {count}")
    
    # Estimate time remaining
    if len(by_scenario) > 0:
        avg_per_scenario = total / len(by_scenario)
        remaining_scenarios = 89 - len(by_scenario)
        remaining_completions = remaining_scenarios * 25
        
        print(f"\nProgress: {len(by_scenario)}/89 scenarios ({len(by_scenario)/89*100:.1f}%)")
        print(f"Remaining: {remaining_scenarios} scenarios (~{remaining_completions} completions)")

if __name__ == "__main__":
    summarize()