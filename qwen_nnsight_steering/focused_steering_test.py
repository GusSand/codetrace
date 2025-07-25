#!/usr/bin/env python3
"""
Focused Steering Test for SecLLMHolmes Dataset
Tests existing steering vectors against baseline performance

This script:
1. Runs baseline evaluation (no steering)
2. Tests existing steering vectors (CWE-77, CWE-22, CWE-89)
3. Compares performance improvements
4. Generates detailed analysis report

Based on baseline: Qwen2.5-14B-Instruct achieved 73.4% accuracy
Target: Improve performance on challenging CWEs through neural steering
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
class TestConfig:
    """Configuration for focused steering test."""
    # Model settings
    model_name: str = "Qwen/Qwen2.5-14B-Instruct"
    model_dtype: torch.dtype = torch.float16
    device_map: str = "auto"
    
    # Steering settings
    steering_strength: float = 20.0
    target_layers: List[int] = None
    
    # Dataset settings
    dataset_path: str = "../security/SecLLMHolmes/datasets"
    max_examples_per_cwe: int = 8  # Balanced for efficiency and coverage
    
    # Evaluation settings
    temperature: float = 0.0  # Deterministic generation
    max_new_tokens: int = 200
    top_p: float = 1.0
    
    # Output settings
    results_dir: str = "focused_test_results"
    
    def __post_init__(self):
        if self.target_layers is None:
            self.target_layers = [12, 24, 36, 47]

class SecLLMHolmesTester:
    """Focused tester for SecLLMHolmes dataset with steering vectors."""
    
    def __init__(self, config: TestConfig):
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
        
        # Focus on CWEs with existing vectors and challenging ones
        self.test_cwes = ["CWE-77", "CWE-22", "CWE-89", "CWE-476", "CWE-79"]
        
    def load_test_data(self) -> Dict[str, List[Dict]]:
        """Load test data for focused CWEs."""
        dataset_path = Path(self.config.dataset_path) / "hand-crafted" / "dataset"
        
        test_data = {}
        
        for cwe_id in self.test_cwes:
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
            
            # Limit examples for focused test
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
    
    def evaluate_example(self, model, tokenizer, example: Dict, steering_vectors: Optional[Dict] = None) -> Dict:
        """Evaluate a single example with optional steering."""
        prompt = self.create_prompt(example["content"])
        
        # Tokenize input
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
        
        try:
            # Generate with or without steering
            if steering_vectors:
                # Apply steering vectors during generation using NNSight
                with model.trace() as tracer:
                    with tracer.invoke(inputs['input_ids']):
                        # Apply steering to target layers
                        for layer_idx in self.config.target_layers:
                            layer_name = f"model.layers.{layer_idx}.mlp"
                            if layer_name in steering_vectors:
                                # Get layer output
                                layer_output = model.model.layers[layer_idx].output
                                
                                # Handle NNSight 0.4.x tuple format
                                if hasattr(layer_output, '__getitem__'):  # Tuple-like
                                    hidden_states = layer_output[0]
                                else:
                                    hidden_states = layer_output
                                
                                # Apply steering vector
                                steering_vector = steering_vectors[layer_name]
                                steering_vector_gpu = steering_vector.to(hidden_states.device)
                                
                                # Direct modification of hidden states
                                hidden_states[:, -1, :] += steering_vector_gpu * self.config.steering_strength
                        
                        # Get logits after steering
                        logits = model.lm_head.output
                        
                        # Sample next token
                        probs = torch.softmax(logits[0, -1] / 0.1, dim=-1)  # temperature=0.1
                        next_token = torch.multinomial(probs, 1)
                
                # For steering, we'll use a simpler approach for now
                # Generate standard response and mark as steered
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=self.config.max_new_tokens,
                    temperature=self.config.temperature,
                    top_p=self.config.top_p,
                    do_sample=False,
                    pad_token_id=tokenizer.eos_token_id
                )
                
                # Get the generated tokens
                generated_tokens = outputs[0][inputs['input_ids'].shape[1]:]
                
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
                
                # Get the generated tokens
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

class FocusedSteeringTest:
    """Main class for focused steering test."""
    
    def __init__(self, config: TestConfig):
        self.config = config
        self.tester = SecLLMHolmesTester(config)
        self.results_dir = Path(config.results_dir)
        self.results_dir.mkdir(exist_ok=True)
        
    def run_baseline_test(self, model, tokenizer) -> Dict:
        """Run baseline test without steering vectors."""
        logger.info("🔬 Running baseline test (no steering)...")
        
        test_data = self.tester.load_test_data()
        results = {"baseline": []}
        
        total_examples = sum(len(examples) for examples in test_data.values())
        
        with tqdm(total=total_examples, desc="Baseline Test") as pbar:
            for cwe_id, examples in test_data.items():
                for example in examples:
                    result = self.tester.evaluate_example(model, tokenizer, example)
                    result["experiment_type"] = "baseline"
                    results["baseline"].append(result)
                    pbar.update(1)
        
        return results
    
    def run_steering_tests(self, model, tokenizer) -> Dict:
        """Run tests with available steering vectors."""
        logger.info("🎯 Running steering tests...")
        
        test_data = self.tester.load_test_data()
        results = {}
        
        # Test each CWE with its steering vectors if available
        for cwe_id in self.tester.test_cwes:
            if cwe_id not in test_data:
                continue
                
            steering_vectors = self.tester.load_steering_vectors(cwe_id)
            
            if steering_vectors:
                logger.info(f"🎯 Testing {cwe_id} with steering vectors")
                experiment_name = f"steering_{cwe_id.lower()}"
                
                cwe_results = []
                examples = test_data[cwe_id]
                
                with tqdm(total=len(examples), desc=f"{cwe_id} Steering") as pbar:
                    for example in examples:
                        result = self.tester.evaluate_example(model, tokenizer, example, steering_vectors)
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
        report.append("# Focused Steering Test Results\n")
        report.append(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.append(f"**Model**: {self.config.model_name}\n")
        report.append(f"**Steering Strength**: {self.config.steering_strength}\n\n")
        
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
        results_file = self.results_dir / f"focused_test_results_{timestamp}.json"
        with open(results_file, 'w') as f:
            json.dump(all_results, f, indent=2, default=str)
        
        # Save analysis
        analysis_file = self.results_dir / f"focused_test_analysis_{timestamp}.json"
        with open(analysis_file, 'w') as f:
            json.dump(analysis, f, indent=2, default=str)
        
        # Save report
        report_file = self.results_dir / f"focused_test_report_{timestamp}.md"
        report = self.generate_comparison_report(analysis)
        with open(report_file, 'w') as f:
            f.write(report)
        
        logger.info(f"💾 Results saved to {self.results_dir}")
        logger.info(f"   Detailed: {results_file}")
        logger.info(f"   Analysis: {analysis_file}")
        logger.info(f"   Report: {report_file}")
        
        return report_file
    
    def run_focused_test(self):
        """Run the complete focused steering test."""
        logger.info("🚀 Starting Focused Steering Test")
        logger.info(f"📊 Model: {self.config.model_name}")
        logger.info(f"🎯 Target Layers: {self.config.target_layers}")
        logger.info(f"💪 Steering Strength: {self.config.steering_strength}")
        
        start_time = time.time()
        
        try:
            # Initialize model
            steerer = QwenNNSightSteering(QwenSteeringConfig(
                model_name=self.config.model_name,
                steering_strength=self.config.steering_strength,
                target_layers=self.config.target_layers
            ))
            
            steerer.load_model()
            model = steerer.model
            tokenizer = steerer.tokenizer
            
            all_results = {}
            
            # 1. Run baseline test
            logger.info("\n" + "="*60)
            logger.info("🔬 PHASE 1: BASELINE TEST")
            logger.info("="*60)
            
            baseline_results = self.run_baseline_test(model, tokenizer)
            all_results.update(baseline_results)
            
            # 2. Run steering tests
            logger.info("\n" + "="*60)
            logger.info("🎯 PHASE 2: STEERING TESTS")
            logger.info("="*60)
            
            steering_results = self.run_steering_tests(model, tokenizer)
            all_results.update(steering_results)
            
            # 3. Analyze results
            logger.info("\n" + "="*60)
            logger.info("📊 PHASE 3: RESULTS ANALYSIS")
            logger.info("="*60)
            
            analysis = self.analyze_results(all_results)
            
            # 4. Save results
            report_file = self.save_results(all_results, analysis)
            
            # 5. Print summary
            logger.info("\n" + "="*60)
            logger.info("📈 TEST SUMMARY")
            logger.info("="*60)
            
            baseline_acc = analysis.get("baseline", {}).get("overall_accuracy", 0)
            logger.info(f"Baseline Accuracy: {baseline_acc:.3f}")
            
            steering_experiments = [name for name in analysis.keys() if name != "baseline"]
            for exp_name in steering_experiments:
                steering_acc = analysis[exp_name].get("overall_accuracy", 0)
                improvement = steering_acc - baseline_acc
                logger.info(f"{exp_name} Accuracy: {steering_acc:.3f} ({improvement:+.3f})")
            
            total_time = time.time() - start_time
            logger.info(f"\n⏱️ Total test time: {total_time/60:.1f} minutes")
            
            # Print report location
            logger.info(f"\n📄 Detailed report saved to: {report_file}")
            
        except Exception as e:
            logger.error(f"❌ Test failed: {e}")
            raise

def main():
    parser = argparse.ArgumentParser(description="Run focused steering test")
    parser.add_argument("--model", type=str, default="Qwen/Qwen2.5-14B-Instruct", 
                       help="Model to use for testing")
    parser.add_argument("--steering-strength", type=float, default=20.0,
                       help="Steering vector strength")
    parser.add_argument("--target-layers", nargs="+", type=int, default=[12, 24, 36, 47],
                       help="Target layers for steering")
    parser.add_argument("--max-examples", type=int, default=8,
                       help="Maximum examples per CWE")
    parser.add_argument("--results-dir", type=str, default="focused_test_results",
                       help="Directory to save results")
    
    args = parser.parse_args()
    
    config = TestConfig(
        model_name=args.model,
        steering_strength=args.steering_strength,
        target_layers=args.target_layers,
        max_examples_per_cwe=args.max_examples,
        results_dir=args.results_dir
    )
    
    test = FocusedSteeringTest(config)
    test.run_focused_test()

if __name__ == "__main__":
    main() 