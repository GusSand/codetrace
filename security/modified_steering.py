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
from nnsight import LanguageModel
from codetrace.batched_utils import batched_get_averages

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

def modified_prepare_prompt_pairs(data, format_fn):
    """
    Prepare prompt pairs from the data using the provided format function.
    """
    result = []
    for x in data:
        # Process prompt and secure_code
        formatted = format_fn(x)
        result.append(formatted)
    
    return result

# Create a simple wrapper class for the model
class SimpleModelWrapper:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
        self.config = model.config
        self.config.name_or_path = "bigcode/starcoderbase-7b"

def main():
    # Load security examples
    with open("security/simplified_security_examples.json", "r") as f:
        security_examples = json.load(f)
    
    # Flatten the examples into a list of prompt-completion pairs
    examples = []
    for category in security_examples.values():
        for example in category:
            examples.append({
                "prompt": example["prompt"],
                "completion": example["secure_code"]
            })
    
    # Initialize model with proper device settings
    model_name = "bigcode/starcoderbase-7b"
    model = LanguageModel(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto",
        use_auth_token=True
    )
    
    # Create dataset from examples
    dataset = datasets.Dataset.from_list(examples)
    
    # Split into steer and test
    dataset = dataset.train_test_split(test_size=0.5, seed=42)
    steer_split = dataset["train"]
    test_split = dataset["test"]
    
    print(f"Steer split size: {len(steer_split)}")
    print(f"Test split size: {len(test_split)}")
    
    # Prepare prompt pairs
    print("Preparing prompt pairs for steering tensor creation")
    
    # Create a format function that combines prompt and completion
    def format_fn(x):
        return f"{x['prompt']}\n{x['completion']}"
    
    prompt_pairs = modified_prepare_prompt_pairs(steer_split, format_fn)
    
    # Create steering tensor
    print("Creating steering tensor with batched_get_averages")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # Tokenize and pad all prompts to the same length
    tokenizer = model.tokenizer
    encoded = tokenizer(prompt_pairs, padding=True, truncation=True, max_length=512, return_tensors="pt")
    padded_prompts = tokenizer.batch_decode(encoded["input_ids"])
    
    steering_tensor = batched_get_averages(
        model=model,
        prompts=padded_prompts,
        target_fn=lambda x: torch.ones_like(x),  # Use all tokens
        batch_size=1,
        layers=list(range(model.config.num_hidden_layers)),
        reduction=None
    )
    
    # Check if the steering tensor is empty
    for layer in range(model.config.num_hidden_layers):
        if steering_tensor[layer].sum() == 0:
            print(f"Warning: Steering tensor is empty for layer {layer}")
    
    # Save the steering tensor
    output_dir = Path("security_steering_results")
    os.makedirs(output_dir, exist_ok=True)
    
    torch.save(steering_tensor, output_dir / "security_tensor.pt")
    
    print("Done!")

if __name__ == "__main__":
    main() 