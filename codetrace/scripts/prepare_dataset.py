import json
from pathlib import Path
import datasets
import re

def extract_fim_type(prompt: str) -> str:
    # Extract FIM type based on the order of fim tags
    tags = re.findall(r'<fim_(prefix|suffix|middle)>', prompt)
    if not tags:
        return None
    return tags[0]  # Return the first FIM tag type found

def prepare_dataset(input_jsonl: str, output_path: str, test_size: float = 0.2):
    # Read JSONL file
    data = []
    with open(input_jsonl, 'r') as f:
        for line in f:
            item = json.loads(line)
            # Extract FIM type from the prompt
            fim_type = extract_fim_type(item['prompt'])
            
            # Create dataset entry with properly formatted FIM prompt
            entry = {
                'fim_type': fim_type,
                'fim_program': item['prompt'],  # This should already be in the correct format
                'canonical_solution': item['canonical_solution'],
                'name': item['name'],
                'language': item['language']
            }
            data.append(entry)
    
    # Create dataset
    ds = datasets.Dataset.from_list(data)
    
    # Split into train/test
    splits = ds.train_test_split(test_size=test_size, seed=42)
    
    # Save train and test splits separately
    train_path = output_path + "_train"
    test_path = output_path + "_test"
    
    splits['train'].save_to_disk(str(train_path))
    splits['test'].save_to_disk(str(test_path))
    
    print(f"Train dataset ({len(splits['train'])} examples) saved to {train_path}")
    print(f"Test dataset ({len(splits['test'])} examples) saved to {test_path}")
    print(f"First example fim_type: {splits['train'][0]['fim_type']}")
    print(f"First example program: {splits['train'][0]['fim_program']}")

if __name__ == "__main__":
    input_jsonl = "starcoder1_fim_task.jsonl"
    output_path = "starcoder1_fim_dataset"
    prepare_dataset(input_jsonl, output_path) 