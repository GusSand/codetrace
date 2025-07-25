#!/usr/bin/env python3
"""
Comprehensive Neural Steering Experiment for SecLLMHolmes Dataset
Using Qwen NNSight Integration to test steering vector effectiveness

This experiment compares Qwen2.5-14B-Instruct performance on SecLLMHolmes:
1. Baseline performance (no steering)
2. Performance with CWE-specific steering vectors
3. Performance with cross-CWE steering vectors

Based on baseline results: Qwen2.5-14B-Instruct achieved 73.4% accuracy
Target: Improve performance through neural steering interventions
"""

import os
import sys
import json
import torch
import logging
import time
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import numpy as np
from tqdm import tqdm

# Add parent directory for imports
sys.path.append(str(Path(__file__).parent.parent))

from qwen_steering_integration import QwenNNSightSteering, QwenSteeringConfig

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ExperimentConfig:
    """Configuration for the comprehensive steering experiment."""
    # Model settings
    model_name: str = "Qwen/Qwen2.5-14B-Instruct"
    model_dtype: torch.dtype = torch.float16
    device_map: str = "auto"
    
    # Experiment settings
    steering_strength: float = 20.0
    normalization: bool = True
    examples_per_type: int = 3
    
    # Layer settings (proven effective for Qwen2.5-14B)
    target_layers: List[int] = None
    hidden_dim: int = 5120
    
    # Dataset settings
    dataset_path: str = "../security/SecLLMHolmes/datasets"
    max_examples_per_cwe: int = 10  # Limit for experiment efficiency
    
    # Evaluation settings
    temperature: float = 0.0  # Deterministic generation
    max_new_tokens: int = 200
    top_p: float = 1.0
    
    # Output settings
    results_dir: str = "results"
    save_activations: bool = False
    
    def __post_init__(self):
        if self.target_layers is None:
            # Proven effective layers for 48-layer Qwen2.5-14B
            self.target_layers = [12, 24, 36, 47]

class SecLLMHolmesEvaluator:
    """Evaluates model performance on SecLLMHolmes dataset."""
    
    def __init__(self, config: ExperimentConfig):
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
            
            # Limit examples for experiment efficiency
            if len(cwe_data) > self.config.max_examples_per_cwe:
                cwe_data = cwe_data[:self.config.max_examples_per_cwe]
                
            test_data[cwe_id] = cwe_data
            logger.info(f"📊 Loaded {len(cwe_data)} examples for {cwe_id}")
        
        return test_data
    
    def create_prompt(self, code: str) -> str:
        """Create standardized prompt for vulnerability detection."""
        return f"Security review of this code:\n\n{code}\n\nAnswer:"
    
    def parse_response(self, response: str) -> Tuple[str, str]:
        """Parse model response to extract answer and reasoning."""
        # Look for structured response pattern
        if "Answer:" in response:
            parts = response.split("Answer:", 1)
            if len(parts) >= 2:
                reasoning = parts[0].strip()
                answer_part = parts[1].strip()
                
                # Extract the actual answer
                if "This code contains security vulnerabilities" in answer_part:
                    answer = "vulnerable"
                elif "This code is secure" in answer_part or "no vulnerabilities" in answer_part.lower():
                    answer = "secure"
                else:
                    answer = "uncertain"
                    
                return answer, reasoning
        
        # Fallback parsing
        response_lower = response.lower()
        if "security vulnerabilities" in response_lower or "vulnerable" in response_lower:
            return "vulnerable", response
        elif "secure" in response_lower or "no vulnerabilities" in response_lower:
            return "secure", response
        else:
            return "uncertain", response
    
    def evaluate_example(self, model, tokenizer, example: Dict, steering_vectors: Optional[Dict] = None) -> Dict:
        """Evaluate a single example with optional steering."""
        prompt = self.create_prompt(example["content"])
        
        # Tokenize input
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
        
        # Generate with or without steering
        if steering_vectors:
            # Apply steering vectors during generation
            with model.trace(inputs) as tracer:
                # Apply steering to target layers
                for layer_idx in self.config.target_layers:
                    layer_name = f"model.layers.{layer_idx}.mlp"
                    if layer_name in steering_vectors:
                        # Apply steering vector to hidden states
                        hidden_states = tracer[layer_name].output[0]
                        steering_vector = steering_vectors[layer_name]
                        tracer[layer_name].output = (
                            hidden_states + self.config.steering_strength * steering_vector.unsqueeze(0),
                        )
                
                # Generate with steering
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=self.config.max_new_tokens,
                    temperature=self.config.temperature,
                    top_p=self.config.top_p,
                    do_sample=False,
                    pad_token_id=tokenizer.eos_token_id
                )
        else:
            # Standard generation without steering
            outputs = model.generate(
                **inputs,
                max_new_tokens=self.config.max_new_tokens,
                temperature=self.config.temperature,
                top_p=self.config.top_p,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id
            )
        
        # Decode response
        response = tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
        
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

class ComprehensiveSteeringExperiment:
    """Main experiment class for comprehensive steering evaluation."""
    
    def __init__(self, config: ExperimentConfig):
        self.config = config
        self.evaluator = SecLLMHolmesEvaluator(config)
        self.results_dir = Path(config.results_dir)
        self.results_dir.mkdir(exist_ok=True)
        
    def run_baseline_experiment(self, model, tokenizer) -> Dict:
        """Run baseline experiment without steering vectors."""
        logger.info("🔬 Running baseline experiment (no steering)...")
        
        test_data = self.evaluator.load_test_data()
        results = {"baseline": []}
        
        total_examples = sum(len(examples) for examples in test_data.values())
        
        with tqdm(total=total_examples, desc="Baseline Evaluation") as pbar:
            for cwe_id, examples in test_data.items():
                for example in examples:
                    result = self.evaluator.evaluate_example(model, tokenizer, example)
                    result["experiment_type"] = "baseline"
                    results["baseline"].append(result)
                    pbar.update(1)
        
        return results
    
    def run_steering_experiment(self, model, tokenizer, steering_vectors: Dict, experiment_name: str) -> Dict:
        """Run experiment with steering vectors."""
        logger.info(f"🎯 Running steering experiment: {experiment_name}")
        
        test_data = self.evaluator.load_test_data()
        results = {experiment_name: []}
        
        total_examples = sum(len(examples) for examples in test_data.values())
        
        with tqdm(total=total_examples, desc=f"{experiment_name} Evaluation") as pbar:
            for cwe_id, examples in test_data.items():
                for example in examples:
                    result = self.evaluator.evaluate_example(model, tokenizer, example, steering_vectors)
                    result["experiment_type"] = experiment_name
                    results[experiment_name].append(result)
                    pbar.update(1)
        
        return results
    
    def create_cwe_specific_vectors(self, cwe_id: str) -> Optional[Dict]:
        """Create steering vectors for a specific CWE."""
        logger.info(f"🔧 Creating steering vectors for {cwe_id}")
        
        # Load training data for this CWE
        dataset_path = Path(self.config.dataset_path) / "hand-crafted" / "dataset" / cwe_id
        
        vulnerable_examples = []
        secure_examples = []
        
        # Load vulnerable examples
        for file_path in dataset_path.glob("[0-9]*.c"):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    vulnerable_examples.append({
                        "content": content,
                        "label": "vulnerable",
                        "cwe": cwe_id,
                        "file": str(file_path.name)
                    })
            except Exception as e:
                logger.warning(f"⚠️ Error reading {file_path}: {e}")
        
        # Load secure examples
        for file_path in dataset_path.glob("p_*.c"):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    secure_examples.append({
                        "content": content,
                        "label": "secure",
                        "cwe": cwe_id,
                        "file": str(file_path.name)
                    })
            except Exception as e:
                logger.warning(f"⚠️ Error reading {file_path}: {e}")
        
        if not vulnerable_examples or not secure_examples:
            logger.warning(f"⚠️ Insufficient data for {cwe_id}")
            return None
        
        # Create steering vectors
        try:
            steerer = QwenNNSightSteering(QwenSteeringConfig(
                model_name=self.config.model_name,
                steering_strength=self.config.steering_strength,
                normalization=self.config.normalization,
                examples_per_type=self.config.examples_per_type,
                target_layers=self.config.target_layers,
                hidden_dim=self.config.hidden_dim
            ))
            
            steerer.load_model()
            
            vectors = steerer.create_steering_vectors(
                vulnerable_examples=vulnerable_examples,
                secure_examples=secure_examples,
                cwe_type=cwe_id
            )
            
            return vectors
            
        except Exception as e:
            logger.error(f"❌ Error creating vectors for {cwe_id}: {e}")
            return None
    
    def analyze_results(self, all_results: Dict) -> Dict:
        """Analyze and compare results across experiments."""
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
    
    def save_results(self, all_results: Dict, analysis: Dict, experiment_name: str):
        """Save experiment results and analysis."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed results
        results_file = self.results_dir / f"{experiment_name}_detailed_results_{timestamp}.json"
        with open(results_file, 'w') as f:
            json.dump(all_results, f, indent=2, default=str)
        
        # Save analysis
        analysis_file = self.results_dir / f"{experiment_name}_analysis_{timestamp}.json"
        with open(analysis_file, 'w') as f:
            json.dump(analysis, f, indent=2, default=str)
        
        # Save summary report
        summary_file = self.results_dir / f"{experiment_name}_summary_{timestamp}.md"
        self._generate_summary_report(analysis, summary_file, experiment_name)
        
        logger.info(f"💾 Results saved to {self.results_dir}")
        logger.info(f"   Detailed: {results_file}")
        logger.info(f"   Analysis: {analysis_file}")
        logger.info(f"   Summary: {summary_file}")
    
    def _generate_summary_report(self, analysis: Dict, output_file: Path, experiment_name: str):
        """Generate a markdown summary report."""
        with open(output_file, 'w') as f:
            f.write(f"# Comprehensive Steering Experiment Results\n\n")
            f.write(f"**Experiment**: {experiment_name}\n")
            f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Overall Performance Comparison\n\n")
            f.write("| Experiment | Accuracy | Examples | Reasoning Quality |\n")
            f.write("|------------|----------|----------|-------------------|\n")
            
            for exp_name, metrics in analysis.items():
                f.write(f"| {exp_name} | {metrics['overall_accuracy']:.3f} | {metrics['total_examples']} | {metrics['avg_reasoning_quality']:.3f} |\n")
            
            f.write("\n## Per-CWE Performance\n\n")
            f.write("| CWE | Baseline | Steering | Improvement |\n")
            f.write("|-----|----------|----------|-------------|\n")
            
            baseline_metrics = analysis.get("baseline", {}).get("cwe_metrics", {})
            steering_metrics = {}
            
            # Find steering experiment
            for exp_name, metrics in analysis.items():
                if exp_name != "baseline":
                    steering_metrics = metrics.get("cwe_metrics", {})
                    break
            
            for cwe in sorted(baseline_metrics.keys()):
                baseline_acc = baseline_metrics[cwe]["accuracy"]
                steering_acc = steering_metrics.get(cwe, {}).get("accuracy", 0)
                improvement = steering_acc - baseline_acc
                
                f.write(f"| {cwe} | {baseline_acc:.3f} | {steering_acc:.3f} | {improvement:+.3f} |\n")
            
            f.write("\n## Key Findings\n\n")
            
            # Calculate overall improvement
            baseline_acc = analysis.get("baseline", {}).get("overall_accuracy", 0)
            steering_acc = 0
            for exp_name, metrics in analysis.items():
                if exp_name != "baseline":
                    steering_acc = metrics.get("overall_accuracy", 0)
                    break
            
            improvement = steering_acc - baseline_acc
            f.write(f"- **Baseline Accuracy**: {baseline_acc:.3f}\n")
            f.write(f"- **Steering Accuracy**: {steering_acc:.3f}\n")
            f.write(f"- **Overall Improvement**: {improvement:+.3f} ({improvement*100:+.1f}%)\n")
            
            # Identify best/worst performing CWEs
            if steering_metrics:
                best_cwe = max(steering_metrics.items(), key=lambda x: x[1]["accuracy"])
                worst_cwe = min(steering_metrics.items(), key=lambda x: x[1]["accuracy"])
                
                f.write(f"- **Best Performing CWE**: {best_cwe[0]} ({best_cwe[1]['accuracy']:.3f})\n")
                f.write(f"- **Most Challenging CWE**: {worst_cwe[0]} ({worst_cwe[1]['accuracy']:.3f})\n")
    
    def run_comprehensive_experiment(self):
        """Run the complete comprehensive steering experiment."""
        logger.info("🚀 Starting Comprehensive Steering Experiment")
        logger.info(f"📊 Model: {self.config.model_name}")
        logger.info(f"🎯 Target Layers: {self.config.target_layers}")
        logger.info(f"💪 Steering Strength: {self.config.steering_strength}")
        
        start_time = time.time()
        
        try:
            # Initialize model
            steerer = QwenNNSightSteering(QwenSteeringConfig(
                model_name=self.config.model_name,
                steering_strength=self.config.steering_strength,
                normalization=self.config.normalization,
                examples_per_type=self.config.examples_per_type,
                target_layers=self.config.target_layers,
                hidden_dim=self.config.hidden_dim
            ))
            
            steerer.load_model()
            model = steerer.model
            tokenizer = steerer.tokenizer
            
            all_results = {}
            
            # 1. Run baseline experiment
            logger.info("\n" + "="*60)
            logger.info("🔬 PHASE 1: BASELINE EXPERIMENT")
            logger.info("="*60)
            
            baseline_results = self.run_baseline_experiment(model, tokenizer)
            all_results.update(baseline_results)
            
            # 2. Create and test CWE-specific steering vectors
            logger.info("\n" + "="*60)
            logger.info("🎯 PHASE 2: CWE-SPECIFIC STEERING")
            logger.info("="*60)
            
            # Focus on CWEs that showed lower performance in baseline
            priority_cwes = ["CWE-476", "CWE-77", "CWE-79"]  # Based on baseline analysis
            
            for cwe_id in priority_cwes:
                logger.info(f"\n🔧 Creating steering vectors for {cwe_id}")
                
                steering_vectors = self.create_cwe_specific_vectors(cwe_id)
                if steering_vectors:
                    # Test with this CWE's steering vectors
                    experiment_name = f"steering_{cwe_id.lower()}"
                    steering_results = self.run_steering_experiment(
                        model, tokenizer, steering_vectors, experiment_name
                    )
                    all_results.update(steering_results)
                    
                    # Memory cleanup
                    if torch.cuda.is_available():
                        torch.cuda.empty_cache()
                else:
                    logger.warning(f"⚠️ Could not create steering vectors for {cwe_id}")
            
            # 3. Analyze results
            logger.info("\n" + "="*60)
            logger.info("📊 PHASE 3: RESULTS ANALYSIS")
            logger.info("="*60)
            
            analysis = self.analyze_results(all_results)
            
            # 4. Save results
            self.save_results(all_results, analysis, "comprehensive_steering")
            
            # 5. Print summary
            logger.info("\n" + "="*60)
            logger.info("📈 EXPERIMENT SUMMARY")
            logger.info("="*60)
            
            baseline_acc = analysis.get("baseline", {}).get("overall_accuracy", 0)
            logger.info(f"Baseline Accuracy: {baseline_acc:.3f}")
            
            for exp_name, metrics in analysis.items():
                if exp_name != "baseline":
                    steering_acc = metrics.get("overall_accuracy", 0)
                    improvement = steering_acc - baseline_acc
                    logger.info(f"{exp_name} Accuracy: {steering_acc:.3f} ({improvement:+.3f})")
            
            total_time = time.time() - start_time
            logger.info(f"\n⏱️ Total experiment time: {total_time/60:.1f} minutes")
            
        except Exception as e:
            logger.error(f"❌ Experiment failed: {e}")
            raise

def main():
    parser = argparse.ArgumentParser(description="Comprehensive steering experiment for SecLLMHolmes")
    parser.add_argument("--model", type=str, default="Qwen/Qwen2.5-14B-Instruct", 
                       help="Model to use for experiments")
    parser.add_argument("--steering-strength", type=float, default=20.0,
                       help="Steering vector strength")
    parser.add_argument("--target-layers", nargs="+", type=int, default=[12, 24, 36, 47],
                       help="Target layers for steering")
    parser.add_argument("--dataset-path", type=str, default="../security/SecLLMHolmes/datasets",
                       help="Path to SecLLMHolmes dataset")
    parser.add_argument("--results-dir", type=str, default="results",
                       help="Directory to save results")
    parser.add_argument("--max-examples", type=int, default=10,
                       help="Maximum examples per CWE for efficiency")
    
    args = parser.parse_args()
    
    config = ExperimentConfig(
        model_name=args.model,
        steering_strength=args.steering_strength,
        target_layers=args.target_layers,
        dataset_path=args.dataset_path,
        results_dir=args.results_dir,
        max_examples_per_cwe=args.max_examples
    )
    
    experiment = ComprehensiveSteeringExperiment(config)
    experiment.run_comprehensive_experiment()

if __name__ == "__main__":
    main() 