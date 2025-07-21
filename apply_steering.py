#!/usr/bin/env python3
import argparse
import json
import os
import torch
import time
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer
import datasets
from datetime import datetime

def log_info(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def main():
    parser = argparse.ArgumentParser(description="Apply steering vectors to specific model layers")
    parser.add_argument("--candidates-file", type=str, required=True,
                        help="Path to steering candidates JSON file")
    parser.add_argument("--output-dir", type=str, required=True,
                        help="Directory to save steering results")
    parser.add_argument("--model", type=str, default="bigcode/starcoderbase-1b",
                        help="Model to use for steering")
    parser.add_argument("--layers", type=str, default="10,11,12,13,14",
                        help="Comma-separated list of layers to apply steering")
    parser.add_argument("--batch-size", type=int, default=32,
                        help="Batch size for processing (default: 32 for A100 80GB)")
    parser.add_argument("--test-size", type=int, default=20,
                        help="Number of examples to use for testing")
    parser.add_argument("--max-length", type=int, default=512,
                        help="Maximum sequence length for tokenization")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed for reproducibility")
    args = parser.parse_args()
    
    # Set random seed
    torch.manual_seed(args.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)
    
    # Parse layers
    layers = [int(l.strip()) for l in args.layers.split(',')]
    print(f"Will apply steering to layers: {layers}")
    
    # Load candidates
    log_info(f"Loading steering candidates from {args.candidates_file}")
    with open(args.candidates_file, 'r') as f:
        candidates = json.load(f)
    log_info(f"Loaded {len(candidates)} candidates")
    
    # Convert candidates to dataset
    candidates_ds = datasets.Dataset.from_list(candidates)
    
    # Initialize model and tokenizer
    log_info(f"Initializing model {args.model}")
    start_time = time.time()
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        device_map="auto",
        torch_dtype=torch.float16,
        trust_remote_code=True
    )
    tokenizer = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)
    log_info(f"Model loaded in {time.time() - start_time:.2f} seconds")
    
    # Set up padding token
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        model.config.pad_token_id = tokenizer.eos_token_id
        log_info("Set up padding token using EOS token")
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Split dataset for steering and testing
    log_info("Creating dataset splits...")
    dataset = candidates_ds.shuffle(seed=args.seed)
    test_ds = dataset.select(range(min(args.test_size, len(dataset))))
    steer_ds = dataset.select(range(args.test_size, len(dataset)))
    
    log_info(f"Created splits - Steering: {len(steer_ds)} examples, Test: {len(test_ds)} examples")
    
    # Save splits for reference
    test_ds.to_json(os.path.join(args.output_dir, "test_split.json"))
    steer_ds.to_json(os.path.join(args.output_dir, "steer_split.json"))
    log_info("Saved dataset splits to disk")
    
    # Process test examples
    log_info("\nProcessing test examples...")
    results = []
    total_start_time = time.time()
    
    for i in range(0, len(test_ds), args.batch_size):
        batch_start_time = time.time()
        batch = test_ds.select(range(i, min(i + args.batch_size, len(test_ds))))
        current_batch_size = len(batch)
        
        log_info(f"Processing batch {i//args.batch_size + 1} ({current_batch_size} examples)")
        
        # Process original programs
        log_info("  Tokenizing original programs...")
        inputs_original = tokenizer(
            [ex["original_program"] for ex in batch],
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=args.max_length
        ).to(model.device)
        
        log_info("  Running inference on original programs...")
        with torch.no_grad():
            outputs_original = model(**inputs_original)
            outputs_original = outputs_original.logits.detach().cpu()
            torch.cuda.empty_cache()
            
        # Process mutated programs
        log_info("  Tokenizing mutated programs...")
        inputs_mutated = tokenizer(
            [ex["mutated_program"] for ex in batch],
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=args.max_length
        ).to(model.device)
        
        log_info("  Running inference on mutated programs...")
        with torch.no_grad():
            outputs_mutated = model(**inputs_mutated)
            outputs_mutated = outputs_mutated.logits.detach().cpu()
            torch.cuda.empty_cache()
        
        # Store results
        log_info("  Storing results...")
        for j, example in enumerate(batch):
            result = {
                "index": example["index"],
                "original_program": example["original_program"],
                "mutated_program": example["mutated_program"],
                "expected_type": example["expected_type"],
                "original_logits": outputs_original[j].numpy().tolist(),
                "mutated_logits": outputs_mutated[j].numpy().tolist(),
            }
            results.append(result)
            
            # Save results after each example in case of crashes
            if (len(results) % 5) == 0:  # Save every 5 examples
                results_file = os.path.join(args.output_dir, "steering_results_partial.json")
                with open(results_file, 'w') as f:
                    json.dump(results, f, indent=2)
                log_info(f"  Saved partial results ({len(results)} examples processed)")
        
        batch_time = time.time() - batch_start_time
        examples_per_second = current_batch_size / batch_time
        log_info(f"Processed batch in {batch_time:.2f}s ({examples_per_second:.2f} examples/s)")
        log_info(f"Progress: {min(i + args.batch_size, len(test_ds))}/{len(test_ds)} examples")
        
        # Show memory usage
        if torch.cuda.is_available():
            gpu_memory = torch.cuda.max_memory_allocated() / 1024**3
            log_info(f"GPU Memory used: {gpu_memory:.2f} GB")
    
    total_time = time.time() - total_start_time
    log_info(f"\nTotal processing time: {total_time:.2f}s")
    log_info(f"Average speed: {len(test_ds)/total_time:.2f} examples/s")
    
    # Save final results
    results_file = os.path.join(args.output_dir, "steering_results.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    log_info(f"Final results saved to {results_file}")

if __name__ == "__main__":
    main() 