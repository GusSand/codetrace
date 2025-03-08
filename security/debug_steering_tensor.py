#!/usr/bin/env python3
import os
import sys
import json
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoModelForCausalLM, AutoTokenizer
import numpy as np
from tqdm import tqdm

# Add the parent directory to the path so we can import from codetrace
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from codetrace.batched_utils import batched_get_averages
from codetrace.interp_utils import collect_hidden_states

def prepare_prompt_pairs(data, format_fn=lambda x: x):
    """Prepare prompt pairs for steering tensor creation."""
    preprocess = lambda d: [format_fn(d["fim_program"]), format_fn(d["mutated_program"])]
    print(f"Preparing prompt pairs for {len(data)} examples")
    prompts = list(map(preprocess, data))
    flat_prompts = []
    for pair in prompts:
        flat_prompts.extend(pair)
    print(f"Created {len(flat_prompts)} prompts")
    return flat_prompts

def subtract_avg(hidden_states):
    """Subtract pairs of prompts at the prompt dimension."""
    print(f"Subtracting averages with hidden states shape: {hidden_states.shape}")
    # Get even and odd indices
    even_indices = torch.arange(0, hidden_states.shape[1], 2, device=hidden_states.device)
    odd_indices = torch.arange(1, hidden_states.shape[1], 2, device=hidden_states.device)
    print(f"Even indices: {even_indices}")
    print(f"Odd indices: {odd_indices}")
    
    # Subtract odd from even
    result = hidden_states[:, even_indices] - hidden_states[:, odd_indices]
    print(f"Result shape: {result.shape}")
    return result

def token_mask_fn(token_id, tokenizer):
    """Create a mask for a specific token."""
    return lambda tokens: tokens == tokenizer.encode(token_id, add_special_tokens=False)[0]

def pad_and_stack_tensors(tensors, pad_value=0):
    """Pad tensors to the same sequence length and stack them."""
    # Find the maximum sequence length
    max_seq_len = max(tensor.shape[2] for tensor in tensors)
    
    # Pad each tensor to the maximum sequence length
    padded_tensors = []
    for tensor in tensors:
        # tensor shape: [num_layers, batch_size, seq_len, hidden_dim]
        num_layers, batch_size, seq_len, hidden_dim = tensor.shape
        
        if seq_len < max_seq_len:
            # Create padding
            padding = torch.zeros(
                (num_layers, batch_size, max_seq_len - seq_len, hidden_dim),
                dtype=tensor.dtype,
                device=tensor.device
            )
            
            # Concatenate the tensor with padding
            padded_tensor = torch.cat([tensor, padding], dim=2)
            padded_tensors.append(padded_tensor)
        else:
            padded_tensors.append(tensor)
    
    # Stack the padded tensors
    return torch.stack(padded_tensors, dim=0)

class SecurityDataset(Dataset):
    def __init__(self, examples):
        self.examples = examples
    
    def __len__(self):
        return len(self.examples)
    
    def __getitem__(self, idx):
        return self.examples[idx]

def custom_collate_fn(batch):
    return batch

def main():
    # Load security examples
    with open("security_steering_examples.json", "r") as f:
        examples = json.load(f)
    
    print(f"Loaded {len(examples)} examples")
    
    # Initialize model and tokenizer
    model_name = "bigcode/starcoderbase-1b"
    print(f"Initializing model {model_name}")
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Create a list of prompts
    batch_size = 2
    all_prompts = []
    
    # Process examples in batches
    for i in range(0, len(examples), batch_size):
        batch = examples[i:i+batch_size]
        prompts = prepare_prompt_pairs(batch)
        all_prompts.extend(prompts)
    
    # Print first few prompts
    print(f"Total prompts: {len(all_prompts)}")
    print(f"First prompt: {all_prompts[0][:100]}...")
    print(f"Second prompt: {all_prompts[1][:100]}...")
    
    # Create steering tensor
    print("Creating steering tensor")
    
    # Custom average function to handle different sequence lengths
    def custom_average_fn(hidden_states_list):
        # Pad and stack the tensors
        padded_stacked = pad_and_stack_tensors(hidden_states_list)
        # Average across the first dimension (batch dimension)
        return torch.mean(padded_stacked, dim=0)
    
    # Collect activations and create steering tensor
    steering_tensor = batched_get_averages(
        model=model,
        prompts=all_prompts,
        target_fn=None,  # We'll handle the subtraction in average_fn
        batch_size=4,
        average_fn=subtract_avg,
        layers=[12],  # Only collect layer 12
    )
    
    # Print steering tensor info
    for layer, tensor in steering_tensor.items():
        print(f"Layer {layer} tensor shape: {tensor.shape}")
        print(f"Layer {layer} tensor sum: {tensor.sum()}")

if __name__ == "__main__":
    main() 