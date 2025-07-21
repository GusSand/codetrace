import datasets
from pathlib import Path

def check_fim_completions():
    print(f"Loading dataset from 'starcoder1_fim_completions'...")
    try:
        ds = datasets.load_from_disk('starcoder1_fim_completions')
        
        print(f"Dataset size: {len(ds)}")
        print(f"Column names: {ds.column_names}")
        
        # Print first few examples
        print("\nExamining first 3 examples:")
        for i in range(min(3, len(ds))):
            example = ds[i]
            print(f"\nExample {i+1}:")
            for key in ds.column_names:
                value = str(example[key])
                print(f"{key}: {value[:100]}{'...' if len(value) > 100 else ''}")
            
            # Check if this is type inference
            if 'fim_type' in ds.column_names and 'generated_text' in ds.column_names:
                print("\nType Inference Check:")
                print(f"Expected Type: {example.get('fim_type', 'N/A')}")
                print(f"Generated Type: {example.get('generated_text', 'N/A')}")
                print(f"Correct: {example.get('correct', 'N/A')}")
        
        return True
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return False

if __name__ == "__main__":
    check_fim_completions() 