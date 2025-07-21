#!/usr/bin/env python3
import datasets
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

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

def analyze_dataset(dataset):
    """Analyze the accuracy of a dataset."""
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
    
    # Calculate category accuracies
    category_stats = {}
    for category, stats in type_stats.items():
        category_accuracy = stats['correct'] / stats['total'] if stats['total'] > 0 else 0
        category_stats[category] = {
            'accuracy': category_accuracy,
            'correct': stats['correct'],
            'total': stats['total']
        }
    
    return {
        'overall_accuracy': accuracy,
        'correct_count': correct_count,
        'total_count': len(dataset),
        'by_category': category_stats
    }

def print_random_examples(original, mutated, n=5):
    """Print random examples from both datasets for manual comparison."""
    import random
    
    indices = random.sample(range(len(original)), n)
    
    print("\n===== RANDOM EXAMPLE COMPARISON =====")
    for i, idx in enumerate(indices):
        orig = original[idx]
        mut = mutated[idx]
        
        print(f"\nExample {i+1}:")
        print(f"Expected Type: {orig['fim_type']}")
        
        # Original program and prediction
        print("\nORIGINAL:")
        print(f"Program: {orig['fim_program'][:100]}..." if len(orig['fim_program']) > 100 else f"Program: {orig['fim_program']}")
        print(f"Prediction: {orig['generated_text']}")
        print(f"Correct: {orig['correct']}")
        
        # Mutated program and prediction
        print("\nMUTATED:")
        print(f"Program: {mut['fim_program'][:100]}..." if len(mut['fim_program']) > 100 else f"Program: {mut['fim_program']}")
        print(f"Prediction: {mut['generated_text']}")
        print(f"Correct: {mut['correct']}")
        
        print("-" * 80)

def compare_and_visualize(original_stats, mutated_stats, output_dir="comparison_results"):
    """Compare results and create visualizations."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Calculate accuracy drop
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
    
    print("\n===== CATEGORY COMPARISON =====")
    print(f"{'Category':<15} {'Original':<15} {'Mutated':<15} {'Drop':<10} {'Drop %':<10}")
    print("-" * 65)
    
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
    
    # Create and save visualizations
    # Convert to pandas dataframe for easier plotting
    df = pd.DataFrame(category_data)
    
    # 1. Bar chart comparing original vs mutated accuracy by category
    plt.figure(figsize=(12, 8))
    melted_df = pd.melt(
        df, 
        id_vars=['category'], 
        value_vars=['original_accuracy', 'mutated_accuracy'],
        var_name='dataset_type', 
        value_name='accuracy'
    )
    melted_df['dataset_type'] = melted_df['dataset_type'].map({
        'original_accuracy': 'Original', 
        'mutated_accuracy': 'Mutated'
    })
    
    sns.barplot(x='category', y='accuracy', hue='dataset_type', data=melted_df)
    plt.title('Type Inference Accuracy by Category')
    plt.xlabel('Type Category')
    plt.ylabel('Accuracy')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'accuracy_by_category.png'))
    
    # 2. Bar chart of accuracy drop percentage by category
    plt.figure(figsize=(12, 8))
    sorted_df = df.sort_values('drop_percentage', ascending=False)
    sns.barplot(x='category', y='drop_percentage', data=sorted_df)
    plt.title('Accuracy Drop Percentage by Category')
    plt.xlabel('Type Category')
    plt.ylabel('Accuracy Drop (%)')
    plt.xticks(rotation=45)
    plt.axhline(y=0, color='r', linestyle='--')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'accuracy_drop_by_category.png'))
    
    # Save results as JSON
    results = {
        'summary': {
            'original_accuracy': original_stats['overall_accuracy'],
            'mutated_accuracy': mutated_stats['overall_accuracy'],
            'accuracy_drop': accuracy_drop,
            'drop_percentage': drop_percentage
        },
        'by_category': category_data
    }
    
    with open(os.path.join(output_dir, 'comparison_results.json'), 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to {output_dir}")

def compare_example_mutations(original, mutated, n=5):
    """Compare specific examples to see how mutation affected the code."""
    import random
    
    indices = random.sample(range(len(original)), n)
    examples = []
    
    for idx in indices:
        orig = original[idx]
        mut = mutated[idx]
        
        example = {
            "expected_type": orig["fim_type"],
            "original_program": orig["fim_program"],
            "mutated_program": mut["fim_program"],
            "original_prediction": orig["generated_text"],
            "mutated_prediction": mut["generated_text"],
            "original_correct": orig["correct"],
            "mutated_correct": mut["correct"]
        }
        examples.append(example)
    
    return examples

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Compare original and mutated datasets")
    parser.add_argument("--original", default="starcoder1_fim_python_completions", help="Path to original dataset")
    parser.add_argument("--mutated", default="starcoder1_fim_python_vars_mutation_full", help="Path to mutated dataset")
    parser.add_argument("--output-dir", default="comparison_results", help="Directory to save results")
    parser.add_argument("--num-examples", type=int, default=5, help="Number of random examples to print")
    args = parser.parse_args()
    
    # Load datasets
    print(f"Loading original dataset from {args.original}")
    original_dataset = datasets.load_from_disk(args.original)
    print(f"Original dataset size: {len(original_dataset)}")
    print(f"Original dataset columns: {original_dataset.column_names}")
    
    print(f"Loading mutated dataset from {args.mutated}")
    mutated_dataset = datasets.load_from_disk(args.mutated)
    print(f"Mutated dataset size: {len(mutated_dataset)}")
    print(f"Mutated dataset columns: {mutated_dataset.column_names}")
    
    # Print some examples for comparison
    print_random_examples(original_dataset, mutated_dataset, n=args.num_examples)
    
    # Analyze datasets
    print("\nAnalyzing original dataset...")
    original_stats = analyze_dataset(original_dataset)
    
    print("Analyzing mutated dataset...")
    mutated_stats = analyze_dataset(mutated_dataset)
    
    # Compare and visualize results
    compare_and_visualize(original_stats, mutated_stats, args.output_dir)
    
    # Save examples for detailed analysis
    examples = compare_example_mutations(original_dataset, mutated_dataset, n=10)
    with open(os.path.join(args.output_dir, "mutation_examples.json"), "w") as f:
        json.dump(examples, f, indent=2)
    
    print(f"Saved 10 example mutations to {os.path.join(args.output_dir, 'mutation_examples.json')}")

if __name__ == "__main__":
    main()