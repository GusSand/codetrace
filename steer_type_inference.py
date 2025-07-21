import json
import logging
import os
import sys
import time
import argparse
from typing import Dict, List, Optional, Tuple, Any, Callable
from datetime import datetime

import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer, LogitsProcessor, LogitsProcessorList, AutoConfig
from transformers.models.gpt2.modeling_gpt2 import GPT2Block
from pathlib import Path
import pickle
from nnsight import LanguageModel
import traceback
import random
import types
import nnsight

# Set the model name
MODEL_NAME = "bigcode/starcoderbase-1b"

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"steer_type_inference_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

CHECKPOINT_DIR = Path('checkpoints')
CHECKPOINT_DIR.mkdir(exist_ok=True)

def save_checkpoint(data: Dict[str, Any], name: str):
    """Save checkpoint data to a file."""
    try:
        checkpoint_path = CHECKPOINT_DIR / f"{name}.pkl"
        with open(checkpoint_path, 'wb') as f:
            pickle.dump(data, f)
        logger.info(f"Saved checkpoint: {checkpoint_path}")
    except Exception as e:
        logger.error(f"Failed to save checkpoint {name}: {e}")

def load_checkpoint(name: str) -> Optional[Dict[str, Any]]:
    """Load checkpoint data from a file."""
    try:
        checkpoint_path = CHECKPOINT_DIR / f"{name}.pkl"
        if checkpoint_path.exists():
            with open(checkpoint_path, 'rb') as f:
                data = pickle.load(f)
            logger.info(f"Loaded checkpoint: {checkpoint_path}")
            return data
    except Exception as e:
        logger.error(f"Failed to load checkpoint {name}: {e}")
    return None

def create_steering_vectors(model, tokenizer, examples, device="cpu"):
    """Create steering vectors from examples."""
    logger.info("Creating steering vectors...")
    
    # Separate positive and negative examples
    positive_examples = [ex for ex in examples if ex.get("correct", False)]
    negative_examples = [ex for ex in examples if not ex.get("correct", False)]
    
    logger.info(f"Found {len(positive_examples)} positive examples and {len(negative_examples)} negative examples")
    
    if not positive_examples or not negative_examples:
        logger.warning("Not enough examples to create steering vectors. Need at least one positive and one negative example.")
        return None
    
    # Create steering vectors for layers (we'll use layers 10-15 by default)
    steering_vectors = {}
    for layer_idx in range(10, 15):
        logger.debug(f"Creating steering vector for layer {layer_idx}")
        
        # Process positive examples
        pos_hidden_states = []
        for example in positive_examples:
            try:
                # Use the input field instead of input_text
                input_text = example.get("input", "")
                if not input_text:
                    logger.warning(f"Missing input field in example {example.get('example_id', 'unknown')}")
                    continue
                
                # Forward pass through the model to get hidden states
                with torch.no_grad():
                    # Process input text
                    inputs = tokenizer(input_text, return_tensors="pt")
                    
                    # For nnsight models, we need to use a special approach to get hidden states
                    from nnsight import InterventionType
                    
                    # Use nnsight's context manager to run a forward pass and capture hidden states
                    with model.trace() as tracer:
                        # Get the output of a specific layer
                        if hasattr(model, 'model') and hasattr(model.model, 'layers'):
                            layer_output = model.model.layers[layer_idx].output
                            
                            # Run the model
                            model(**inputs)
                    
                    # Extract the hidden states from the trace
                    hidden_states = tracer.get_value(layer_output).detach()
                    
                    # Process the hidden states (take the mean across sequence length)
                    pos_hidden_states.append(hidden_states.mean(dim=1).squeeze())
            except Exception as e:
                logger.error(f"Error processing positive example: {str(e)}")
                logger.error(f"Exception details: {str(e)}")
                import traceback
                logger.error(traceback.format_exc())
        
        # Process negative examples
        neg_hidden_states = []
        for example in negative_examples:
            try:
                input_text = example.get("input", "")
                if not input_text:
                    logger.warning(f"Missing input field in example {example.get('example_id', 'unknown')}")
                    continue
                
                # Forward pass to get hidden states
                with torch.no_grad():
                    # Process input text
                    inputs = tokenizer(input_text, return_tensors="pt")
                    
                    # For nnsight models, use the same approach as above
                    from nnsight import InterventionType
                    
                    # Use nnsight's context manager to run a forward pass and capture hidden states
                    with model.trace() as tracer:
                        # Get the output of a specific layer
                        if hasattr(model, 'model') and hasattr(model.model, 'layers'):
                            layer_output = model.model.layers[layer_idx].output
                            
                            # Run the model
                            model(**inputs)
                    
                    # Extract the hidden states from the trace
                    hidden_states = tracer.get_value(layer_output).detach()
                    
                    # Process the hidden states
                    neg_hidden_states.append(hidden_states.mean(dim=1).squeeze())
            except Exception as e:
                logger.error(f"Error processing negative example: {str(e)}")
                logger.error(f"Exception details: {str(e)}")
                import traceback
                logger.error(traceback.format_exc())
        
        if not pos_hidden_states or not neg_hidden_states:
            logger.warning(f"No valid hidden states for layer {layer_idx}")
            continue
        
        # Calculate mean vectors
        pos_mean = torch.stack(pos_hidden_states).mean(dim=0)
        neg_mean = torch.stack(neg_hidden_states).mean(dim=0)
        
        # Compute steering vector (positive - negative)
        steering_vector = pos_mean - neg_mean
        
        # Log statistics for the steering vector
        logger.debug(f"Layer {layer_idx} steering vector stats: mean={steering_vector.mean().item():.4f}, std={steering_vector.std().item():.4f}, norm={torch.norm(steering_vector).item():.4f}")
        
        steering_vectors[layer_idx] = steering_vector
    
    return steering_vectors

def apply_steering_to_model(model, steering_vectors, scale=1.0):
    """Apply steering to the model by patching the forward methods of layers."""
    logger.info(f"Applying steering to model with scale {scale}")
    
    # Save original forward methods
    original_forwards = {}
    
    # Apply steering to each layer
    for layer_idx, steering_vector in steering_vectors.items():
        if steering_vector is None:
            continue
        
        # Get the layer from the model
        layer = model.model.layers[layer_idx]
        original_forwards[layer_idx] = layer.forward
        
        # Create a patched forward method
        def make_patched_forward(layer_idx, original_forward, steering_vector, scale):
            def patched_forward(self, *args, **kwargs):
                # Call the original forward method
                output = original_forward(*args, **kwargs)
                
                # Apply steering to the output
                if isinstance(output, torch.Tensor):
                    # Apply steering to the hidden states
                    steered_output = output + scale * steering_vector
                    return steered_output
                elif isinstance(output, tuple) and len(output) > 0:
                    # The first element is typically the hidden states
                    hidden_states = output[0]
                    steered_hidden_states = hidden_states + scale * steering_vector
                    return (steered_hidden_states,) + output[1:]
                
                return output
            
            return patched_forward
        
        # Patch the forward method
        patched_forward = make_patched_forward(layer_idx, original_forwards[layer_idx], steering_vector, scale)
        layer.forward = types.MethodType(patched_forward, layer)
        logger.info(f"Applied steering to layer {layer_idx}")
    
    return original_forwards

def remove_steering_from_model(model, original_forwards):
    """Remove steering from model by restoring original forward methods."""
    logger.info("Removing steering from model")
    
    for layer_idx, original_forward in original_forwards.items():
        layer = model.model.layers[layer_idx]
        layer.forward = original_forward
        logger.info(f"Restored original forward method for layer {layer_idx}")
    
    logger.info("All steering removed from model")

def clean_type_prediction(text: str) -> str:
    """Clean up type predictions."""
    # First try to find just the type name without additional content
    if not text:
        logger.warning("Invalid or empty type: ")
        return ""
    
    # Split by newlines and take first non-empty line
    lines = [line.strip() for line in text.split('\n')]
    lines = [line for line in lines if line]
    
    if lines:
        # For simple types, return the first line
        return lines[0]
    
    # If no valid lines, return the original stripped text
    return text.strip()

class SteeringCallback:
    """Callback to apply steering to hidden states during generation."""
    
    def __init__(self, model, steering_vectors, layers, scale=1.0):
        self.model = model
        self.steering_vectors = steering_vectors
        self.layers = layers
        self.scale = scale
        self.stats = {}
        
    def __call__(self, hidden_states, layer_idx):
        """Apply steering to hidden states."""
        if layer_idx not in self.layers or layer_idx not in self.steering_vectors:
            return hidden_states
        
        # Log initial stats
        if layer_idx not in self.stats:
            self.stats[layer_idx] = {
                "initial_mean": hidden_states.mean().item(),
                "initial_std": hidden_states.std().item(),
                "initial_norm": torch.norm(hidden_states).item()
            }
        
        # Apply steering vector
        steering_vector = self.steering_vectors[layer_idx]
        
        # Make sure the steering vector is compatible with hidden states
        if len(hidden_states.shape) == 3:  # [batch_size, seq_len, hidden_size]
            # Expand steering vector to match hidden states shape
            steering_vector = steering_vector.unsqueeze(0).unsqueeze(0)
            steering_vector = steering_vector.expand(hidden_states.shape[0], hidden_states.shape[1], -1)
        
        # Apply steering with scale
        hidden_states = hidden_states + self.scale * steering_vector.to(hidden_states.device)
        
        # Log final stats
        self.stats[layer_idx].update({
            "final_mean": hidden_states.mean().item(),
            "final_std": hidden_states.std().item(),
            "final_norm": torch.norm(hidden_states).item()
        })
        
        return hidden_states

def hook_model(model, callback):
    """Hook the model to apply steering during forward pass."""
    original_forwards = {}
    
    for layer_idx in callback.layers:
        if hasattr(model, 'model') and hasattr(model.model, 'layers'):
            layer = model.model.layers[layer_idx]
            
            # Save original forward
            original_forwards[layer_idx] = layer.forward
            
            # Define new forward
            def make_forward(layer_idx, original_forward):
                def new_forward(*args, **kwargs):
                    output = original_forward(*args, **kwargs)
                    
                    # Apply steering to hidden states
                    if isinstance(output, tuple) and len(output) > 0:
                        # If output is a tuple, the hidden states might be the first element
                        if isinstance(output[0], torch.Tensor):
                            hidden_states = output[0]
                            modified = callback(hidden_states, layer_idx)
                            output = (modified,) + output[1:]
                    elif isinstance(output, torch.Tensor):
                        # If output is a tensor, it's probably the hidden states
                        hidden_states = output
                        modified = callback(hidden_states, layer_idx)
                        output = modified
                    
                    return output
                return new_forward
            
            # Replace forward method
            layer.forward = make_forward(layer_idx, original_forwards[layer_idx])
    
    return original_forwards

class SteeringLogitsProcessor:
    """Custom logits processor that applies steering to the logits."""
    
    def __init__(self, steering_vectors, device="cuda", scale=1.0):
        self.steering_vectors = steering_vectors
        self.device = device
        self.scale = scale
        logger.info(f"Initialized SteeringLogitsProcessor with scale {scale}")
        
        # Calculate and log statistics for steering vectors
        for layer_idx, vector in steering_vectors.items():
            logger.info(f"Layer {layer_idx} steering vector stats:")
            logger.info(f"  Mean: {vector.mean().item():.4f}")
            logger.info(f"  Std: {vector.std().item():.4f}")
            logger.info(f"  Norm: {torch.norm(vector).item():.4f}")
    
    def __call__(self, layer_idx, hidden_states, **kwargs):
        """Apply steering to hidden states."""
        if layer_idx not in self.steering_vectors:
            return hidden_states
        
        # Get the steering vector for this layer
        steering_vector = self.steering_vectors[layer_idx].to(self.device)
        
        # Log statistics before steering
        batch_size = hidden_states.size(0)
        seq_len = hidden_states.size(1)
        logger.debug(f"Layer {layer_idx} hidden states shape: {hidden_states.shape}")
        logger.debug(f"Layer {layer_idx} hidden states stats before steering:")
        logger.debug(f"  Mean: {hidden_states.mean().item():.4f}")
        logger.debug(f"  Std: {hidden_states.std().item():.4f}")
        logger.debug(f"  Norm: {torch.norm(hidden_states).item():.4f}")
        
        # Apply steering to the last token's hidden state in each sequence
        for b in range(batch_size):
            # Apply the steering vector to the last token
            hidden_states[b, -1] = hidden_states[b, -1] + self.scale * steering_vector
            
            # Renormalize to maintain scale
            norm = torch.norm(hidden_states[b, -1], dim=-1, keepdim=True)
            hidden_states[b, -1] = hidden_states[b, -1] / (norm + 1e-8)
        
        # Log statistics after steering
        logger.debug(f"Layer {layer_idx} hidden states stats after steering:")
        logger.debug(f"  Mean: {hidden_states.mean().item():.4f}")
        logger.debug(f"  Std: {hidden_states.std().item():.4f}")
        logger.debug(f"  Norm: {torch.norm(hidden_states).item():.4f}")
        
        return hidden_states

def run_inference(examples, generator, tokenizer, batch_size=1, steering_vectors=None, layers=None, scale=1.0, force_rerun=False, save_checkpoints=True):
    """
    Run inference with and without steering and collect results.
    
    Args:
        examples: List of examples to process
        generator: The model to use for generation
        tokenizer: The tokenizer to use
        batch_size: Number of examples to process in each batch
        steering_vectors: Dictionary of steering vectors for each layer
        layers: List of layers to apply steering to
        scale: Scale factor for steering
        force_rerun: Whether to force rerun inference even if checkpoint exists
        save_checkpoints: Whether to save checkpoints
        
    Returns:
        List of results for each example
    """
    results = []
    
    unsteered_correct = 0
    steered_correct = 0
    total_examples = len(examples)
    mutations_processed = 0
    
    # Try to load checkpoint for unsteered results
    checkpoint_path = "checkpoints/unsteered_results.pkl"
    if os.path.exists(checkpoint_path) and not force_rerun and save_checkpoints:
        logger.info(f"Loading unsteered results from checkpoint: {checkpoint_path}")
        try:
            with open(checkpoint_path, "rb") as f:
                results = pickle.load(f)
                
            # Count correct predictions
            for result in results:
                if result.get("unsteered_correct", False):
                    unsteered_correct += 1
                    
            logger.info(f"Loaded {len(results)} results from checkpoint with {unsteered_correct} correct predictions")
            
            # Skip unsteered inference if checkpoint loaded
            logger.info(f"Unsteered accuracy: {unsteered_correct / total_examples:.4f}")
            
            return results
        except Exception as e:
            logger.error(f"Error loading checkpoint: {str(e)}")
            # Continue with inference
    
    # Run inference if no checkpoint or force_rerun
    logger.info(f"Running inference without steering (force_rerun={force_rerun} or save_checkpoints={not save_checkpoints})")
    
    for example in examples:
        logger.info(f"Processing example: {example.get('example_id', 'unknown')}")
        fim_type = example.get("fim_type", "")
        logger.info(f"FIM type: {fim_type}")
        
        # Get mutations
        mutations = example.get("mutations", [])
        logger.info(f"Number of mutations: {len(mutations)}")
        
        # Process each mutation
        for mutation in mutations:
            # Create a result object for this mutation
            mutation_result = {
                "example_id": example.get("example_id", ""),
                "mutation_number": mutation.get("mutation_number", ""),
                "fim_type": fim_type,
                "original_code": mutation.get("original_code", ""),
                "mutated_code": mutation.get("mutated_code", ""),
                "prefix": mutation.get("prefix", ""),
                "fim_type": fim_type
            }
            
            mutations_processed += 1
            
            # Run unsteered inference
            mutation_number = mutation.get("mutation_number", "unknown")
            logger.info(f"Running unsteered inference for mutation {mutation_number}")
            
            try:
                # Prepare the input
                prefix = mutation.get("prefix", "")
                
                # Run unsteered inference using huggingface-style API
                # This approach is simpler and more compatible
                from transformers import TextGenerationPipeline
                
                # Create a pipeline with the model and tokenizer
                generation_pipeline = TextGenerationPipeline(model=generator, tokenizer=tokenizer)
                
                # Generate text directly with the pipeline
                generated_output = generation_pipeline(
                    prefix,
                    max_length=len(tokenizer(prefix)["input_ids"]) + 20,
                    temperature=0.7,
                    num_return_sequences=1
                )
                
                # Extract the generated text from the pipeline output
                generated_text = generated_output[0]["generated_text"]
                
                # Get only the newly generated part (after the prefix)
                if generated_text.startswith(prefix):
                    generated_text = generated_text[len(prefix):]
                
                logger.info(f"Generated text (first 100 chars): {generated_text[:100]}...")
                
                # Clean up the prediction
                cleaned_prediction = clean_type_prediction(generated_text)
                mutation_result["unsteered_prediction"] = cleaned_prediction
                
                # Check accuracy
                is_correct = cleaned_prediction == fim_type
                mutation_result["unsteered_correct"] = is_correct
                if is_correct:
                    unsteered_correct += 1
            except Exception as e:
                logger.error(f"Error during unsteered inference: {str(e)}")
                import traceback
                logger.error(traceback.format_exc())
                mutation_result["unsteered_prediction"] = ""
                mutation_result["unsteered_correct"] = False
            
            # Run steered inference if steering vectors are provided
            if steering_vectors and layers:
                logger.info(f"Running steered inference for mutation {mutation_number}")
                
                try:
                    # Apply steering to the model
                    logger.info(f"Applying steering with scale {scale}")
                    original_forwards = apply_steering_to_model(generator, steering_vectors, scale)
                    
                    # Run steered inference using the same approach as unsteered
                    from transformers import TextGenerationPipeline
                    
                    # Create a pipeline with the steered model and tokenizer
                    steered_pipeline = TextGenerationPipeline(model=generator, tokenizer=tokenizer)
                    
                    # Generate text directly with the pipeline
                    steered_output = steered_pipeline(
                        prefix,
                        max_length=len(tokenizer(prefix)["input_ids"]) + 20,
                        temperature=0.7,
                        num_return_sequences=1
                    )
                    
                    # Extract the generated text from the pipeline output
                    steered_text = steered_output[0]["generated_text"]
                    
                    # Get only the newly generated part (after the prefix)
                    if steered_text.startswith(prefix):
                        steered_text = steered_text[len(prefix):]
                    
                    logger.info(f"Steered text (first 100 chars): {steered_text[:100]}...")
                    
                    # Clean up the prediction
                    cleaned_steered = clean_type_prediction(steered_text)
                    mutation_result["steered_prediction"] = cleaned_steered
                    
                    # Check accuracy
                    is_steered_correct = cleaned_steered == fim_type
                    mutation_result["steered_correct"] = is_steered_correct
                    if is_steered_correct:
                        steered_correct += 1
                    
                    # Restore the model to its original state
                    remove_steering_from_model(generator, original_forwards)
                    
                except Exception as e:
                    logger.error(f"Error during steered inference: {str(e)}")
                    import traceback
                    logger.error(traceback.format_exc())
                    mutation_result["steered_prediction"] = ""
                    mutation_result["steered_correct"] = False
            
            # Add the result for this mutation
            results.append(mutation_result)
    
    logger.info(f"Final unsteered accuracy: {unsteered_correct / total_examples:.4f}")
    
    # Save checkpoint
    if save_checkpoints:
        os.makedirs("checkpoints", exist_ok=True)
        with open(checkpoint_path, "wb") as f:
            pickle.dump(results, f)
        logger.info(f"Saved checkpoint: {checkpoint_path}")
    
    logger.info(f"Unsteered accuracy: {unsteered_correct / total_examples:.4f}")
    
    if steered_correct > 0:
        logger.info(f"Steered accuracy: {steered_correct / total_examples:.4f}")
    
    return results

def analyze_results(results):
    """Analyze the results of steered and unsteered predictions."""
    # Count total examples and mutations
    total_examples = len(results)
    total_mutations = 0
    
    # Track correct predictions
    unsteered_correct = 0
    steered_correct = 0
    
    # Track examples where steering improved or worsened the result
    improved = 0
    worsened = 0
    unchanged = 0
    
    # Flag to check if any mutation has steered results
    has_steered_results = False
    
    # Process based on the new results structure
    if results and isinstance(results[0], dict) and "example_id" in results[0]:
        # New structure: flat list of mutation results
        total_mutations = len(results)
        
        for mutation in results:
            # Count unsteered correct
            if mutation.get("unsteered_correct", False):
                unsteered_correct += 1
                
            # Count steered correct and compare
            if "steered_correct" in mutation:
                has_steered_results = True
                if mutation.get("steered_correct", False):
                    steered_correct += 1
                
                # Compare steered and unsteered
                if mutation.get("steered_correct", False) and not mutation.get("unsteered_correct", False):
                    improved += 1
                elif not mutation.get("steered_correct", False) and mutation.get("unsteered_correct", False):
                    worsened += 1
                else:
                    unchanged += 1
    else:
        # Old structure: examples with nested mutations
        for result in results:
            for mutation in result.get("mutations", []):
                total_mutations += 1
                
                # Count unsteered correct
                if mutation.get("unsteered_correct", False):
                    unsteered_correct += 1
                    
                # Count steered correct and compare
                if "steered_correct" in mutation:
                    has_steered_results = True
                    if mutation.get("steered_correct", False):
                        steered_correct += 1
                    
                    # Compare steered and unsteered
                    if mutation.get("steered_correct", False) and not mutation.get("unsteered_correct", False):
                        improved += 1
                    elif not mutation.get("steered_correct", False) and mutation.get("unsteered_correct", False):
                        worsened += 1
                    else:
                        unchanged += 1
    
    # Calculate accuracies
    unsteered_accuracy = unsteered_correct / total_mutations if total_mutations > 0 else 0
    steered_accuracy = steered_correct / total_mutations if total_mutations > 0 else 0
    
    logger.info(f"Total examples: {total_examples}")
    logger.info(f"Total mutations: {total_mutations}")
    logger.info(f"Unsteered correct: {unsteered_correct} ({unsteered_accuracy:.4f})")
    
    if has_steered_results:
        logger.info(f"Steered correct: {steered_correct} ({steered_accuracy:.4f})")
        logger.info(f"Improved: {improved} ({improved/total_mutations:.4f if total_mutations > 0 else 0.0})")
        logger.info(f"Worsened: {worsened} ({worsened/total_mutations:.4f if total_mutations > 0 else 0.0})")
        logger.info(f"Unchanged: {unchanged} ({unchanged/total_mutations:.4f if total_mutations > 0 else 0.0})")
    
    # Return analysis results
    return {
        "total_examples": total_examples,
        "total_mutations": total_mutations,
        "unsteered_correct": unsteered_correct,
        "unsteered_accuracy": unsteered_accuracy,
        "steered_correct": steered_correct,
        "steered_accuracy": steered_accuracy,
        "improved": improved,
        "worsened": worsened,
        "unchanged": unchanged
    }

def select_steering_examples(results, num_positive=10, num_negative=10, balance=True):
    """Select examples for steering based on success/failure."""
    positive_examples = []
    negative_examples = []
    
    for result in results:
        example_id = result.get("example_id")
        expected_type = result.get("expected_type")
        
        for mutation in result.get("mutations", []):
            # Skip if no unsteered prediction
            if "unsteered_prediction" not in mutation:
                continue
                
            # Create a steering example
            example = {
                "example_id": example_id,
                "mutation_number": mutation.get("mutation_number"),
                "input": mutation.get("prefix", ""),
                "expected_type": expected_type,
                "prediction": mutation.get("unsteered_prediction", ""),
                "correct": mutation.get("unsteered_correct", False)
            }
            
            # Collect positive and negative examples
            if example["correct"]:
                positive_examples.append(example)
            else:
                negative_examples.append(example)
    
    # Balance the examples if needed
    if balance:
        # If we don't have enough positive examples, we use all of them
        if len(positive_examples) < num_positive:
            num_positive = len(positive_examples)
            
        # If we don't have enough negative examples, we use all of them
        if len(negative_examples) < num_negative:
            num_negative = len(negative_examples)
            
        # Balance based on the smaller set
        if num_positive > 0 and num_negative > 0:
            # Choose the smaller of the two as the limiting factor
            if num_positive < num_negative:
                num_negative = num_positive
            else:
                num_positive = num_negative
    
    # Randomly select examples
    positive_examples = random.sample(positive_examples, min(num_positive, len(positive_examples)))
    negative_examples = random.sample(negative_examples, min(num_negative, len(negative_examples)))
    
    logger.info(f"Selected {len(positive_examples)} positive examples and {len(negative_examples)} negative examples for steering")
    
    return positive_examples, negative_examples

def process_file(input_file, output_file, batch_size=1, force_rerun=False, save_checkpoints=True):
    """
    Process a file containing mutation results, run inference, and save results.
    
    Args:
        input_file: Path to input file
        output_file: Path to output file
        batch_size: Number of examples to process in each batch
        force_rerun: Whether to force rerun inference even if checkpoint exists
        save_checkpoints: Whether to save checkpoints
    """
    logger.info(f"Input file: {input_file}")
    logger.info(f"Output file: {output_file}")
    logger.info(f"Batch size: {batch_size}")
    logger.info(f"Force rerun: {force_rerun}")
    
    # Load mutation results
    logger.info(f"Loading mutation results from {input_file}")
    with open(input_file, "r") as f:
        examples = json.load(f)
    logger.info(f"Loaded {len(examples)} examples")
    
    # Load model
    model_name = "bigcode/starcoderbase-1b"
    logger.info(f"Loading model {model_name}")
    from nnsight import LanguageModel
    generator = LanguageModel(model_name, device_map="auto")
    tokenizer = generator.tokenizer
    
    # Select some examples for steering
    positive_examples = []
    negative_examples = []
    
    # Find examples with correct and incorrect predictions
    for example in examples:
        mutations = example.get("mutations", [])
        if not mutations:
            continue
        
        for mutation in mutations:
            if mutation.get("prediction", "") == example.get("fim_type", ""):
                positive_examples.append(mutation)
            else:
                negative_examples.append(mutation)
    
    logger.info(f"Selected {len(positive_examples)} positive examples and {len(negative_examples)} negative examples for steering")
    
    # Create steering vectors if examples available
    steering_vectors = None
    layers = None
    if positive_examples and negative_examples:
        steering_vectors, layers = create_steering_vectors(generator, tokenizer, positive_examples, negative_examples)
    
    # Run inference
    results = run_inference(
        examples=examples,
        generator=generator,
        tokenizer=tokenizer,
        batch_size=batch_size,
        steering_vectors=steering_vectors,
        layers=layers,
        scale=1.0,
        force_rerun=force_rerun,
        save_checkpoints=save_checkpoints
    )
    
    # Analyze results
    analyze_results(results)
    
    # Save results
    logger.info(f"Saving results to {output_file}")
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    logger.info("Processing complete")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Type inference with steering")
    parser.add_argument("input_file", help="Path to the input mutation results JSON file")
    parser.add_argument("output_file", help="Path to save the steering results JSON file")
    parser.add_argument("--batch-size", type=int, default=8, help="Batch size for processing examples")
    parser.add_argument("--force-rerun", action="store_true", help="Force rerun inference even if checkpoints exist")
    args = parser.parse_args()
    
    logger.info("Starting type inference with steering")
    logger.info(f"Input file: {args.input_file}")
    logger.info(f"Output file: {args.output_file}")
    logger.info(f"Batch size: {args.batch_size}")
    logger.info(f"Force rerun: {args.force_rerun}")
    
    process_file(args.input_file, args.output_file, batch_size=args.batch_size, force_rerun=args.force_rerun)
    
    logger.info("Script completed successfully")

if __name__ == "__main__":
    main()