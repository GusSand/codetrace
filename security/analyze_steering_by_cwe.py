#!/usr/bin/env python3
import os
import json
import argparse
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
from typing import Dict, List, Any

def load_results(results_dir: str) -> Dict[str, Any]:
    """
    Load the steering results from the specified directory.
    """
    results = {}
    
    # Load test results
    test_results_path = os.path.join(results_dir, "test_results.json")
    if os.path.exists(test_results_path):
        with open(test_results_path, 'r') as f:
            results["test"] = json.load(f)
    
    # Load test with steering results
    test_steer_results_path = os.path.join(results_dir, "test_steer_results.json")
    if os.path.exists(test_steer_results_path):
        with open(test_steer_results_path, 'r') as f:
            results["test_steer"] = json.load(f)
    
    # Load steering dataset
    steering_file_path = os.path.join(results_dir, "steering_data.json")
    if not os.path.exists(steering_file_path):
        # Try to find it in the parent directory
        steering_file_path = os.path.join(os.path.dirname(results_dir), "security_steering_data.json")
    
    if os.path.exists(steering_file_path):
        with open(steering_file_path, 'r') as f:
            results["steering_data"] = json.load(f)
    
    return results

def analyze_by_cwe(results: Dict[str, Any]) -> Dict[str, Dict[str, float]]:
    """
    Analyze the steering success rate by CWE type.
    """
    analysis = {}
    
    if "test" not in results or "test_steer" not in results or "steering_data" not in results:
        return analysis
    
    # Group steering data by CWE
    cwe_to_steering_examples = defaultdict(list)
    for example in results["steering_data"]:
        cwe = example.get("cwe", "unknown")
        cwe_to_steering_examples[cwe].append(example)
    
    # Calculate success rates by CWE
    cwe_to_stats = {}
    for cwe, examples in cwe_to_steering_examples.items():
        cwe_to_stats[cwe] = {
            "num_examples": len(examples),
            "test_success": 0,
            "test_steer_success": 0
        }
    
    # Count test successes (this is an estimation as we don't have direct mapping)
    total_test_successes = results["test"].get("num_succ", 0)
    total_test_examples = results["test"].get("total", 1)
    test_success_rate = total_test_successes / total_test_examples if total_test_examples > 0 else 0
    
    # Count test_steer successes (this is an estimation as we don't have direct mapping)
    total_test_steer_successes = results["test_steer"].get("num_succ", 0)
    total_test_steer_examples = results["test_steer"].get("total", 1)
    test_steer_success_rate = total_test_steer_successes / total_test_steer_examples if total_test_steer_examples > 0 else 0
    
    # Estimate success counts proportionally
    for cwe, stats in cwe_to_stats.items():
        num_examples = stats["num_examples"]
        stats["test_success_rate"] = test_success_rate
        stats["test_steer_success_rate"] = test_steer_success_rate
        stats["estimated_test_successes"] = num_examples * test_success_rate
        stats["estimated_test_steer_successes"] = num_examples * test_steer_success_rate
        stats["estimated_improvement"] = test_steer_success_rate - test_success_rate
        stats["percent_improvement"] = (test_steer_success_rate - test_success_rate) / test_success_rate * 100 if test_success_rate > 0 else 0
    
    return cwe_to_stats

def plot_cwe_results(cwe_stats: Dict[str, Dict[str, float]], output_path: str = None):
    """
    Create a bar chart showing the improvement by CWE type.
    """
    cwe_names = list(cwe_stats.keys())
    improvements = [stats["estimated_improvement"] * 100 for stats in cwe_stats.values()]  # Convert to percentage
    
    # Sort by improvement
    sorted_indices = np.argsort(improvements)
    sorted_cwe_names = [cwe_names[i] for i in sorted_indices]
    sorted_improvements = [improvements[i] for i in sorted_indices]
    
    plt.figure(figsize=(12, 8))
    plt.bar(sorted_cwe_names, sorted_improvements)
    plt.axhline(y=0, color='r', linestyle='-', alpha=0.3)
    plt.xlabel('CWE Type')
    plt.ylabel('Estimated Improvement (%)')
    plt.title('Steering Improvement by CWE Type')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path)
    else:
        plt.show()

def main():
    parser = argparse.ArgumentParser(description='Analyze steering results by CWE type')
    parser.add_argument('--results_dir', type=str, required=True,
                      help='Directory containing the steering results')
    parser.add_argument('--output_file', type=str, default=None,
                      help='Output file for the CWE analysis chart')
    args = parser.parse_args()
    
    # Load results
    print(f"Loading results from {args.results_dir}...")
    results = load_results(args.results_dir)
    
    if not results.get("test") or not results.get("test_steer"):
        print("Error: Could not find test and test_steer results. Make sure you're pointing to the correct directory.")
        return
    
    if not results.get("steering_data"):
        print("Error: Could not find steering data. Make sure security_steering_data.json is in the parent directory.")
        return
    
    # Analyze by CWE
    print("Analyzing results by CWE type...")
    cwe_stats = analyze_by_cwe(results)
    
    # Print the analysis
    print("\nSteering effectiveness by CWE type:")
    print("=" * 80)
    print(f"{'CWE':<10} {'Examples':<10} {'Test Succ %':<15} {'Test+Steer %':<15} {'Improvement':<15} {'% Change':<10}")
    print("-" * 80)
    
    for cwe, stats in sorted(cwe_stats.items(), key=lambda x: x[1]['estimated_improvement'], reverse=True):
        print(f"{cwe:<10} {stats['num_examples']:<10} {stats['test_success_rate']*100:<15.2f} "
              f"{stats['test_steer_success_rate']*100:<15.2f} {stats['estimated_improvement']*100:<15.2f} "
              f"{stats['percent_improvement']:<10.2f}")
    
    # Plot the results
    if args.output_file:
        print(f"\nCreating chart and saving to {args.output_file}...")
        plot_cwe_results(cwe_stats, args.output_file)
    else:
        print("\nCreating chart...")
        plot_cwe_results(cwe_stats)
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    main() 