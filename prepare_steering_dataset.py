#!/usr/bin/env python3
"""
Script to prepare the nuprl-staging/py_typeinf_fim dataset for use with mutate_dataset.py and launch_steer.py.
"""

import os
import argparse
from pathlib import Path
import subprocess
from datasets import load_dataset

def main():
    parser = argparse.ArgumentParser(description="Prepare dataset for steering")
    parser.add_argument("--output-dir", type=str, default="data/steering_data",
                        help="Directory to save the prepared datasets")
    parser.add_argument("--model", type=str, default="bigcode/starcoderbase-1b",
                        help="Model to use for mutations")
    parser.add_argument("--batch-size", type=int, default=100,
                        help="Batch size for mutations")
    parser.add_argument("--max-candidates", type=int, default=3500,
                        help="Maximum number of candidates to generate")
    parser.add_argument("--mutations", type=str, default="types,vars,delete",
                        help="Comma-separated list of mutations to apply")
    parser.add_argument("--overwrite", action="store_true",
                        help="Overwrite existing datasets")
    args = parser.parse_args()

    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Paths for the datasets
    original_ds_path = os.path.join(args.output_dir, "original_dataset")
    mutated_ds_path = os.path.join(args.output_dir, "mutated_dataset")
    
    # Step 1: Download and save the original dataset
    if not os.path.exists(original_ds_path) or args.overwrite:
        print(f"Downloading and saving the nuprl-staging/py_typeinf_fim dataset to {original_ds_path}...")
        ds = load_dataset("nuprl-staging/py_typeinf_fim", split="train")
        
        # Add typechecks column (required by SteeringManager)
        ds = ds.add_column("typechecks", [True] * len(ds))
        
        # Save to disk
        ds.save_to_disk(original_ds_path)
        print(f"Dataset saved to {original_ds_path}")
    else:
        print(f"Using existing dataset at {original_ds_path}")
    
    # Step 2: Run mutate_dataset.py to create mutated programs
    if not os.path.exists(mutated_ds_path) or args.overwrite:
        print(f"Creating mutated programs using mutate_dataset.py...")
        
        # Set environment variable for vllm
        os.environ["VLLM_LOGGING_LEVEL"] = "ERROR"
        
        # Run the mutate_dataset.py script
        cmd = [
            "python", "codetrace/scripts/mutate_dataset.py",
            "--completions-ds", original_ds_path,
            "--mutated-ds", mutated_ds_path,
            "--model", args.model,
            "--lang", "py",
            "--mutations", args.mutations,
            "--batch-size", str(args.batch_size),
            "--max-num-candidates", str(args.max_candidates)
        ]
        
        if args.overwrite:
            cmd.append("--overwrite")
        
        print(f"Running command: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
        print(f"Mutated dataset created at {mutated_ds_path}")
    else:
        print(f"Using existing mutated dataset at {mutated_ds_path}")
    
    # Step 3: Print instructions for using the dataset with launch_steer.py
    print("\nDataset preparation complete!")
    print("\nTo use this dataset with launch_steer.py, run:")
    print(f"""
    python codetrace/scripts/launch_steer.py \\
      --model "{args.model}" \\
      --candidates "{mutated_ds_path}" \\
      --output-dir "steering_results" \\
      --layers "10,11,12,13,14" \\
      --steer-name "type_steer" \\
      --test-name "type_test" \\
      --tensor-name "type_tensor" \\
      --collect-batchsize 4 \\
      --patch-batchsize 2 \\
      --max-num-candidates 1000 \\
      --test-size 100
    """)

if __name__ == "__main__":
    main() 