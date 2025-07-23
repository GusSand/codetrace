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
import shutil
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
        logger.error("Error logging enabled (quiet mode)")

def success_rate(ds: datasets.Dataset) -> str:
    total = 0
    success = 0
    for i, example in enumerate(ds):
        if example.get("success", False):
            success += 1
        total += 1
    return f"{success}/{total} ({success/total:.1%})"

def is_1tok(fim_type: str, tokenizer: PreTrainedTokenizer) -> bool:
    return len(tokenizer.encode(fim_type)) == len(tokenizer.encode(" " + fim_type))

def _identify_expected_type(prompt: str) -> str:
    """Identify the token to be filled in the prompt."""
    middle_marker = "<FILL_MIDDLE>"
    prefix_marker = "<PREFIX>"
    suffix_marker = "<SUFFIX>"
    
    if middle_marker in prompt:
        # FIM format: find expected between FILL_MIDDLE marker and SUFFIX marker
        middle_start = prompt.find(middle_marker) + len(middle_marker)
        suffix_start = prompt.find(suffix_marker)
        if suffix_start != -1:
            return prompt[middle_start:suffix_start].strip()
    
    return None

def _is_valid_type_completion(generated: str, canonical_solution: str = None) -> bool:
    """
    Checks if the generated type completion is valid.
    A valid completion should match the canonical solution if provided.
    Otherwise, it should follow Python type syntax conventions.
    """
    # Strip whitespace and comments
    generated = generated.strip()
    
    # If canonical solution is provided, check for match
    if canonical_solution:
        # Simple case: exact match
        if generated == canonical_solution:
            return True
            
        # Check for known equivalence patterns
        # e.g., List[int] vs list[int], Optional[T] vs Union[T, None]
        if _flexible_match(canonical_solution, generated):
            return True
        
        return False
    
    # No canonical solution provided, check for valid Python type syntax
    
    # Check for empty completion
    if not generated:
        return False
    
    # Check if balanced parentheses, brackets, etc.
    if not is_balanced(generated, '(', ')'):
        return False
    if not is_balanced(generated, '[', ']'):
        return False
    if not is_balanced(generated, '{', '}'):
        return False
    
    return True

    def is_balanced(text, open_char, close_char):
        """Check if parentheses, brackets, etc. are balanced in text."""
        stack = []
        for char in text:
            if char == open_char:
                stack.append(char)
            elif char == close_char:
                if not stack:  # More closing than opening
                    return False
                stack.pop()
        return len(stack) == 0  # All opening chars should be closed

def _flexible_match(expected: str, generated: str) -> bool:
    """
    Check if generated type matches expected type with some flexibility.
    Handles common equivalence patterns in Python type annotations.
    """
    # Normalize whitespace
    expected = expected.replace(" ", "")
    generated = generated.replace(" ", "")
    
    # Exact match after whitespace normalization
    if expected == generated:
        return True
    
    # Handle case differences for builtin types
    # e.g., list vs List, dict vs Dict, etc.
    expected_lower = expected.lower()
    generated_lower = generated.lower()
    
    builtin_types = ["list", "dict", "set", "tuple", "str", "int", "float", "bool"]
    for builtin in builtin_types:
        # Replace exact word (not partial matches)
        if builtin in expected_lower and builtin in generated_lower:
            expected_lower = expected_lower.replace(builtin, "#TYPE#")
            generated_lower = generated_lower.replace(builtin, "#TYPE#")
    
    if expected_lower == generated_lower:
        return True
    
    # Handle Optional[T] vs Union[T, None] vs T | None equivalence
    if "optional[" in expected_lower and "union[" in generated_lower:
        # Convert Optional[T] to Union[T, None] for comparison
        expected_union = expected_lower.replace("optional[", "union[").replace("]", ",none]")
        if expected_union == generated_lower:
            return True
    
    if "union[" in expected_lower and "optional[" in generated_lower:
        # Convert Union[T, None] to Optional[T] for comparison
        if "none" in expected_lower or "null" in expected_lower:
            generated_union = generated_lower.replace("optional[", "union[").replace("]", ",none]")
            if expected_lower == generated_union:
                return True
    
    return False

def _is_fim_format(prompt: str) -> bool:
    """Check if prompt is in FIM format."""
    return "<PREFIX>" in prompt and "<SUFFIX>" in prompt

def _format_fim_prompt(prompt: str, model_fim: Union[FimObj,FimChat]) -> str:
    """Format prompt for fill-in-middle."""
    
    if model_fim.is_chat:
        # Handle chat format separately
        fmt_prompt = prepare_fim_prompt(prompt, model_fim.prefix, model_fim.middle, model_fim.suffix, model_fim.middle)
        # For chat, convert to messages with instructions
        messages = [
            {"role": "system", "content": "You are a helpful coding assistant that completes code according to instructions."},
            {"role": "user", "content": fmt_prompt},
        ]
        # Convert to chat format specific to the model
        return model_fim.tokenizer.apply_chat_template(messages, tokenize=False)
    else:
        # Regular fill-in-the-middle format
        if "<PREFIX>" in prompt and "<SUFFIX>" in prompt:
            # Extract components
            prefix = prompt.split("<PREFIX>")[1].split("<FILL_MIDDLE>")[0]
            suffix = prompt.split("<SUFFIX>")[1]
            return model_fim.prefix + prefix + model_fim.middle + suffix
        else:
            # If not in FIM format, return as is
            return prompt

def _save(data: List[Dict[str,Any]], path:str, message:str):
    """Save dataset with progress message."""
    logger.info(f"Saving {message}...")
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    dataset = datasets.Dataset.from_list(data)
    dataset.save_to_disk(path)
    logger.info(f"Saved {len(data)} examples to {path}")

def _process_batch_completions(outputs, current_batch, tokenizer, model_name):
    """Process batch of completions and record results."""
    
    results = []
    
    for i, output in enumerate(outputs):
        original_example = current_batch[i]
        all_tokens = output.outputs[0].token_ids
                
        # Get completed text
        all_text = tokenizer.decode(all_tokens, skip_special_tokens=True)
        
        # Check if prompt already has FIM format markers
        if _is_fim_format(original_example["prompt"]):
            # Get expected type from prompt
            expected_type = _identify_expected_type(original_example["prompt"])
            
            # Determine if the completion is successful
            is_success = _is_valid_type_completion(all_text, expected_type)
            
            result = {
                "prompt": original_example["prompt"],
                "completion": all_text,
                "expected_type": expected_type,
                "success": is_success,
                "model": model_name
            }
        else:
            # For non-FIM prompts, just record completion without validation
            result = {
                "prompt": original_example["prompt"],
                "completion": all_text,
                "model": model_name
            }
        
        # Copy any additional fields from original example
        for key in original_example:
            if key not in result and key != "prompt":
                result[key] = original_example[key]
        
        results.append(result)
    
    return results

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
    # resume from completions if they exist
    output_path = new_ds_path

    if output_path.exists():
        try:
            completed = datasets.load_from_disk(str(output_path))
            completed_size = len(completed)
            logger.info(f"Resuming from {completed_size} examples")
                        
            # Skip completed examples
            completed_dict = {
                hex_encode(example["prompt"]): i
                for i, example in enumerate(completed)
            }
            
            # If streaming dataset
            if hasattr(ds, "_iter_datasets"):
                # For streaming datasets, we can't slice directly
                collected = []
                for i, example in enumerate(ds):
                    if i < completed_size:
                        continue
                    collected.append(example)
                    if max_n > 0 and len(collected) >= max_n:
                        break
                ds = datasets.Dataset.from_list(collected)
            else:
                # For regular datasets, we can slice
                if max_n > 0:
                    ds = ds.select(range(completed_size, min(completed_size + max_n, len(ds))))
                else:
                    ds = ds.select(range(completed_size, len(ds)))
            
            data = [example for example in completed]
        except Exception as e:
            logger.warning(f"Error loading existing dataset: {e}")
            logger.warning("Starting from scratch")
            data = []
    else:
        data = []
    
    # Set up sampling parameters for generation
    sampling_params = SamplingParams(temperature=0, max_tokens=50)
    
    # Process in batches
    total = len(ds) if not hasattr(ds, "_iter_datasets") else (max_n if max_n > 0 else float('inf'))
    
    logger.info(f"Processing {total} examples in batches of {batch_size}")
    
    current_batch = []
    batch_prompts = []
    
    # For tracking progress
    example_count = 0
    save_interval = 250  # Save after processing this many examples
    
    try:
        for example in tqdm(ds, total=total, desc="Generating completions"):
            # Format prompt for model
            prompt = _format_fim_prompt(example["prompt"], model_fim)
            
            current_batch.append(example)
            batch_prompts.append(prompt)
            
            # When batch is full or at end of dataset
            if len(batch_prompts) >= batch_size:
                # Generate completions
                outputs = llm.generate(batch_prompts, sampling_params)
                
                # Process results
                results = _process_batch_completions(outputs, current_batch, tokenizer, model_name)
                data.extend(results)
                
                # Clear batch
                current_batch = []
                batch_prompts = []
                
                # Save periodically
                example_count += len(results)
                if example_count % save_interval < batch_size:
                    _save(data, str(output_path), f"{example_count}/{total}")
                
                # Report success rate periodically
                if example_count % (save_interval * 4) < batch_size:
                    logger.info(f"Current success rate: {success_rate(datasets.Dataset.from_list(data))}")
        
        # Process any remaining examples
        if batch_prompts:
            outputs = llm.generate(batch_prompts, sampling_params)
            results = _process_batch_completions(outputs, current_batch, tokenizer, model_name)
            data.extend(results)
        
        # Final save
        _save(data, str(output_path), "completion")
        
        # Final success rate
        final_ds = datasets.Dataset.from_list(data)
        logger.info(f"Final dataset size: {len(final_ds)}")
        logger.info(f"Final success rate: {success_rate(final_ds)}")
        
    except KeyboardInterrupt:
        logger.warning("Interrupted by user, saving current progress...")
        _save(data, str(output_path), "partial completion (interrupted)")
        logger.info(f"Saved {len(data)} examples before interruption")
    
    return datasets.Dataset.from_list(data)

if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore", message=".*is_training is now deprecated.*")
    warnings.filterwarnings("ignore", message=".*Overriding torch_dtype=None with `torch_dtype=torch.float16`.*")
    warnings.filterwarnings("ignore", message=".*Your max_tokens is set to 50, but you input has 1 prompt.*")
    warnings.filterwarnings("ignore", message=".*You passed along.*pass `trust_remote_code=True`.*")
    warnings.filterwarnings("ignore", message=".*A new version of the following files was downloaded.*")
    
    # VLLM warning about logging level
    if os.environ.get("VLLM_LOGGING_LEVEL", None) is None:
        logger.warning(
            "VLLM logging level not set, logs may be very verbose.\n"
            "Please set env var VLLM_LOGGING_LEVEL=ERROR"
        )
    
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
            ds = datasets.load_dataset(args.prompt_ds, streaming=True, token=token)
        else:
            # Try without authentication
            try:
                ds = datasets.load_dataset(args.prompt_ds, streaming=True)
            except Exception as e:
                logger.error(f"Error loading dataset without authentication: {e}")
                logger.error("Please login using 'huggingface-cli login' first")
                exit(1)
    
    dtype = getattr(torch, args.dtype)
    llm = LLM(args.model, dtype=dtype, tensor_parallel_size=num_available_devices())
    model_fim = get_model_fim(args.model)
    
    main(llm, tokenizer, ds, Path(args.new_ds_name), model_fim, args.batch_size,
         args.model_name or args.model, args.max_size) 