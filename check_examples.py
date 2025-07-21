import datasets
import random

# Set random seed for reproducibility
random.seed(42)

def check_dataset(path, name):
    print(f"\n===== Checking {name} =====")
    ds = datasets.load_from_disk(path)
    print(f"Dataset size: {len(ds)} examples")
    print(f"Columns: {ds.column_names}")
    
    # Sample some random examples
    indices = random.sample(range(len(ds)), min(5, len(ds)))
    
    print("\nRandom examples:")
    for i, idx in enumerate(indices):
        example = ds[idx]
        print(f"\nExample {i+1} (index {idx}):")
        print(f"FIM Type: {example['fim_type']}")
        print(f"Generated text: '{example['generated_text']}'")
        print(f"Correct: {example.get('correct', 'N/A')}")
        
        # Check if expected type matches the generated text
        expected = example['fim_type']
        generated = example['generated_text']
        if expected.strip() == generated.strip():
            print("Expected matches generated: YES")
        else:
            print("Expected matches generated: NO")
    
    # Count correct predictions
    if 'correct' in ds.column_names:
        correct_count = sum(1 for ex in ds if ex['correct'])
        accuracy = correct_count / len(ds)
        print(f"\nOverall accuracy: {accuracy:.4f} ({correct_count}/{len(ds)})")

print("Checking both original and mutated datasets...")
check_dataset('starcoder1_fim_python_completions', 'Original Dataset')
check_dataset('starcoder1_fim_python_vars_mutation_full', 'Mutated Dataset')