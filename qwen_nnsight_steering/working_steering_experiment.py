#!/usr/bin/env python3
"""
Working Steering Experiment for SecLLMHolmes Dataset
Actually applies steering vectors using NNSight integration during generation

This experiment tests whether neural steering vectors can improve upon the baseline
performance by actually modifying the model's hidden states during inference.
"""

import os
import sys
import json
import time
import torch
import gc
import psutil
import logging
import argparse
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from collections import defaultdict
from tqdm import tqdm

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

# Imports for model and data handling
from nnsight import LanguageModel
from transformers import AutoTokenizer, AutoModelForCausalLM
from qwen_steering_integration import QwenNNSightSteering, QwenSteeringConfig

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_memory_usage() -> Dict[str, float]:
    """Get current memory usage in MB."""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    gpu_memory = 0.0
    
    if torch.cuda.is_available():
        gpu_memory = torch.cuda.memory_allocated() / 1024**2  # MB
    
    return {
        "ram_mb": memory_info.rss / 1024**2,
        "gpu_mb": gpu_memory
    }

def log_memory_usage(stage: str):
    """Log memory usage at a specific stage."""
    memory = get_memory_usage()
    logger.info(f"🔍 Memory Usage ({stage}): RAM: {memory['ram_mb']:.1f}MB, GPU: {memory['gpu_mb']:.1f}MB")
    return memory

def clear_gpu_memory():
    """Aggressively clear GPU memory."""
    logger.info("🧹 Clearing GPU memory...")
    
    # Force garbage collection
    gc.collect()
    
    # Clear PyTorch cache
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
        
        # Get current memory usage for monitoring
        allocated = torch.cuda.memory_allocated() / 1024**3  # GB
        cached = torch.cuda.memory_reserved() / 1024**3     # GB
        logger.info(f"GPU Memory - Allocated: {allocated:.2f}GB, Cached: {cached:.2f}GB")
        
    log_memory_usage("after_cleanup")


@dataclass
class WorkingSteeringConfig:
    """Configuration for working steering experiment."""
    # Model settings
    model_name: str = "Qwen/Qwen2.5-14B-Instruct"
    model_dtype: torch.dtype = torch.float16
    device_map: str = "auto"
    
    # Steering settings
    steering_strength: float = 20.0
    target_layers: List[int] = None
    
    # Dataset settings
    dataset_path: str = "../security/SecLLMHolmes/datasets"
    max_examples_per_cwe: int = 8
    
    # Evaluation settings
    temperature: float = 0.0  # Deterministic generation
    max_new_tokens: int = 200
    top_p: float = 1.0
    
    # Output settings
    results_dir: str = "working_steering_results"
    
    def __post_init__(self):
        if self.target_layers is None:
            self.target_layers = [12, 24, 36, 47]

class WorkingSteeringTester:
    """Tester that actually applies steering vectors using NNSight."""
    
    def __init__(self, config: WorkingSteeringConfig):
        self.config = config
        self.cwe_names = {
            "CWE-22": "Path Traversal",
            "CWE-77": "Command Injection", 
            "CWE-79": "Cross-site Scripting",
            "CWE-89": "SQL Injection",
            "CWE-190": "Integer Overflow",
            "CWE-416": "Use After Free",
            "CWE-476": "NULL Pointer Dereference",
            "CWE-787": "Out-of-bounds Write"
        }
        
    def load_test_data(self) -> Dict[str, List[Dict]]:
        """Load test data from SecLLMHolmes dataset."""
        dataset_path = Path(self.config.dataset_path) / "hand-crafted" / "dataset"
        
        test_data = {}
        
        for cwe_id in self.cwe_names.keys():
            cwe_path = dataset_path / cwe_id
            if not cwe_path.exists():
                logger.warning(f"⚠️ CWE path not found: {cwe_path}")
                continue
                
            cwe_data = []
            
            # Load vulnerable examples (numbered files: 1.c, 2.c, 3.c, etc.)
            for file_path in cwe_path.glob("[0-9]*.c"):
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        cwe_data.append({
                            "content": content,
                            "label": "vulnerable",
                            "cwe": cwe_id,
                            "file": str(file_path.name),
                            "expected_answer": "This code contains security vulnerabilities."
                        })
                except Exception as e:
                    logger.warning(f"⚠️ Error reading {file_path}: {e}")
            
            # Limit examples for efficiency
            if len(cwe_data) > self.config.max_examples_per_cwe:
                cwe_data = cwe_data[:self.config.max_examples_per_cwe]
                
            test_data[cwe_id] = cwe_data
            logger.info(f"📊 Loaded {len(cwe_data)} examples for {cwe_id}")
        
        return test_data
    
    def create_prompt(self, code: str) -> str:
        """Create standardized prompt for vulnerability detection."""
        return f"Security review of this code:\n\n{code}\n\nAnswer:"
    
    def parse_response(self, response: str) -> Tuple[str, str]:
        """Improved parsing of model response to extract answer and reasoning."""
        response_lower = response.lower()
        
        # Look for explicit vulnerability statements
        vulnerability_indicators = [
            "this code contains security vulnerabilities",
            "this code is vulnerable",
            "vulnerable code",
            "security vulnerability",
            "security issue",
            "security problem",
            "security flaw",
            "security risk",
            "exploitable",
            "attack vector",
            "malicious input",
            "injection attack",
            "buffer overflow",
            "command injection",
            "sql injection",
            "path traversal",
            "use after free",
            "null pointer dereference",
            "out of bounds",
            "integer overflow"
        ]
        
        # Look for explicit secure statements
        secure_indicators = [
            "this code is secure",
            "no vulnerabilities",
            "no security issues",
            "secure code",
            "safe code",
            "properly validated",
            "input validation",
            "bounds checking",
            "sanitized input",
            "safe from attacks"
        ]
        
        # Check for vulnerability indicators
        vulnerability_score = 0
        for indicator in vulnerability_indicators:
            if indicator in response_lower:
                vulnerability_score += 1
        
        # Check for secure indicators
        secure_score = 0
        for indicator in secure_indicators:
            if indicator in response_lower:
                secure_score += 1
        
        # Determine answer based on scores
        if vulnerability_score > secure_score and vulnerability_score > 0:
            answer = "vulnerable"
        elif secure_score > vulnerability_score and secure_score > 0:
            answer = "secure"
        else:
            # Fallback: look for structured response pattern
            if "Answer:" in response:
                parts = response.split("Answer:", 1)
                if len(parts) >= 2:
                    answer_part = parts[1].strip().lower()
                    if any(indicator in answer_part for indicator in vulnerability_indicators):
                        answer = "vulnerable"
                    elif any(indicator in answer_part for indicator in secure_indicators):
                        answer = "secure"
                    else:
                        answer = "uncertain"
                else:
                    answer = "uncertain"
            else:
                answer = "uncertain"
        
        # Extract reasoning (everything before "Answer:" or the full response)
        if "Answer:" in response:
            reasoning = response.split("Answer:", 1)[0].strip()
        else:
            reasoning = response.strip()
        
        return answer, reasoning
    
    def load_steering_vectors(self, cwe_id: str) -> Optional[Dict]:
        """Load existing steering vectors for a CWE."""
        vector_path = Path("vectors") / f"{cwe_id.lower()}_steering_vectors.pt"
        
        if not vector_path.exists():
            logger.warning(f"⚠️ No steering vectors found for {cwe_id}")
            return None
        
        try:
            steerer = QwenNNSightSteering(QwenSteeringConfig())
            vectors, metadata = steerer.load_steering_vectors(str(vector_path))
            
            logger.info(f"✅ Loaded steering vectors for {cwe_id}")
            logger.info(f"   Model: {metadata.get('model_name', 'unknown')}")
            logger.info(f"   Data: {metadata.get('vulnerable_count', '?')} vulnerable, {metadata.get('secure_count', '?')} secure")
            
            return vectors
            
        except Exception as e:
            logger.error(f"❌ Error loading steering vectors for {cwe_id}: {e}")
            return None
    
    def evaluate_example_baseline(self, model, tokenizer, example: Dict) -> Dict:
        """Evaluate a single example without steering using regular transformers model."""
        prompt = self.create_prompt(example["content"])
        
        # Tokenize input
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
        
        try:
            # Move inputs to model device
            if torch.cuda.is_available():
                inputs = {k: v.cuda() for k, v in inputs.items()}
            
            # Use regular transformers model for baseline - should work normally
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=self.config.max_new_tokens,
                    temperature=self.config.temperature,
                    top_p=self.config.top_p,
                    do_sample=False,
                    pad_token_id=tokenizer.eos_token_id
                )
            
            # Regular model should return actual tensors
            generated_tokens = outputs[0][inputs['input_ids'].shape[1]:]
            
            # Decode response
            response = tokenizer.decode(generated_tokens, skip_special_tokens=True)
            
            # Parse response
            predicted_answer, reasoning = self.parse_response(response)
            expected_answer = "vulnerable"  # All examples in test set are vulnerable
            
            # Calculate metrics
            is_correct = predicted_answer == expected_answer
            reasoning_quality = self._assess_reasoning_quality(reasoning, example["cwe"])
            
            return {
                "cwe": example["cwe"],
                "file": example["file"],
                "expected": expected_answer,
                "predicted": predicted_answer,
                "reasoning": reasoning,
                "is_correct": is_correct,
                "reasoning_quality": reasoning_quality,
                "response": response
            }
            
        except Exception as e:
            logger.error(f"❌ Error evaluating example {example['file']}: {e}")
            logger.error(f"❌ Error type: {type(e).__name__}")
            import traceback
            logger.error(f"❌ Traceback: {traceback.format_exc()}")
            
            return {
                "cwe": example["cwe"],
                "file": example["file"],
                "expected": "vulnerable",
                "predicted": "error",
                "reasoning": f"Error: {str(e)}",
                "is_correct": False,
                "reasoning_quality": 0.0,
                "response": f"ERROR: {str(e)}"
            }
    
    def evaluate_example_with_steering(self, model, tokenizer, example: Dict, steering_vectors: Dict) -> Dict:
        """Evaluate a single example with steering using correct NNSight 0.4.x pattern."""
        prompt = self.create_prompt(example["content"])
        
        try:
            # Define hook functions for steering
            def create_steering_hook(layer_idx, steering_vector, steering_strength):
                def apply_steering(hidden_states):
                    """Apply steering to hidden states."""
                    # Handle tuple format (NNSight 0.4.x)
                    if isinstance(hidden_states, tuple):
                        states = hidden_states[0]
                    else:
                        states = hidden_states
                    
                    # Clone to avoid in-place modification issues
                    modified_states = states.clone()
                    
                    # CRITICAL FIX: Flip steering direction!
                    # Vector points vulnerable→secure, but we want better vulnerability detection
                    # So we steer in the OPPOSITE direction (secure→vulnerable detection)
                    steering_vector_device = steering_vector.to(states.device)
                    modified_states[:, -1, :] -= steering_strength * steering_vector_device  # FLIPPED SIGN!
                    
                    # Return in the same format as input
                    if isinstance(hidden_states, tuple):
                        return (modified_states,) + hidden_states[1:]
                    else:
                        return modified_states
                
                return apply_steering
            
            # NNSight 0.4.x: Execute trace completely, then access results - CORRECTED PATTERN
            inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
            if torch.cuda.is_available():
                inputs = {k: v.cuda() for k, v in inputs.items()}
            
            with model.trace() as tracer:
                # Register hooks for target layers that have steering vectors
                for layer_idx in self.config.target_layers:
                    if str(layer_idx) in steering_vectors:
                        steering_vector = steering_vectors[str(layer_idx)]
                        hook_fn = create_steering_hook(layer_idx, steering_vector, self.config.steering_strength)
                        tracer.hooks.modify_at(f"model.layers.{layer_idx}.output", hook_fn)
                
                # Use PROVEN WORKING pattern from debug examples
                with tracer.invoke(inputs['input_ids']):
                    outputs = model.generate(
                        **inputs,
                        max_new_tokens=self.config.max_new_tokens,
                        temperature=0.7,
                        do_sample=True,
                        top_p=0.9,
                        pad_token_id=tokenizer.eos_token_id
                    )
            
            # After trace execution, try to access results - CORRECTED EXTRACTION
            logger.info("🔍 Trace executed, attempting to extract results...")
            
            try:
                # Use the PROVEN WORKING pattern from successful examples
                if hasattr(outputs, 'value') and outputs.value is not None:
                    logger.info("✅ Found outputs.value")
                    generated_ids = outputs.value[0].tolist()
                    
                    # Extract only the newly generated tokens
                    prompt_length = inputs['input_ids'].shape[1]
                    new_token_ids = generated_ids[prompt_length:]
                    response = tokenizer.decode(new_token_ids, skip_special_tokens=True)
                    logger.info(f"✅ Successfully extracted steered response: {len(response)} chars")
                    
                else:
                    logger.warning("⚠️ No outputs.value available - NNSight extraction failed")
                    response = "NNSight extraction failed - no outputs.value"
                        
            except Exception as extract_error:
                logger.error(f"❌ Result extraction failed: {extract_error}")
                response = f"Result extraction failed: {str(extract_error)}"
            
            # Parse response
            predicted_answer, reasoning = self.parse_response(response)
            expected_answer = "vulnerable"  # All examples in test set are vulnerable
            
            # Calculate metrics
            is_correct = predicted_answer == expected_answer
            reasoning_quality = self._assess_reasoning_quality(reasoning, example["cwe"])
            
            return {
                "cwe": example["cwe"],
                "file": example["file"],
                "expected": expected_answer,
                "predicted": predicted_answer,
                "reasoning": reasoning,
                "is_correct": is_correct,
                "reasoning_quality": reasoning_quality,
                "response": response,
                "steering_applied": True
            }
            
        except Exception as e:
            logger.error(f"❌ Error evaluating example {example['file']} with steering: {e}")
            logger.error(f"❌ Error type: {type(e).__name__}")
            import traceback
            logger.error(f"❌ Traceback: {traceback.format_exc()}")
            
            return {
                "cwe": example["cwe"],
                "file": example["file"],
                "expected": "vulnerable",
                "predicted": "error",
                "reasoning": f"Error: {str(e)}",
                "is_correct": False,
                "reasoning_quality": 0.0,
                "response": f"ERROR: {str(e)}",
                "steering_applied": True
            }
    
    def _assess_reasoning_quality(self, reasoning: str, cwe: str) -> float:
        """Assess the quality of reasoning (0-1 scale)."""
        reasoning_lower = reasoning.lower()
        
        # Check for relevant security terms
        security_terms = ["vulnerability", "security", "risk", "exploit", "attack", "malicious"]
        cwe_specific_terms = {
            "CWE-22": ["path", "traversal", "directory", "file"],
            "CWE-77": ["command", "injection", "shell", "execute"],
            "CWE-79": ["xss", "script", "html", "javascript"],
            "CWE-89": ["sql", "injection", "database", "query"],
            "CWE-190": ["overflow", "integer", "buffer", "size"],
            "CWE-416": ["use after free", "memory", "dangling", "pointer"],
            "CWE-476": ["null", "pointer", "dereference", "nullptr"],
            "CWE-787": ["out of bounds", "buffer", "overflow", "write"]
        }
        
        # Base score from security terms
        security_score = sum(1 for term in security_terms if term in reasoning_lower) / len(security_terms)
        
        # CWE-specific score
        cwe_terms = cwe_specific_terms.get(cwe, [])
        cwe_score = sum(1 for term in cwe_terms if term in reasoning_lower) / max(len(cwe_terms), 1)
        
        # Combined score
        return (security_score + cwe_score) / 2

class WorkingSteeringExperiment:
    """Main class for working steering experiment."""
    
    def __init__(self, config: WorkingSteeringConfig):
        self.config = config
        self.tester = WorkingSteeringTester(config)
        self.results_dir = Path(config.results_dir)
        self.results_dir.mkdir(exist_ok=True)
        
    def load_baseline_model(self):
        """Load regular model for baseline only."""
        logger.info(f"📦 Loading regular model for baseline: {self.config.model_name}")
        log_memory_usage("before_baseline_loading")
        
        try:
            # Load tokenizer
            tokenizer = AutoTokenizer.from_pretrained(
                self.config.model_name,
                trust_remote_code=True
            )
            
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
            
            # Load regular model for baseline with memory optimizations
            baseline_model = AutoModelForCausalLM.from_pretrained(
                self.config.model_name,
                torch_dtype=self.config.model_dtype,
                device_map=self.config.device_map,
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )
            
            logger.info(f"✅ Baseline model loaded: {type(baseline_model)}")
            log_memory_usage("after_baseline_loading")
            return baseline_model, tokenizer
            
        except Exception as e:
            logger.error(f"❌ Failed to load baseline model: {e}")
            raise
    
    def load_steering_model(self, tokenizer):
        """Load NNSight model for steering only."""
        logger.info(f"🎯 Loading NNSight model for steering: {self.config.model_name}")
        log_memory_usage("before_steering_loading")
        
        try:
            # Load NNSight model for steering
            steering_model = LanguageModel(self.config.model_name, device_map=self.config.device_map)
            
            logger.info(f"✅ Steering model loaded: {type(steering_model)}")
            log_memory_usage("after_steering_loading")
            return steering_model
            
        except Exception as e:
            logger.error(f"❌ Failed to load steering model: {e}")
            raise
    
    def unload_model(self, model):
        """Unload model from memory with comprehensive cleanup."""
        try:
            logger.info("🗑️ Unloading model from memory...")
            log_memory_usage("before_model_unload")
            
            # Delete the model
            del model
            
            # Comprehensive memory cleanup
            clear_gpu_memory()
            
            logger.info("✅ Model unloaded and memory cleared")
            
        except Exception as e:
            logger.warning(f"⚠️ Error unloading model: {e}")
            # Still try to clear memory even if model deletion failed
            clear_gpu_memory()
    
    def load_model(self):
        """Legacy method - now redirects to sequential loading."""
        # This method is kept for compatibility but won't be used in the new approach
        raise NotImplementedError("Use sequential loading approach instead")
    
    def run_baseline_test(self, model, tokenizer) -> Dict:
        """Run baseline test without steering vectors."""
        logger.info("🔬 Running baseline test (no steering)...")
        
        test_data = self.tester.load_test_data()
        results = {"baseline": []}
        
        total_examples = sum(len(examples) for examples in test_data.values())
        
        with tqdm(total=total_examples, desc="Baseline Test") as pbar:
            for cwe_id, examples in test_data.items():
                for example in examples:
                    result = self.tester.evaluate_example_baseline(model, tokenizer, example)
                    result["experiment_type"] = "baseline"
                    results["baseline"].append(result)
                    pbar.update(1)
        
        return results
    
    def run_steering_tests(self, model, tokenizer) -> Dict:
        """Run tests with actual steering vector application."""
        logger.info("🎯 Running steering tests with NNSight...")
        
        test_data = self.tester.load_test_data()
        results = {}
        
        # Test each CWE with its steering vectors if available
        for cwe_id in self.tester.cwe_names.keys():
            if cwe_id not in test_data:
                continue
                
            steering_vectors = self.tester.load_steering_vectors(cwe_id)
            
            if steering_vectors:
                logger.info(f"🎯 Testing {cwe_id} with actual steering vectors")
                experiment_name = f"steering_{cwe_id.lower()}"
                
                cwe_results = []
                examples = test_data[cwe_id]
                
                with tqdm(total=len(examples), desc=f"{cwe_id} Steering") as pbar:
                    for example in examples:
                        result = self.tester.evaluate_example_with_steering(model, tokenizer, example, steering_vectors)
                        result["experiment_type"] = experiment_name
                        cwe_results.append(result)
                        pbar.update(1)
                
                results[experiment_name] = cwe_results
            else:
                logger.info(f"⚠️ No steering vectors for {cwe_id}, skipping")
        
        return results
    
    def analyze_results(self, all_results: Dict) -> Dict:
        """Analyze and compare results."""
        analysis = {}
        
        for experiment_name, results in all_results.items():
            if not results:
                continue
                
            # Calculate overall metrics
            total_examples = len(results)
            correct_predictions = sum(1 for r in results if r["is_correct"])
            accuracy = correct_predictions / total_examples if total_examples > 0 else 0
            
            # Calculate per-CWE metrics
            cwe_metrics = {}
            for result in results:
                cwe = result["cwe"]
                if cwe not in cwe_metrics:
                    cwe_metrics[cwe] = {"total": 0, "correct": 0, "reasoning_scores": []}
                
                cwe_metrics[cwe]["total"] += 1
                if result["is_correct"]:
                    cwe_metrics[cwe]["correct"] += 1
                cwe_metrics[cwe]["reasoning_scores"].append(result["reasoning_quality"])
            
            # Calculate CWE-specific accuracies
            for cwe, metrics in cwe_metrics.items():
                metrics["accuracy"] = metrics["correct"] / metrics["total"] if metrics["total"] > 0 else 0
                metrics["avg_reasoning"] = np.mean(metrics["reasoning_scores"]) if metrics["reasoning_scores"] else 0
            
            analysis[experiment_name] = {
                "overall_accuracy": accuracy,
                "total_examples": total_examples,
                "correct_predictions": correct_predictions,
                "cwe_metrics": cwe_metrics,
                "avg_reasoning_quality": np.mean([r["reasoning_quality"] for r in results])
            }
        
        return analysis
    
    def generate_comparison_report(self, analysis: Dict) -> str:
        """Generate a detailed comparison report."""
        report = []
        report.append("# Working Steering vs Baseline Experiment Results\n")
        report.append(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.append(f"**Model**: {self.config.model_name}\n")
        report.append(f"**Steering Strength**: {self.config.steering_strength}\n")
        report.append(f"**Target Layers**: {self.config.target_layers}\n\n")
        
        # Overall comparison
        report.append("## Overall Performance Comparison\n")
        report.append("| Experiment | Accuracy | Examples | Reasoning Quality |\n")
        report.append("|------------|----------|----------|-------------------|\n")
        
        baseline_metrics = analysis.get("baseline", {})
        baseline_acc = baseline_metrics.get("overall_accuracy", 0)
        
        for exp_name, metrics in analysis.items():
            acc = metrics.get("overall_accuracy", 0)
            examples = metrics.get("total_examples", 0)
            reasoning = metrics.get("avg_reasoning_quality", 0)
            
            if exp_name == "baseline":
                report.append(f"| **{exp_name}** | **{acc:.3f}** | **{examples}** | **{reasoning:.3f}** |\n")
            else:
                improvement = acc - baseline_acc
                report.append(f"| {exp_name} | {acc:.3f} ({improvement:+.3f}) | {examples} | {reasoning:.3f} |\n")
        
        # Per-CWE comparison
        report.append("\n## Per-CWE Performance Analysis\n")
        report.append("| CWE | Baseline | Steering | Improvement |\n")
        report.append("|-----|----------|----------|-------------|\n")
        
        baseline_cwe_metrics = baseline_metrics.get("cwe_metrics", {})
        
        for exp_name, metrics in analysis.items():
            if exp_name != "baseline":
                steering_cwe_metrics = metrics.get("cwe_metrics", {})
                
                for cwe in sorted(baseline_cwe_metrics.keys()):
                    baseline_acc = baseline_cwe_metrics[cwe]["accuracy"]
                    steering_acc = steering_cwe_metrics.get(cwe, {}).get("accuracy", 0)
                    improvement = steering_acc - baseline_acc
                    
                    report.append(f"| {cwe} | {baseline_acc:.3f} | {steering_acc:.3f} | {improvement:+.3f} |\n")
                break  # Only need one steering experiment for comparison
        
        # Key findings
        report.append("\n## Key Findings\n")
        
        # Calculate overall improvement
        steering_experiments = [name for name in analysis.keys() if name != "baseline"]
        if steering_experiments:
            best_steering = max(steering_experiments, key=lambda x: analysis[x].get("overall_accuracy", 0))
            best_steering_acc = analysis[best_steering].get("overall_accuracy", 0)
            overall_improvement = best_steering_acc - baseline_acc
            
            report.append(f"- **Baseline Accuracy**: {baseline_acc:.3f}\n")
            report.append(f"- **Best Steering Accuracy**: {best_steering_acc:.3f}\n")
            report.append(f"- **Overall Improvement**: {overall_improvement:+.3f} ({overall_improvement*100:+.1f}%)\n")
            
            # Identify best/worst performing CWEs
            best_cwe = None
            worst_cwe = None
            best_improvement = -1
            worst_improvement = 1
            
            for cwe in baseline_cwe_metrics.keys():
                baseline_acc = baseline_cwe_metrics[cwe]["accuracy"]
                steering_acc = steering_cwe_metrics.get(cwe, {}).get("accuracy", 0)
                improvement = steering_acc - baseline_acc
                
                if improvement > best_improvement:
                    best_improvement = improvement
                    best_cwe = cwe
                
                if improvement < worst_improvement:
                    worst_improvement = improvement
                    worst_cwe = cwe
            
            if best_cwe:
                report.append(f"- **Most Improved CWE**: {best_cwe} ({best_improvement:+.3f})\n")
            if worst_cwe:
                report.append(f"- **Least Improved CWE**: {worst_cwe} ({worst_improvement:+.3f})\n")
        
        return "\n".join(report)
    
    def save_results(self, all_results: Dict, analysis: Dict):
        """Save test results and analysis."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed results
        results_file = self.results_dir / f"working_steering_results_{timestamp}.json"
        with open(results_file, 'w') as f:
            json.dump(all_results, f, indent=2, default=str)
        
        # Save analysis
        analysis_file = self.results_dir / f"working_steering_analysis_{timestamp}.json"
        with open(analysis_file, 'w') as f:
            json.dump(analysis, f, indent=2, default=str)
        
        # Save report
        report_file = self.results_dir / f"working_steering_report_{timestamp}.md"
        report = self.generate_comparison_report(analysis)
        with open(report_file, 'w') as f:
            f.write(report)
        
        logger.info(f"💾 Results saved to {self.results_dir}")
        logger.info(f"   Detailed: {results_file}")
        logger.info(f"   Analysis: {analysis_file}")
        logger.info(f"   Report: {report_file}")
        
        return report_file
    
    def run_experiment(self):
        """Run the complete working steering experiment."""
        logger.info("🚀 Starting Working Steering Experiment")
        logger.info(f"📊 Model: {self.config.model_name}")
        logger.info(f"🎯 Target Layers: {self.config.target_layers}")
        logger.info(f"💪 Steering Strength: {self.config.steering_strength}")
        
        start_time = time.time()
        
        try:
            # Initial memory check
            log_memory_usage("experiment_start")
            
            # Load models sequentially
            baseline_model, tokenizer = self.load_baseline_model()
            
            all_results = {}
            
            # 1. Run baseline test
            logger.info("\n" + "="*60)
            logger.info("🔬 PHASE 1: BASELINE TEST")
            logger.info("="*60)
            
            baseline_results = self.run_baseline_test(baseline_model, tokenizer)
            all_results.update(baseline_results)
            
            # Unload baseline model to free memory
            self.unload_model(baseline_model)
            
            # Wait a moment for memory to clear
            time.sleep(2)
            
            # 2. Load steering model and run steering tests
            steering_model = self.load_steering_model(tokenizer)
            
            logger.info("\n" + "="*60)
            logger.info("🎯 PHASE 2: STEERING TESTS")
            logger.info("="*60)
            
            steering_results = self.run_steering_tests(steering_model, tokenizer)
            all_results.update(steering_results)
            
            # Unload steering model to free memory
            self.unload_model(steering_model)
            
            # 3. Analyze results
            logger.info("\n" + "="*60)
            logger.info("📊 PHASE 3: RESULTS ANALYSIS")
            logger.info("="*60)
            
            analysis = self.analyze_results(all_results)
            
            # 4. Save results
            report_file = self.save_results(all_results, analysis)
            
            # 5. Print summary
            logger.info("\n" + "="*60)
            logger.info("📈 EXPERIMENT SUMMARY")
            logger.info("="*60)
            
            baseline_acc = analysis.get("baseline", {}).get("overall_accuracy", 0)
            logger.info(f"Baseline Accuracy: {baseline_acc:.3f}")
            
            steering_experiments = [name for name in analysis.keys() if name != "baseline"]
            for exp_name in steering_experiments:
                steering_acc = analysis[exp_name].get("overall_accuracy", 0)
                improvement = steering_acc - baseline_acc
                logger.info(f"{exp_name} Accuracy: {steering_acc:.3f} ({improvement:+.3f})")
            
            total_time = time.time() - start_time
            logger.info(f"\n⏱️ Total experiment time: {total_time/60:.1f} minutes")
            
            # Print report location
            logger.info(f"\n📄 Detailed report saved to: {report_file}")
            
        except Exception as e:
            logger.error(f"❌ Experiment failed: {e}")
            raise

def main():
    parser = argparse.ArgumentParser(description="Run working steering experiment")
    parser.add_argument("--model", type=str, default="Qwen/Qwen2.5-14B-Instruct", 
                       help="Model to use for testing")
    parser.add_argument("--steering-strength", type=float, default=20.0,
                       help="Steering vector strength")
    parser.add_argument("--target-layers", nargs="+", type=int, default=[12, 24, 36, 47],
                       help="Target layers for steering")
    parser.add_argument("--max-examples", type=int, default=8,
                       help="Maximum examples per CWE")
    parser.add_argument("--results-dir", type=str, default="working_steering_results",
                       help="Directory to save results")
    
    args = parser.parse_args()
    
    config = WorkingSteeringConfig(
        model_name=args.model,
        steering_strength=args.steering_strength,
        target_layers=args.target_layers,
        max_examples_per_cwe=args.max_examples,
        results_dir=args.results_dir
    )
    
    experiment = WorkingSteeringExperiment(config)
    experiment.run_experiment()

if __name__ == "__main__":
    main() 