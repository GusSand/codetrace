#!/usr/bin/env python3
import sys
import os
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from functools import partial
import itertools as it
from typing import List, Dict, Any, Callable
import datasets
from pathlib import Path

# Add the parent directory to the path so we can import from codetrace
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codetrace.parsing_utils import STARCODER_FIM, fim_placeholder, prepare_fim_prompt, get_model_fim
from codetrace.steering import prepare_prompt_pairs, subtract_avg

def modified_tokenize(tokenizer, fim_obj, prompt: str) -> str:
    """Modified tokenize method that handles prompts without placeholders."""
    try:
        # If the prompt has a placeholder, use the standard prepare_fim_prompt
        if fim_obj.placeholder in prompt and not fim_obj._is_fim(prompt):
            return prepare_fim_prompt(tokenizer, fim_obj, prompt)
        # If the prompt is already in FIM format, return it as is
        elif fim_obj._is_fim(prompt):
            return prompt
        # If the prompt doesn't have a placeholder, just return it as is
        else:
            return prompt
    except Exception as e:
        print(f"Error in modified_tokenize: {e}")
        return prompt

def modified_prepare_prompt_pairs(data: List[Dict[str, Any]], format_fn: Callable[[str], str]) -> List[str]:
    """Modified prepare_prompt_pairs that handles prompts without placeholders."""
    result = []
    for x in data:
        # Process fim_program
        fim_program_formatted = format_fn(x["fim_program"])
        result.append(fim_program_formatted)
        
        # Process mutated_program
        mutated_program_formatted = format_fn(x["mutated_program"])
        result.append(mutated_program_formatted)
    
    return result

# Create a simple wrapper class for the model
class SimpleModelWrapper:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
        self.config = model.config
        self.config.name_or_path = "bigcode/starcoderbase-1b"

def main():
    # Load the security examples
    with open("security/security_steering_examples.json", "r") as f:
        examples = json.load(f)
    
    # Initialize tokenizer and model
    model_name = "bigcode/starcoderbase-1b"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model_hf = AutoModelForCausalLM.from_pretrained(model_name)
    
    # Create a simple wrapper for the model
    model = SimpleModelWrapper(model_hf, tokenizer)
    
    # Create a dataset from the examples
    dataset = datasets.Dataset.from_list(examples)
    
    # Add the _original_program field
    dataset = dataset.map(
        lambda x: {"_original_program": x["fim_program"].replace("<FILL>", x["fim_type"])},
        desc="Adding column for original unfimmed program"
    )
    
    # Split the dataset into steer and test splits
    steer_size = len(dataset) // 2
    test_size = len(dataset) - steer_size
    
    indices = list(range(len(dataset)))
    steer_indices = indices[:steer_size]
    test_indices = indices[steer_size:]
    
    steer_split = dataset.select(steer_indices)
    test_split = dataset.select(test_indices)
    
    print(f"Steer split size: {len(steer_split)}")
    print(f"Test split size: {len(test_split)}")
    
    # Create the steering tensor
    print("Preparing prompt pairs for steering tensor creation")
    
    # Create a format function that mimics the tokenize method
    format_fn = partial(modified_tokenize, tokenizer, STARCODER_FIM)
    
    dataloader = torch.utils.data.DataLoader(
        steer_split,
        batch_size=2,
        collate_fn=partial(modified_prepare_prompt_pairs, format_fn=format_fn)
    )
    
    # Debug: print the first batch of prompts
    for batch in dataloader:
        print(f"Batch size: {len(batch)}")
        print(f"First prompt in batch: {batch[0][:100]}...")
        print(f"Second prompt in batch: {batch[1][:100]}...")
        break
    
    # Create a simple token mask function
    def token_mask_fn(hidden_states, tokens):
        # Just return the last token
        return hidden_states[:, -1]
    
    # Import batched_get_averages here to avoid circular imports
    from codetrace.batched_utils import batched_get_averages
    
    print("Creating steering tensor with batched_get_averages")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Move the model to the device
    model.model.to(device)
    
    steering_tensor = batched_get_averages(
        model.model,
        dataloader,
        batch_size=2,
        target_fn=token_mask_fn,
        reduction="sum",
        layers=[10]
    )
    
    # Check if the steering tensor is empty
    for layer in [10]:
        if steering_tensor[layer].sum() == 0:
            print(f"Warning: Steering tensor is empty for layer {layer}")
    
    # Save the steering tensor
    output_dir = Path("security_steering_results")
    os.makedirs(output_dir, exist_ok=True)
    
    torch.save(steering_tensor, output_dir / "security_tensor.pt")
    
    print("Done!")

if __name__ == "__main__":
    main() 