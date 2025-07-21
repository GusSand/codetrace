#!/usr/bin/env python3
import datasets
import argparse
import sys
from collections import defaultdict
from typing import Dict, List, Tuple
import re
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def categorize_type(type_str: str) -> str:
    """Categorize the type into broader categories."""
    if type_str in ['str', 'String']:
        return 'string'
    elif type_str in ['int', 'float', 'number']:
        return 'numeric'
    elif type_str in ['dict', 'Dict']:
        return 'dictionary'
    elif type_str in ['list', 'List', 'Tuple', 'tuple']:
        return 'sequence'
    elif 'Optional' in type_str:
        return 'optional'
    elif type_str in ['bool', 'boolean']:
        return 'boolean'
    elif type_str in ['DataFrame']:
        return 'dataframe'
    else:
        return 'other'

def analyze_context(program: str) -> List[str]:
    """Analyze the context in which the type appears."""
    contexts = []
    
    # Check for function parameters
    if re.search(r'def\s+\w+\s*\([^)]*<FILL>[^)]*\)', program):
        contexts.append('function_parameter')
    
    # Check for return type hints
    if '->' in program:
        contexts.append('return_type')
        
    # Check for class methods
    if 'class' in program and 'def' in program:
        contexts.append('class_method')
        
    # Check for docstrings
    if '"""' in program or "'''" in program:
        contexts.append('documented')
        
    # Check for type annotations in variable assignments
    if re.search(r'\w+\s*:\s*<FILL>', program):
        contexts.append('variable_annotation')
    
    return contexts or ['other']

def analyze_dataset(dataset_path: str, name: str = "dataset"):
    """Analyze a single dataset and return statistics."""
    print(f"Loading {name} from {dataset_path}")
    ds = datasets.load_from_disk(dataset_path)
    print(f"{name.capitalize()} size: {len(ds)} examples")
    
    # Initialize counters
    type_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
    context_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
    
    # Analyze each example
    for example in ds:
        expected_type = example['fim_type']
        generated_type = example['generated_text']
        program = example['fim_program']
        
        # Analyze by type category
        type_category = categorize_type(expected_type)
        type_stats[type_category]['total'] += 1
        
        # Check if correct prediction
        if example.get('correct', False) or (expected_type.strip() == generated_type.strip()):
            type_stats[type_category]['correct'] += 1
            
        # Analyze by context
        contexts = analyze_context(program)
        for context in contexts:
            context_stats[context]['total'] += 1
            if example.get('correct', False) or (expected_type.strip() == generated_type.strip()):
                context_stats[context]['correct'] += 1
    
    overall_correct = sum(stats['correct'] for _, stats in type_stats.items())
    overall_total = sum(stats['total'] for _, stats in type_stats.items())
    overall_accuracy = overall_correct / overall_total if overall_total > 0 else 0
    
    return {
        "type_stats": type_stats,
        "context_stats": context_stats,
        "overall_accuracy": overall_accuracy,
        "overall_correct": overall_correct,
        "overall_total": overall_total
    }

def print_comparison_results(original_stats, mutated_stats):
    """Print comparison between original and mutated datasets."""
    print("\n===== OVERALL COMPARISON =====")
    print(f"Original accuracy: {original_stats['overall_accuracy']:.4f} ({original_stats['overall_correct']}/{original_stats['overall_total']})")
    print(f"Mutated accuracy: {mutated_stats['overall_accuracy']:.4f} ({mutated_stats['overall_correct']}/{mutated_stats['overall_total']})")
    
    accuracy_drop = original_stats['overall_accuracy'] - mutated_stats['overall_accuracy']
    drop_percentage = (accuracy_drop / original_stats['overall_accuracy'] * 100) if original_stats['overall_accuracy'] > 0 else 0
    
    print(f"Accuracy drop: {accuracy_drop:.4f} ({drop_percentage:.2f}%)")
    
    # Print type category comparison
    print("\n===== TYPE CATEGORY COMPARISON =====")
    print(f"{'Type Category':<15} {'Original':<15} {'Mutated':<15} {'Accuracy Drop':<15} {'Drop %':<10}")
    print("-" * 70)
    
    # Get all categories
    all_categories = set(original_stats['type_stats'].keys()) | set(mutated_stats['type_stats'].keys())
    
    for category in sorted(all_categories):
        orig_stats = original_stats['type_stats'].get(category, {'correct': 0, 'total': 0})
        mut_stats = mutated_stats['type_stats'].get(category, {'correct': 0, 'total': 0})
        
        orig_acc = orig_stats['correct'] / orig_stats['total'] if orig_stats['total'] > 0 else 0
        mut_acc = mut_stats['correct'] / mut_stats['total'] if mut_stats['total'] > 0 else 0
        
        acc_drop = orig_acc - mut_acc
        drop_pct = (acc_drop / orig_acc * 100) if orig_acc > 0 else 0
        
        print(f"{category:<15} {orig_acc:.4f} ({orig_stats['correct']}/{orig_stats['total']})  {mut_acc:.4f} ({mut_stats['correct']}/{mut_stats['total']})  {acc_drop:.4f}  {drop_pct:>8.2f}%")
    
    # Print context comparison
    print("\n===== CONTEXT COMPARISON =====")
    print(f"{'Context':<20} {'Original':<15} {'Mutated':<15} {'Accuracy Drop':<15} {'Drop %':<10}")
    print("-" * 75)
    
    # Get all contexts
    all_contexts = set(original_stats['context_stats'].keys()) | set(mutated_stats['context_stats'].keys())
    
    for context in sorted(all_contexts):
        orig_stats = original_stats['context_stats'].get(context, {'correct': 0, 'total': 0})
        mut_stats = mutated_stats['context_stats'].get(context, {'correct': 0, 'total': 0})
        
        orig_acc = orig_stats['correct'] / orig_stats['total'] if orig_stats['total'] > 0 else 0
        mut_acc = mut_stats['correct'] / mut_stats['total'] if mut_stats['total'] > 0 else 0
        
        acc_drop = orig_acc - mut_acc
        drop_pct = (acc_drop / orig_acc * 100) if orig_acc > 0 else 0
        
        print(f"{context:<20} {orig_acc:.4f} ({orig_stats['correct']}/{orig_stats['total']})  {mut_acc:.4f} ({mut_stats['correct']}/{mut_stats['total']})  {acc_drop:.4f}  {drop_pct:>8.2f}%")

def save_results(original_stats, mutated_stats, output_dir):
    """Save comparison results to output directory."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Create summary data
    summary = {
        "original": {
            "accuracy": original_stats['overall_accuracy'],
            "correct": original_stats['overall_correct'],
            "total": original_stats['overall_total']
        },
        "mutated": {
            "accuracy": mutated_stats['overall_accuracy'],
            "correct": mutated_stats['overall_correct'],
            "total": mutated_stats['overall_total']
        },
        "comparison": {
            "accuracy_drop": original_stats['overall_accuracy'] - mutated_stats['overall_accuracy'],
            "accuracy_drop_percentage": ((original_stats['overall_accuracy'] - mutated_stats['overall_accuracy']) / 
                                        original_stats['overall_accuracy'] * 100) if original_stats['overall_accuracy'] > 0 else 0
        }
    }
    
    # Create type category data
    type_data = []
    all_categories = set(original_stats['type_stats'].keys()) | set(mutated_stats['type_stats'].keys())
    
    for category in sorted(all_categories):
        orig_stats = original_stats['type_stats'].get(category, {'correct': 0, 'total': 0})
        mut_stats = mutated_stats['type_stats'].get(category, {'correct': 0, 'total': 0})
        
        orig_acc = orig_stats['correct'] / orig_stats['total'] if orig_stats['total'] > 0 else 0
        mut_acc = mut_stats['correct'] / mut_stats['total'] if mut_stats['total'] > 0 else 0
        
        type_data.append({
            "category": category,
            "original_accuracy": orig_acc,
            "mutated_accuracy": mut_acc,
            "accuracy_drop": orig_acc - mut_acc,
            "drop_percentage": ((orig_acc - mut_acc) / orig_acc * 100) if orig_acc > 0 else 0,
            "original_correct": orig_stats['correct'],
            "original_total": orig_stats['total'],
            "mutated_correct": mut_stats['correct'],
            "mutated_total": mut_stats['total']
        })
    
    # Create context data
    context_data = []
    all_contexts = set(original_stats['context_stats'].keys()) | set(mutated_stats['context_stats'].keys())
    
    for context in sorted(all_contexts):
        orig_stats = original_stats['context_stats'].get(context, {'correct': 0, 'total': 0})
        mut_stats = mutated_stats['context_stats'].get(context, {'correct': 0, 'total': 0})
        
        orig_acc = orig_stats['correct'] / orig_stats['total'] if orig_stats['total'] > 0 else 0
        mut_acc = mut_stats['correct'] / mut_stats['total'] if mut_stats['total'] > 0 else 0
        
        context_data.append({
            "context": context,
            "original_accuracy": orig_acc,
            "mutated_accuracy": mut_acc,
            "accuracy_drop": orig_acc - mut_acc,
            "drop_percentage": ((orig_acc - mut_acc) / orig_acc * 100) if orig_acc > 0 else 0,
            "original_correct": orig_stats['correct'],
            "original_total": orig_stats['total'],
            "mutated_correct": mut_stats['correct'],
            "mutated_total": mut_stats['total']
        })
    
    # Save results as JSON
    results = {
        "summary": summary,
        "type_categories": type_data,
        "contexts": context_data
    }
    
    with open(os.path.join(output_dir, "type_inference_comparison.json"), "w") as f:
        json.dump(results, f, indent=2)
    
    # Generate visualizations
    plt.figure(figsize=(12, 8))
    
    # Convert to pandas dataframes for easier plotting
    type_df = pd.DataFrame(type_data)
    context_df = pd.DataFrame(context_data)
    
    # Type category accuracy comparison
    plt.figure(figsize=(10, 6))
    type_plot_data = pd.melt(
        type_df, 
        id_vars=['category'], 
        value_vars=['original_accuracy', 'mutated_accuracy'],
        var_name='Dataset', 
        value_name='Accuracy'
    )
    type_plot_data['Dataset'] = type_plot_data['Dataset'].map({
        'original_accuracy': 'Original', 
        'mutated_accuracy': 'Mutated'
    })
    
    sns.barplot(x='category', y='Accuracy', hue='Dataset', data=type_plot_data)
    plt.title('Type Inference Accuracy by Category')
    plt.xlabel('Type Category')
    plt.ylabel('Accuracy')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "type_category_comparison.png"))
    
    # Context accuracy comparison
    plt.figure(figsize=(10, 6))
    context_plot_data = pd.melt(
        context_df, 
        id_vars=['context'], 
        value_vars=['original_accuracy', 'mutated_accuracy'],
        var_name='Dataset', 
        value_name='Accuracy'
    )
    context_plot_data['Dataset'] = context_plot_data['Dataset'].map({
        'original_accuracy': 'Original', 
        'mutated_accuracy': 'Mutated'
    })
    
    sns.barplot(x='context', y='Accuracy', hue='Dataset', data=context_plot_data)
    plt.title('Type Inference Accuracy by Context')
    plt.xlabel('Context')
    plt.ylabel('Accuracy')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "context_comparison.png"))
    
    # Accuracy drop chart by type
    plt.figure(figsize=(10, 6))
    sorted_type_df = type_df.sort_values('drop_percentage', ascending=False)
    sns.barplot(x='category', y='drop_percentage', data=sorted_type_df)
    plt.title('Accuracy Drop by Type Category (%)')
    plt.xlabel('Type Category')
    plt.ylabel('Accuracy Drop (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "type_accuracy_drop.png"))
    
    print(f"Results and visualizations saved to {output_dir}")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Compare type inference accuracy between original and mutated datasets")
    parser.add_argument("--original", required=True, help="Path to the original dataset")
    parser.add_argument("--mutated", required=True, help="Path to the mutated dataset")
    parser.add_argument("--output-dir", default="type_inference_comparison", help="Directory to save results")
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    # Analyze datasets
    original_stats = analyze_dataset(args.original, "original dataset")
    mutated_stats = analyze_dataset(args.mutated, "mutated dataset")
    
    # Print comparison results
    print_comparison_results(original_stats, mutated_stats)
    
    # Save results and visualizations
    save_results(original_stats, mutated_stats, args.output_dir)

if __name__ == '__main__':
    main() 