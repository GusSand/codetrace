#!/usr/bin/env python3
"""
Memory-Efficient CWE-Specific Neural Steering Experiment for Qwen2.5-14B (NNSight 0.4.x)

This version processes examples one at a time and aggressively manages memory
to work within GPU constraints while using the REAL SecLLMHolmes dataset.

Usage:
    python cwe_steering_memory_efficient.py

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
current_dir = Path(__file__).parent.absolute()
security_dir = current_dir.parent.parent
sys.path.insert(0, str(security_dir))

# Check NNSight availability
try:
    import nnsight
    from nnsight import LanguageModel
    print("✅ NNSight available for steering vectors")
    print(f"📦 NNSight version: {nnsight.__version__}")
except ImportError as e:
    print(f"❌ NNSight not available: {e}")
    sys.exit(1)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cwe_steering_memory_efficient.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ExperimentConfig:
    """Configuration for memory-efficient CWE steering experiment."""
    model_name: str = "Qwen/Qwen2.5-14B-Instruct"
    device: str = "auto"
    max_length: int = 256  # Reduced from 512
    steering_strength: float = 1.0
    steering_layers: List[int] = None  # Will use last layer only
    results_dir: str = "results_memory_efficient"
    max_examples_per_type: int = 2  # Reduced from 5
    
    def __post_init__(self):
        if self.steering_layers is None:
            self.steering_layers = [-1]  # Only last layer to save memory

def aggressive_memory_cleanup():
    """Aggressively clear GPU and system memory."""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
    gc.collect()
    time.sleep(0.1)  # Give system time to cleanup

def get_memory_usage():
    """Get current memory usage."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # MB

def load_secllmholmes_data(dataset_path: str) -> Dict[str, List[Dict[str, Any]]]:
    """Load REAL SecLLMHolmes dataset with memory limits."""
    dataset_path = Path(dataset_path)
    if not dataset_path.exists():
        raise FileNotFoundError(f"SecLLMHolmes dataset not found at {dataset_path}")
    
    cwe_data = {}
    cwe_dirs = [d for d in dataset_path.iterdir() if d.is_dir() and d.name.startswith('CWE-')]
    
    logger.info(f"🔍 Found {len(cwe_dirs)} CWE directories")
    
    for cwe_dir in sorted(cwe_dirs):
        cwe_name = cwe_dir.name
        cwe_data[cwe_name] = []
        
        # Load vulnerable examples (no "p_" prefix) - limit to 2 for memory
        vulnerable_files = [f for f in cwe_dir.iterdir() 
                           if f.is_file() and not f.name.startswith('p_')][:2]
        
        # Load secure examples (with "p_" prefix) - limit to 2 for memory
        secure_files = [f for f in cwe_dir.iterdir()
                       if f.is_file() and f.name.startswith('p_')][:2]
        
        # Process vulnerable examples
        for file_path in sorted(vulnerable_files):
            try:
                content = file_path.read_text(encoding='utf-8')
                # Truncate content to reduce memory usage
                if len(content) > 2000:
                    content = content[:2000] + "..."
                cwe_data[cwe_name].append({
                    'content': content,
                    'label': 'vulnerable',
                    'filename': file_path.name,
                    'cwe': cwe_name
                })
            except Exception as e:
                logger.warning(f"⚠️ Failed to read {file_path}: {e}")
        
        # Process secure examples
        for file_path in sorted(secure_files):
            try:
                content = file_path.read_text(encoding='utf-8')
                # Truncate content to reduce memory usage
                if len(content) > 2000:
                    content = content[:2000] + "..."
                cwe_data[cwe_name].append({
                    'content': content,
                    'label': 'secure', 
                    'filename': file_path.name,
                    'cwe': cwe_name
                })
            except Exception as e:
                logger.warning(f"⚠️ Failed to read {file_path}: {e}")
        
        logger.info(f"📖 Loaded {len(cwe_data[cwe_name])} examples for {cwe_name}")
    
    return cwe_data

def create_vulnerability_prompt(code: str) -> str:
    """Create a short prompt for vulnerability detection."""
    # Shortened prompt to reduce memory
    return f"""Code security analysis:
```
{code[:500]}...
```
Vulnerable? Yes/No:"""

def create_steering_vectors_memory_efficient(model, examples: List[Dict[str, Any]], config: ExperimentConfig) -> Dict[str, torch.Tensor]:
    """
    Create steering vectors with extreme memory efficiency.
    Process one example at a time and immediately clear memory.
    """
    vulnerable_examples = [ex for ex in examples if ex['label'] == 'vulnerable'][:config.max_examples_per_type]
    secure_examples = [ex for ex in examples if ex['label'] == 'secure'][:config.max_examples_per_type]
    
    if len(vulnerable_examples) == 0 or len(secure_examples) == 0:
        logger.warning("⚠️ No vulnerable or secure examples found")
        return {}
    
    logger.info(f"📊 Creating steering vectors from {len(vulnerable_examples)} vulnerable and {len(secure_examples)} secure examples")
    
    steering_vectors = {}
    
    for layer_idx in config.steering_layers:
        logger.info(f"🎯 Processing layer {layer_idx}")
        
        # Collect activations one by one to minimize memory usage
        vulnerable_activations = []
        secure_activations = []
        
        # Process vulnerable examples one at a time
        for i, ex in enumerate(vulnerable_examples):
            try:
                logger.info(f"  Processing vulnerable example {i+1}/{len(vulnerable_examples)}")
                prompt = create_vulnerability_prompt(ex['content'])
                
                aggressive_memory_cleanup()
                
                with model.trace() as tracer:
                    with tracer.invoke(prompt):
                        # Get activation for specific layer
                        activation = model.model.layers[layer_idx].output.save()
                
                if activation is not None and len(activation.shape) >= 2:
                    # Take mean over sequence dimension and move to CPU immediately
                    act_mean = activation[0].mean(dim=0).detach().cpu()
                    vulnerable_activations.append(act_mean)
                    logger.info(f"    ✅ Got activation shape: {act_mean.shape}")
                else:
                    logger.warning(f"    ⚠️ Invalid activation")
                
                # Aggressive cleanup after each example
                del activation
                aggressive_memory_cleanup()
                    
            except Exception as e:
                logger.error(f"❌ Error processing vulnerable example {i+1}: {e}")
                aggressive_memory_cleanup()
                continue
        
        # Process secure examples one at a time  
        for i, ex in enumerate(secure_examples):
            try:
                logger.info(f"  Processing secure example {i+1}/{len(secure_examples)}")
                prompt = create_vulnerability_prompt(ex['content'])
                
                aggressive_memory_cleanup()
                
                with model.trace() as tracer:
                    with tracer.invoke(prompt):
                        activation = model.model.layers[layer_idx].output.save()
                
                if activation is not None and len(activation.shape) >= 2:
                    # Take mean over sequence dimension and move to CPU immediately
                    act_mean = activation[0].mean(dim=0).detach().cpu()
                    secure_activations.append(act_mean)
                    logger.info(f"    ✅ Got activation shape: {act_mean.shape}")
                else:
                    logger.warning(f"    ⚠️ Invalid activation")
                
                # Aggressive cleanup after each example
                del activation
                aggressive_memory_cleanup()
                    
            except Exception as e:
                logger.error(f"❌ Error processing secure example {i+1}: {e}")
                aggressive_memory_cleanup()
                continue
        
        # Create steering vector if we have activations
        if len(vulnerable_activations) > 0 and len(secure_activations) > 0:
            try:
                # Move back to GPU for computation
                vulnerable_mean = torch.stack(vulnerable_activations).mean(dim=0).cuda()
                secure_mean = torch.stack(secure_activations).mean(dim=0).cuda()
                steering_vector = (vulnerable_mean - secure_mean).detach()
                steering_vectors[f"layer_{layer_idx}"] = steering_vector
                logger.info(f"✅ Created steering vector for layer {layer_idx} with shape {steering_vector.shape}")
                
                # Clean up intermediate tensors
                del vulnerable_mean, secure_mean
                aggressive_memory_cleanup()
                
            except Exception as e:
                logger.error(f"❌ Error creating steering vector for layer {layer_idx}: {e}")
        else:
            logger.warning(f"⚠️ Could not create steering vector for layer {layer_idx} - insufficient activations")
        
        # Clear activation lists
        vulnerable_activations.clear()
        secure_activations.clear()
    
    return steering_vectors

def evaluate_steering_memory_efficient(model, examples: List[Dict[str, Any]], 
                                     steering_vectors: Dict[str, torch.Tensor], 
                                     config: ExperimentConfig) -> Dict[str, Any]:
    """
    Evaluate steering effectiveness with memory constraints.
    """
    results = {
        'baseline_correct': 0,
        'steered_correct': 0,
        'total_examples': 0,
        'improvements': [],
        'examples': []
    }
    
    # Limit examples for memory
    limited_examples = examples[:4]  # Only test on 4 examples max
    
    for i, example in enumerate(limited_examples):
        try:
            logger.info(f"🧪 Evaluating example {i+1}/{len(limited_examples)}: {example['filename']}")
            prompt = create_vulnerability_prompt(example['content'])
            expected_vulnerable = (example['label'] == 'vulnerable')
            
            aggressive_memory_cleanup()
            
            # Baseline generation (no steering)
            baseline_response = "UNKNOWN"
            try:
                with model.trace() as tracer:
                    with tracer.invoke(prompt):
                        baseline_output = model.lm_head.output.save()
                
                if baseline_output is not None:
                    # Get the most likely next token
                    baseline_logits = baseline_output[0, -1, :]  # Last token logits
                    top_token = baseline_logits.argmax().item()
                    baseline_response = model.tokenizer.decode([top_token])
                    logger.info(f"  📊 Baseline response: '{baseline_response}'")
                    
            except Exception as e:
                logger.error(f"❌ Error in baseline generation: {e}")
                baseline_response = "ERROR"
            
            aggressive_memory_cleanup()
            
            # Steered generation
            steered_response = "UNKNOWN"
            try:
                with model.trace() as tracer:
                    with tracer.invoke(prompt):
                        # Apply steering vectors
                        for layer_key, steering_vector in steering_vectors.items():
                            layer_idx = int(layer_key.split('_')[1])
                            current_activation = model.model.layers[layer_idx].output
                            # Apply steering - reshape steering vector to match activation
                            steering_addition = steering_vector.unsqueeze(0).unsqueeze(0)  # Add batch and sequence dims
                            model.model.layers[layer_idx].output = current_activation + config.steering_strength * steering_addition
                        
                        steered_output = model.lm_head.output.save()
                
                if steered_output is not None:
                    steered_logits = steered_output[0, -1, :]
                    top_token = steered_logits.argmax().item()
                    steered_response = model.tokenizer.decode([top_token])
                    logger.info(f"  🎯 Steered response: '{steered_response}'")
                    
            except Exception as e:
                logger.error(f"❌ Error in steered generation: {e}")
                steered_response = "ERROR"
            
            aggressive_memory_cleanup()
            
            # Simple evaluation based on "Yes"/"No" in response
            baseline_says_vulnerable = "yes" in baseline_response.lower() or "y" in baseline_response.lower()
            steered_says_vulnerable = "yes" in steered_response.lower() or "y" in steered_response.lower()
            
            baseline_correct = baseline_says_vulnerable == expected_vulnerable
            steered_correct = steered_says_vulnerable == expected_vulnerable
            
            if baseline_correct:
                results['baseline_correct'] += 1
            if steered_correct:
                results['steered_correct'] += 1
                
            improvement = 1 if steered_correct and not baseline_correct else (-1 if baseline_correct and not steered_correct else 0)
            results['improvements'].append(improvement)
            
            results['examples'].append({
                'filename': example['filename'],
                'expected_vulnerable': expected_vulnerable,
                'baseline_response': baseline_response,
                'steered_response': steered_response,
                'baseline_correct': baseline_correct,
                'steered_correct': steered_correct,
                'improvement': improvement
            })
            
            results['total_examples'] += 1
            
        except Exception as e:
            logger.error(f"❌ Error evaluating example {example.get('filename', 'unknown')}: {e}")
            aggressive_memory_cleanup()
            continue
    
    return results

def run_memory_efficient_experiment(config: ExperimentConfig):
    """
    Run the memory-efficient CWE steering experiment.
    """
    logger.info("🚀 Starting Memory-Efficient CWE Steering Experiment (NNSight 0.4.x)")
    
    # Create results directory
    results_dir = Path(config.results_dir)
    results_dir.mkdir(exist_ok=True)
    (results_dir / "steering_vectors").mkdir(exist_ok=True)
    
    experiment_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    logger.info(f"🧪 Experiment ID: {experiment_id}")
    
    start_time = time.time()
    
    # Load model
    logger.info(f"🚀 Loading model: {config.model_name}")
    aggressive_memory_cleanup()
    
    try:
        model = LanguageModel(config.model_name, device_map=config.device)
        logger.info("✅ Model loaded successfully")
        logger.info(f"📊 Model layers: {len(model.model.layers)}")
    except Exception as e:
        logger.error(f"❌ Failed to load model: {e}")
        return
    
    # Load SecLLMHolmes dataset  
    logger.info("📚 Loading REAL SecLLMHolmes dataset (memory-limited)...")
    dataset_path = security_dir / "SecLLMHolmes" / "datasets" / "hand-crafted" / "dataset"
    
    if not dataset_path.exists():
        logger.error(f"❌ SecLLMHolmes dataset not found at {dataset_path}")
        return
        
    try:
        cwe_data = load_secllmholmes_data(dataset_path)
        total_examples = sum(len(examples) for examples in cwe_data.values())
        logger.info(f"📊 Loaded {total_examples} total REAL examples across {len(cwe_data)} CWEs")
        
    except Exception as e:
        logger.error(f"❌ Failed to load dataset: {e}")
        return
    
    # Process each CWE with memory efficiency
    all_results = {}
    
    for cwe_name, examples in cwe_data.items():
        logger.info(f"🎯 Processing CWE: {cwe_name}")
        
        try:
            # Create steering vectors with memory efficiency
            logger.info(f"🎯 Creating memory-efficient steering vectors for {cwe_name}")
            steering_vectors = create_steering_vectors_memory_efficient(model, examples, config)
            
            if not steering_vectors:
                logger.warning(f"⚠️ No steering vectors created for {cwe_name}")
                continue
            
            # Save steering vectors
            steering_file = results_dir / "steering_vectors" / f"{cwe_name.lower()}_steering_vectors.pt"
            torch.save(steering_vectors, steering_file)
            logger.info(f"💾 Saved steering vectors to: {steering_file}")
            
            # Evaluate steering effectiveness
            logger.info(f"🧪 Evaluating steering effectiveness for {cwe_name}")
            evaluation_results = evaluate_steering_memory_efficient(model, examples, steering_vectors, config)
            
            # Calculate metrics
            total = evaluation_results['total_examples']
            baseline_acc = evaluation_results['baseline_correct'] / total if total > 0 else 0
            steered_acc = evaluation_results['steered_correct'] / total if total > 0 else 0
            improvements = evaluation_results['improvements']
            avg_improvement = np.mean(improvements) if improvements else 0
            
            positive_improvements = len([x for x in improvements if x > 0])
            negative_improvements = len([x for x in improvements if x < 0])
            no_change = len([x for x in improvements if x == 0])
            
            logger.info(f"📊 {cwe_name} Summary:")
            logger.info(f"  Examples Tested: {total}")
            logger.info(f"  Baseline Accuracy: {baseline_acc:.3f}")
            logger.info(f"  Steered Accuracy: {steered_acc:.3f}")
            logger.info(f"  Average Improvement: {avg_improvement:.3f}")
            logger.info(f"  Improvements: +{positive_improvements}/-{negative_improvements}/={no_change}")
            
            # Store results
            all_results[cwe_name] = {
                'baseline_accuracy': baseline_acc,
                'steered_accuracy': steered_acc,
                'average_improvement': avg_improvement,
                'positive_improvements': positive_improvements,
                'negative_improvements': negative_improvements,
                'no_change': no_change,
                'total_examples': total,
                'detailed_results': evaluation_results
            }
            
            # Save intermediate results
            intermediate_file = results_dir / f"intermediate_{cwe_name.lower()}_{experiment_id}.json"
            with open(intermediate_file, 'w') as f:
                json.dump(all_results[cwe_name], f, indent=2, default=str)
            logger.info(f"💾 Saved intermediate results: {intermediate_file}")
            
        except Exception as e:
            logger.error(f"❌ Error processing {cwe_name}: {e}")
            continue
        
        # Aggressive memory cleanup between CWEs
        logger.info("🧹 Aggressive memory cleanup...")
        aggressive_memory_cleanup()
    
    # Final results
    end_time = time.time()
    duration = end_time - start_time
    
    logger.info(f"\n🎉 Memory-Efficient CWE Steering Experiment Complete!")
    
    if all_results:
        overall_baseline = np.mean([r['baseline_accuracy'] for r in all_results.values()])
        overall_steered = np.mean([r['steered_accuracy'] for r in all_results.values()])
        overall_improvement = np.mean([r['average_improvement'] for r in all_results.values()])
        
        total_examples = sum(r['total_examples'] for r in all_results.values())
        total_positive = sum(r['positive_improvements'] for r in all_results.values())
        improvement_rate = total_positive / total_examples if total_examples > 0 else 0
        
        logger.info(f"📁 Results saved to: {results_dir}")
        logger.info(f"⏱️ Total Duration: {duration:.1f} seconds")
        logger.info(f"📊 Overall Results:")
        logger.info(f"   CWEs Tested: {len(all_results)}")
        logger.info(f"   Total Examples: {total_examples}")
        logger.info(f"   Baseline Accuracy: {overall_baseline:.3f}")
        logger.info(f"   Steered Accuracy: {overall_steered:.3f}")
        logger.info(f"   Average Improvement: {overall_improvement:.3f}")
        logger.info(f"   Improvement Rate: {improvement_rate:.3f}")
        
        # Save final results
        final_results = {
            'experiment_id': experiment_id,
            'config': asdict(config),
            'duration_seconds': duration,
            'overall_metrics': {
                'baseline_accuracy': overall_baseline,
                'steered_accuracy': overall_steered,
                'average_improvement': overall_improvement,
                'improvement_rate': improvement_rate,
                'total_examples': total_examples,
                'cwes_tested': len(all_results)
            },
            'cwe_results': all_results,
            'nnsight_version': nnsight.__version__
        }
        
        final_file = results_dir / f"cwe_steering_memory_efficient_{experiment_id}.json"
        with open(final_file, 'w') as f:
            json.dump(final_results, f, indent=2, default=str)
        
        logger.info(f"✅ Memory-efficient CWE steering experiment completed!")
        logger.info(f"📄 Final results: {final_file}")
        
    else:
        logger.error("❌ No results generated - experiment failed")

if __name__ == "__main__":
    config = ExperimentConfig()
    run_memory_efficient_experiment(config) 