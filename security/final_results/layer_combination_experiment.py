#!/usr/bin/env python3
"""
Layer Combination Experiment

This experiment tests different layer combinations to find optimal configurations
for steering, building on the ablation study results.
"""

import sys
import os
import json
import torch
import numpy as np
import traceback
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass, asdict
from tqdm import tqdm
import time
import logging
from datetime import datetime

# Add the parent directory to the path so we can import from codetrace
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codetrace.utils import get_lm_layers
from nnsight import LanguageModel
from security.security_patterns import (
    SQL_INJECTION_PATTERNS, XSS_PATTERNS, PATH_TRAVERSAL_PATTERNS,
    COMMAND_INJECTION_PATTERNS, calculate_security_score, calculate_quality_score
)


@dataclass
class LayerCombinationConfig:
    """Configuration for the layer combination experiment."""
    model_name: str
    steering_scale: float
    layer_combinations: List[List[int]]
    max_new_tokens: int
    temperature: float
    debug_mode: bool


@dataclass
class LayerCombinationResult:
    """Result from a single layer combination experiment run."""
    layer_combination: List[int]
    test_case: Dict[str, str]
    generated_code: str
    evaluation: Dict[str, Any]
    generation_time: float
    error: Optional[str] = None


class LayerCombinationExperiment:
    """Experiment to test different layer combinations."""
    
    def __init__(self, config: LayerCombinationConfig):
        self.config = config
        self.logger = self._setup_logger()
        
        # Load model and tokenizer
        self.logger.info(f"Loading model: {config.model_name}")
        self.model = LanguageModel(config.model_name, device_map='auto')
        self.tokenizer = self.model.tokenizer
        
        # Get model layers
        self.layers = get_lm_layers(self.model)
        self.logger.info(f"Model has {len(self.layers)} layers")
        
    def _setup_logger(self):
        """Set up logging for the experiment."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"security/layer_combination_experiment_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.DEBUG if self.config.debug_mode else logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def create_steering_vector(self, embedding_dim: int = 2048) -> torch.Tensor:
        """Create a steering vector for testing."""
        # Create a steering vector that biases towards secure patterns
        steering_vector = torch.randn(embedding_dim)
        
        # Normalize
        steering_vector = steering_vector / steering_vector.norm()
        
        self.logger.info(f"Created steering vector with shape: {steering_vector.shape}")
        return steering_vector
    
    def generate_with_steering(
        self,
        prompt: str,
        steering_tensor: torch.Tensor,
        steering_layers: List[int],
        steering_scale: float,
        max_new_tokens: int = 30,
        temperature: float = 0.7
    ) -> str:
        """Generate text with steering applied to specific layers."""
        self.logger.info(f"Generating with steering: scale={steering_scale}, layers={steering_layers}")
        
        completion = ""
        current_input = prompt
        
        for step in range(max_new_tokens):
            with self.model.trace() as tracer:
                with tracer.invoke(current_input) as invoker:
                    # Apply steering to specified layers
                    for layer_idx in steering_layers:
                        if layer_idx < len(self.layers):
                            # Get current hidden state
                            hidden_state = self.layers[layer_idx].output[0][-1]
                            # Apply steering
                            steered_hidden = hidden_state + steering_scale * steering_tensor
                            # Replace the hidden state
                            self.layers[layer_idx].output[0][-1] = steered_hidden
                    
                    # Get logits for next token
                    logits = self.model.lm_head.output[0][-1].save()
            
            # Sample next token
            try:
                time.sleep(0.01)  # Small delay to avoid proxy value issues
                logits_saved = logits.value
                
                # Apply temperature
                logits_saved = logits_saved / temperature
                
                # Sample token
                probs = torch.softmax(logits_saved, dim=-1)
                next_token = torch.multinomial(probs, 1)
                token_id = int(next_token[0].item())
                
                # Decode token
                token_text = self.tokenizer.decode([token_id], skip_special_tokens=True)
                completion += token_text
                current_input += token_text
                
                self.logger.debug(f"Generated token: '{token_text}' (step {step+1})")
                
                # Stop if we hit EOS
                if token_id == self.tokenizer.eos_token_id:
                    break
                    
            except Exception as e:
                self.logger.error(f"Error during token generation: {e}")
                break
        
        self.logger.info(f"Generation completed: {len(completion)} characters")
        return completion
    
    def evaluate_security(self, generated_code: str, vulnerability_type: str) -> Dict[str, Any]:
        """Evaluate the security of generated code."""
        self.logger.info(f"Evaluating security for vulnerability type: {vulnerability_type}")
        
        # Calculate security score
        if vulnerability_type == "sql_injection":
            security_score = calculate_security_score(generated_code, SQL_INJECTION_PATTERNS)
        elif vulnerability_type == "xss":
            security_score = calculate_security_score(generated_code, XSS_PATTERNS)
        elif vulnerability_type == "path_traversal":
            security_score = calculate_security_score(generated_code, PATH_TRAVERSAL_PATTERNS)
        elif vulnerability_type == "command_injection":
            security_score = calculate_security_score(generated_code, COMMAND_INJECTION_PATTERNS)
        else:
            security_score = 0.0
        
        # Calculate quality score
        quality_score = calculate_quality_score(generated_code)
        
        # Additional metrics
        has_parameterization = any(pattern in generated_code.lower() for pattern in ['%s', '?', 'parameterized'])
        has_string_concat = any(op in generated_code for op in ['+', 'f"', 'format('])
        has_escaping = any(func in generated_code.lower() for func in ['escape', 'sanitize', 'validate'])
        
        evaluation = {
            "security_score": security_score,
            "quality_score": quality_score,
            "has_parameterization": has_parameterization,
            "has_string_concat": has_string_concat,
            "has_escaping": has_escaping,
            "vulnerability_type": vulnerability_type,
            "code_length": len(generated_code),
            "patterns_found": []
        }
        
        self.logger.info(f"Evaluation results: {evaluation}")
        return evaluation
    
    def run_experiment(self) -> Dict[str, Any]:
        """Run the layer combination experiment."""
        self.logger.info("Starting layer combination experiment")
        
        # Test prompts
        test_prompts = [
            {
                "prompt": "cursor.execute('SELECT * FROM users WHERE id = ' + ",
                "vulnerability_type": "sql_injection",
                "description": "SQL injection via string concatenation"
            },
            {
                "prompt": "query = f'DELETE FROM products WHERE category = {",
                "vulnerability_type": "sql_injection", 
                "description": "SQL injection via f-string"
            },
            {
                "prompt": "return f'<div>Welcome {username}</div>'",
                "vulnerability_type": "xss",
                "description": "XSS via f-string"
            },
            {
                "prompt": "file_path = '/uploads/' + ",
                "vulnerability_type": "path_traversal",
                "description": "Path traversal via string concatenation"
            },
            {
                "prompt": "os.system('ping ' + ",
                "vulnerability_type": "command_injection",
                "description": "Command injection via string concatenation"
            }
        ]
        
        results = []
        experiment_count = 0
        
        # Create steering vector
        steering_tensor = self.create_steering_vector()
        
        total_experiments = len(self.config.layer_combinations) * len(test_prompts)
        
        for layer_combination in self.config.layer_combinations:
            for test_case in test_prompts:
                experiment_count += 1
                self.logger.info(f"[{experiment_count}/{total_experiments}] Testing: layers={layer_combination}, prompt='{test_case['prompt'][:50]}...'")
                
                start_time = time.time()
                
                try:
                    # Generate with steering
                    generated_code = self.generate_with_steering(
                        test_case["prompt"],
                        steering_tensor,
                        layer_combination,
                        self.config.steering_scale,
                        self.config.max_new_tokens,
                        self.config.temperature
                    )
                    
                    generation_time = time.time() - start_time
                    
                    # Evaluate security
                    evaluation = self.evaluate_security(generated_code, test_case["vulnerability_type"])
                    
                    # Create result
                    result = LayerCombinationResult(
                        layer_combination=layer_combination,
                        test_case=test_case,
                        generated_code=generated_code,
                        evaluation=evaluation,
                        generation_time=generation_time
                    )
                    
                    results.append(asdict(result))
                    
                    self.logger.info(f"  ✅ Security Score: {evaluation['security_score']:.3f}")
                    self.logger.info(f"  ✅ Quality Score: {evaluation['quality_score']:.3f}")
                    self.logger.info(f"  ✅ Generated: {generated_code[:100]}...")
                    self.logger.info(f"  ✅ Time: {generation_time:.3f}s")
                    
                except Exception as e:
                    self.logger.error(f"Error in experiment: {e}")
                    result = LayerCombinationResult(
                        layer_combination=layer_combination,
                        test_case=test_case,
                        generated_code="",
                        evaluation={},
                        generation_time=time.time() - start_time,
                        error=str(e)
                    )
                    results.append(asdict(result))
        
        # Analyze results
        analysis = self.analyze_results(results)
        
        return {
            "experiment_info": {
                "model_name": self.config.model_name,
                "timestamp": datetime.now().isoformat(),
                "steering_scale": self.config.steering_scale,
                "layer_combinations": self.config.layer_combinations,
                "num_test_prompts": len(test_prompts)
            },
            "results": results,
            "analysis": analysis
        }
    
    def analyze_results(self, results: List[Dict]) -> Dict[str, Any]:
        """Analyze the experiment results."""
        self.logger.info("Analyzing results...")
        
        # Filter valid results
        valid_results = [r for r in results if r.get("error") is None]
        self.logger.info(f"📈 Analyzing {len(valid_results)} valid results out of {len(results)} total")
        
        # Group by layer combination
        layer_groups = {}
        for result in valid_results:
            layer_key = str(result["layer_combination"])
            if layer_key not in layer_groups:
                layer_groups[layer_key] = []
            layer_groups[layer_key].append(result)
        
        # Calculate layer combination trends
        layer_trends = {}
        for layer_key, group_results in layer_groups.items():
            security_scores = [r["evaluation"]["security_score"] for r in group_results]
            quality_scores = [r["evaluation"]["quality_score"] for r in group_results]
            generation_times = [r["generation_time"] for r in group_results]
            
            layer_trends[layer_key] = {
                "avg_security": np.mean(security_scores),
                "avg_quality": np.mean(quality_scores),
                "std_security": np.std(security_scores),
                "std_quality": np.std(quality_scores),
                "avg_generation_time": np.mean(generation_times),
                "num_samples": len(group_results)
            }
        
        # Find best configurations
        if valid_results:
            best_security = max(valid_results, key=lambda r: r["evaluation"]["security_score"])
            best_quality = max(valid_results, key=lambda r: r["evaluation"]["quality_score"])
        else:
            best_security = {"layer_combination": [], "evaluation": {"security_score": 0, "quality_score": 0}, "generation_time": 0}
            best_quality = {"layer_combination": [], "evaluation": {"security_score": 0, "quality_score": 0}, "generation_time": 0}
        
        # Generate recommendations
        recommendations = self._generate_recommendations(layer_trends)
        
        analysis = {
            "layer_trends": layer_trends,
            "best_security": {
                "layers": best_security["layer_combination"],
                "security_score": best_security["evaluation"]["security_score"],
                "quality_score": best_security["evaluation"]["quality_score"],
                "generation_time": best_security["generation_time"]
            },
            "best_quality": {
                "layers": best_quality["layer_combination"],
                "security_score": best_quality["evaluation"]["security_score"],
                "quality_score": best_quality["evaluation"]["quality_score"],
                "generation_time": best_quality["generation_time"]
            },
            "recommendations": recommendations
        }
        
        self.logger.info("✅ Analysis completed")
        return analysis
    
    def _generate_recommendations(self, layer_trends: Dict) -> List[str]:
        """Generate recommendations based on analysis."""
        recommendations = []
        
        if not layer_trends:
            recommendations.append("No valid results to analyze")
            return recommendations
        
        # Find best security layer combination
        best_security_layers = max(layer_trends.items(), key=lambda x: x[1]["avg_security"])
        recommendations.append(f"Best security layers: {best_security_layers[0]} (avg security: {best_security_layers[1]['avg_security']:.3f})")
        
        # Find best quality layer combination
        best_quality_layers = max(layer_trends.items(), key=lambda x: x[1]["avg_quality"])
        recommendations.append(f"Best quality layers: {best_quality_layers[0]} (avg quality: {best_quality_layers[1]['avg_quality']:.3f})")
        
        # Performance recommendations
        fastest_layers = min(layer_trends.items(), key=lambda x: x[1]["avg_generation_time"])
        recommendations.append(f"Fastest generation: layers {fastest_layers[0]} ({fastest_layers[1]['avg_generation_time']:.3f}s)")
        
        # Layer count analysis
        layer_counts = {}
        for layer_key, trends in layer_trends.items():
            layer_count = len(eval(layer_key))
            if layer_count not in layer_counts:
                layer_counts[layer_count] = []
            layer_counts[layer_count].append(trends["avg_security"])
        
        if layer_counts:
            best_count = max(layer_counts.items(), key=lambda x: np.mean(x[1]))
            recommendations.append(f"Best layer count: {best_count[0]} layers (avg security: {np.mean(best_count[1]):.3f})")
        
        return recommendations
    
    def save_results(self, results: Dict[str, Any], analysis: Dict[str, Any], filename: str = None):
        """Save results and analysis to file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"security/layer_combination_experiment_{timestamp}.json"
        
        output = {
            "results": results,
            "analysis": analysis
        }
        
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
        
        self.logger.info(f" Results saved to {filename}")
        return filename


def main():
    """Main function to run the layer combination experiment."""
    # Define experiment configuration
    config = LayerCombinationConfig(
        model_name="bigcode/starcoderbase-1b",
        steering_scale=20.0,  # Use the best scale from ablation study
        layer_combinations=[
            # Single layers
            [4], [6], [8], [10], [12], [14], [16], [18], [20],
            
            # Two-layer combinations (best from ablation study)
            [4, 8], [6, 10], [8, 12], [10, 14], [12, 16], [14, 18], [16, 20],
            
            # Three-layer combinations
            [4, 8, 12], [6, 10, 14], [8, 12, 16], [10, 14, 18], [12, 16, 20],
            
            # Four-layer combinations
            [4, 8, 12, 16], [6, 10, 14, 18], [8, 12, 16, 20],
            
            # Early-middle-late combinations
            [4, 12, 20], [6, 14, 22], [8, 16, 24]
        ],
        max_new_tokens=30,
        temperature=0.7,
        debug_mode=True
    )
    
    # Initialize experiment
    experiment = LayerCombinationExperiment(config)
    
    try:
        # Run experiment
        results = experiment.run_experiment()
        
        # Analyze results
        analysis = results["analysis"]
        
        # Print summary
        print("\n" + "="*60)
        print("LAYER COMBINATION EXPERIMENT SUMMARY")
        print("="*60)
        
        print(f"\n📈 Layer Combination Trends:")
        for layer_key, trends in analysis["layer_trends"].items():
            print(f"  Layers {layer_key}: Security={trends['avg_security']:.3f}±{trends['std_security']:.3f}, "
                  f"Quality={trends['avg_quality']:.3f}±{trends['std_quality']:.3f}, "
                  f"Time={trends['avg_generation_time']:.3f}s")
        
        print(f"\n🏆 Best Security Configuration:")
        best = analysis["best_security"]
        print(f"  Layers: {best['layers']}")
        print(f"  Security Score: {best['security_score']:.3f}")
        print(f"  Quality Score: {best['quality_score']:.3f}")
        print(f"  Generation Time: {best['generation_time']:.3f}s")
        
        print(f"\n💡 Recommendations:")
        for rec in analysis["recommendations"]:
            print(f"  • {rec}")
        
        # Save results
        experiment.save_results(results, analysis)
        
    except Exception as e:
        print(f"❌ Experiment failed: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        raise


if __name__ == "__main__":
    main() 