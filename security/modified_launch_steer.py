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
from argparse import ArgumentParser

# Add the parent directory to the path so we can import from codetrace
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codetrace.parsing_utils import STARCODER_FIM, fim_placeholder, prepare_fim_prompt, get_model_fim
from codetrace.steering import prepare_prompt_pairs, subtract_avg, SteeringManager

# Monkey patch the prepare_prompt_pairs function to handle prompts without placeholders
def modified_prepare_prompt_pairs(data: List[Dict[str, Any]], format_fn: Callable[[str], str]) -> List[str]:
    """Modified prepare_prompt_pairs that handles prompts without placeholders."""
    result = []
    for x in data:
        # Process fim_program
        try:
            fim_program_formatted = format_fn(x["fim_program"])
            result.append(fim_program_formatted)
        except Exception as e:
            print(f"Error formatting fim_program: {e}")
            # If there's an error, just use the original text
            result.append(x["fim_program"])
        
        # Process mutated_program
        try:
            # For mutated_program, we'll just use it as is since it doesn't have a placeholder
            result.append(x["mutated_program"])
        except Exception as e:
            print(f"Error formatting mutated_program: {e}")
            result.append(x["mutated_program"])
    
    return result

# Monkey patch the SteeringManager.tokenize method to handle prompts without placeholders
original_tokenize = SteeringManager.tokenize

def modified_tokenize(self, prompt: str) -> str:
    """Modified tokenize method that handles prompts without placeholders."""
    try:
        # If the prompt has a placeholder, use the standard prepare_fim_prompt
        if self.fim_obj.placeholder in prompt and not self.fim_obj._is_fim(prompt):
            return prepare_fim_prompt(self.tokenizer, self.fim_obj, prompt)
        # If the prompt is already in FIM format, return it as is
        elif self.fim_obj._is_fim(prompt):
            return prompt
        # If the prompt doesn't have a placeholder, just return it as is
        else:
            return prompt
    except Exception as e:
        print(f"Error in modified_tokenize: {e}")
        return prompt

# Add the missing _check_for_field method
def _check_for_field(self, examples, field):
    """Check if a field exists in the examples dataset."""
    if field is None:
        return False
    return field in examples.features

# Add the missing _compute_patch_field method
def _compute_patch_field(self, field):
    """Compute the patch field name."""
    return f"patch_{field}"

# Modify the steer_test_splits method to explicitly update self.splits
original_steer_test_splits = SteeringManager.steer_test_splits

def modified_steer_test_splits(self, test_size=100, dedup_prog_threshold=25, dedup_type_threshold=4, shuffle=True, seed=42, separate_by_column="fim_type"):
    """Modified steer_test_splits method that explicitly updates self.splits."""
    steer_split, test_split = original_steer_test_splits(self, test_size, dedup_prog_threshold, dedup_type_threshold, shuffle, seed, separate_by_column)
    
    # Explicitly update the splits dictionary
    self.splits = {
        "steer": steer_split,
        "test": test_split
    }
    
    print(f"Updated self.splits with keys: {list(self.splits.keys())}")
    
    return steer_split, test_split

# Apply the monkey patches
SteeringManager.tokenize = modified_tokenize
SteeringManager._check_for_field = _check_for_field
SteeringManager._compute_patch_field = _compute_patch_field
SteeringManager.steer_test_splits = modified_steer_test_splits

# Add the splits attribute to SteeringManager
original_init = SteeringManager.__init__

def modified_init(self, *args, **kwargs):
    original_init(self, *args, **kwargs)
    self.splits = {}
    self.steering_field = "fim_type"
    if self.steer_split is not None:
        self.splits["steer"] = self.steer_split
    if self.test_split is not None:
        self.splits["test"] = self.test_split

SteeringManager.__init__ = modified_init

from codetrace.steering import prepare_prompt_pairs as original_prepare_prompt_pairs
import codetrace.steering
codetrace.steering.prepare_prompt_pairs = modified_prepare_prompt_pairs

# Now import the rest of the modules
from codetrace.scripts.launch_steer import main, run_steer, print_color, none_or_str

if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("--model",type=str, required=True)
    parser.add_argument("--candidates", type=none_or_str, required=True)
    parser.add_argument("--output-dir", type=str, required=True)
    parser.add_argument("--layers", type=str, required=True)
    # dataset
    parser.add_argument("--split", type=str, default=None)
    parser.add_argument("--subset", type=str, default=None)
    parser.add_argument("--dedup-prog-threshold", type=int, default=25)
    parser.add_argument("--dedup-type-threshold", type=int, default=4)
    # naming
    parser.add_argument("--steer-name", required=True)
    parser.add_argument("--test-name", required=True)
    parser.add_argument("--tensor-name", required=True)
    parser.add_argument("--steering-field", type=str, default=None)

    parser.add_argument("-b1","--collect-batchsize", type=int, default=4)
    parser.add_argument("-b2","--patch-batchsize",type=int, default=2)
    parser.add_argument("--dtype", choices=["bfloat16","float32"],default="bfloat16")
    parser.add_argument("--max-num-candidates", type=int, default=-1)
    parser.add_argument("--test-size", type=int, default=100)
    parser.add_argument("--run-steering-splits", type=str, default="steer,test,rand")
    
    args = vars(parser.parse_args())
    
    # Convert layers string to list
    args["layers"] = [int(l) for l in args["layers"].split(",")]
    
    # Convert run_steering_splits string to list
    args["run_steering_splits"] = args["run_steering_splits"].split(",")
    
    print("Running modified launch_steer.py with monkey-patched functions to handle prompts without placeholders")
    main(**args) 