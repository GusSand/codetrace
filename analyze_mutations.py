#!/usr/bin/env python3
import json
import sys
import os
from collections import Counter

def analyze_results(results_file):
    """Analyze mutation robustness results."""
    if not os.path.exists(results_file):
        print(f"Results file {results_file} not found.")
        return
    
    with open(results_file, 'r') as f:
        data = json.load(f)
    
    # Basic statistics
    total_examples = len(data)
    total_mutations = sum(r.get("total_mutations_attempted", 0) for r in data)
    exact_matches = sum(sum(1 for m in r.get("mutations", []) if m.get("exact_match", False)) for r in data)
    
    print(f"Total examples: {total_examples}")
    print(f"Total mutations: {total_mutations}")
    print(f"Average mutations per example: {total_mutations/total_examples:.2f}")
    print(f"Exact matches: {exact_matches} ({exact_matches/total_mutations*100:.2f}%)")
    
    # Mutation count distribution
    mutation_counts = [len(r['mutations']) for r in data]
    print("\nDistribution of mutation counts:")
    for i in range(1, 11):
        count = mutation_counts.count(i)
        print(f"  {i} mutations: {count} examples ({count/total_examples*100:.2f}%)")
    
    # Examples with failed mutations
    failed_examples = [r for r in data if r.get("failed_mutations")]
    print(f"\nExamples with failed mutations: {len(failed_examples)} ({len(failed_examples)/total_examples*100:.2f}%)")
    
    # Examples that stopped early
    early_stop = [r for r in data if len(r['mutations']) < 10]
    print(f"\nExamples that stopped before 10 mutations: {len(early_stop)} ({len(early_stop)/total_examples*100:.2f}%)")
    
    if early_stop:
        print("\nReasons for early stopping:")
        for r in early_stop:
            example_id = r["example_id"]
            mutation_count = len(r["mutations"])
            print(f"  Example {example_id} stopped at {mutation_count} mutations")
    
    # Analyze exact matches
    print("\nExact match analysis:")
    exact_match_counts = [sum(1 for m in r.get("mutations", []) if m.get("exact_match", False)) for r in data]
    exact_match_distribution = Counter(exact_match_counts)
    
    for count, frequency in sorted(exact_match_distribution.items()):
        print(f"  {count} exact matches: {frequency} examples ({frequency/total_examples*100:.2f}%)")
    
    # Examples with high robustness (all mutations succeeded and many exact matches)
    high_robustness = [r for r in data if len(r.get("mutations", [])) == 10 and 
                      sum(1 for m in r.get("mutations", []) if m.get("exact_match", True)) >= 8]
    
    print(f"\nExamples with high robustness (10 mutations, 8+ exact matches): {len(high_robustness)} ({len(high_robustness)/total_examples*100:.2f}%)")
    
    # Examples with low robustness (all mutations succeeded but few exact matches)
    low_robustness = [r for r in data if len(r.get("mutations", [])) == 10 and 
                     sum(1 for m in r.get("mutations", []) if m.get("exact_match", True)) <= 2]
    
    print(f"Examples with low robustness (10 mutations, ≤2 exact matches): {len(low_robustness)} ({len(low_robustness)/total_examples*100:.2f}%)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_mutations.py <results_file>")
        sys.exit(1)
    
    results_file = sys.argv[1]
    analyze_results(results_file) 