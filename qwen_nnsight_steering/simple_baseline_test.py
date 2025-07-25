#!/usr/bin/env python3
"""
Simple Baseline Test for SecLLMHolmes Dataset
Evaluates Qwen2.5-14B-Instruct performance without steering vectors

This establishes the baseline performance that steering vectors should improve upon.
Based on previous baseline: Qwen2.5-14B-Instruct achieved 73.4% accuracy
"""

import os
import sys
import json
import torch
import logging
import time
import argparse
from pathlib import Path
from typing import List, Dict, Tuple
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
class BaselineConfig:
    """Configuration for baseline test."""
    # Model settings
    model_name: str = "Qwen/Qwen2.5-14B-Instruct"
    model_dtype: torch.dtype = torch.float16
    device_map: str = "auto"
    
    # Dataset settings
    dataset_path: str = "../security/SecLLMHolmes/datasets"
    max_examples_per_cwe: int = 8
    
    # Evaluation settings
    temperature: float = 0.0  # Deterministic generation
    max_new_tokens: int = 200
    top_p: float = 1.0
    
    # Output settings
    results_dir: str = "baseline_results"

class SecLLMHolmesBaselineTester:
    """Baseline tester for SecLLMHolmes dataset."""
    
    def __init__(self, config: BaselineConfig):
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
    
    def evaluate_example(self, model, tokenizer, example: Dict) -> Dict:
        """Evaluate a single example."""
        prompt = self.create_prompt(example["content"])
        
        # Tokenize input
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
        
        try:
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

class BaselineTest:
    """Main class for baseline test."""
    
    def __init__(self, config: BaselineConfig):
        self.config = config
        self.tester = SecLLMHolmesBaselineTester(config)
        self.results_dir = Path(config.results_dir)
        self.results_dir.mkdir(exist_ok=True)
        
    def execute_baseline_test(self, model, tokenizer) -> Dict:
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
    
    def analyze_results(self, results: Dict) -> Dict:
        """Analyze baseline results."""
        analysis = {}
        
        for experiment_name, experiment_results in results.items():
            if not experiment_results:
                continue
                
            # Calculate overall metrics
            total_examples = len(experiment_results)
            correct_predictions = sum(1 for r in experiment_results if r["is_correct"])
            accuracy = correct_predictions / total_examples if total_examples > 0 else 0
            
            # Calculate per-CWE metrics
            cwe_metrics = {}
            for result in experiment_results:
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
                "avg_reasoning_quality": np.mean([r["reasoning_quality"] for r in experiment_results])
            }
        
        return analysis
    
    def generate_report(self, analysis: Dict) -> str:
        """Generate a detailed baseline report."""
        report = []
        report.append("# SecLLMHolmes Baseline Test Results\n")
        report.append(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.append(f"**Model**: {self.config.model_name}\n")
        report.append(f"**Temperature**: {self.config.temperature}\n\n")
        
        # Overall performance
        baseline_metrics = analysis.get("baseline", {})
        baseline_acc = baseline_metrics.get("overall_accuracy", 0)
        total_examples = baseline_metrics.get("total_examples", 0)
        reasoning_quality = baseline_metrics.get("avg_reasoning_quality", 0)
        
        report.append("## Overall Performance\n")
        report.append(f"- **Accuracy**: {baseline_acc:.3f} ({baseline_acc*100:.1f}%)\n")
        report.append(f"- **Total Examples**: {total_examples}\n")
        report.append(f"- **Reasoning Quality**: {reasoning_quality:.3f}\n\n")
        
        # Per-CWE performance
        report.append("## Per-CWE Performance\n")
        report.append("| CWE | Description | Accuracy | Examples | Reasoning Quality |\n")
        report.append("|-----|-------------|----------|----------|-------------------|\n")
        
        cwe_metrics = baseline_metrics.get("cwe_metrics", {})
        for cwe in sorted(cwe_metrics.keys()):
            metrics = cwe_metrics[cwe]
            cwe_name = self.tester.cwe_names.get(cwe, "Unknown")
            acc = metrics["accuracy"]
            examples = metrics["total"]
            reasoning = metrics["avg_reasoning"]
            
            report.append(f"| {cwe} | {cwe_name} | {acc:.3f} | {examples} | {reasoning:.3f} |\n")
        
        # Performance analysis
        report.append("\n## Performance Analysis\n")
        
        # Best and worst performing CWEs
        if cwe_metrics:
            best_cwe = max(cwe_metrics.items(), key=lambda x: x[1]["accuracy"])
            worst_cwe = min(cwe_metrics.items(), key=lambda x: x[1]["accuracy"])
            
            report.append(f"- **Best Performing CWE**: {best_cwe[0]} ({best_cwe[1]['accuracy']:.3f})\n")
            report.append(f"- **Most Challenging CWE**: {worst_cwe[0]} ({worst_cwe[1]['accuracy']:.3f})\n")
        
        # Comparison with previous baseline
        report.append(f"- **Previous Baseline (Qwen2.5-14B-Instruct)**: 73.4%\n")
        report.append(f"- **Current Baseline**: {baseline_acc*100:.1f}%\n")
        
        if baseline_acc > 0.734:
            report.append(f"- **Improvement**: +{(baseline_acc-0.734)*100:.1f}%\n")
        else:
            report.append(f"- **Difference**: {(baseline_acc-0.734)*100:.1f}%\n")
        
        return "\n".join(report)
    
    def save_results(self, results: Dict, analysis: Dict):
        """Save test results and analysis."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save detailed results
        results_file = self.results_dir / f"baseline_results_{timestamp}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        # Save analysis
        analysis_file = self.results_dir / f"baseline_analysis_{timestamp}.json"
        with open(analysis_file, 'w') as f:
            json.dump(analysis, f, indent=2, default=str)
        
        # Save report
        report_file = self.results_dir / f"baseline_report_{timestamp}.md"
        report = self.generate_report(analysis)
        with open(report_file, 'w') as f:
            f.write(report)
        
        logger.info(f"💾 Results saved to {self.results_dir}")
        logger.info(f"   Detailed: {results_file}")
        logger.info(f"   Analysis: {analysis_file}")
        logger.info(f"   Report: {report_file}")
        
        return report_file
    
    def run_baseline_test(self):
        """Run the complete baseline test."""
        logger.info("🚀 Starting Baseline Test")
        logger.info(f"📊 Model: {self.config.model_name}")
        
        start_time = time.time()
        
        try:
            # Initialize model - use underlying model for baseline testing
            steerer = QwenNNSightSteering(QwenSteeringConfig(
                model_name=self.config.model_name
            ))
            
            steerer.load_model()
            # Use the underlying model directly for baseline testing
            model = steerer.model.model  # Get the actual Qwen model
            tokenizer = steerer.tokenizer
            
            # Run baseline test
            logger.info("\n" + "="*60)
            logger.info("🔬 BASELINE TEST")
            logger.info("="*60)
            
            results = self.execute_baseline_test(model, tokenizer)
            
            # Analyze results
            logger.info("\n" + "="*60)
            logger.info("📊 RESULTS ANALYSIS")
            logger.info("="*60)
            
            analysis = self.analyze_results(results)
            
            # Save results
            report_file = self.save_results(results, analysis)
            
            # Print summary
            logger.info("\n" + "="*60)
            logger.info("📈 BASELINE SUMMARY")
            logger.info("="*60)
            
            baseline_acc = analysis.get("baseline", {}).get("overall_accuracy", 0)
            total_examples = analysis.get("baseline", {}).get("total_examples", 0)
            reasoning_quality = analysis.get("baseline", {}).get("avg_reasoning_quality", 0)
            
            logger.info(f"Overall Accuracy: {baseline_acc:.3f} ({baseline_acc*100:.1f}%)")
            logger.info(f"Total Examples: {total_examples}")
            logger.info(f"Reasoning Quality: {reasoning_quality:.3f}")
            
            # Compare with previous baseline
            previous_baseline = 0.734
            if baseline_acc > previous_baseline:
                logger.info(f"Improvement over previous baseline: +{(baseline_acc-previous_baseline)*100:.1f}%")
            else:
                logger.info(f"Difference from previous baseline: {(baseline_acc-previous_baseline)*100:.1f}%")
            
            total_time = time.time() - start_time
            logger.info(f"\n⏱️ Total test time: {total_time/60:.1f} minutes")
            
            # Print report location
            logger.info(f"\n📄 Detailed report saved to: {report_file}")
            
        except Exception as e:
            logger.error(f"❌ Test failed: {e}")
            raise

def main():
    parser = argparse.ArgumentParser(description="Run baseline test for SecLLMHolmes")
    parser.add_argument("--model", type=str, default="Qwen/Qwen2.5-14B-Instruct", 
                       help="Model to use for testing")
    parser.add_argument("--max-examples", type=int, default=8,
                       help="Maximum examples per CWE")
    parser.add_argument("--results-dir", type=str, default="baseline_results",
                       help="Directory to save results")
    
    args = parser.parse_args()
    
    config = BaselineConfig(
        model_name=args.model,
        max_examples_per_cwe=args.max_examples,
        results_dir=args.results_dir
    )
    
    test = BaselineTest(config)
    test.run_baseline_test()

if __name__ == "__main__":
    main() 