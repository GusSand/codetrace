import datasets
from codetrace.py_mutator import PyMutator
import argparse
import random
import traceback
import logging
import os
import torch
from vllm import LLM, SamplingParams
from codetrace.parsing_utils import get_model_fim, prepare_fim_prompt
from transformers import AutoTokenizer
from tqdm import tqdm
import json
from pathlib import Path

# Set up logger
logger = logging.getLogger("mutation_robustness")

def setup_logging(verbose_level):
    """Configure logging based on verbosity level."""
    log_level = logging.WARNING
    if verbose_level == 1:
        log_level = logging.INFO
    elif verbose_level >= 2:
        log_level = logging.DEBUG
    
    # Configure with timestamp for better tracking of long-running processes
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=log_level
    )
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Configure logger
    logger.setLevel(log_level)
    
    if verbose_level >= 2:
        logger.debug("Debug logging enabled")
    elif verbose_level == 1:
        logger.info("Info logging enabled")
    elif verbose_level == 0:
        logger.warning("Warning logging enabled (standard)")
    else:
        logger.warning("Quiet mode: only errors will be displayed")

def apply_mutation(mutator, program, fim_type):
    """Apply variable renaming mutation to a program"""
    try:
        if program is None:
            logger.warning("Program is None, skipping mutation")
            return None, "program_is_none"
            
        logger.debug(f"Program starts with: {program[:50]}...")
        logger.debug(f"FIM type: {fim_type}")
        
        # Apply only variable renaming
        mutated_program = mutator.random_mutate(program, fim_type, ["rename_vars"])
        
        if mutated_program is None:
            logger.warning("Mutation returned None, using original program")
            return program, "mutation_returned_none"
            
        if mutated_program == program:
            logger.warning("Mutation produced identical program")
            return program, "identical_program"
            
        return mutated_program, None
    except Exception as e:
        logger.error(f"Error applying mutation: {str(e)}")
        logger.debug(f"Traceback: {traceback.format_exc()}")
        return None, f"mutation_error: {str(e)}"

def extract_completion_type(completion: str) -> str:
    """Extract the type from a completion."""
    if not completion:
        return None
    # The completion should be just the type, but let's clean it up
    return completion.strip()

def get_completion(llm, prompt, tokenizer, model_fim):
    """Get a completion from the LLM for a given prompt and extract its fim_type"""
    try:
        # Format the prompt for FIM if needed
        if not "<fim_middle>" in prompt:
            formatted_prompt = prepare_fim_prompt(tokenizer, model_fim, prompt)
        else:
            formatted_prompt = prompt
            
        # Generate completion
        sampling_params = SamplingParams(temperature=0, max_tokens=10)
        outputs = llm.generate([formatted_prompt], sampling_params)
        
        if not outputs or not outputs[0].outputs:
            logger.warning("No output generated")
            return None, False, "no_output_generated", None
            
        generated_text = outputs[0].outputs[0].text
        
        # Check if the completion is valid (non-empty)
        is_valid = len(generated_text.strip()) > 0
        failure_reason = "empty_completion" if not is_valid else None
        
        # Extract fim_type from completion
        completion_fim_type = extract_completion_type(generated_text)
            
        return generated_text, is_valid, failure_reason, completion_fim_type
    except Exception as e:
        logger.error(f"Error getting completion: {str(e)}")
        logger.debug(f"Traceback: {traceback.format_exc()}")
        return None, False, f"completion_error: {str(e)}", None

def save_results(results, output_path, message=""):
    """Save results to a file"""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        if message:
            logger.info(message)
    except Exception as e:
        logger.error(f"Error saving results: {str(e)}")
        logger.debug(f"Traceback: {traceback.format_exc()}")

def main():
    parser = argparse.ArgumentParser(description="Test robustness of LLM completions against variable renaming mutations")
    parser.add_argument("--input-path", type=str, required=True, help="Path to the input dataset")
    parser.add_argument("--output-path", type=str, required=True, help="Path to save the results")
    parser.add_argument("--model", type=str, required=True, help="Model to use for completions")
    parser.add_argument("--num-samples", type=int, default=1000, help="Number of samples to test")
    parser.add_argument("--max-mutations", type=int, default=10, help="Maximum number of mutations to apply")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--batch-size", type=int, default=1, help="Batch size for completions")
    parser.add_argument("--dtype", choices=["bfloat16", "float16", "float32"], default="float16", help="Data type for model")
    parser.add_argument("--save-frequency", type=int, default=5, help="How often to save results (every N examples)")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase output verbosity")
    args = parser.parse_args()
    
    # Set up logging
    setup_logging(args.verbose)
    
    # Set random seed
    random.seed(args.seed)
    
    # Load dataset
    logger.info(f"Loading dataset from {args.input_path}...")
    ds = datasets.load_from_disk(args.input_path)
    
    logger.info(f"Dataset has {len(ds)} examples with columns: {ds.column_names}")
    
    # Select successful examples (those with 'correct' field set to True)
    if 'correct' in ds.column_names:
        successful_ds = ds.filter(lambda x: x['correct'] == True)
        logger.info(f"Found {len(successful_ds)} successful examples")
    else:
        logger.warning("No 'correct' field found in dataset, using all examples")
        successful_ds = ds
    
    # Select a random subset of examples
    if len(successful_ds) > args.num_samples:
        indices = random.sample(range(len(successful_ds)), args.num_samples)
        test_ds = successful_ds.select(indices)
        logger.info(f"Selected {len(test_ds)} random examples for testing")
    else:
        test_ds = successful_ds
        logger.info(f"Using all {len(test_ds)} examples for testing")
    
    # Initialize tokenizer and model
    logger.info(f"Initializing tokenizer and model {args.model}...")
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    model_fim = get_model_fim(args.model)
    
    # Initialize LLM
    logger.info("Initializing LLM...")
    dtype_map = {
        "bfloat16": torch.bfloat16,
        "float16": torch.float16,
        "float32": torch.float32
    }
    llm = LLM(model=args.model, dtype=dtype_map[args.dtype], trust_remote_code=True)
    
    # Initialize mutator
    mutator = PyMutator()
    
    # Results storage
    results = []
    
    # Check if results file already exists and load it if it does
    if os.path.exists(args.output_path):
        try:
            with open(args.output_path, 'r') as f:
                results = json.load(f)
            logger.info(f"Loaded {len(results)} existing results from {args.output_path}")
            
            # Get the IDs of examples that have already been processed
            processed_ids = set(r["example_id"] for r in results)
        except Exception as e:
            logger.error(f"Error loading existing results: {str(e)}")
            results = []
            processed_ids = set()
    else:
        processed_ids = set()
    
    # Process each example
    for i, example in enumerate(tqdm(test_ds, desc="Testing examples", ncols=100)):
        # Skip if already processed
        if i in processed_ids:
            logger.info(f"Skipping example {i} (already processed)")
            continue
            
        logger.info(f"\nProcessing example {i+1}/{len(test_ds)}")
        logger.info(f"FIM type: {example['fim_type']}")
        
        # Extract program and type
        if "fim_program" not in example or example["fim_program"] is None:
            logger.warning(f"Example {i} missing fim_program field or it's None, skipping")
            continue
            
        program = example["fim_program"]
        fim_type = example["fim_type"]
        
        # Get the original prompt
        if "_prompt" in example:
            original_prompt = example["_prompt"]
        else:
            # Format the prompt for FIM
            original_prompt = prepare_fim_prompt(tokenizer, model_fim, program)
        
        # Test the original program first
        logger.debug("Testing original program...")
        original_completion, original_success, original_failure, original_completion_type = get_completion(llm, original_prompt, tokenizer, model_fim)
        
        if not original_success:
            logger.warning("Original program failed to generate a valid completion, skipping")
            continue
            
        # Initialize result record
        result_record = {
            "example_id": i,
            "fim_type": fim_type,  # This is the expected type
            "original_success": original_success,
            "original_completion": original_completion,
            "original_completion_type": original_completion_type,
            "mutations": [],  # Will store only mutations that produce different fim_types
            "failed_mutations": [],  # Track which mutations produced different fim_types
            "total_mutations_attempted": 0,
            "total_mutations_succeeded": 0,
            # Add FIM-related fields from input dataset
            "key": example["key"],
            "prefix": example["prefix"],
            "suffix": example["suffix"],
            "middle": example["middle"],
            "fim_program": program,
            "hexsha": example.get("hexsha", ""),
            "_generated": example.get("_generated", ""),
            "generated_text": example.get("generated_text", ""),
            "model_name": example.get("model_name", "")
        }
        
        # Apply mutations and test completions
        current_program = program
        mutation_count = 0
        
        # Continue applying mutations until we reach the maximum
        while mutation_count < args.max_mutations:
            # Apply mutation
            logger.debug(f"Applying mutation {mutation_count+1}...")
            mutated_program, mutation_failure = apply_mutation(mutator, current_program, fim_type)
            
            if mutation_failure:
                logger.debug(f"Mutation failed: {mutation_failure}")
                result_record["total_mutations_attempted"] += 1
                mutation_count += 1
                continue
                
            # Format the mutated program for FIM
            mutated_prompt = prepare_fim_prompt(tokenizer, model_fim, mutated_program)
            
            # Get completion
            logger.debug("Getting completion for mutated program...")
            mutated_completion, mutated_success, completion_failure, completion_fim_type = get_completion(llm, mutated_prompt, tokenizer, model_fim)
            
            result_record["total_mutations_attempted"] += 1
            
            if mutated_success:
                result_record["total_mutations_succeeded"] += 1
                
                # Check if the completion's fim_type matches the expected type
                if completion_fim_type != fim_type:
                    # Found a type mismatch - this is what we're looking for!
                    mutation_record = {
                        "mutation_number": mutation_count + 1,
                        "success": True,
                        "completion": mutated_completion,
                        "completion_fim_type": completion_fim_type,
                        "expected_fim_type": fim_type,
                        "original_code": program,
                        "mutated_code": mutated_program,
                        "fim_type": fim_type,
                        "prefix": example["prefix"],
                        "suffix": example["suffix"],
                        "middle": example["middle"],
                        "fim_program": mutated_program,
                        "prompt": mutated_prompt
                    }
                    result_record["mutations"] = [mutation_record]  # Save only this type-mismatched mutation
                    result_record["failed_mutations"].append(mutation_count + 1)
                    logger.info(f"Mutation {mutation_count + 1} produced different fim_type: expected {fim_type}, got {completion_fim_type}")
                    break
            
            # Update for next iteration
            current_program = mutated_program
            mutation_count += 1
        
        # Add result to results list only if we found a type mismatch
        if result_record["mutations"]:
            results.append(result_record)
        
        # Save results periodically
        if (i + 1) % args.save_frequency == 0 or i == len(test_ds) - 1:
            save_results(results, args.output_path, f"Saving results after {i+1} examples...")
    
    # Final save
    save_results(results, args.output_path, f"Saving final results to {args.output_path}...")
    
    # Calculate statistics
    if results:
        total_examples = len(test_ds)
        type_mismatches = len(results)
        
        logger.info(f"Total examples tested: {total_examples}")
        logger.info(f"Examples with type mismatches: {type_mismatches} ({type_mismatches/total_examples*100:.2f}%)")
        
        # Calculate average number of mutations before type mismatch
        mutations_before_mismatch = [min(r["failed_mutations"]) for r in results if r["failed_mutations"]]
        
        if mutations_before_mismatch:
            avg_mutations = sum(mutations_before_mismatch) / len(mutations_before_mismatch)
            logger.info(f"Average number of mutations before type mismatch: {avg_mutations:.2f}")
    else:
        logger.warning("No type mismatches found in any examples")

if __name__ == "__main__":
    main()
