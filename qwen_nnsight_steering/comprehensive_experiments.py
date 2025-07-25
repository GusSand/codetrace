#!/usr/bin/env python3
"""
Comprehensive Experiments with SecLLMHolmes Data
This runs REAL experiments to get actual performance results.

Goal: Demonstrate that vector-informed approaches outperform baseline prompting
on actual SecLLMHolmes vulnerability detection tasks.
"""

import os
import sys
import json
import logging
import time
import torch
import numpy as np
from typing import Dict, List, Tuple, Any, Optional
from pathlib import Path
from dataclasses import dataclass
import pandas as pd
from collections import defaultdict

# Add parent directory for imports
sys.path.append(str(Path(__file__).parent.parent))

from qwen_steering_integration import QwenNNSightSteering, QwenSteeringConfig
from vector_informed_evaluation import VectorInformedEvaluator

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ExperimentResult:
    """Results from a single experiment."""
    approach: str
    cwe_type: str
    test_case_id: str
    predicted_vulnerable: bool
    actual_vulnerable: bool
    confidence_score: float
    response_text: str
    processing_time: float
    
    @property
    def is_correct(self) -> bool:
        return self.predicted_vulnerable == self.actual_vulnerable

class SecLLMHolmesDataLoader:
    """Load and process SecLLMHolmes data for experiments."""
    
    def __init__(self, dataset_path: str = "../security/SecLLMHolmes/datasets"):
        self.dataset_path = Path(dataset_path)
        
    def load_cwe_examples(self, cwe_id: str, max_examples: int = 10) -> Dict[str, List[Dict]]:
        """Load vulnerable and secure examples for a CWE."""
        cwe_upper = cwe_id.upper() if cwe_id.startswith('cwe') else f"CWE-{cwe_id.split('-')[1]}"
        cwe_path = self.dataset_path / "hand-crafted" / "dataset" / cwe_upper
        
        if not cwe_path.exists():
            logger.error(f"❌ CWE path not found: {cwe_path}")
            return {"vulnerable": [], "secure": []}
        
        examples = {"vulnerable": [], "secure": []}
        
        # Load vulnerable examples (numbered files: 1.c, 2.c, etc.)
        vulnerable_files = sorted(cwe_path.glob("[0-9]*.c")) + sorted(cwe_path.glob("[0-9]*.py"))
        for i, file_path in enumerate(vulnerable_files[:max_examples]):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    examples["vulnerable"].append({
                        "id": f"{cwe_id}_vuln_{i+1}",
                        "code": f.read().strip(),
                        "file": file_path.name,
                        "vulnerable": True
                    })
            except Exception as e:
                logger.warning(f"⚠️ Error reading {file_path}: {e}")
        
        # Load secure examples (p_*.c, p_*.py files)
        secure_files = sorted(cwe_path.glob("p_[0-9]*.c")) + sorted(cwe_path.glob("p_[0-9]*.py"))
        for i, file_path in enumerate(secure_files[:max_examples]):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    examples["secure"].append({
                        "id": f"{cwe_id}_secure_{i+1}",
                        "code": f.read().strip(),
                        "file": file_path.name,
                        "vulnerable": False
                    })
            except Exception as e:
                logger.warning(f"⚠️ Error reading {file_path}: {e}")
        
        logger.info(f"📊 Loaded {cwe_id}: {len(examples['vulnerable'])} vulnerable, {len(examples['secure'])} secure")
        return examples

class ExperimentRunner:
    """Runs comprehensive experiments comparing different approaches."""
    
    def __init__(self, model_name: str = "Qwen/Qwen2.5-1.5B-Instruct"):
        self.model_name = model_name
        self.data_loader = SecLLMHolmesDataLoader()
        self.vector_evaluator = VectorInformedEvaluator()
        self.model_steerer = None
        
        # Available CWEs to test
        self.test_cwes = ["cwe-77", "cwe-22", "cwe-89"]
        
    def initialize_model(self) -> bool:
        """Initialize the model for experiments."""
        logger.info(f"🚀 Initializing model: {self.model_name}")
        
        try:
            config = QwenSteeringConfig(
                model_name=self.model_name,
                target_layers=[4, 8, 12, 23] if "1.5B" in self.model_name else [12, 24, 36, 47],
                device_map="cuda:0" if torch.cuda.is_available() else "cpu"
            )
            
            self.model_steerer = QwenNNSightSteering(config)
            self.model_steerer.load_model()
            
            logger.info("✅ Model initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Model initialization failed: {e}")
            return False
    
    def load_steering_vectors(self) -> bool:
        """Load steering vectors for experiments."""
        logger.info("📚 Loading steering vectors...")
        
        vector_files = [f"vectors/{cwe}_steering_vectors.pt" for cwe in self.test_cwes]
        
        if not self.vector_evaluator.load_steering_vectors(vector_files):
            logger.error("❌ Failed to load steering vectors")
            return False
            
        # Analyze vector patterns
        self.vector_evaluator.analyze_vector_patterns()
        return True
    
    def run_baseline_approach(self, code: str, cwe_type: str) -> ExperimentResult:
        """Run baseline approach (simple prompting)."""
        prompt = f"""Analyze this code for security vulnerabilities:

{code}

Is this code vulnerable to security attacks? Answer 'Yes' or 'No' and provide your reasoning:"""
        
        start_time = time.time()
        
        try:
            # Generate response
            inputs = self.model_steerer.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
            
            if torch.cuda.is_available():
                inputs = {k: v.cuda() for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model_steerer.model.generate(
                    inputs['input_ids'],
                    max_new_tokens=100,
                    temperature=0.1,
                    do_sample=True,
                    top_p=0.9,
                    pad_token_id=self.model_steerer.tokenizer.eos_token_id
                )
            
            # Decode response
            input_length = inputs['input_ids'].shape[1]
            response = self.model_steerer.tokenizer.decode(outputs[0][input_length:], skip_special_tokens=True)
            
            # Parse prediction
            predicted_vulnerable = self._parse_vulnerability_prediction(response)
            confidence = 0.5  # Baseline has no confidence measure
            
            processing_time = time.time() - start_time
            
            return ExperimentResult(
                approach="baseline",
                cwe_type=cwe_type,
                test_case_id="unknown",
                predicted_vulnerable=predicted_vulnerable,
                actual_vulnerable=True,  # Will be set by caller
                confidence_score=confidence,
                response_text=response[:200],
                processing_time=processing_time
            )
            
        except Exception as e:
            logger.error(f"❌ Baseline approach failed: {e}")
            return ExperimentResult(
                approach="baseline",
                cwe_type=cwe_type,
                test_case_id="unknown",
                predicted_vulnerable=False,
                actual_vulnerable=True,
                confidence_score=0.0,
                response_text=f"ERROR: {str(e)}",
                processing_time=time.time() - start_time
            )
    
    def run_enhanced_prompting(self, code: str, cwe_type: str) -> ExperimentResult:
        """Run enhanced prompting approach (what the 'breakthrough' actually did)."""
        cwe_focus = {
            "cwe-22": "Focus on path traversal, directory access, and file system vulnerabilities.",
            "cwe-77": "Focus on command injection, shell execution, and system call vulnerabilities.", 
            "cwe-89": "Focus on SQL injection, database query safety, and parameterized statements.",
        }
        
        focus = cwe_focus.get(cwe_type, "Focus on security vulnerabilities and safe coding practices.")
        
        prompt = f"""You are a security expert specializing in vulnerability detection.

{focus}

Analyze this code with heightened security awareness:

{code}

Is this code vulnerable? Answer 'Yes' or 'No' and provide detailed analysis:"""
        
        start_time = time.time()
        
        try:
            # Generate response (same as baseline but with enhanced prompt)
            inputs = self.model_steerer.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
            
            if torch.cuda.is_available():
                inputs = {k: v.cuda() for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model_steerer.model.generate(
                    inputs['input_ids'],
                    max_new_tokens=100,
                    temperature=0.1,
                    do_sample=True,
                    top_p=0.9,
                    pad_token_id=self.model_steerer.tokenizer.eos_token_id
                )
            
            # Decode response
            input_length = inputs['input_ids'].shape[1]
            response = self.model_steerer.tokenizer.decode(outputs[0][input_length:], skip_special_tokens=True)
            
            # Parse prediction
            predicted_vulnerable = self._parse_vulnerability_prediction(response)
            confidence = 0.6  # Slightly higher than baseline
            
            processing_time = time.time() - start_time
            
            return ExperimentResult(
                approach="enhanced_prompting",
                cwe_type=cwe_type,
                test_case_id="unknown",
                predicted_vulnerable=predicted_vulnerable,
                actual_vulnerable=True,
                confidence_score=confidence,
                response_text=response[:200],
                processing_time=processing_time
            )
            
        except Exception as e:
            logger.error(f"❌ Enhanced prompting failed: {e}")
            return ExperimentResult(
                approach="enhanced_prompting",
                cwe_type=cwe_type,
                test_case_id="unknown",
                predicted_vulnerable=False,
                actual_vulnerable=True,
                confidence_score=0.0,
                response_text=f"ERROR: {str(e)}",
                processing_time=time.time() - start_time
            )
    
    def run_vector_informed_approach(self, code: str, cwe_type: str) -> ExperimentResult:
        """Run our vector-informed approach."""
        start_time = time.time()
        
        try:
            # Get vector-informed assessment
            assessment = self.vector_evaluator.vector_informed_assessment(code, cwe_type)
            
            if "error" in assessment:
                raise ValueError(assessment["error"])
            
            # Extract prediction based on deterministic score
            deterministic_score = assessment["deterministic_score"]
            predicted_vulnerable = deterministic_score > 0.5
            confidence = assessment["vector_insights"]["confidence_score"]
            
            processing_time = time.time() - start_time
            
            return ExperimentResult(
                approach="vector_informed",
                cwe_type=cwe_type,
                test_case_id="unknown",
                predicted_vulnerable=predicted_vulnerable,
                actual_vulnerable=True,
                confidence_score=confidence,
                response_text=assessment["recommendation"],
                processing_time=processing_time
            )
            
        except Exception as e:
            logger.error(f"❌ Vector-informed approach failed: {e}")
            return ExperimentResult(
                approach="vector_informed",
                cwe_type=cwe_type,
                test_case_id="unknown",
                predicted_vulnerable=False,
                actual_vulnerable=True,
                confidence_score=0.0,
                response_text=f"ERROR: {str(e)}",
                processing_time=time.time() - start_time
            )
    
    def _parse_vulnerability_prediction(self, response: str) -> bool:
        """Parse whether the model predicted the code is vulnerable."""
        response_lower = response.lower()
        
        # Look for clear indicators
        if "yes" in response_lower and "vulnerable" in response_lower:
            return True
        if "no" in response_lower and ("not vulnerable" in response_lower or "safe" in response_lower):
            return False
        
        # Default heuristics
        if any(word in response_lower for word in ["vulnerable", "attack", "exploit", "danger", "risk"]):
            return True
        if any(word in response_lower for word in ["safe", "secure", "protected", "no vulnerability"]):
            return False
            
        # If unclear, default to vulnerable (conservative)
        return True
    
    def run_comprehensive_experiment(self, max_examples_per_cwe: int = 5) -> Dict[str, Any]:
        """Run comprehensive experiments across all approaches and CWEs."""
        logger.info("🧪 Starting comprehensive experiments...")
        
        results = []
        approaches = ["baseline", "enhanced_prompting", "vector_informed"]
        
        for cwe_type in self.test_cwes:
            logger.info(f"\n🎯 Testing {cwe_type.upper()}")
            
            # Load examples for this CWE
            examples = self.data_loader.load_cwe_examples(cwe_type, max_examples_per_cwe)
            
            # Test both vulnerable and secure examples
            for vulnerability_type, example_list in examples.items():
                is_vulnerable = (vulnerability_type == "vulnerable")
                
                for example in example_list:
                    code = example["code"]
                    test_id = example["id"]
                    
                    logger.info(f"  📝 Testing {test_id}")
                    
                    # Run all approaches on this example
                    for approach in approaches:
                        if approach == "baseline":
                            result = self.run_baseline_approach(code, cwe_type)
                        elif approach == "enhanced_prompting":
                            result = self.run_enhanced_prompting(code, cwe_type)
                        elif approach == "vector_informed":
                            result = self.run_vector_informed_approach(code, cwe_type)
                        
                        # Set correct values
                        result.test_case_id = test_id
                        result.actual_vulnerable = is_vulnerable
                        
                        results.append(result)
                        
                        # Log result
                        correct = "✅" if result.is_correct else "❌"
                        logger.info(f"    {approach}: {correct} (pred={result.predicted_vulnerable}, "
                                  f"actual={is_vulnerable}, conf={result.confidence_score:.3f})")
        
        # Analyze results
        analysis = self._analyze_results(results)
        
        return {
            "model_name": self.model_name,
            "total_examples": len(results) // len(approaches),
            "approaches_tested": approaches,
            "cwes_tested": self.test_cwes,
            "raw_results": [vars(r) for r in results],
            "analysis": analysis,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def _analyze_results(self, results: List[ExperimentResult]) -> Dict[str, Any]:
        """Analyze experimental results."""
        logger.info("📊 Analyzing results...")
        
        # Group by approach
        by_approach = defaultdict(list)
        for result in results:
            by_approach[result.approach].append(result)
        
        analysis = {}
        
        for approach, approach_results in by_approach.items():
            correct = sum(1 for r in approach_results if r.is_correct)
            total = len(approach_results)
            accuracy = correct / total if total > 0 else 0.0
            
            # Calculate per-CWE performance
            cwe_performance = {}
            for cwe in self.test_cwes:
                cwe_results = [r for r in approach_results if r.cwe_type == cwe]
                if cwe_results:
                    cwe_correct = sum(1 for r in cwe_results if r.is_correct)
                    cwe_accuracy = cwe_correct / len(cwe_results)
                    cwe_performance[cwe] = {
                        "accuracy": cwe_accuracy,
                        "correct": cwe_correct,
                        "total": len(cwe_results)
                    }
            
            # Calculate average confidence
            confidences = [r.confidence_score for r in approach_results]
            avg_confidence = np.mean(confidences) if confidences else 0.0
            
            # Calculate average processing time
            times = [r.processing_time for r in approach_results]
            avg_time = np.mean(times) if times else 0.0
            
            analysis[approach] = {
                "overall_accuracy": accuracy,
                "correct_predictions": correct,
                "total_predictions": total,
                "cwe_performance": cwe_performance,
                "average_confidence": avg_confidence,
                "average_processing_time": avg_time
            }
        
        return analysis

def main():
    """Run the comprehensive experiments."""
    logger.info("🚀 Starting Comprehensive SecLLMHolmes Experiments")
    
    # Initialize experiment runner
    runner = ExperimentRunner("Qwen/Qwen2.5-1.5B-Instruct")
    
    # Initialize model
    if not runner.initialize_model():
        logger.error("❌ Failed to initialize model")
        return
    
    # Load steering vectors
    if not runner.load_steering_vectors():
        logger.error("❌ Failed to load steering vectors")
        return
    
    # Run experiments
    results = runner.run_comprehensive_experiment(max_examples_per_cwe=3)
    
    # Save results
    output_file = f"experiment_results_{runner.model_name.replace('/', '_')}_{int(time.time())}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    # Display summary
    print("\n" + "="*80)
    print("🎯 COMPREHENSIVE EXPERIMENT RESULTS")
    print("="*80)
    
    print(f"\n📊 Model: {results['model_name']}")
    print(f"📊 Total Examples: {results['total_examples']}")
    print(f"📊 CWEs Tested: {', '.join(results['cwes_tested'])}")
    
    print(f"\n🏆 PERFORMANCE COMPARISON:")
    analysis = results['analysis']
    
    for approach in results['approaches_tested']:
        if approach in analysis:
            stats = analysis[approach]
            print(f"\n  {approach.upper()}:")
            print(f"    Overall Accuracy: {stats['overall_accuracy']:.1%}")
            print(f"    Avg Confidence: {stats['average_confidence']:.3f}")
            print(f"    Avg Time: {stats['average_processing_time']:.2f}s")
            
            print(f"    Per-CWE Performance:")
            for cwe, perf in stats['cwe_performance'].items():
                print(f"      {cwe}: {perf['accuracy']:.1%} ({perf['correct']}/{perf['total']})")
    
    print(f"\n💾 Full results saved to: {output_file}")
    print("\n✅ Comprehensive experiments complete!")

if __name__ == "__main__":
    main() 