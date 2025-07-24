#!/usr/bin/env python3
"""
Extended baseline experiment for additional large models with memory management.
Includes: Qwen14B, Phi3-Medium-14B, DeepSeekCoder-33B, Gemma2-27B, StarCoder2-15B
"""

import os
import sys
import json
import time
import torch
import gc
import logging
from typing import Dict, List, Any
from pathlib import Path
from datetime import datetime

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from comprehensive_baseline_experiment import ComprehensiveSecLLMHolmesExperiment, ExperimentConfig

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExtendedBaselineExperiment(ComprehensiveSecLLMHolmesExperiment):
    """Extended experiment with aggressive memory management for large models."""
    
    def __init__(self, config: ExperimentConfig):
        super().__init__(config)
        
    def clear_gpu_memory(self):
        """Aggressively clear GPU memory between models."""
        logger.info("Clearing GPU memory...")
        
        # Force garbage collection
        gc.collect()
        
        # Clear PyTorch cache
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
            
            # Get current memory usage
            allocated = torch.cuda.memory_allocated() / 1024**3  # GB
            cached = torch.cuda.memory_reserved() / 1024**3     # GB
            logger.info(f"GPU Memory - Allocated: {allocated:.2f}GB, Cached: {cached:.2f}GB")
    
    def run_model_experiment(self, model_name: str, dataset: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Run experiment for a single model with aggressive memory management."""
        logger.info(f"Starting extended experiment for model: {model_name}")
        
        # Clear memory before loading model
        self.clear_gpu_memory()
        
        try:
            # Import transformers here to avoid early GPU allocation
            from transformers import AutoTokenizer, AutoModelForCausalLM
            
            # Load model and tokenizer with memory optimizations
            logger.info(f"Loading model: {model_name}")
            
            # Special handling for different model families
            model_kwargs = {
                "torch_dtype": torch.float16,
                "device_map": "auto",
                "trust_remote_code": True,
                "low_cpu_mem_usage": True
            }
            
            # Model-specific optimizations
            if "qwen" in model_name.lower():
                model_kwargs["use_flash_attention_2"] = False  # Compatibility
            elif "phi" in model_name.lower():
                model_kwargs["trust_remote_code"] = True
            elif "deepseek" in model_name.lower():
                model_kwargs["torch_dtype"] = torch.bfloat16  # Better for DeepSeek
            elif "gemma" in model_name.lower():
                model_kwargs["torch_dtype"] = torch.bfloat16  # Better for Gemma
            
            tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
            
            model = AutoModelForCausalLM.from_pretrained(model_name, **model_kwargs)
            
            # Check memory after loading
            if torch.cuda.is_available():
                allocated = torch.cuda.memory_allocated() / 1024**3
                logger.info(f"Model loaded - GPU Memory: {allocated:.2f}GB")
            
            model_results = {
                "model_name": model_name,
                "config": self.config.__dict__,
                "trials": []
            }
            
            # Run multiple trials
            for trial_num in range(1, self.config.num_trials + 1):
                logger.info(f"Running trial {trial_num}/{self.config.num_trials} for {model_name}")
                
                trial_results = {
                    "trial": trial_num,
                    "per_cwe_results": {},
                    "start_time": time.time()
                }
                
                # Process each CWE
                for cwe, examples in dataset.items():
                    logger.info(f"Processing {cwe.upper()} ({len(examples)} examples)")
                    
                    cwe_results = {"examples": []}
                    
                    # Process each example
                    for example in examples:
                        prompt = self.format_prompt(example)
                        
                        # Tokenize with truncation for large models
                        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
                        inputs = {k: v.to(model.device) for k, v in inputs.items()}
                        
                        with torch.no_grad():
                            try:
                                outputs = model.generate(
                                    **inputs,
                                    temperature=self.config.temperature,
                                    top_p=self.config.top_p,
                                    max_new_tokens=self.config.max_new_tokens,
                                    pad_token_id=tokenizer.eos_token_id,
                                    do_sample=False,
                                    eos_token_id=tokenizer.eos_token_id
                                )
                            except RuntimeError as e:
                                if "out of memory" in str(e).lower():
                                    logger.warning(f"OOM error for {model_name}, skipping this example")
                                    continue
                                else:
                                    raise e
                        
                        # Decode response
                        generated_tokens = outputs[0][inputs['input_ids'].shape[1]:]
                        raw_response = tokenizer.decode(generated_tokens, skip_special_tokens=True)
                        
                        # Parse response
                        predicted_answer, predicted_reason = self.parse_response(raw_response)
                        
                        # Calculate accuracy
                        ground_truth = "yes" if example["is_vulnerable"] else "no"
                        accuracy = 1.0 if predicted_answer == ground_truth else 0.0
                        
                        # Store results
                        example_results = {
                            "example": example,
                            "prompt": prompt,
                            "raw_response": raw_response,
                            "predicted_answer": predicted_answer,
                            "predicted_reason": predicted_reason,
                            "accuracy": accuracy
                        }
                        
                        cwe_results["examples"].append(example_results)
                        
                        # Clear cache after each example for large models
                        if torch.cuda.is_available() and "33b" in model_name.lower():
                            torch.cuda.empty_cache()
                    
                    # Calculate CWE-level metrics
                    if cwe_results["examples"]:
                        accuracies = [ex["accuracy"] for ex in cwe_results["examples"]]
                        cwe_results["accuracy"] = sum(accuracies) / len(accuracies)
                        cwe_results["std_accuracy"] = 0.0  # Deterministic with temp=0
                        cwe_results["num_examples"] = len(accuracies)
                    else:
                        cwe_results["accuracy"] = 0.0
                        cwe_results["std_accuracy"] = 0.0
                        cwe_results["num_examples"] = 0
                    
                    trial_results["per_cwe_results"][cwe] = cwe_results
                
                # Calculate trial-level metrics
                trial_results["end_time"] = time.time()
                trial_results["duration"] = trial_results["end_time"] - trial_results["start_time"]
                
                # Overall accuracy across all CWEs for this trial
                all_accuracies = []
                for cwe_results in trial_results["per_cwe_results"].values():
                    all_accuracies.extend([ex["accuracy"] for ex in cwe_results["examples"]])
                
                if all_accuracies:
                    trial_results["overall_accuracy"] = sum(all_accuracies) / len(all_accuracies)
                    trial_results["overall_std"] = 0.0  # Deterministic
                else:
                    trial_results["overall_accuracy"] = 0.0
                    trial_results["overall_std"] = 0.0
                
                model_results["trials"].append(trial_results)
                
                # Save intermediate results
                self.save_intermediate_results(model_name, trial_num, trial_results)
                
                # Clear cache between trials
                self.clear_gpu_memory()
            
            # Calculate model-level aggregated metrics
            model_results["aggregated_metrics"] = self.calculate_aggregated_metrics(model_results["trials"])
            
            return model_results
            
        except Exception as e:
            logger.error(f"Error running experiment for {model_name}: {e}")
            return {
                "model_name": model_name,
                "error": str(e),
                "trials": [],
                "aggregated_metrics": {"overall_metrics": {"mean_accuracy": 0.0}}
            }
        
        finally:
            # Always clean up model to free memory
            try:
                del model
                del tokenizer
            except:
                pass
            self.clear_gpu_memory()

def main():
    """Run extended baseline experiments for additional large models."""
    
    # Configuration for extended models
    config = ExperimentConfig(
        models=[
            "Qwen/Qwen2.5-Coder-14B-Instruct",      # Qwen 14B
            "microsoft/Phi-3-medium-14b-instruct",   # Phi3 Medium 14B  
            "deepseek-ai/deepseek-coder-33b-base",   # DeepSeek Coder 33B
            "google/gemma-2-27b",                    # Gemma 2 27B
            "bigcode/starcoder2-15b"                 # StarCoder2 15B
        ],
        num_trials=3,  # Keep consistent with first experiment
        temperature=0.0,
        top_p=1.0,
        max_new_tokens=200,
        output_dir="extended_results"
    )
    
    # Create extended experiment
    experiment = ExtendedBaselineExperiment(config)
    
    # Run comprehensive experiments
    logger.info("Starting extended baseline experiments for large models")
    logger.info(f"Models: {config.models}")
    logger.info("⚠️  Large models - expect longer runtime and high memory usage")
    
    experiment.run_comprehensive_experiment()

if __name__ == "__main__":
    main() 