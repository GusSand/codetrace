#!/usr/bin/env python3
import datasets
import argparse
import json
import os
from pathlib import Path
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def categorize_type(type_str):
    """Categorize the type into broader categories."""
    if type_str in ['str', 'String']:
        return 'string'
    elif type_str in ['int', 'float', 'number']:
        return 'numeric'
    elif type_str in ['dict', 'Dict']:
        return 'dictionary'
    elif type_str in ['list', 'List', 'Tuple', 'tuple'] or '[' in type_str:
        return 'sequence'
    elif 'Optional' in type_str:
        return 'optional'
    elif type_str in ['bool', 'boolean']:
        return 'boolean'
    elif 'Any' in type_str or 'Union' in type_str:
        return 'flexible'
    elif type_str in ['None', 'NoneType']:
        return 'none'
    else:
        return 'other'

def analyze_context(program):
    """Analyze the context in which the type appears."""
    contexts = []
    
    # Check for function parameters
    if "def " in program and "(" in program:
        contexts.append('function')
    
    # Check for return type hints
    if '->' in program:
        contexts.append('return_type')
    
    # Check for class definitions
    if 'class ' in program:
        contexts.append('class')
    
    # Check for variable assignments
    if ' = ' in program:
        contexts.append('assignment')
    
    # Check for list comprehensions
    if '[' in program and 'for' in program:
        contexts.append('comprehension')
    
    return contexts or ['other']

def analyze_dataset(dataset):
    """Analyze a dataset and return statistics."""
    # Get overall accuracy
    correct_count = sum(1 for ex in dataset if ex['correct'])
    accuracy = correct_count / len(dataset)
    
    # Analyze by type category
    type_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
    for example in dataset:
        expected_type = example['fim_type']
        category = categorize_type(expected_type)
        
        type_stats[category]['total'] += 1
        if example['correct']:
            type_stats[category]['correct'] += 1
    
    # Calculate context stats
    context_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
    for example in dataset:
        contexts = analyze_context(example['fim_program'])
        for context in contexts:
            context_stats[context]['total'] += 1
            if example['correct']:
                context_stats[context]['correct'] += 1
    
    # Calculate category accuracies
    category_stats = {}
    for category, stats in type_stats.items():
        category_accuracy = stats['correct'] / stats['total'] if stats['total'] > 0 else 0
        category_stats[category] = {
            'accuracy': category_accuracy,
            'correct': stats['correct'],
            'total': stats['total']
        }
    
    # Calculate context accuracies
    context_data = {}
    for context, stats in context_stats.items():
        context_accuracy = stats['correct'] / stats['total'] if stats['total'] > 0 else 0
        context_data[context] = {
            'accuracy': context_accuracy,
            'correct': stats['correct'],
            'total': stats['total']
        }
    
    return {
        'overall_accuracy': accuracy,
        'correct_count': correct_count,
        'total_count': len(dataset),
        'by_category': category_stats,
        'by_context': context_data
    }

def compare_and_visualize(original_stats, mutated_stats, output_dir):
    """Compare the original and mutated results, create visualizations."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Calculate overall change
    accuracy_drop = original_stats['overall_accuracy'] - mutated_stats['overall_accuracy']
    drop_percentage = (accuracy_drop / original_stats['overall_accuracy'] * 100) if original_stats['overall_accuracy'] > 0 else 0
    
    # Print overall comparison
    print("\n===== OVERALL COMPARISON =====")
    print(f"Original accuracy: {original_stats['overall_accuracy']:.4f} ({original_stats['correct_count']}/{original_stats['total_count']})")
    print(f"Mutated accuracy: {mutated_stats['overall_accuracy']:.4f} ({mutated_stats['correct_count']}/{mutated_stats['total_count']})")
    print(f"Accuracy drop: {accuracy_drop:.4f} ({drop_percentage:.2f}%)")
    
    # Prepare category data for comparison
    categories = set(original_stats['by_category'].keys()) | set(mutated_stats['by_category'].keys())
    category_data = []
    
    print("\n===== TYPE CATEGORY COMPARISON =====")
    print(f"{'Category':<15} {'Original':<20} {'Mutated':<20} {'Drop':<10} {'Drop %':<10}")
    print("-" * 75)
    
    for category in sorted(categories):
        orig_stats = original_stats['by_category'].get(category, {'accuracy': 0, 'correct': 0, 'total': 0})
        mut_stats = mutated_stats['by_category'].get(category, {'accuracy': 0, 'correct': 0, 'total': 0})
        
        orig_acc = orig_stats['accuracy']
        mut_acc = mut_stats['accuracy']
        cat_drop = orig_acc - mut_acc
        drop_pct = (cat_drop / orig_acc * 100) if orig_acc > 0 else 0
        
        print(f"{category:<15} {orig_acc:.4f} ({orig_stats['correct']}/{orig_stats['total']})  {mut_acc:.4f} ({mut_stats['correct']}/{mut_stats['total']})  {cat_drop:.4f}  {drop_pct:>8.2f}%")
        
        category_data.append({
            'category': category,
            'original_accuracy': orig_acc,
            'mutated_accuracy': mut_acc,
            'accuracy_drop': cat_drop,
            'drop_percentage': drop_pct,
            'original_correct': orig_stats['correct'],
            'original_total': orig_stats['total'],
            'mutated_correct': mut_stats['correct'],
            'mutated_total': mut_stats['total'],
        })
    
    # Prepare context data for comparison
    contexts = set(original_stats['by_context'].keys()) | set(mutated_stats['by_context'].keys())
    context_data = []
    
    print("\n===== CONTEXT COMPARISON =====")
    print(f"{'Context':<15} {'Original':<20} {'Mutated':<20} {'Drop':<10} {'Drop %':<10}")
    print("-" * 75)
    
    for context in sorted(contexts):
        orig_stats = original_stats['by_context'].get(context, {'accuracy': 0, 'correct': 0, 'total': 0})
        mut_stats = mutated_stats['by_context'].get(context, {'accuracy': 0, 'correct': 0, 'total': 0})
        
        orig_acc = orig_stats['accuracy']
        mut_acc = mut_stats['accuracy']
        ctx_drop = orig_acc - mut_acc
        drop_pct = (ctx_drop / orig_acc * 100) if orig_acc > 0 else 0
        
        print(f"{context:<15} {orig_acc:.4f} ({orig_stats['correct']}/{orig_stats['total']})  {mut_acc:.4f} ({mut_stats['correct']}/{mut_stats['total']})  {ctx_drop:.4f}  {drop_pct:>8.2f}%")
        
        context_data.append({
            'context': context,
            'original_accuracy': orig_acc,
            'mutated_accuracy': mut_acc,
            'accuracy_drop': ctx_drop,
            'drop_percentage': drop_pct,
            'original_correct': orig_stats['correct'],
            'original_total': orig_stats['total'],
            'mutated_correct': mut_stats['correct'],
            'mutated_total': mut_stats['total'],
        })
    
    # Create and save visualizations
    # 1. Bar chart comparing original vs mutated accuracy by category
    plt.figure(figsize=(12, 8))
    df_cat = pd.DataFrame(category_data)
    df_cat_melt = pd.melt(
        df_cat, 
        id_vars=['category'], 
        value_vars=['original_accuracy', 'mutated_accuracy'],
        var_name='dataset_type', 
        value_name='accuracy'
    )
    df_cat_melt['dataset_type'] = df_cat_melt['dataset_type'].map({
        'original_accuracy': 'Original', 
        'mutated_accuracy': 'Mutated'
    })
    
    sns.barplot(x='category', y='accuracy', hue='dataset_type', data=df_cat_melt)
    plt.title('Type Inference Accuracy by Category')
    plt.xlabel('Type Category')
    plt.ylabel('Accuracy')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'accuracy_by_category.png'))
    
    # 2. Bar chart of accuracy drop by category
    plt.figure(figsize=(12, 8))
    df_cat_sorted = df_cat.sort_values('drop_percentage', ascending=False)
    sns.barplot(x='category', y='drop_percentage', data=df_cat_sorted)
    plt.title('Accuracy Drop Percentage by Category')
    plt.xlabel('Type Category')
    plt.ylabel('Accuracy Drop (%)')
    plt.xticks(rotation=45)
    plt.axhline(y=0, color='r', linestyle='--')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'drop_by_category.png'))
    
    # 3. Context comparison
    plt.figure(figsize=(12, 8))
    df_ctx = pd.DataFrame(context_data)
    df_ctx_melt = pd.melt(
        df_ctx, 
        id_vars=['context'], 
        value_vars=['original_accuracy', 'mutated_accuracy'],
        var_name='dataset_type', 
        value_name='accuracy'
    )
    df_ctx_melt['dataset_type'] = df_ctx_melt['dataset_type'].map({
        'original_accuracy': 'Original', 
        'mutated_accuracy': 'Mutated'
    })
    
    sns.barplot(x='context', y='accuracy', hue='dataset_type', data=df_ctx_melt)
    plt.title('Type Inference Accuracy by Context')
    plt.xlabel('Code Context')
    plt.ylabel('Accuracy')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'accuracy_by_context.png'))
    
    # Save detailed results to file
    results = {
        'summary': {
            'original_accuracy': original_stats['overall_accuracy'],
            'mutated_accuracy': mutated_stats['overall_accuracy'],
            'accuracy_drop': accuracy_drop,
            'drop_percentage': drop_percentage
        },
        'by_category': category_data,
        'by_context': context_data
    }
    
    with open(os.path.join(output_dir, 'type_inference_comparison.json'), 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to {output_dir}")
    
    return results

def find_candidates_for_steering(original_dataset, mutated_dataset, n=10):
    """Find examples that failed in both datasets but might be good candidates for steering."""
    candidates = []
    
    # We want examples that:
    # 1. Failed in both original and mutated datasets
    # 2. Have a clear expected type
    # 3. Have meaningful variable names in the original
    for i in range(min(len(original_dataset), len(mutated_dataset))):
        orig_ex = original_dataset[i]
        mut_ex = mutated_dataset[i]
        
        if not orig_ex['correct'] and not mut_ex['correct']:
            expected_type = orig_ex['fim_type']
            # Skip overly complex types for initial steering attempts
            if len(expected_type) < 30 and categorize_type(expected_type) != 'other':
                candidates.append({
                    'index': i,
                    'original_program': orig_ex['fim_program'],
                    'mutated_program': mut_ex['fim_program'],
                    'expected_type': expected_type,
                    'generated_type_original': orig_ex['generated_text'],
                    'generated_type_mutated': mut_ex['generated_text'],
                    'category': categorize_type(expected_type),
                    'contexts': analyze_context(orig_ex['fim_program'])
                })
    
    # Sort candidates by type category to get a diverse set
    candidates.sort(key=lambda x: x['category'])
    
    # Select a diverse set of candidates
    selected = []
    categories_seen = set()
    
    # First, get one from each category
    for candidate in candidates:
        if candidate['category'] not in categories_seen and len(selected) < n:
            selected.append(candidate)
            categories_seen.add(candidate['category'])
    
    # Fill remaining spots with other candidates
    remaining = [c for c in candidates if c not in selected]
    while len(selected) < n and remaining:
        selected.append(remaining.pop(0))
    
    return selected

def main():
    parser = argparse.ArgumentParser(description="Analyze and compare type inference results")
    parser.add_argument("--original-results", type=str, required=True,
                        help="Path to the original results directory")
    parser.add_argument("--mutated-results", type=str, required=True,
                        help="Path to the mutated results directory")
    parser.add_argument("--output-dir", type=str, default="type_inference_analysis",
                        help="Directory to save analysis results")
    parser.add_argument("--steering-candidates", type=str, default=None,
                        help="Path to save steering candidates")
    parser.add_argument("--max-candidates", type=int, default=10,
                        help="Maximum number of steering candidates to find")
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Load results
    print(f"Loading original results from {args.original_results}")
    original_ds = datasets.load_from_disk(args.original_results)
    
    print(f"Loading mutated results from {args.mutated_results}")
    mutated_ds = datasets.load_from_disk(args.mutated_results)
    
    # Analyze datasets
    print("Analyzing original results...")
    original_stats = analyze_dataset(original_ds)
    
    print("Analyzing mutated results...")
    mutated_stats = analyze_dataset(mutated_ds)
    
    # Compare and visualize results
    compare_and_visualize(original_stats, mutated_stats, args.output_dir)
    
    # Find candidates for steering
    print("\nFinding candidates for steering vector creation...")
    candidates = find_candidates_for_steering(
        original_ds, mutated_ds, args.max_candidates
    )
    
    # Save steering candidates if path is provided
    if args.steering_candidates:
        # Use the provided path directly instead of joining with output_dir
        steering_file = args.steering_candidates
        with open(steering_file, 'w') as f:
            json.dump(candidates, f, indent=2)
        print(f"Saved {len(candidates)} steering candidates to {steering_file}")

if __name__ == "__main__":
    main() 