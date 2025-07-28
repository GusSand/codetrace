#!/usr/bin/env python3
"""
Quick check of evaluation results
"""

import json
import os
import glob
from datetime import datetime

def check_results():
    print("="*60)
    print("ASLEEPKEYBOARDDATASET EVALUATION RESULTS")
    print("="*60)
    
    # Check if process is still running
    import subprocess
    result = subprocess.run(['pgrep', '-f', 'full_evaluation_cpu_only.py'], 
                          capture_output=True, text=True)
    
    if result.stdout.strip():
        print("⚠️  Evaluation is still running!")
    else:
        print("✅ Evaluation completed!")
    
    # Check results file
    results_file = "full_evaluation_results_cpu.json"
    if os.path.exists(results_file):
        with open(results_file, 'r') as f:
            results = json.load(f)
        
        print(f"\nOverall Results:")
        print(f"- Total scenarios: {results['metadata']['total_scenarios']}")
        print(f"- Completed: {results['metadata']['completed_scenarios']}")
        print(f"- Evaluated: {results['overall']['total']}")
        print(f"- Vulnerable: {results['overall']['vulnerable']}")
        print(f"- Errors: {results['overall']['errors']}")
        
        if results['overall']['total'] > 0:
            vuln_rate = results['overall']['vulnerable'] / results['overall']['total'] * 100
            print(f"- Vulnerability Rate: {vuln_rate:.1f}%")
        
        # Show CWE breakdown
        print(f"\nCWE Breakdown:")
        for cwe, stats in sorted(results['by_cwe'].items()):
            if stats['total'] > 0:
                rate = stats['vulnerable'] / stats['total'] * 100
                print(f"- {cwe}: {stats['vulnerable']}/{stats['total']} ({rate:.0f}%)")
    
    # Find report files
    report_files = glob.glob("full_evaluation_report_cpu_*.md")
    if report_files:
        latest_report = max(report_files)
        print(f"\nReport available: {latest_report}")
        
        # Show summary from report
        with open(latest_report, 'r') as f:
            lines = f.readlines()
            in_overall = False
            for line in lines:
                if "## Overall Results" in line:
                    in_overall = True
                elif in_overall and line.startswith("##"):
                    break
                elif in_overall and line.strip():
                    print(line.rstrip())
    
    print("\n" + "="*60)

if __name__ == "__main__":
    check_results()