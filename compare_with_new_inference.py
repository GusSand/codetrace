#!/usr/bin/env python3
import datasets
import argparse
import sys
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
import torch
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForCausalLM
from collections import defaultdict
import re

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

def load_model_and_tokenizer(model_id, device="cuda"):
    """Load the model and tokenizer."""
    print(f"Loading model and tokenizer from {model_id}")
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    
    # Use 8-bit quantization to reduce memory usage
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto",
        torch_dtype=torch.float16,
        trust_remote_code=True,
        offload_folder="offload",
    )
    return model, tokenizer

def run_inference(model, tokenizer, dataset, max_samples=None, max_new_tokens=20):
    """Run inference on a dataset and return updated examples with predictions."""
    if max_samples and max_samples < len(dataset):
        # Sample a subset for quicker testing
        indices = random.sample(range(len(dataset)), max_samples)
        dataset = dataset.select(indices)
    
    results = []
    
    # Print first few examples for debugging
    print("\nDebugging dataset examples:")
    for i in range(min(3, len(dataset))):
        example = dataset[i]
        print(f"Example {i+1}:")
        print(f"FIM Type: {example['fim_type']}")
        print(f"Expected solution: {example['canonical_solution']}")
        print(f"Program snippet (first 100 chars): {example['fim_program'][:100]}...")
        print(f"Generated text: {example['generated_text']}")
        print(f"Correct: {example['correct']}")
        print("-" * 50)
    
    print("\nRunning inference on examples...")
    processed_count = {
        'total': 0,
        'success': 0,
        'error': 0
    }
    
    formats_found = set()
    
    for idx in tqdm(range(len(dataset)), desc="Running inference"):
        try:
            example = dataset[idx]
            program = example['fim_program']
            
            # Keep track of formats we're seeing
            format_markers = []
            if '<fim_prefix>' in program: format_markers.append('fim_prefix')
            if '<fim_suffix>' in program: format_markers.append('fim_suffix')
            if '<fim_middle>' in program: format_markers.append('fim_middle')
            if '<FILL>' in program: format_markers.append('FILL')
            if '_CodetraceSpecialPlaceholder_' in program: format_markers.append('CodetraceSpecialPlaceholder')
            
            if format_markers:
                formats_found.add(tuple(format_markers))
            
            # Extract the prompt for code completion
            if '<fim_prefix>' in program and '<fim_suffix>' in program:
                # Original dataset format - old FIM format
                prompt = program.split('<fim_suffix>')[0].replace('<fim_prefix>', '')
            elif '_CodetraceSpecialPlaceholder_' in program:
                # Mutated dataset format - extract the part before the placeholder
                prompt = program.split('_CodetraceSpecialPlaceholder_')[0]
            else:
                # Default case - use the program as is
                prompt = program
            
            # Tokenize and generate
            inputs = tokenizer(prompt, return_tensors="pt")
            
            # Move inputs to the same device as model
            for k, v in inputs.items():
                inputs[k] = v.to(model.device)
            
            with torch.no_grad():
                outputs = model.generate(
                    inputs.input_ids,
                    attention_mask=inputs.get('attention_mask', None),
                    max_new_tokens=max_new_tokens,
                    do_sample=False,
                    pad_token_id=tokenizer.eos_token_id,
                    num_beams=1,
                    temperature=1.0
                )
            
            # Get only the newly generated tokens
            generated_tokens = outputs[0, inputs.input_ids.shape[1]:]
            generated_text = tokenizer.decode(generated_tokens, skip_special_tokens=True)
            
            # For code completion, the canonical solution is the expected output
            expected_solution = example['canonical_solution'].strip()
            
            # Trim the generated text to be comparable to expected solution
            generated_first_line = generated_text.strip().split('\n')[0] if generated_text.strip() else ""
            expected_first_line = expected_solution.split('\n')[0] if expected_solution else ""
            
            # Check if generated text matches expected solution (exact or partial)
            correct = False
            if generated_first_line and expected_first_line:
                if generated_first_line == expected_first_line:
                    correct = True
                elif generated_first_line in expected_first_line or expected_first_line in generated_first_line:
                    # Consider partial matches
                    correct = True
            
            # Create a new example with the prediction results
            new_example = dict(example)
            new_example['new_generated_text'] = generated_text
            new_example['new_first_line'] = generated_first_line
            new_example['expected_first_line'] = expected_first_line
            new_example['new_correct'] = correct
            
            # Print a few examples to see what's happening
            if idx < 3:
                print(f"\nExample {idx+1} prediction:")
                print(f"Format markers: {format_markers}")
                print(f"Prompt: '{prompt[-100:]}...'")
                print(f"Original generated: '{example['generated_text']}'")
                print(f"New generated: '{generated_text}'")
                print(f"Expected solution: '{expected_solution}'")
                print(f"Correct: {correct}")
            
            processed_count['success'] += 1
            results.append(new_example)
        except Exception as e:
            print(f"Error processing example {idx}: {str(e)}")
            # Keep the example but mark as error
            new_example = dict(dataset[idx])
            new_example['new_generated_text'] = ""
            new_example['new_correct'] = False
            new_example['error'] = str(e)
            processed_count['error'] += 1
            results.append(new_example)
        
        processed_count['total'] += 1
    
    # Count correct predictions
    correct_count = sum(1 for ex in results if ex['new_correct'])
    print(f"\nCorrect predictions: {correct_count}/{len(results)} ({correct_count/len(results)*100:.2f}%)")
    print(f"Processing stats: {processed_count['success']} successful, {processed_count['error']} errors")
    print(f"FIM formats found: {formats_found}")
    
    # Convert back to dataset
    return datasets.Dataset.from_list(results)

def analyze_dataset(dataset):
    """Analyze the inference results on a dataset."""
    # Get overall accuracy
    correct_count = sum(1 for ex in dataset if ex['new_correct'])
    accuracy = correct_count / len(dataset)
    
    # Analyze by type category
    type_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
    for example in dataset:
        expected_type = example.get('fim_type', 'unknown')
        category = categorize_type(expected_type)
        
        type_stats[category]['total'] += 1
        if example['new_correct']:
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

def compare_and_visualize(original_stats, mutated_stats, output_dir):
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
    
    with open(os.path.join(output_dir, 'inference_comparison.json'), 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to {output_dir}")

def parse_args():
    parser = argparse.ArgumentParser(description="Run type inference on original and mutated datasets and compare results")
    parser.add_argument("--original", default="starcoder1_fim_python_completions", help="Path to original dataset")
    parser.add_argument("--mutated", default="starcoder1_fim_python_vars_mutation_full", help="Path to mutated dataset")
    parser.add_argument("--model", default="bigcode/starcoderbase-1b", help="Model ID to use for inference")
    parser.add_argument("--output-dir", default="type_inference_results", help="Directory to save results")
    parser.add_argument("--max-samples", type=int, default=50, help="Maximum number of samples to test (for faster testing)")
    parser.add_argument("--device", default="auto", help="Device to run inference on")
    parser.add_argument("--max-new-tokens", type=int, default=20, help="Maximum number of tokens to generate")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Set random seed
    random.seed(args.seed)
    torch.manual_seed(args.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)
    
    # Load datasets
    print(f"Loading original dataset from {args.original}")
    original_dataset = datasets.load_from_disk(args.original)
    print(f"Original dataset size: {len(original_dataset)}")
    
    print(f"Loading mutated dataset from {args.mutated}")
    mutated_dataset = datasets.load_from_disk(args.mutated)
    print(f"Mutated dataset size: {len(mutated_dataset)}")
    
    # Load model and tokenizer
    model, tokenizer = load_model_and_tokenizer(args.model, args.device)
    
    # Run inference on both datasets
    print("\nRunning inference on original dataset...")
    original_with_predictions = run_inference(
        model, tokenizer, original_dataset, 
        max_samples=args.max_samples,
        max_new_tokens=args.max_new_tokens
    )
    
    print("\nRunning inference on mutated dataset...")
    mutated_with_predictions = run_inference(
        model, tokenizer, mutated_dataset, 
        max_samples=args.max_samples,
        max_new_tokens=args.max_new_tokens
    )
    
    # Analyze results
    print("\nAnalyzing results...")
    original_stats = analyze_dataset(original_with_predictions)
    mutated_stats = analyze_dataset(mutated_with_predictions)
    
    # Compare and visualize
    compare_and_visualize(original_stats, mutated_stats, args.output_dir)
    
    # Save some example predictions for manual inspection
    examples_path = os.path.join(args.output_dir, "example_predictions.json")
    num_examples = min(10, len(original_with_predictions))
    
    examples = []
    for i in range(num_examples):
        orig_ex = original_with_predictions[i]
        mut_ex = mutated_with_predictions[i]
        
        examples.append({
            "original_program": orig_ex['fim_program'],
            "mutated_program": mut_ex['fim_program'],
            "expected_type": orig_ex['fim_type'],
            "original_prediction": orig_ex['new_generated_text'],
            "mutated_prediction": mut_ex['new_generated_text'],
            "original_correct": orig_ex['new_correct'],
            "mutated_correct": mut_ex['new_correct']
        })
    
    with open(examples_path, 'w') as f:
        json.dump(examples, f, indent=2)
    
    print(f"Saved {num_examples} example predictions to {examples_path}")

if __name__ == "__main__":
    main() 