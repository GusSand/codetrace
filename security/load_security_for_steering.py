#!/usr/bin/env python3
import json
import os
import datasets
from typing import Optional, Dict, Any, List, Tuple
import numpy as np

def load_security_examples(file_path: str = "security_steering_examples.json", split: Optional[str] = None) -> datasets.Dataset:
    """
    Load security examples from the JSON file and convert to a dataset format
    compatible with the steering pipeline.
    
    Args:
        file_path: Path to the security examples JSON file
        split: Optional split name to filter examples (not used currently)
        
    Returns:
        A Hugging Face dataset containing the security examples
    """
    # Load examples from file
    with open(file_path, "r") as f:
        examples = json.load(f)
    
    # Convert to a Hugging Face dataset
    ds = datasets.Dataset.from_list(examples)
    
    # Add any required fields that might be missing
    # The steering manager expects _original_program field for deduplication
    if "_original_program" not in ds.features:
        ds = ds.map(lambda example: {"_original_program": example["idx"]})
    
    print(f"Loaded {len(ds)} security examples from {file_path}")
    print(f"Features: {list(ds.features.keys())}")
    
    return ds

def split_security_examples(
    ds: datasets.Dataset, 
    test_size: float = 0.5,
    seed: int = 42
) -> Tuple[datasets.Dataset, datasets.Dataset]:
    """
    Split the security examples into steer and test splits.
    
    Args:
        ds: Dataset containing security examples
        test_size: Fraction of examples to use for testing
        seed: Random seed for reproducibility
        
    Returns:
        Tuple of (steer_split, test_split)
    """
    # Create a train-test split
    splits = ds.train_test_split(test_size=test_size, seed=seed)
    steer_split = splits["train"]
    test_split = splits["test"]
    
    print(f"Split {len(ds)} examples into {len(steer_split)} for steering and {len(test_split)} for testing")
    
    return steer_split, test_split

if __name__ == "__main__":
    # Load the security examples
    ds = load_security_examples()
    
    # Split into steer and test sets
    steer_split, test_split = split_security_examples(ds)
    
    # Save the splits (optional)
    steer_split.to_json("security_steer_split.json")
    test_split.to_json("security_test_split.json")
    
    print("Security examples prepared for steering pipeline.") 