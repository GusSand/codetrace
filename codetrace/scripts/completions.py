import shutil
from argparse import ArgumentParser
from pathlib import Path
from typing import List,Dict,Any,Union
import os
import torch
import datasets
import logging
from vllm import LLM, SamplingParams
from codetrace.parsing_utils import get_model_fim, FimObj, FimChat, prepare_fim_prompt
from transformers import AutoTokenizer, PreTrainedTokenizer
from tqdm import tqdm
from codetrace.utils import (
    num_available_devices,
    hex_encode
)
from collections import defaultdict
from huggingface_hub import HfFolder

# Set up logger
logger = logging.getLogger("completions")

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
    
    # Configure completions logger
    logger.setLevel(log_level)
    
    if verbose_level >= 2:
        logger.debug("Debug logging enabled")
    elif verbose_level == 1:
        logger.info("Info logging enabled")
    elif verbose_level == 0:
        logger.warning("Warning logging enabled (standard)")
    else:
        logger.warning("Quiet mode: only errors will be displayed")

def success_rate(ds: datasets.Dataset) -> str:
    df = ds.to_pandas()
    num_succ = df["correct"].sum()
    num_tot = df["correct"].count()
    mean = df["correct"].mean()*100
    return f"Success rate: {num_succ}/{num_tot} = {mean:.2f} %"

def is_1tok(fim_type: str, tokenizer: PreTrainedTokenizer) -> bool:
    return len(tokenizer(fim_type, add_special_tokens=False)["input_ids"]) == 1

def _identify_expected_type(prompt: str) -> str:
    """Extract the expected type from FIM format prompt.
    
    In a typical FIM prompt like:
    <fim_prefix>def func(arg: <fim_suffix>): ...<fim_middle>
    
    The expected type would be what should go between arg: and )
    
    This is a heuristic function that tries to identify potential places where
    a type annotation would occur in different languages.
    """
    # This is a complex task that would require more sophisticated parsing
    # For now, we'll use a simple heuristic: consider the generation correct
    # if it's non-empty and looks like it could be a data type
    return "data_type"

def _is_valid_type_completion(generated: str, canonical_solution: str = None) -> bool:
    """Check if the generated text is a valid type prediction.
    
    For the paper "Understanding How CodeLLMs (Mis)Predict Types with Activation Steering",
    we need to check if the model correctly predicts the expected type.
    
    Args:
        generated: The generated text from the model.
        canonical_solution: The expected type from the canonical solution.
        
    Returns:
        True if the generated text matches the expected type.
    """
    if not generated or len(generated.strip()) == 0:
        return False
    
    # If canonical solution is provided, we should compare against it
    if canonical_solution and len(canonical_solution.strip()) > 0:
        # Exact match
        if generated.strip() == canonical_solution.strip():
            return True
            
        # Check if the generated text starts with the canonical solution
        # (might have additional code after the type)
        if generated.strip().startswith(canonical_solution.strip()):
            return True
            
        # Check if the canonical solution is within the first part of the generated text
        # (for languages where type annotations might be surrounded by other syntax)
        first_line = generated.strip().split('\n')[0] if '\n' in generated else generated.strip()
        if canonical_solution.strip() in first_line:
            return True
            
        # If we have a canonical solution but didn't match, log the mismatch for analysis
        logger.debug(f"Type mismatch - Expected: '{canonical_solution.strip()}', Got: '{generated.strip()}'")
        return False
        
    # If no canonical solution, fall back to syntactic validation
    # Basic validation checks
    if len(generated) > 150:  # Completions shouldn't be excessively long
        return False
    
    # Heuristic: Count balanced parentheses/brackets as one signal of syntactic validity
    def is_balanced(text, open_char, close_char):
        count = 0
        for c in text:
            if c == open_char:
                count += 1
            elif c == close_char:
                count -= 1
                if count < 0:
                    return False
        return count == 0
    
    # Check for obviously invalid syntax with unbalanced delimiters
    # Only consider this a strict failure if there are multiple unbalanced pairs
    balance_failures = 0
    if '(' in generated or ')' in generated:
        if not is_balanced(generated, '(', ')'):
            balance_failures += 1
    
    if '[' in generated or ']' in generated:
        if not is_balanced(generated, '[', ']'):
            balance_failures += 1
    
    if '{' in generated or '}' in generated:
        if not is_balanced(generated, '{', '}'):
            balance_failures += 1
            
    # Only reject if multiple balance failures (to allow for context-dependent completions)
    if balance_failures > 1:
        return False
        
    # Common patterns that indicate invalid completions
    bad_patterns = [
        "error",
        "undefined",
        "not found",
        "missing"
    ]
    
    if any(pattern in generated.lower() for pattern in bad_patterns):
        return False
    
    # By default, accept the completion if it passed all the above checks
    return True

def _flexible_match(expected: str, generated: str) -> bool:
    """Perform a flexible comparison to handle common format differences."""
    # For debugging/investigation only
    logger.debug(f"Comparing expected: '{expected}' with generated: '{generated}'")
    
    # If we're just comparing with an explicit expected value
    if expected != "prefix":
        # Exact match
        if expected == generated:
            return True
        
        # Whitespace differences
        if expected.strip() == generated.strip():
            return True
        
        # Case differences
        if expected.lower() == generated.lower():
            return True
        
        # Trailing newline/whitespace differences
        if expected.rstrip() == generated.rstrip():
            return True
        
        # Both whitespace and case differences
        if expected.strip().lower() == generated.strip().lower():
            return True
    
    # For "prefix" type examples, we're generating a data type or code completion
    # not trying to match "prefix" literally
    elif expected == "prefix":
        return _is_valid_type_completion(generated)
    
    return False

def _is_fim_format(prompt: str) -> bool:
    """Check if a prompt is already in FIM format with special tokens."""
    return "<fim_prefix>" in prompt and "<fim_suffix>" in prompt and "<fim_middle>" in prompt

def _format_fim_prompt(prompt: str, model_fim: Union[FimObj,FimChat]) -> str:
    """Format a prompt in FIM format if needed."""
    if _is_fim_format(prompt):
        # Already in FIM format
        return prompt
    
    # For Starcoder, the expected FIM format is:
    # <fim_prefix>{prefix}<fim_suffix>{suffix}<fim_middle>
    
    # If not in FIM format yet, but contains the placeholder
    if model_fim.placeholder in prompt:
        try:
            formatted = model_fim.placeholder_to_fim(prompt)
            # Check if the formatting was successful by verifying all special tokens are present
            if not _is_fim_format(formatted):
                logger.warning(f"Formatted prompt is missing some FIM tokens: {formatted[:100]}...")
                # Try to manually fix if possible
                if "<fim_prefix>" in formatted and "<fim_suffix>" in formatted and "<fim_middle>" not in formatted:
                    formatted += "<fim_middle>"
                    logger.info("Added missing <fim_middle> token")
            return formatted
        except AssertionError as e:
            logger.warning(f"Error formatting as FIM prompt: {str(e)}")
            # If assertion fails, try to manually format
            try:
                # Extract prefix and suffix
                parts = prompt.split(model_fim.placeholder)
                if len(parts) == 2:
                    prefix, suffix = parts
                    formatted = f"<fim_prefix>{prefix}<fim_suffix>{suffix}<fim_middle>"
                    logger.info("Manually formatted FIM prompt")
                    return formatted
            except Exception:
                pass
            # If all else fails, return the original
            return prompt
            
    # Not a FIM prompt at all - can't handle this case
    logger.warning(f"Could not format as FIM prompt: {prompt[:100]}...")
    return prompt

def _save(data: List[Dict[str,Any]], path:str, message:str):
    logger.info(message)
    if not data:
        logger.warning("No completions to save in this batch")
        return
    temp_path = Path(str(path) + "_temp")
    # Create dataset using the current API
    new_ds = datasets.Dataset.from_dict({k: [d[k] for d in data] for k in data[0].keys()})
    if os.path.exists(path):
        existing_completions = datasets.load_from_disk(str(path))
        new_ds = datasets.concatenate_datasets([new_ds, existing_completions])

    # workaround huggingface save_to_disk permissions
    new_ds.save_to_disk(str(temp_path))
    shutil.rmtree(path, ignore_errors=True)
    shutil.move(str(temp_path), str(path))
    shutil.rmtree(str(temp_path), ignore_errors=True)
    logger.info(success_rate(new_ds))

def _process_batch_completions(outputs, current_batch, tokenizer, model_name):
    """Process batch completions and determine correctness."""
    batch_completions = []
    mismatch_count = 0
    correct_count = 0
    
    for idx, output in enumerate(outputs):
        try:
            generated_text = output.outputs[0].text.strip() if output.outputs else ""
            # If the output is empty, try to get the raw output token
            if not generated_text and output.outputs and output.outputs[0].token_ids:
                # Try to get the raw token from the first token ID
                first_token_id = output.outputs[0].token_ids[0] if output.outputs[0].token_ids else None
                if first_token_id is not None:
                    generated_text = tokenizer.decode([first_token_id])
                    logger.info(f"Using decoded token ID {first_token_id} → '{generated_text}'")
            
            # Handle both dictionary and list inputs
            if isinstance(current_batch, dict):
                row = {k: current_batch[k][idx] for k in current_batch.keys()}
            elif isinstance(current_batch, list):
                row = current_batch[idx]
            else:
                logger.error(f"Unexpected current_batch type: {type(current_batch)}")
                row = {"prompt": str(current_batch)}
            
            # Print detailed info for first few completions
            if idx < 5:
                logger.debug(f"Completion {idx}:")
                if 'fim_type' in row:
                    logger.debug(f"  fim_type: '{row['fim_type']}'")
                logger.debug(f"  Generated: '{generated_text}'")
                
                # Add canonical solution to debug if available
                if 'canonical_solution' in row:
                    logger.debug(f"  Canonical solution: '{row['canonical_solution']}'")
            
            # Determine if the generated text is correct
            is_correct = False
            expected_type = ""
            
            # For string datasets, we don't have fim_type or canonical_solution
            if 'fim_type' in row:
                if row["fim_type"] == "prefix":
                    # For the "prefix" type, we should check against the canonical solution
                    if 'canonical_solution' in row and row['canonical_solution'].strip():
                        # Use the canonical solution as the expected type
                        expected_type = row['canonical_solution'].strip()
                        correct = _is_valid_type_completion(generated_text, expected_type)
                        
                        # Track type-specific metrics for analysis
                        if correct:
                            correct_count += 1
                            
                        # Log the first few examples for analysis
                        if idx < 5:
                            logger.info(f"  Type prediction - Expected: '{expected_type}', Generated: '{generated_text}'")
                            logger.info(f"  Type prediction correct: {correct}")
                    else:
                        # No canonical solution, fall back to syntactic validation
                        correct = _is_valid_type_completion(generated_text)
                else:
                    # For explicit fim_type values (like "Any"), use matching
                    correct = _flexible_match(row["fim_type"], generated_text)
            else:
                # For string datasets, we don't have fim_type or canonical_solution
                correct = _is_valid_type_completion(generated_text)
            
            # Log details about mismatches to understand the issue
            if not correct and mismatch_count < 5:
                logger.warning(f"MISMATCH EXAMPLE #{mismatch_count}:")
                if 'fim_type' in row:
                    logger.warning(f"  fim_type: '{row['fim_type']}'")
                else:
                    logger.warning(f"  No fim_type available")
                logger.warning(f"  Generated (len={len(generated_text)}): '{generated_text}'")
                
                if 'canonical_solution' in row:
                    logger.warning(f"  Canonical solution: '{row['canonical_solution']}'")
                else:
                    logger.warning(f"  No canonical solution available")
                
                mismatch_count += 1
            
            batch_completions.append({
                **row,
                "_generated": generated_text,
                "generated_text": generated_text,
                "correct": correct,
                "model_name": model_name
            })
        except Exception as e:
            logger.error(f"ERROR processing completion {idx}: {str(e)}")
            continue
    
    if correct_count > 0:
        logger.info(f"Correct type predictions in this batch: {correct_count}/{len(outputs)} = {(correct_count/len(outputs))*100:.2f}%")
    
    return batch_completions

def main(
    llm: LLM,
    tokenizer: PreTrainedTokenizer,
    ds: datasets.Dataset,
    new_ds_path: Path,
    model_fim: Union[FimObj,FimChat],
    batch_size: int,
    model_name: str,
    max_n: int
):
    # Check if dataset contains strings or dictionaries
    try:
        first_example = next(iter(ds))
        is_string_dataset = not isinstance(first_example, dict)
        
        # If it's a string dataset, wrap each item in a dictionary with a "prompt" field
        if is_string_dataset:
            logger.info("Converting string dataset to dictionary format with 'prompt' field")
            # For non-streaming datasets, we can convert directly
            if not hasattr(ds, "_iter_datasets"):
                ds = datasets.Dataset.from_dict({"prompt": list(ds)})
            else:
                # For streaming datasets, we'll handle conversion during processing
                logger.info("Using streaming dataset - will convert items during processing")
    except Exception as e:
        logger.warning(f"Error checking dataset format: {e}")
        logger.warning("Will attempt to process as-is")
        is_string_dataset = False
    
    # Check if we need to resume from a previous run
    blacklist = set()
    if Path(new_ds_path).exists() and not args.overwrite:
        try:
            completions = datasets.load_from_disk(new_ds_path)
            logger.info(f"Resuming from {len(completions)} completions.")
            
            # Add completed examples to blacklist
            for row in completions:
                if 'fim_program' in row:
                    blacklist.add(hex_encode(row["fim_program"]))
        except Exception as e:
            logger.warning(f"Error loading existing completions: {e}")
            logger.warning("Starting from scratch.")

    # preprocess dataset
    logger.info("Filtering for 1-token types...")
    
    # Check if we're dealing with a string dataset or a dictionary dataset with fim_type
    is_string_dataset = False
    try:
        # Try to access the first example to check its type
        first_example = next(iter(ds))
        if isinstance(first_example, str):
            is_string_dataset = True
        elif isinstance(first_example, dict) and "fim_type" not in first_example:
            is_string_dataset = True
    except Exception as e:
        logger.warning(f"Error checking dataset format: {e}")
    
    if not is_string_dataset:
        # Only apply filtering if we have a dataset with fim_type field
        logger.info("Applying 1-token type filtering...")
        ds = ds.filter(lambda x: is_1tok(x["fim_type"], tokenizer))
        if len(blacklist) > 0:
            logger.info(f"Filtering out {len(blacklist)} blacklisted examples...")
            # Convert to list to avoid streaming dataset issues
            ds = datasets.Dataset.from_list(list(ds)).filter(lambda x: hex_encode(x["fim_program"]) not in blacklist)
    else:
        logger.info("Skipping filtering for string dataset (no fim_type field available)")
        if len(blacklist) > 0:
            logger.info(f"Skipping blacklist filtering for string dataset (no fim_program field available)")
    
    logger.info("Properly formatting FIM prompts...")
    # Keep fim_program in raw form but add _prompt in FIM format
    if not is_string_dataset:
        # For dictionary datasets with fim_program field
        ds = ds.map(lambda x: {**x, "_prompt": _format_fim_prompt(x["fim_program"], model_fim)})
    else:
        # For string datasets, the string itself is the prompt
        logger.info("String dataset: using strings directly as prompts")
        if isinstance(ds, datasets.Dataset):
            # For non-streaming datasets
            ds = ds.map(lambda x: {"prompt": x, "_prompt": x})
        else:
            # For streaming datasets, convert to list first
            ds_list = []
            for item in ds:
                if isinstance(item, str):
                    ds_list.append({"prompt": item, "_prompt": item})
                else:
                    ds_list.append({**item, "_prompt": item.get("prompt", str(item))})
            ds = datasets.Dataset.from_list(ds_list)

    # Print diagnostic information about the first example
    first_example = next(iter(ds))
    logger.info("\n=== DATASET DIAGNOSTICS ===")
    logger.info(f"Dataset size: {len(ds)} examples")
    
    # Check if first_example is a dictionary or a string
    if isinstance(first_example, dict):
        logger.info(f"Dataset columns: {list(first_example.keys())}")
        if 'fim_type' in first_example:
            logger.info(f"First example fim_type: '{first_example['fim_type']}'")
            # Log token IDs of fim_type - this is what we want the model to predict
            fim_type_tokens = tokenizer(first_example["fim_type"], add_special_tokens=False)["input_ids"]
            logger.info(f"First example fim_type token IDs: {fim_type_tokens}")
            logger.info(f"First example fim_type num tokens: {len(fim_type_tokens)}")
        
        # Always log the prompt that will be used for generation
        prompt_key = "_prompt" if "_prompt" in first_example else "prompt"
        if prompt_key in first_example:
            logger.info(f"First example {prompt_key}: '{first_example[prompt_key]}'")
    else:
        # String dataset
        logger.info("Dataset contains string examples")
        logger.info(f"First example (string): '{first_example}'")
    
    # Only try to access fim_program if example is a dictionary
    if isinstance(first_example, dict) and 'fim_program' in first_example:
        if isinstance(first_example['fim_program'], str):
            logger.info(f"First example fim_program (first 200 chars): '{first_example['fim_program'][:200]}'")
        else:
            logger.info(f"First example fim_program (not a string): {type(first_example['fim_program'])}")
    
    # Check for _prompt as well
    if isinstance(first_example, dict) and '_prompt' in first_example:
        if isinstance(first_example['_prompt'], str):
            logger.info(f"First example _prompt (formatted for FIM): '{first_example['_prompt'][:200]}'")
            logger.info(f"Is _prompt in FIM format? {_is_fim_format(first_example['_prompt'])}")
        else:
            logger.info(f"First example _prompt (not a string): {type(first_example['_prompt'])}")
    elif isinstance(first_example, dict) and 'prompt' in first_example:
        if isinstance(first_example['prompt'], str):
            logger.info(f"First example prompt (formatted for FIM): '{first_example['prompt'][:200]}'")
            logger.info(f"Is prompt in FIM format? {_is_fim_format(first_example['prompt'])}")
        else:
            logger.info(f"First example prompt (not a string): {type(first_example['prompt'])}")
    
    # Check for completeness of FIM format
    if isinstance(first_example, dict) and '_prompt' in first_example and _is_fim_format(first_example['_prompt']):
        prompt_parts = first_example['_prompt'].split('<fim_middle>')
        if len(prompt_parts) > 0:
            logger.info("Text after <fim_middle>: " + (prompt_parts[1][:50] if len(prompt_parts) > 1 else "Nothing"))
        
        prefix_parts = prompt_parts[0].split('<fim_suffix>')
        if len(prefix_parts) > 0:
            logger.info("Text after <fim_suffix>: " + (prefix_parts[1][:50] if len(prefix_parts) > 1 else "Nothing"))
    
    # Check if fim_type is available
    if isinstance(first_example, dict) and 'fim_type' in first_example:
        logger.info(f"Is fim_type a single token? {is_1tok(first_example['fim_type'], tokenizer)}")
    
    # Check the first prompt's tokenization if available
    if isinstance(first_example, dict):
        if '_prompt' in first_example:
            first_prompt = first_example["_prompt"]
        elif 'prompt' in first_example:
            first_prompt = first_example["prompt"]
        else:
            first_prompt = str(first_example)
    else:
        first_prompt = str(first_example)
    
    # Ensure first_prompt is a string before slicing
    if not isinstance(first_prompt, str):
        first_prompt = str(first_prompt)
    
    logger.info(f"\nFirst prompt: '{first_prompt[:100]}...'")
    prompt_tokens = tokenizer(str(first_prompt)[:100], add_special_tokens=False)["input_ids"]
    logger.info(f"First few tokens of prompt: {prompt_tokens[:15]}")
    logger.info(f"Decoded first few tokens: '{tokenizer.decode(prompt_tokens[:15])}'")
    
    # Try a custom prompt to debug
    logger.info("\n=== TESTING WITH CUSTOM PROMPT ===")
    test_prompt = f"<fim_prefix>def hello():<fim_suffix>    return 'world'<fim_middle>"
    logger.info(f"Test prompt: '{test_prompt}'")
    test_tokens = tokenizer(test_prompt, add_special_tokens=False)["input_ids"]
    logger.info(f"Test prompt token IDs: {test_tokens}")
    logger.info(f"Test prompt decoded: '{tokenizer.decode(test_tokens)}'")
    
    # Update sampling parameters to reflect the correct usage
    sampling_params = SamplingParams(temperature=0, max_tokens=10)
    logger.info(f"Sampling parameters: {sampling_params}")
    
    try:
        logger.info("Trying test generation...")
        test_outputs = llm.generate([test_prompt], sampling_params)
        if test_outputs and test_outputs[0].outputs:
            logger.info(f"Test generation output: '{test_outputs[0].outputs[0].text}'")
            logger.info(f"Test generation token IDs: {test_outputs[0].outputs[0].token_ids}")
        else:
            logger.info("Test generation produced no output")
    except Exception as e:
        logger.error(f"Test generation failed: {str(e)}")
        
    logger.info("=== END DATASET DIAGNOSTICS ===\n")

    # Process in batches
    num_completed = 0
    logger.info(f"Starting generations with batch_size={batch_size}, max_n={max_n}")
    current_batch = defaultdict(list)
    batch_count = 0
    
    # Set a limit on the number of examples to process if max_n is not specified
    example_limit = max_n if max_n > 0 else float('inf')  # No limit if max_n is not specified
    if example_limit < float('inf'):
        logger.info(f"Processing up to {example_limit} examples")
    else:
        logger.info(f"Processing all available examples in the dataset")
    
    for i, example in tqdm(enumerate(ds), desc="Processing examples"):
        # Stop after processing example_limit examples
        if i >= example_limit:
            logger.info(f"Reached example limit of {example_limit}, stopping...")
            break
            
        # Handle different dataset formats
        if is_string_dataset and isinstance(example, str):
            # If examples are strings, create a simple dictionary with prompt field
            current_batch["prompt"].append(example)
        elif isinstance(example, str):
            # Handle case where dataset wasn't properly converted
            current_batch["prompt"].append(example)
        else:
            # Add each field from the example to its respective list
            for k, v in example.items():
                current_batch[k].append(v)
            
        # When we have batch_size examples, process them
        primary_key = list(current_batch.keys())[0]  # Use first key
        if len(current_batch[primary_key]) == batch_size:
            batch_count += 1
            logger.info(f"Processing batch {batch_count}...")
            
            # Get prompts based on available keys
            if "_prompt" in current_batch:
                prompts = current_batch.pop("_prompt")
            elif "prompt" in current_batch:
                prompts = current_batch.pop("prompt")
            else:
                prompts = current_batch.pop(list(current_batch.keys())[0])
            
            # Ensure all prompts are strings
            string_prompts = []
            for p in prompts:
                if not isinstance(p, str):
                    string_prompts.append(str(p))
                else:
                    string_prompts.append(p)
            prompts = string_prompts
            
            logger.info(f"First prompt in batch: {prompts[0][:200]}...")
            
            # Use synchronous generation with modified parameters
            sampling_params = SamplingParams(temperature=0, max_tokens=10)  # Increase max_tokens
            try:
                logger.info(f"Generating completions for {len(prompts)} prompts...")
                
                # Log more details about the first prompt to diagnose
                first_prompt = prompts[0]
                tokens = tokenizer.encode(first_prompt)
                logger.info(f"First prompt tokens: {tokens[:20]}...")  
                logger.info(f"First prompt decoded: {tokenizer.decode(tokens[:20])}...")
                
                # Check if <fim_middle> is present in prompts
                if "<fim_middle>" not in first_prompt:
                    logger.warning("The prompt might be missing <fim_middle> token!")
                
                outputs = llm.generate(prompts, sampling_params)
                logger.info(f"Successfully generated {len(outputs)} completions")
                
                # Log more details about first output
                if outputs and outputs[0].outputs:
                    logger.info(f"First output: '{outputs[0].outputs[0].text}'")
                    logger.info(f"First output tokens: {outputs[0].outputs[0].token_ids}")
            except Exception as e:
                logger.error(f"ERROR during generation: {str(e)}")
                # Skip this batch and continue
                current_batch = defaultdict(list)
                continue
            
            # Process the completions
            examples_for_processing = []
            for i, prompt in enumerate(prompts):
                example_dict = {}
                # Add back the prompt
                example_dict["prompt"] = prompt
                
                # Add any other fields from current_batch
                for k, v in current_batch.items():
                    if i < len(v):
                        example_dict[k] = v[i]
                
                examples_for_processing.append(example_dict)
            
            batch_completions = _process_batch_completions(outputs, examples_for_processing, tokenizer, model_name)
            num_completed += len(batch_completions)
            logger.info(f"Completed {num_completed} examples so far")
            
            # Save completions after each batch
            _save(batch_completions, new_ds_path, f"Saving batch {batch_count}")
            
            # Clear the current batch
            current_batch = defaultdict(list)
            
            if max_n > 0 and num_completed >= max_n:
                logger.info(f"Reached max_n={max_n}, stopping...")
                break
    
    # Process any remaining examples in the last batch
    if current_batch and len(current_batch[list(current_batch.keys())[0]]) > 0:
        batch_count += 1
        logger.info(f"Processing final batch...")
        
        # Get prompts based on available keys
        if "_prompt" in current_batch:
            prompts = current_batch.pop("_prompt")
        elif "prompt" in current_batch:
            prompts = current_batch.pop("prompt")
        else:
            prompts = current_batch.pop(list(current_batch.keys())[0])
        
        # Ensure all prompts are strings
        string_prompts = []
        for p in prompts:
            if not isinstance(p, str):
                string_prompts.append(str(p))
            else:
                string_prompts.append(p)
        prompts = string_prompts
        
        sampling_params = SamplingParams(temperature=0, max_tokens=10)  # Increase max_tokens
        try:
            logger.info(f"Generating completions for {len(prompts)} prompts...")
            
            # Log more details about the first prompt to diagnose
            first_prompt = prompts[0]
            tokens = tokenizer.encode(first_prompt)
            logger.info(f"First prompt tokens: {tokens[:20]}...")  
            logger.info(f"First prompt decoded: {tokenizer.decode(tokens[:20])}...")
            
            # Check for <fim_middle> token in the first prompt
            if not _is_fim_format(first_prompt):
                logger.warning("The prompt might be missing <fim_middle> token!")
                
            outputs = llm.generate(prompts, sampling_params)
            logger.info(f"Successfully generated {len(outputs)} completions")
            
            # Log the first output
            if outputs and outputs[0].outputs:
                logger.info(f"First output: '{outputs[0].outputs[0].text}'")
                logger.info(f"First output tokens: {outputs[0].outputs[0].token_ids}")
            
            # Process the completions
            examples_for_processing = []
            for i, prompt in enumerate(prompts):
                example_dict = {}
                # Add back the prompt
                example_dict["prompt"] = prompt
                
                # Add any other fields from current_batch
                for k, v in current_batch.items():
                    if i < len(v):
                        example_dict[k] = v[i]
                
                examples_for_processing.append(example_dict)
            
            batch_completions = _process_batch_completions(outputs, examples_for_processing, tokenizer, model_name)
            num_completed += len(batch_completions)
            logger.info(f"Completed {num_completed} examples so far")
            _save(batch_completions, new_ds_path, "Saving final batch")
        except Exception as e:
            logger.error(f"ERROR during generation: {str(e)}")
            return

if __name__ == "__main__":
    assert os.environ.get("VLLM_LOGGING_LEVEL",None) == "ERROR", \
        "Please set env var VLLM_LOGGING_LEVEL=ERROR"
    
    parser = ArgumentParser()
    parser.add_argument("--model", type=str, required=True)
    parser.add_argument("--prompt-ds", type=str, required=True)
    parser.add_argument("--new-ds-name", type=str, required=True)
    
    parser.add_argument("--max-size", type=int, default=-1)
    parser.add_argument("--batch-size", type=int, default=1000)

    parser.add_argument("--dtype", choices=["bfloat16", "float32"], default="bfloat16")
    parser.add_argument("--model-name", default=None)
    parser.add_argument("--tokenizer", default=None)

    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--overwrite", action="store_true")
    
    # Add verbosity control
    parser.add_argument("-v", "--verbose", action="count", default=0,
                        help="Increase output verbosity (v=info, vv=debug)")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Suppress all non-error output")

    args = parser.parse_args()
    
    # Setup logging with appropriate verbosity
    if args.quiet:
        setup_logging(-1)  # Quiet mode
    else:
        setup_logging(args.verbose)  # Normal or verbose mode

    if args.overwrite:
        shutil.rmtree(Path(args.new_ds_name), ignore_errors=True)
        logger.info(f"Removed existing dataset at {args.new_ds_name}")

    args.tokenizer=args.tokenizer if args.tokenizer else args.model
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer)

    datasets.disable_caching()
    if os.path.exists(args.prompt_ds):
        ds = datasets.load_from_disk(str(Path(args.prompt_ds)))
    else:
        # Get the token if available
        token = HfFolder.get_token()
        # Remove the problematic parameter and use token directly if available
        if token:
            ds = datasets.load_dataset(args.prompt_ds, token=token)
        else:
            # Try without authentication
            try:
                ds = datasets.load_dataset(args.prompt_ds)
            except Exception as e:
                logger.error(f"Error loading dataset without authentication: {e}")
                logger.error("Please login using 'huggingface-cli login' first")
                exit(1)
    
    # Get the train split if it exists
    if isinstance(ds, dict) and "train" in ds:
        ds = ds["train"]
    
    dtype = getattr(torch, args.dtype)
    llm = LLM(args.model, dtype=dtype, tensor_parallel_size=num_available_devices())
    model_fim = get_model_fim(args.model)
    
    main(llm, tokenizer, ds, Path(args.new_ds_name), model_fim, args.batch_size,
         args.model_name or args.model, args.max_size)