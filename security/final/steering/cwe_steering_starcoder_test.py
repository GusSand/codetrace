#!/usr/bin/env python3
"""
CWE-Specific Neural Steering Experiment with StarCoder Models (Following Successful Patterns)

This version uses StarCoder models that showed 4.4x-13x improvements in previous experiments
to isolate whether the current issues are Qwen2.5-specific or methodology-specific.

Based on successful experiments that used:
- StarCoder 1B/7B models  
- Proven NNSight patterns
- Multi-layer steering with scales 5.0-20.0
- Real vulnerability detection tasks

Usage:
    python cwe_steering_starcoder_test.py

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
        logging.FileHandler('cwe_steering_starcoder_test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class StarCoderExperimentConfig:
    """Configuration for StarCoder CWE steering experiment (following successful patterns)."""
    model_name: str = "bigcode/starcoderbase-1b"  # Proven to work in previous experiments
    device: str = "auto"
    max_new_tokens: int = 50  # Generate full responses
    temperature: float = 0.1  # Low temperature for consistent results
    steering_strength: float = 20.0  # High strength like successful experiments (scale 20.0)
    steering_layers: List[int] = None  # Will use proven layer combinations
    results_dir: str = "results_starcoder_test"
    max_examples_per_type: int = 3  # More examples for better steering
    
    def __post_init__(self):
        if self.steering_layers is None:
            # Use proven layer combinations from successful experiments
            # StarCoder 1B has ~24 layers, so use [4, 12, 20] pattern
            self.steering_layers = [4, 12, 20]  # Early, middle, late - proven optimal

def aggressive_memory_cleanup():
    """Aggressively clear GPU and system memory."""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()
    gc.collect()
    time.sleep(0.1)

def load_secllmholmes_data(dataset_path: str) -> Dict[str, List[Dict[str, Any]]]:
    """Load REAL SecLLMHolmes dataset (same as before)."""
    dataset_path = Path(dataset_path)
    if not dataset_path.exists():
        raise FileNotFoundError(f"SecLLMHolmes dataset not found at {dataset_path}")
    
    cwe_data = {}
    cwe_dirs = [d for d in dataset_path.iterdir() if d.is_dir() and d.name.startswith('CWE-')][:3]  # Test on first 3 CWEs
    
    logger.info(f"🔍 Found {len(cwe_dirs)} CWE directories (testing first 3)")
    
    for cwe_dir in sorted(cwe_dirs):
        cwe_name = cwe_dir.name
        cwe_data[cwe_name] = []
        
        # Load vulnerable examples (no "p_" prefix)
        vulnerable_files = [f for f in cwe_dir.iterdir() 
                           if f.is_file() and not f.name.startswith('p_')][:3]
        
        # Load secure examples (with "p_" prefix)
        secure_files = [f for f in cwe_dir.iterdir()
                       if f.is_file() and f.name.startswith('p_')][:3]
        
        # Process vulnerable examples
        for file_path in sorted(vulnerable_files):
            try:
                content = file_path.read_text(encoding='utf-8')
                if len(content) > 1000:  # Shorter for StarCoder
                    content = content[:1000] + "..."
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
                if len(content) > 1000:  # Shorter for StarCoder
                    content = content[:1000] + "..."
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
    """Create a detailed prompt for vulnerability assessment (proven format)."""
    # Use format similar to successful experiments
    return f"""<instruction>
Analyze the following code for security vulnerabilities.

Code:
{code[:600]}

Question: Is this code vulnerable to security attacks?
Answer: """

def create_starcoder_steering_vectors(model, examples: List[Dict[str, Any]], config: StarCoderExperimentConfig) -> Dict[str, torch.Tensor]:
    """
    Create steering vectors using StarCoder with proven NNSight patterns from successful experiments.
    """
    vulnerable_examples = [ex for ex in examples if ex['label'] == 'vulnerable'][:config.max_examples_per_type]
    secure_examples = [ex for ex in examples if ex['label'] == 'secure'][:config.max_examples_per_type]
    
    if len(vulnerable_examples) == 0 or len(secure_examples) == 0:
        logger.warning("⚠️ No vulnerable or secure examples found")
        return {}
    
    logger.info(f"📊 Creating StarCoder steering vectors from {len(vulnerable_examples)} vulnerable and {len(secure_examples)} secure examples")
    
    steering_vectors = {}
    
    for layer_idx in config.steering_layers:
        logger.info(f"🎯 Processing StarCoder layer {layer_idx}")
        
        vulnerable_activations = []
        secure_activations = []
        
        # Process vulnerable examples
        for i, ex in enumerate(vulnerable_examples):
            try:
                logger.info(f"  Processing vulnerable example {i+1}/{len(vulnerable_examples)}")
                prompt = create_vulnerability_prompt(ex['content'])
                
                aggressive_memory_cleanup()
                
                with model.trace() as tracer:
                    with tracer.invoke(prompt):
                        # StarCoder layer access pattern (simpler than Qwen2.5)
                        layer_output = model.transformer.h[layer_idx].output.save()
                
                # StarCoder output handling (different from Qwen2.5 tuples)
                if layer_output is not None:
                    if hasattr(layer_output, 'shape') and len(layer_output.shape) >= 3:
                        # Take last token activation 
                        act_last = layer_output[0, -1, :].detach().cpu()
                        vulnerable_activations.append(act_last)
                        logger.info(f"    ✅ Got StarCoder activation shape: {act_last.shape}")
                    else:
                        logger.warning(f"    ⚠️ Invalid StarCoder activation shape")
                
                del layer_output
                aggressive_memory_cleanup()
                    
            except Exception as e:
                logger.error(f"❌ Error processing vulnerable example {i+1}: {e}")
                aggressive_memory_cleanup()
                continue
        
        # Process secure examples
        for i, ex in enumerate(secure_examples):
            try:
                logger.info(f"  Processing secure example {i+1}/{len(secure_examples)}")
                prompt = create_vulnerability_prompt(ex['content'])
                
                aggressive_memory_cleanup()
                
                with model.trace() as tracer:
                    with tracer.invoke(prompt):
                        layer_output = model.transformer.h[layer_idx].output.save()
                
                if layer_output is not None:
                    if hasattr(layer_output, 'shape') and len(layer_output.shape) >= 3:
                        act_last = layer_output[0, -1, :].detach().cpu()
                        secure_activations.append(act_last)
                        logger.info(f"    ✅ Got StarCoder activation shape: {act_last.shape}")
                    else:
                        logger.warning(f"    ⚠️ Invalid StarCoder activation shape")
                
                del layer_output
                aggressive_memory_cleanup()
                    
            except Exception as e:
                logger.error(f"❌ Error processing secure example {i+1}: {e}")
                aggressive_memory_cleanup()
                continue
        
        # Create steering vector if we have sufficient activations
        if len(vulnerable_activations) > 0 and len(secure_activations) > 0:
            try:
                logger.info(f"  Creating StarCoder steering vector from {len(vulnerable_activations)} vulnerable and {len(secure_activations)} secure activations")
                
                # Compute means and steering direction
                vulnerable_mean = torch.stack(vulnerable_activations).mean(dim=0).cuda()
                secure_mean = torch.stack(secure_activations).mean(dim=0).cuda()
                
                # Steering vector: direction from vulnerable toward secure (proven formula)
                steering_vector = (secure_mean - vulnerable_mean).detach()
                
                # Normalize like successful experiments
                norm = torch.norm(steering_vector)
                if norm > 0:
                    steering_vector = steering_vector / norm
                    logger.info(f"✅ Created normalized StarCoder steering vector for layer {layer_idx} with shape {steering_vector.shape}, norm: {norm:.4f}")
                else:
                    logger.warning(f"⚠️ Zero norm steering vector for layer {layer_idx}")
                
                steering_vectors[f"layer_{layer_idx}"] = steering_vector
                
                # Clean up intermediate tensors
                del vulnerable_mean, secure_mean
                aggressive_memory_cleanup()
                
            except Exception as e:
                logger.error(f"❌ Error creating steering vector for layer {layer_idx}: {e}")
        else:
            logger.warning(f"⚠️ Could not create steering vector for layer {layer_idx} - insufficient activations (vulnerable: {len(vulnerable_activations)}, secure: {len(secure_activations)})")
        
        # Clear activation lists
        vulnerable_activations.clear()
        secure_activations.clear()
    
    return steering_vectors

def generate_with_starcoder_steering(model, prompt: str, steering_vectors: Dict[str, torch.Tensor], 
                                    config: StarCoderExperimentConfig) -> str:
    """
    Generate text WITH StarCoder steering applied (following successful patterns).
    """
    try:
        with model.trace() as tracer:
            with tracer.invoke(prompt) as invoker:
                # Apply steering to StarCoder layers (proven pattern)
                for layer_key, steering_vector in steering_vectors.items():
                    layer_idx = int(layer_key.split('_')[1])
                    
                    if layer_idx < len(model.transformer.h):
                        # Apply steering to StarCoder layer output
                        current_output = model.transformer.h[layer_idx].output
                        
                        # StarCoder steering application (different from Qwen2.5)
                        steered_output = current_output.clone()
                        steered_output[0, -1, :] += config.steering_strength * steering_vector
                        model.transformer.h[layer_idx].output = steered_output
                
                # Generate with steering applied (proven NNSight pattern)
                outputs = model.generate(
                    invoker.input,
                    max_new_tokens=config.max_new_tokens,
                    temperature=config.temperature,
                    do_sample=True,
                    pad_token_id=model.tokenizer.eos_token_id
                )
                
                # Decode generated tokens
                input_length = len(invoker.input[0])
                generated_tokens = outputs[0][input_length:]
                response = model.tokenizer.decode(generated_tokens, skip_special_tokens=True)
                
                return response.strip()
                
    except Exception as e:
        logger.error(f"❌ Error in StarCoder steered generation: {e}")
        return "ERROR_STARCODER_STEERED_GENERATION"

def generate_without_starcoder_steering(model, prompt: str, config: StarCoderExperimentConfig) -> str:
    """
    Generate text WITHOUT steering (StarCoder baseline).
    """
    try:
        # Tokenize input
        inputs = model.tokenizer(prompt, return_tensors="pt").to(model.device)
        
        # Generate baseline response
        with torch.no_grad():
            outputs = model.generate(
                inputs.input_ids,
                max_new_tokens=config.max_new_tokens,
                temperature=config.temperature,
                do_sample=True,
                pad_token_id=model.tokenizer.eos_token_id
            )
        
        # Decode generated tokens
        input_length = inputs.input_ids.shape[1]
        generated_tokens = outputs[0][input_length:]
        response = model.tokenizer.decode(generated_tokens, skip_special_tokens=True)
        
        return response.strip()
        
    except Exception as e:
        logger.error(f"❌ Error in StarCoder baseline generation: {e}")
        return "ERROR_STARCODER_BASELINE_GENERATION"

def evaluate_starcoder_response(response: str, expected_vulnerable: bool) -> Tuple[bool, float]:
    """
    Evaluate a StarCoder vulnerability assessment response.
    """
    response_lower = response.lower()
    
    # Look for clear vulnerability indicators (same as before)
    vulnerable_indicators = ['vulnerable', 'yes', 'security vulnerability', 'unsafe', 'exploitable', 'injection', 'dangerous', 'attack']
    secure_indicators = ['secure', 'no', 'safe', 'protected', 'not vulnerable', 'properly sanitized']
    
    vulnerable_score = sum(1 for indicator in vulnerable_indicators if indicator in response_lower)
    secure_score = sum(1 for indicator in secure_indicators if indicator in response_lower)
    
    # Determine assessment
    if vulnerable_score > secure_score:
        predicted_vulnerable = True
        confidence = vulnerable_score / (vulnerable_score + secure_score + 1)
    elif secure_score > vulnerable_score:
        predicted_vulnerable = False
        confidence = secure_score / (vulnerable_score + secure_score + 1)
    else:
        # Default to secure if unclear
        predicted_vulnerable = False
        confidence = 0.5
    
    # Check if prediction matches expectation
    correct = predicted_vulnerable == expected_vulnerable
    
    return correct, confidence

def evaluate_starcoder_steering(model, examples: List[Dict[str, Any]], 
                               steering_vectors: Dict[str, torch.Tensor], 
                               config: StarCoderExperimentConfig) -> Dict[str, Any]:
    """
    Evaluate StarCoder steering effectiveness using full text generation.
    """
    results = {
        'baseline_correct': 0,
        'steered_correct': 0,
        'total_examples': 0,
        'improvements': [],
        'examples': [],
        'baseline_confidence': [],
        'steered_confidence': []
    }
    
    # Test on all available examples
    test_examples = examples[:6]  # Test 6 examples for good statistics
    
    for i, example in enumerate(test_examples):
        try:
            logger.info(f"🧪 Evaluating StarCoder example {i+1}/{len(test_examples)}: {example['filename']}")
            prompt = create_vulnerability_prompt(example['content'])
            expected_vulnerable = (example['label'] == 'vulnerable')
            
            aggressive_memory_cleanup()
            
            # StarCoder baseline generation (no steering)
            logger.info(f"  📊 Generating StarCoder baseline response...")
            baseline_response = generate_without_starcoder_steering(model, prompt, config)
            baseline_correct, baseline_confidence = evaluate_starcoder_response(baseline_response, expected_vulnerable)
            
            logger.info(f"  📊 StarCoder baseline response: '{baseline_response[:100]}...'")
            logger.info(f"  📊 StarCoder baseline assessment: {'✅' if baseline_correct else '❌'} (confidence: {baseline_confidence:.3f})")
            
            aggressive_memory_cleanup()
            
            # StarCoder steered generation
            logger.info(f"  🎯 Generating StarCoder steered response...")
            steered_response = generate_with_starcoder_steering(model, prompt, steering_vectors, config)
            steered_correct, steered_confidence = evaluate_starcoder_response(steered_response, expected_vulnerable)
            
            logger.info(f"  🎯 StarCoder steered response: '{steered_response[:100]}...'")
            logger.info(f"  🎯 StarCoder steered assessment: {'✅' if steered_correct else '❌'} (confidence: {steered_confidence:.3f})")
            
            # Calculate improvement
            if steered_correct and not baseline_correct:
                improvement = 1  # Improvement
            elif baseline_correct and not steered_correct:
                improvement = -1  # Degradation
            else:
                improvement = 0  # No change
            
            # Store results
            if baseline_correct:
                results['baseline_correct'] += 1
            if steered_correct:
                results['steered_correct'] += 1
                
            results['improvements'].append(improvement)
            results['baseline_confidence'].append(baseline_confidence)
            results['steered_confidence'].append(steered_confidence)
            
            results['examples'].append({
                'filename': example['filename'],
                'expected_vulnerable': expected_vulnerable,
                'baseline_response': baseline_response,
                'steered_response': steered_response,
                'baseline_correct': baseline_correct,
                'steered_correct': steered_correct,
                'baseline_confidence': baseline_confidence,
                'steered_confidence': steered_confidence,
                'improvement': improvement
            })
            
            results['total_examples'] += 1
            
            logger.info(f"  📊 Expected: {'vulnerable' if expected_vulnerable else 'secure'}")
            logger.info(f"  📊 Baseline: {'✅' if baseline_correct else '❌'} | Steered: {'✅' if steered_correct else '❌'} | Improvement: {improvement}")
            
        except Exception as e:
            logger.error(f"❌ Error evaluating StarCoder example {example.get('filename', 'unknown')}: {e}")
            aggressive_memory_cleanup()
            continue
    
    return results

def run_starcoder_test_experiment(config: StarCoderExperimentConfig):
    """
    Run the StarCoder CWE steering test experiment (following successful patterns).
    """
    logger.info("🚀 Starting StarCoder CWE Steering Test Experiment (Following Successful Patterns)")
    
    # Create results directory
    results_dir = Path(config.results_dir)
    results_dir.mkdir(exist_ok=True)
    (results_dir / "steering_vectors").mkdir(exist_ok=True)
    
    experiment_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    logger.info(f"🧪 Experiment ID: {experiment_id}")
    
    start_time = time.time()
    
    # Load StarCoder model (proven to work)
    logger.info(f"🚀 Loading StarCoder model: {config.model_name}")
    aggressive_memory_cleanup()
    
    try:
        model = LanguageModel(config.model_name, device_map=config.device)
        logger.info("✅ StarCoder model loaded successfully")
        logger.info(f"📊 StarCoder layers: {len(model.transformer.h)}")  # StarCoder architecture
    except Exception as e:
        logger.error(f"❌ Failed to load StarCoder model: {e}")
        return
    
    # Load dataset
    logger.info("📚 Loading REAL SecLLMHolmes dataset for StarCoder test...")
    dataset_path = security_dir / "SecLLMHolmes" / "datasets" / "hand-crafted" / "dataset"
    
    if not dataset_path.exists():
        logger.error(f"❌ SecLLMHolmes dataset not found at {dataset_path}")
        return
        
    try:
        cwe_data = load_secllmholmes_data(dataset_path)  # Testing first 3 CWEs
        total_examples = sum(len(examples) for examples in cwe_data.values())
        logger.info(f"📊 Loaded {total_examples} total REAL examples across {len(cwe_data)} CWEs for StarCoder test")
        
    except Exception as e:
        logger.error(f"❌ Failed to load dataset: {e}")
        return
    
    # Process each CWE with StarCoder
    all_results = {}
    successful_cwes = 0
    
    for cwe_name, examples in cwe_data.items():
        logger.info(f"🎯 Processing CWE with StarCoder: {cwe_name}")
        
        try:
            # Create StarCoder steering vectors
            logger.info(f"🎯 Creating StarCoder steering vectors for {cwe_name}")
            steering_vectors = create_starcoder_steering_vectors(model, examples, config)
            
            if not steering_vectors:
                logger.warning(f"⚠️ No StarCoder steering vectors created for {cwe_name}")
                continue
            
            # Save steering vectors
            steering_file = results_dir / "steering_vectors" / f"{cwe_name.lower()}_starcoder_steering_vectors.pt"
            torch.save(steering_vectors, steering_file)
            logger.info(f"💾 Saved StarCoder steering vectors to: {steering_file}")
            
            # Evaluate StarCoder steering effectiveness
            logger.info(f"🧪 Evaluating StarCoder steering effectiveness for {cwe_name}")
            evaluation_results = evaluate_starcoder_steering(model, examples, steering_vectors, config)
            
            # Calculate metrics
            total = evaluation_results['total_examples']
            baseline_acc = evaluation_results['baseline_correct'] / total if total > 0 else 0
            steered_acc = evaluation_results['steered_correct'] / total if total > 0 else 0
            improvements = evaluation_results['improvements']
            avg_improvement = np.mean(improvements) if improvements else 0
            
            avg_baseline_confidence = np.mean(evaluation_results['baseline_confidence']) if evaluation_results['baseline_confidence'] else 0
            avg_steered_confidence = np.mean(evaluation_results['steered_confidence']) if evaluation_results['steered_confidence'] else 0
            
            positive_improvements = len([x for x in improvements if x > 0])
            negative_improvements = len([x for x in improvements if x < 0])
            no_change = len([x for x in improvements if x == 0])
            
            logger.info(f"📊 {cwe_name} StarCoder Results:")
            logger.info(f"  Examples Tested: {total}")
            logger.info(f"  Baseline Accuracy: {baseline_acc:.3f} (confidence: {avg_baseline_confidence:.3f})")
            logger.info(f"  Steered Accuracy: {steered_acc:.3f} (confidence: {avg_steered_confidence:.3f})")
            logger.info(f"  Average Improvement: {avg_improvement:.3f}")
            logger.info(f"  Improvements: +{positive_improvements}/-{negative_improvements}/={no_change}")
            
            # Store results
            all_results[cwe_name] = {
                'baseline_accuracy': baseline_acc,
                'steered_accuracy': steered_acc,
                'average_improvement': avg_improvement,
                'baseline_confidence': avg_baseline_confidence,
                'steered_confidence': avg_steered_confidence,
                'positive_improvements': positive_improvements,
                'negative_improvements': negative_improvements,
                'no_change': no_change,
                'total_examples': total,
                'detailed_results': evaluation_results
            }
            
            successful_cwes += 1
            
            # Save intermediate results
            intermediate_file = results_dir / f"intermediate_starcoder_{cwe_name.lower()}_{experiment_id}.json"
            with open(intermediate_file, 'w') as f:
                json.dump(all_results[cwe_name], f, indent=2, default=str)
            logger.info(f"💾 Saved StarCoder intermediate results: {intermediate_file}")
            
        except Exception as e:
            logger.error(f"❌ Error processing {cwe_name} with StarCoder: {e}")
            continue
        
        # Memory cleanup between CWEs
        logger.info("🧹 Memory cleanup...")
        aggressive_memory_cleanup()
    
    # Final results
    end_time = time.time()
    duration = end_time - start_time
    
    logger.info(f"\n🎉 StarCoder CWE Steering Test Experiment Complete!")
    
    if all_results:
        overall_baseline = np.mean([r['baseline_accuracy'] for r in all_results.values()])
        overall_steered = np.mean([r['steered_accuracy'] for r in all_results.values()])
        overall_improvement = np.mean([r['average_improvement'] for r in all_results.values()])
        
        total_examples = sum(r['total_examples'] for r in all_results.values())
        total_positive = sum(r['positive_improvements'] for r in all_results.values())
        improvement_rate = total_positive / total_examples if total_examples > 0 else 0
        
        logger.info(f"📁 StarCoder results saved to: {results_dir}")
        logger.info(f"⏱️ Total Duration: {duration:.1f} seconds")
        logger.info(f"📊 STARCODER RESULTS:")
        logger.info(f"   CWEs Successfully Tested: {successful_cwes}/{len(cwe_data)}")
        logger.info(f"   Total Examples: {total_examples}")
        logger.info(f"   Baseline Accuracy: {overall_baseline:.3f}")
        logger.info(f"   Steered Accuracy: {overall_steered:.3f}")
        logger.info(f"   Average Improvement: {overall_improvement:.3f}")
        logger.info(f"   Improvement Rate: {improvement_rate:.3f}")
        
        # Save final results
        final_results = {
            'experiment_id': experiment_id,
            'config': asdict(config),
            'experiment_type': 'STARCODER_CWE_STEERING_TEST',
            'model_used': config.model_name,
            'steering_approach': 'Multi-layer steering with proven patterns',
            'success_summary': {
                'successful_cwes': successful_cwes,
                'total_cwes': len(cwe_data),
                'success_rate': successful_cwes / len(cwe_data) if cwe_data else 0
            },
            'duration_seconds': duration,
            'overall_metrics': {
                'baseline_accuracy': overall_baseline,
                'steered_accuracy': overall_steered,
                'average_improvement': overall_improvement,
                'improvement_rate': improvement_rate,
                'total_examples': total_examples,
                'cwes_tested': len(all_results)
            },
            'comparison_to_previous': {
                'previous_best_improvement': '4.4x-13x improvements achieved',
                'current_improvement_rate': f'{improvement_rate:.1%}',
                'model_comparison': 'StarCoder 1B vs previous StarCoder experiments'
            },
            'cwe_results': all_results,
            'nnsight_version': nnsight.__version__
        }
        
        final_file = results_dir / f"cwe_steering_starcoder_test_{experiment_id}.json"
        with open(final_file, 'w') as f:
            json.dump(final_results, f, indent=2, default=str)
        
        logger.info(f"✅ StarCoder CWE steering test experiment completed successfully!")
        logger.info(f"📄 Final results: {final_file}")
        
        # Compare to expected results
        if improvement_rate > 0.1:  # 10% improvement rate
            logger.info(f"🎯 SUCCESS: StarCoder shows {improvement_rate:.1%} improvement rate!")
            logger.info(f"📈 This confirms the methodology works - issue was likely Qwen2.5-specific!")
        elif improvement_rate > 0:
            logger.info(f"🔍 PARTIAL SUCCESS: StarCoder shows {improvement_rate:.1%} improvement rate")
            logger.info(f"📊 Better than Qwen2.5's 0.0% - methodology partially working")
        else:
            logger.info(f"⚠️ Still no improvement with StarCoder - deeper issue with current implementation")
            logger.info(f"📋 Need to investigate NNSight API changes or methodology")
        
    else:
        logger.error("❌ No results generated - StarCoder experiment failed")

if __name__ == "__main__":
    config = StarCoderExperimentConfig()
    run_starcoder_test_experiment(config) 