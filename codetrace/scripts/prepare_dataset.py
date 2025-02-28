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

def prepare_dataset(input_jsonl: str, output_path: str):
    # Read JSONL file
    data = []
    with open(input_jsonl, 'r') as f:
        for line in f:
            item = json.loads(line)
            # Extract FIM type from the prompt
            fim_type = extract_fim_type(item['prompt'])
            
            # Create dataset entry
            entry = {
                'fim_type': fim_type,
                'fim_program': item['prompt'],
                'canonical_solution': item['canonical_solution'],
                'name': item['name'],
                'language': item['language']
            }
            data.append(entry)
    
    # Create dataset
    ds = datasets.Dataset.from_list(data)
    
    # Save dataset
    ds.save_to_disk(output_path)
    print(f"Dataset saved to {output_path}")
    print(f"First example fim_type: {ds[0]['fim_type']}")
    print(f"Total examples: {len(ds)}")

if __name__ == "__main__":
    input_jsonl = "starcoder1_fim_task.jsonl"
    output_path = "starcoder1_fim_dataset"
    prepare_dataset(input_jsonl, output_path) 