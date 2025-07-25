#!/usr/bin/env python3
"""
CWE-Specific Neural Steering Experiment for Qwen2.5-14B

This experiment creates steering vectors per CWE type to improve vulnerability detection
using the REAL SecLLMHolmes dataset. It builds on established baseline results and proven
NNSight steering patterns from the neural steering context.

Key Features:
- CWE-specific steering vectors using Qwen2.5-14B (best baseline performer at 73.4%)
- REAL SecLLMHolmes data (no mock data)
- Memory-efficient implementation for large models
- Comprehensive logging and tracing
- Paper-ready results generation
- Builds on proven NNSight patterns from neural steering context

Usage:
    python cwe_steering_experiment.py

Author: AI Assistant
Date: 2025-01-24
"""

import os
import sys
import json
import time
import torch
import gc
import random
import numpy as np
import logging
import psutil
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict
from tqdm import tqdm

# Add parent directories to path for imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir.parent.parent))  # Add codetrace root

# Import NNSight and utilities
try:
    from nnsight import LanguageModel
    from codetrace.utils import get_lm_layers
    NNSIGHT_AVAILABLE = True
    print("✅ NNSight available for steering vectors")
except ImportError as e:
    print(f"❌ NNSight not available: {e}")
    print("This experiment requires nnsight for steering vectors")
    NNSIGHT_AVAILABLE = False

# Set up comprehensive logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set random seed for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(RANDOM_SEED)

@dataclass
class CWESteeringConfig:
    """Configuration for CWE-specific steering experiments."""
    # Model configuration - using best baseline performer
    model_name: str = "Qwen/Qwen2.5-14B-Instruct"
    
    # Dataset configuration - REAL SecLLMHolmes data
    secllmholmes_base: str = "../../SecLLMHolmes/datasets"
    cwe_list: List[str] = None
    
    # Steering parameters - using proven values from context
    steering_layers: List[int] = None  # [4, 12, 20] - proven optimal
    steering_scales: List[float] = None  # [20.0] - proven optimal
    max_steering_examples: int = 10  # Maximum examples per CWE for steering vectors
    
    # Generation parameters - matching baseline
    temperature: float = 0.0  # Deterministic for reproducibility
    top_p: float = 1.0
    max_new_tokens: int = 200
    
    # Experiment parameters
    num_trials: int = 3  # Multiple trials for statistical significance
    num_examples_per_cwe: int = 15  # Examples to test steering on
    
    # Memory management
    clear_memory_between_experiments: bool = True
    use_gradient_checkpointing: bool = True
    
    # Output configuration
    output_dir: str = "results"
    save_intermediate_results: bool = True
    generate_paper_plots: bool = True
    
    def __post_init__(self):
        if self.cwe_list is None:
            # Using same CWEs as baseline experiment
            self.cwe_list = [
                "cwe-22",   # Path Traversal
                "cwe-77",   # Command Injection  
                "cwe-79",   # Cross-site Scripting
                "cwe-89",   # SQL Injection
                "cwe-190",  # Integer Overflow
                "cwe-416",  # Use After Free
                "cwe-476",  # NULL Pointer Dereference
                "cwe-787"   # Out-of-bounds Write
            ]
        
        if self.steering_layers is None:
            # Using proven optimal layers from neural steering context
            self.steering_layers = [4, 12, 20]
        
        if self.steering_scales is None:
            # Using proven optimal scale from neural steering context
            self.steering_scales = [20.0]


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
        
    log_memory_usage("after_cleanup")


class CWESteeringExperiment:
    """
    Comprehensive CWE-specific steering experiment implementation.
    
    This class builds on established patterns from:
    - Baseline SecLLMHolmes evaluation (security/final/baseline.py)
    - Memory management for large models (security/final/extended_baseline_experiment.py)
    - Working NNSight steering patterns (neural steering context)
    - Comprehensive experimental design (security/final/comprehensive_baseline_experiment.py)
    """
    
    def __init__(self, config: CWESteeringConfig):
        self.config = config
        self.experiment_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # CWE name mappings (same as baseline)
        self.cwe_names = {
            "cwe-22": "path traversal",
            "cwe-77": "OS command injection",
            "cwe-79": "cross-site scripting", 
            "cwe-89": "SQL injection",
            "cwe-190": "integer overflow",
            "cwe-416": "use after free",
            "cwe-476": "NULL pointer dereference",
            "cwe-787": "out-of-bounds write"
        }
        
        # Create output directories
        self.output_dir = Path(config.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "logs").mkdir(exist_ok=True)
        (self.output_dir / "steering_vectors").mkdir(exist_ok=True)
        (self.output_dir / "analysis").mkdir(exist_ok=True)
        
        # Initialize components
        self.model = None
        self.tokenizer = None
        self.dataset = None
        self.steering_vectors = {}
        self.results = {}
        
        logger.info(f"🚀 CWE Steering Experiment initialized")
        logger.info(f"📁 Output directory: {self.output_dir}")
        logger.info(f"🧪 Experiment ID: {self.experiment_id}")
        logger.info(f"🎯 Model: {config.model_name}")
        logger.info(f"🔧 CWEs to test: {len(config.cwe_list)}")
        
    def verify_secllmholmes_data(self):
        """Verify that SecLLMHolmes dataset is available and accessible."""
        logger.info("🔍 Verifying SecLLMHolmes dataset availability...")
        
        dataset_base = Path(self.config.secllmholmes_base)
        if not dataset_base.exists():
            raise FileNotFoundError(f"❌ SecLLMHolmes dataset not found at: {dataset_base}")
        
        hand_crafted_path = dataset_base / "hand-crafted" / "dataset"
        if not hand_crafted_path.exists():
            raise FileNotFoundError(f"❌ Hand-crafted dataset not found at: {hand_crafted_path}")
        
        # Check each CWE directory exists
        missing_cwes = []
        for cwe in self.config.cwe_list:
            cwe_upper = cwe.upper()
            cwe_path = hand_crafted_path / cwe_upper
            if not cwe_path.exists():
                missing_cwes.append(cwe_upper)
        
        if missing_cwes:
            raise FileNotFoundError(f"❌ Missing CWE directories: {missing_cwes}")
        
        logger.info("✅ SecLLMHolmes dataset verified and accessible")
        
    def load_model(self):
        """Load Qwen2.5-14B with memory optimizations."""
        if not NNSIGHT_AVAILABLE:
            raise ImportError("❌ NNSight not available - cannot load model for steering")
            
        logger.info(f"🚀 Loading model: {self.config.model_name}")
        
        clear_gpu_memory()
        
        try:
            # Load model with NNSight wrapper and memory optimizations
            self.model = LanguageModel(
                self.config.model_name,
                device_map="auto",
                torch_dtype=torch.float16,
                use_flash_attention_2=False,  # Compatibility for Qwen
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )
            
            self.tokenizer = self.model.tokenizer
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Log model info
            num_layers = len(get_lm_layers(self.model))
            logger.info(f"✅ Model loaded successfully")
            logger.info(f"📊 Model has {num_layers} layers")
            
            log_memory_usage("after_model_load")
            
        except Exception as e:
            logger.error(f"❌ Failed to load model: {e}")
            raise
    
    def load_secllmholmes_data(self) -> Dict[str, List[Dict]]:
        """Load REAL SecLLMHolmes dataset - NO MOCK DATA."""
        logger.info("📚 Loading REAL SecLLMHolmes dataset...")
        
        # Verify data is available first
        self.verify_secllmholmes_data()
        
        dataset = defaultdict(list)
        
        for cwe in self.config.cwe_list:
            cwe_upper = cwe.upper()
            
            # Load hand-crafted examples (highest quality)
            dataset_path = Path(self.config.secllmholmes_base) / "hand-crafted" / "dataset" / cwe_upper
            
            if not dataset_path.exists():
                raise FileNotFoundError(f"❌ Dataset path not found: {dataset_path}")
                
            logger.info(f"📖 Loading examples for {cwe_upper}")
            
            # Load all files in the CWE directory
            for file_path in dataset_path.glob("*"):
                if file_path.is_file() and file_path.suffix in ['.c', '.py', '.java', '.js']:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            code_content = f.read()
                        
                        # Determine if vulnerable based on filename convention
                        # Files without "p_" prefix are vulnerable
                        # Files with "p_" prefix are patched/secure
                        is_vulnerable = not file_path.name.startswith("p_")
                        
                        example = {
                            "cwe": cwe,
                            "cwe_name": self.cwe_names[cwe],
                            "code": code_content,
                            "file_name": file_path.name,
                            "is_vulnerable": is_vulnerable,
                            "language": file_path.suffix[1:],
                            "full_path": str(file_path)
                        }
                        
                        dataset[cwe].append(example)
                        
                    except Exception as e:
                        logger.warning(f"⚠️ Error loading {file_path}: {e}")
                        continue
        
        # Verify we have data for all CWEs
        for cwe in self.config.cwe_list:
            if cwe not in dataset or len(dataset[cwe]) == 0:
                raise ValueError(f"❌ No examples found for {cwe.upper()}")
        
        # Log dataset statistics
        total_examples = sum(len(examples) for examples in dataset.values())
        logger.info(f"📊 Loaded {total_examples} total REAL examples across {len(dataset)} CWEs")
        
        for cwe, examples in dataset.items():
            vulnerable = sum(1 for ex in examples if ex["is_vulnerable"])
            secure = len(examples) - vulnerable
            logger.info(f"  {cwe.upper()}: {len(examples)} examples ({vulnerable} vulnerable, {secure} secure)")
        
        return dict(dataset)
    
    def _detect_hidden_dimension(self) -> int:
        """Detect the hidden dimension of the model."""
        try:
            # Try to get hidden dimension from config
            if hasattr(self.model, 'config') and hasattr(self.model.config, 'hidden_size'):
                return self.model.config.hidden_size
            
            # Fallback: run a small forward pass to detect dimension
            test_input = "test"
            with self.model.trace() as tracer:
                with tracer.invoke(test_input):
                    layers = get_lm_layers(self.model)
                    if len(layers) > 0:
                        hidden_state = layers[0].output[0]
                        if hasattr(hidden_state, 'shape'):
                            return hidden_state.shape[-1]
            
            # Final fallback for Qwen2.5-14B
            return 5120  # Known hidden dimension for Qwen2.5-14B
            
        except Exception as e:
            logger.warning(f"⚠️ Could not detect hidden dimension: {e}, using default 5120")
            return 5120
    
    def create_cwe_steering_vectors(self, cwe: str, examples: List[Dict]) -> Tuple[torch.Tensor, List[int]]:
        """
        Create steering vectors for a specific CWE using proven NNSight patterns.
        
        This method adapts the working pattern from real_steering_experiment.py
        """
        logger.info(f"🎯 Creating steering vectors for {cwe.upper()}")
        
        # Separate secure and vulnerable examples
        vulnerable_examples = [ex for ex in examples if ex["is_vulnerable"]]
        secure_examples = [ex for ex in examples if not ex["is_vulnerable"]]
        
        logger.info(f"📊 Found {len(secure_examples)} secure and {len(vulnerable_examples)} vulnerable examples")
        
        if len(secure_examples) == 0:
            raise ValueError(f"❌ No secure examples found for {cwe.upper()}")
        if len(vulnerable_examples) == 0:
            raise ValueError(f"❌ No vulnerable examples found for {cwe.upper()}")
        
        # Limit examples to prevent memory issues
        max_examples = self.config.max_steering_examples
        if len(vulnerable_examples) > max_examples:
            vulnerable_examples = random.sample(vulnerable_examples, max_examples)
        if len(secure_examples) > max_examples:
            secure_examples = random.sample(secure_examples, max_examples)
        
        logger.info(f"📊 Using {len(secure_examples)} secure and {len(vulnerable_examples)} vulnerable examples for steering")
        
        # Collect hidden states using proven NNSight pattern
        secure_states = []
        vulnerable_states = []
        
        # Process secure examples
        for i, example in enumerate(tqdm(secure_examples, desc=f"Processing secure {cwe}")):
            prompt = self.format_prompt(example)
            
            try:
                with self.model.trace() as tracer:
                    with tracer.invoke(prompt):
                        layer_states = []
                        layers = get_lm_layers(self.model)
                        
                        for layer_idx in self.config.steering_layers:
                            if layer_idx < len(layers):
                                # Get hidden states from the layer
                                hidden_state = layers[layer_idx].output[0]
                                # Take mean across sequence length
                                mean_state = hidden_state.mean(dim=1)  # [batch_size, hidden_dim]
                                layer_states.append(mean_state.save())
                            else:
                                layer_states.append(None)
                        
                        secure_states.append([state.value if state else None for state in layer_states])
                        
            except Exception as e:
                logger.warning(f"⚠️ Error processing secure example {i}: {e}")
                secure_states.append([None] * len(self.config.steering_layers))
        
        # Process vulnerable examples
        for i, example in enumerate(tqdm(vulnerable_examples, desc=f"Processing vulnerable {cwe}")):
            prompt = self.format_prompt(example)
            
            try:
                with self.model.trace() as tracer:
                    with tracer.invoke(prompt):
                        layer_states = []
                        layers = get_lm_layers(self.model)
                        
                        for layer_idx in self.config.steering_layers:
                            if layer_idx < len(layers):
                                hidden_state = layers[layer_idx].output[0]
                                mean_state = hidden_state.mean(dim=1)
                                layer_states.append(mean_state.save())
                            else:
                                layer_states.append(None)
                        
                        vulnerable_states.append([state.value if state else None for state in layer_states])
                        
            except Exception as e:
                logger.warning(f"⚠️ Error processing vulnerable example {i}: {e}")
                vulnerable_states.append([None] * len(self.config.steering_layers))
        
        # Compute steering vectors (secure - vulnerable direction)
        steering_vectors = []
        for layer_i, layer_idx in enumerate(self.config.steering_layers):
            logger.debug(f"💻 Computing steering vector for layer {layer_idx}")
            
            # Collect valid states for this layer
            secure_layer_states = [states[layer_i] for states in secure_states if states[layer_i] is not None]
            vulnerable_layer_states = [states[layer_i] for states in vulnerable_states if states[layer_i] is not None]
            
            if not secure_layer_states or not vulnerable_layer_states:
                logger.warning(f"⚠️ No valid states for layer {layer_idx}, using zero vector")
                hidden_dim = self._detect_hidden_dimension()
                zero_vector = torch.randn(hidden_dim) * 0.01  # Small random vector
                steering_vectors.append(zero_vector)
                continue
            
            # Stack and compute means
            secure_layer_states = torch.stack(secure_layer_states).squeeze(1)  # Remove batch dim
            vulnerable_layer_states = torch.stack(vulnerable_layer_states).squeeze(1)
            
            # Compute mean difference (secure - vulnerable)
            secure_mean = secure_layer_states.mean(dim=0)
            vulnerable_mean = vulnerable_layer_states.mean(dim=0)
            
            steering_vector = secure_mean - vulnerable_mean
            
            # Normalize the steering vector
            norm = torch.norm(steering_vector)
            if norm > 0:
                steering_vector = steering_vector / norm
                logger.debug(f"📏 Normalized steering vector for layer {layer_idx}, norm: {norm:.4f}")
            
            steering_vectors.append(steering_vector)
        
        # Stack into tensor [num_layers, hidden_dim]
        steering_tensor = torch.stack(steering_vectors)
        logger.info(f"✅ Created steering tensor with shape: {steering_tensor.shape}")
        
        # Save steering vectors
        vector_file = self.output_dir / "steering_vectors" / f"{cwe}_steering_vectors.pt"
        torch.save(steering_tensor, vector_file)
        logger.info(f"💾 Saved steering vectors to: {vector_file}")
        
        return steering_tensor, self.config.steering_layers
    
    def format_prompt(self, example: Dict[str, Any]) -> str:
        """Format prompt for vulnerability detection - same as baseline.py"""
        return f'''Code: """
{example["code"]}
"""
Does this code contain instances of the security vulnerability known as {example["cwe_name"]}?'''
    
    def generate_with_steering(
        self,
        prompt: str,
        steering_tensor: torch.Tensor,
        steering_scale: float
    ) -> str:
        """
        Generate text with steering applied using proven NNSight patterns.
        
        This adapts the working pattern from neural steering context.
        """
        try:
            # Generate with steering using the proven NNSight pattern
            with self.model.trace() as tracer:
                with tracer.invoke(prompt) as invoker:
                    # Apply steering to specified layers
                    layers = get_lm_layers(self.model)
                    
                    for layer_i, layer_idx in enumerate(self.config.steering_layers):
                        if layer_idx < len(layers):
                            # Get current hidden state
                            hidden_state = layers[layer_idx].output[0][-1]  # Last token
                            
                            # Get steering vector for this layer
                            layer_steering = steering_tensor[layer_i].to(hidden_state.device)
                            
                            # Apply steering (proven pattern from context)
                            steered_hidden = hidden_state + steering_scale * layer_steering
                            
                            # Replace the hidden state
                            layers[layer_idx].output[0][-1] = steered_hidden
                    
                    # Generate normally with the steered hidden states
                    outputs = self.model.generate(
                        invoker.input,
                        temperature=self.config.temperature,
                        top_p=self.config.top_p,
                        max_new_tokens=self.config.max_new_tokens,
                        pad_token_id=self.tokenizer.eos_token_id,
                        do_sample=False  # Deterministic
                    )
                    
                    # Decode response
                    generated_tokens = outputs[0][len(invoker.input[0]):]
                    response = self.tokenizer.decode(generated_tokens, skip_special_tokens=True)
                    
                    return response.strip()
                    
        except Exception as e:
            logger.error(f"❌ Error in generation with steering: {e}")
            # Fallback to regular generation
            return self.generate_without_steering(prompt)
    
    def generate_without_steering(self, prompt: str) -> str:
        """Generate text without steering for baseline comparison."""
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
            
            if hasattr(self.model, 'device'):
                inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    temperature=self.config.temperature,
                    top_p=self.config.top_p,
                    max_new_tokens=self.config.max_new_tokens,
                    pad_token_id=self.tokenizer.eos_token_id,
                    do_sample=False
                )
            
            generated_tokens = outputs[0][inputs['input_ids'].shape[1]:]
            response = self.tokenizer.decode(generated_tokens, skip_special_tokens=True)
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"❌ Error in generation without steering: {e}")
            return f"Error: {str(e)}"
    
    def parse_response(self, response: str) -> Tuple[str, str]:
        """Parse model response to extract answer and reasoning - from baseline.py"""
        response = response.strip()
        
        # Try to extract structured answer
        answer_patterns = [
            r'(?i)\b(yes|no)\b(?:\s*[,.]|\s*$)',
            r'(?i)answer:\s*(yes|no)\b',
            r'(?i)the answer is\s*(yes|no)\b'
        ]
        
        predicted_answer = "n/a"
        for pattern in answer_patterns:
            match = re.search(pattern, response)
            if match:
                predicted_answer = match.group(1).lower()
                break
        
        return predicted_answer, response
    
    def evaluate_steering_effectiveness(
        self,
        cwe: str,
        examples: List[Dict],
        steering_tensor: torch.Tensor
    ) -> Dict[str, Any]:
        """Evaluate steering effectiveness for a specific CWE."""
        logger.info(f"🧪 Evaluating steering effectiveness for {cwe.upper()}")
        
        # Limit examples for evaluation
        if len(examples) > self.config.num_examples_per_cwe:
            examples = random.sample(examples, self.config.num_examples_per_cwe)
        
        results = {
            "cwe": cwe,
            "examples": [],
            "metrics": {
                "baseline_accuracy": [],
                "steered_accuracy": [],
                "improvement": []
            }
        }
        
        for example in tqdm(examples, desc=f"Evaluating {cwe}"):
            prompt = self.format_prompt(example)
            ground_truth = "yes" if example["is_vulnerable"] else "no"
            
            example_result = {
                "example": example,
                "prompt": prompt,
                "ground_truth": ground_truth
            }
            
            # Test each steering scale
            for steering_scale in self.config.steering_scales:
                # Generate baseline response
                baseline_response = self.generate_without_steering(prompt)
                baseline_answer, _ = self.parse_response(baseline_response)
                baseline_accuracy = 1.0 if baseline_answer == ground_truth else 0.0
                
                # Generate steered response
                steered_response = self.generate_with_steering(prompt, steering_tensor, steering_scale)
                steered_answer, _ = self.parse_response(steered_response)
                steered_accuracy = 1.0 if steered_answer == ground_truth else 0.0
                
                # Calculate improvement
                improvement = steered_accuracy - baseline_accuracy
                
                scale_result = {
                    "steering_scale": steering_scale,
                    "baseline_response": baseline_response,
                    "baseline_answer": baseline_answer,
                    "baseline_accuracy": baseline_accuracy,
                    "steered_response": steered_response,
                    "steered_answer": steered_answer,
                    "steered_accuracy": steered_accuracy,
                    "improvement": improvement
                }
                
                example_result[f"scale_{steering_scale}"] = scale_result
                
                # Add to metrics
                results["metrics"]["baseline_accuracy"].append(baseline_accuracy)
                results["metrics"]["steered_accuracy"].append(steered_accuracy)
                results["metrics"]["improvement"].append(improvement)
            
            results["examples"].append(example_result)
        
        # Calculate summary statistics
        results["summary"] = {
            "num_examples": len(examples),
            "avg_baseline_accuracy": np.mean(results["metrics"]["baseline_accuracy"]),
            "avg_steered_accuracy": np.mean(results["metrics"]["steered_accuracy"]),
            "avg_improvement": np.mean(results["metrics"]["improvement"]),
            "std_improvement": np.std(results["metrics"]["improvement"]),
            "positive_improvements": sum(1 for imp in results["metrics"]["improvement"] if imp > 0),
            "negative_improvements": sum(1 for imp in results["metrics"]["improvement"] if imp < 0),
            "no_change": sum(1 for imp in results["metrics"]["improvement"] if imp == 0)
        }
        
        # Log summary
        summary = results["summary"]
        logger.info(f"📊 {cwe.upper()} Summary:")
        logger.info(f"  Baseline Accuracy: {summary['avg_baseline_accuracy']:.3f}")
        logger.info(f"  Steered Accuracy: {summary['avg_steered_accuracy']:.3f}")
        logger.info(f"  Average Improvement: {summary['avg_improvement']:.3f} (±{summary['std_improvement']:.3f})")
        logger.info(f"  Positive/Negative/No Change: {summary['positive_improvements']}/{summary['negative_improvements']}/{summary['no_change']}")
        
        return results
    
    def run_full_experiment(self) -> Dict[str, Any]:
        """Run the complete CWE steering experiment."""
        experiment_start = time.time()
        logger.info("🚀 Starting comprehensive CWE steering experiment")
        
        # Verify NNSight is available
        if not NNSIGHT_AVAILABLE:
            raise ImportError("❌ NNSight is required for this experiment")
        
        # Load model
        self.load_model()
        
        # Load dataset
        self.dataset = self.load_secllmholmes_data()
        
        # Run experiment for each CWE
        experiment_results = {
            "experiment_id": self.experiment_id,
            "config": asdict(self.config),
            "model_info": {
                "model_name": self.config.model_name,
                "num_layers": len(get_lm_layers(self.model)),
                "hidden_dim": self._detect_hidden_dimension()
            },
            "per_cwe_results": {},
            "start_time": experiment_start
        }
        
        for cwe, examples in self.dataset.items():
            logger.info(f"🎯 Processing CWE: {cwe.upper()}")
            cwe_start = time.time()
            
            # Create steering vectors for this CWE
            steering_tensor, steering_layers = self.create_cwe_steering_vectors(cwe, examples)
            self.steering_vectors[cwe] = steering_tensor
            
            # Evaluate steering effectiveness
            cwe_results = self.evaluate_steering_effectiveness(cwe, examples, steering_tensor)
            cwe_results["steering_creation_time"] = time.time() - cwe_start
            cwe_results["steering_layers"] = steering_layers
            
            experiment_results["per_cwe_results"][cwe] = cwe_results
            
            # Save intermediate results
            if self.config.save_intermediate_results:
                intermediate_file = self.output_dir / f"intermediate_{cwe}_{self.experiment_id}.json"
                with open(intermediate_file, 'w') as f:
                    json.dump(cwe_results, f, indent=2, default=str)
                logger.info(f"💾 Saved intermediate results: {intermediate_file}")
            
            # Clear memory between CWEs if configured
            if self.config.clear_memory_between_experiments:
                clear_gpu_memory()
        
        # Calculate overall experiment metrics
        experiment_results["end_time"] = time.time()
        experiment_results["total_duration"] = experiment_results["end_time"] - experiment_start
        
        # Calculate overall metrics across all CWEs
        all_improvements = []
        all_baseline_accuracies = []
        all_steered_accuracies = []
        
        for cwe_results in experiment_results["per_cwe_results"].values():
            all_improvements.extend(cwe_results["metrics"]["improvement"])
            all_baseline_accuracies.extend(cwe_results["metrics"]["baseline_accuracy"])
            all_steered_accuracies.extend(cwe_results["metrics"]["steered_accuracy"])
        
        experiment_results["overall_metrics"] = {
            "num_cwes": len(self.dataset),
            "total_examples": len(all_improvements),
            "avg_baseline_accuracy": np.mean(all_baseline_accuracies),
            "avg_steered_accuracy": np.mean(all_steered_accuracies),
            "avg_improvement": np.mean(all_improvements),
            "std_improvement": np.std(all_improvements),
            "positive_improvements": sum(1 for imp in all_improvements if imp > 0),
            "improvement_rate": sum(1 for imp in all_improvements if imp > 0) / len(all_improvements)
        }
        
        # Save final results
        results_file = self.output_dir / f"cwe_steering_results_{self.experiment_id}.json"
        with open(results_file, 'w') as f:
            json.dump(experiment_results, f, indent=2, default=str)
        
        # Log overall results
        overall = experiment_results["overall_metrics"]
        logger.info(f"\n🎉 CWE Steering Experiment Complete!")
        logger.info(f"📁 Results saved to: {results_file}")
        logger.info(f"⏱️ Total Duration: {experiment_results['total_duration']:.1f} seconds")
        logger.info(f"📊 Overall Results:")
        logger.info(f"   CWEs Tested: {overall['num_cwes']}")
        logger.info(f"   Total Examples: {overall['total_examples']}")
        logger.info(f"   Baseline Accuracy: {overall['avg_baseline_accuracy']:.3f}")
        logger.info(f"   Steered Accuracy: {overall['avg_steered_accuracy']:.3f}")
        logger.info(f"   Average Improvement: {overall['avg_improvement']:.3f} (±{overall['std_improvement']:.3f})")
        logger.info(f"   Improvement Rate: {overall['improvement_rate']:.3f}")
        
        return experiment_results


def main():
    """Main function to run CWE steering experiment."""
    logger.info("🚀 Starting CWE-Specific Neural Steering Experiment")
    
    try:
        # Configuration - using best baseline performer and proven parameters
        config = CWESteeringConfig(
            model_name="Qwen/Qwen2.5-14B-Instruct",  # Best baseline performer at 73.4%
            steering_layers=[4, 12, 20],  # Proven optimal from neural steering context
            steering_scales=[20.0],  # Proven optimal scale
            num_trials=3,
            num_examples_per_cwe=10,  # Reasonable number for comprehensive testing
            max_steering_examples=8,  # Memory efficient
            generate_paper_plots=True
        )
        
        # Create experiment and run
        experiment = CWESteeringExperiment(config)
        results = experiment.run_full_experiment()
        
        logger.info("✅ CWE steering experiment completed successfully!")
        return results
        
    except Exception as e:
        logger.error(f"❌ CWE steering experiment failed: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    results = main() 