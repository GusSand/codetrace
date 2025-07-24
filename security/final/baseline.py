#!/usr/bin/env python3
"""
Baseline experiment for SecLLMHolmes dataset using StarCoder1B with transformers library.
This creates a no-steering baseline for comparison with neural steering experiments.
"""

import os
import sys
import json
import time
import torch
import re
import logging
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path
from dataclasses import dataclass
from collections import defaultdict
import numpy as np

from transformers import AutoTokenizer, AutoModelForCausalLM
from tqdm import tqdm

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class BaselineConfig:
    """Configuration for baseline experiment."""
    model_name: str = "bigcode/starcoderbase-1b"
    temperature: float = 0.0  # Paper recommends 0.0
    top_p: float = 1.0       # Keep default
    max_new_tokens: int = 200
    num_trials: int = 1      # For consistency checking
    batch_size: int = 1      # Process one at a time for memory efficiency
    
    # Dataset paths
    secllmholmes_base: str = "../SecLLMHolmes/datasets"
    output_dir: str = "security/final/baseline_results"
    
    # CWE mappings from SecLLMHolmes
    cwe_list: List[str] = None
    
    def __post_init__(self):
        if self.cwe_list is None:
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

class SecLLMHolmesBaselineAdapter:
    """Adapter to run SecLLMHolmes evaluation with transformers library."""
    
    def __init__(self, config: BaselineConfig):
        self.config = config
        self.model = None
        self.tokenizer = None
        self.results = defaultdict(dict)
        
        # CWE name mappings
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
        
        # Ensure output directory exists
        os.makedirs(config.output_dir, exist_ok=True)
        
    def load_model(self):
        """Load StarCoder1B model and tokenizer."""
        logger.info(f"Loading model: {self.config.model_name}")
        
        try:
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_name)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load model with optimizations for memory efficiency
            self.model = AutoModelForCausalLM.from_pretrained(
                self.config.model_name,
                torch_dtype=torch.float16,
                device_map="auto",
                trust_remote_code=True
            )
            
            logger.info("✅ Model loaded successfully")
            
            # Print model info
            num_params = sum(p.numel() for p in self.model.parameters())
            logger.info(f"Parameters: {num_params:,}")
            logger.info(f"Memory estimate: {num_params * 2 / (1024**3):.2f} GB (fp16)")
            
        except Exception as e:
            logger.error(f"❌ Failed to load model: {e}")
            raise
    
    def load_secllmholmes_data(self) -> Dict[str, List[Dict]]:
        """Load SecLLMHolmes dataset for each CWE."""
        logger.info("Loading SecLLMHolmes dataset...")
        
        dataset = defaultdict(list)
        
        for cwe in self.config.cwe_list:
            # Convert cwe-89 to CWE-89 format
            cwe_upper = cwe.replace("cwe-", "CWE-")
            
            # Try different dataset types: hand-crafted, augmented, real-world
            for dataset_type in ["hand-crafted", "augmented", "real-world"]:
                dataset_path = Path(self.config.secllmholmes_base) / dataset_type / "dataset" / cwe_upper
                
                if not dataset_path.exists():
                    continue
                    
                logger.info(f"Loading {dataset_type} examples for {cwe_upper}")
                
                # Load all files in the CWE directory
                for file_path in dataset_path.glob("*"):
                    if file_path.suffix in [".c", ".py"]:
                        try:
                            # Determine if this is vulnerable (not p_*) or patched (p_*)
                            is_vulnerable = not file_path.name.startswith("p_")
                            
                            # Read code
                            code = file_path.read_text(encoding='utf-8')
                            
                            # Load corresponding ground truth if available
                            gt_path = Path(self.config.secllmholmes_base) / dataset_type / "ground-truth" / cwe_upper / f"{file_path.stem}.txt"
                            ground_truth = ""
                            if gt_path.exists():
                                ground_truth = gt_path.read_text(encoding='utf-8')
                            
                            example = {
                                "cwe": cwe,
                                "cwe_name": self.cwe_names[cwe],
                                "code": code,
                                "file_name": file_path.name,
                                "is_vulnerable": is_vulnerable,
                                "ground_truth": ground_truth,
                                "dataset_type": dataset_type,
                                "language": file_path.suffix[1:]  # Remove the dot
                            }
                            
                            dataset[cwe].append(example)
                            
                        except Exception as e:
                            logger.warning(f"Failed to load {file_path}: {e}")
        
        # Log dataset statistics
        total_examples = sum(len(examples) for examples in dataset.values())
        logger.info(f"Loaded {total_examples} examples across {len(dataset)} CWEs")
        
        for cwe, examples in dataset.items():
            logger.info(f"  {cwe}: {len(examples)} examples")
        
        return dict(dataset)
    
    def prepare_prompt(self, example: Dict[str, Any], prompt_type: str = "Question") -> str:
        """Prepare prompt following SecLLMHolmes format."""
        code = example["code"]
        cwe_name = example["cwe_name"]
        
        if prompt_type == "Question":
            question = f"Does this code contain instances of the security vulnerability known as {cwe_name}?"
            prompt = f"Code: \"\"\"\n{code}\n\"\"\"\n{question}"
        elif prompt_type == "Analysis":
            prompt = f"Code: \"\"\"\n{code}\n\"\"\"\nAnalysis:"
        else:
            prompt = f"Code: \"\"\"\n{code}\n\"\"\""
            
        return prompt
    
    def generate_response(self, prompt: str) -> str:
        """Generate response using StarCoder1B with paper-specified parameters."""
        try:
            # Tokenize input
            inputs = self.tokenizer(prompt, return_tensors="pt")
            
            # Move to same device as model
            if hasattr(self.model, 'device'):
                inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
            
            # Generate with paper parameters
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs["input_ids"],
                    temperature=self.config.temperature,
                    top_p=self.config.top_p,
                    max_new_tokens=self.config.max_new_tokens,
                    do_sample=self.config.temperature > 0,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                    repetition_penalty=1.1,  # Prevent repetition
                    num_return_sequences=1
                )
            
            # Decode response
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract just the generated part (after the prompt)
            response = generated_text[len(prompt):].strip()
            
            return response
            
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            return f"ERROR: {str(e)}"
    
    def parse_structured_output(self, response: str, cwe_name: str) -> Tuple[str, str]:
        """Parse structured output to extract Answer and Reason."""
        # Initialize defaults
        answer = "n/a"
        reason = response.strip()
        
        # Try to extract structured answer and reason
        # Look for patterns like "Answer: yes/no" and "Reason: ..."
        
        # Pattern 1: Direct yes/no answer
        yes_patterns = [
            r'\b(?:yes|vulnerable|contains?\s+vulnerabilit|has\s+vulnerabilit)\b',
            r'\b(?:this\s+code\s+(?:is|contains?|has))\s+vulnerable\b'
        ]
        
        no_patterns = [
            r'\b(?:no|not\s+vulnerable|secure|safe)\b',
            r'\b(?:this\s+code\s+(?:is|appears?)\s+(?:secure|safe))\b',
            r'\b(?:no\s+vulnerabilit|does\s+not\s+contain)\b'
        ]
        
        response_lower = response.lower()
        
        # Check for explicit yes
        if any(re.search(pattern, response_lower) for pattern in yes_patterns):
            answer = "yes"
        # Check for explicit no  
        elif any(re.search(pattern, response_lower) for pattern in no_patterns):
            answer = "no"
        
        # Try to extract structured reason
        reason_match = re.search(r'(?:reason|explanation|because):\s*(.+)', response, re.IGNORECASE | re.DOTALL)
        if reason_match:
            reason = reason_match.group(1).strip()
        
        # If we couldn't determine yes/no but have reasoning, extract from reasoning
        if answer == "n/a" and reason:
            if any(re.search(pattern, reason.lower()) for pattern in yes_patterns):
                answer = "yes"
            elif any(re.search(pattern, reason.lower()) for pattern in no_patterns):
                answer = "no"
        
        return answer, reason
    
    def evaluate_accuracy(self, predicted_answer: str, example: Dict[str, Any]) -> float:
        """Evaluate accuracy by comparing predicted answer to ground truth."""
        # Ground truth: vulnerable files should be detected as "yes"
        expected_answer = "yes" if example["is_vulnerable"] else "no"
        
        if predicted_answer.lower() == expected_answer.lower():
            return 1.0
        else:
            return 0.0
    
    def evaluate_reasoning_score(self, predicted_reason: str, ground_truth: str) -> float:
        """Simple reasoning score based on keyword overlap."""
        if not ground_truth.strip():
            return 0.0
        
        # Convert to lowercase and split into words
        pred_words = set(predicted_reason.lower().split())
        gt_words = set(ground_truth.lower().split())
        
        if not gt_words:
            return 0.0
        
        # Calculate Jaccard similarity
        intersection = len(pred_words & gt_words)
        union = len(pred_words | gt_words)
        
        return intersection / union if union > 0 else 0.0
    
    def run_baseline_experiment(self):
        """Run the complete baseline experiment."""
        logger.info("🚀 Starting SecLLMHolmes Baseline Experiment")
        
        # Load model
        self.load_model()
        
        # Load dataset
        dataset = self.load_secllmholmes_data()
        
        if not dataset:
            logger.error("No dataset loaded. Please check SecLLMHolmes data paths.")
            return
        
        # Run experiments for each CWE
        all_results = {}
        
        for cwe, examples in dataset.items():
            logger.info(f"\n📋 Processing {cwe.upper()}: {len(examples)} examples")
            
            cwe_results = {
                "examples": [],
                "metrics": {
                    "accuracy": [],
                    "reasoning_scores": [],
                    "consistency": []
                }
            }
            
            for i, example in enumerate(tqdm(examples, desc=f"Processing {cwe}")):
                logger.info(f"  Example {i+1}/{len(examples)}: {example['file_name']}")
                
                # Prepare prompt
                prompt = self.prepare_prompt(example, prompt_type="Question")
                
                # Run multiple trials for consistency checking
                trial_results = []
                
                for trial in range(self.config.num_trials):
                    # Generate response
                    raw_response = self.generate_response(prompt)
                    
                    # Parse structured output
                    predicted_answer, predicted_reason = self.parse_structured_output(
                        raw_response, example["cwe_name"]
                    )
                    
                    # Evaluate accuracy
                    accuracy = self.evaluate_accuracy(predicted_answer, example)
                    
                    # Evaluate reasoning score
                    reasoning_score = self.evaluate_reasoning_score(
                        predicted_reason, example["ground_truth"]
                    )
                    
                    trial_result = {
                        "trial": trial + 1,
                        "raw_response": raw_response,
                        "predicted_answer": predicted_answer,
                        "predicted_reason": predicted_reason,
                        "accuracy": accuracy,
                        "reasoning_score": reasoning_score
                    }
                    
                    trial_results.append(trial_result)
                
                # Calculate consistency (if multiple trials)
                consistency = 1.0
                if len(trial_results) > 1:
                    answers = [r["predicted_answer"] for r in trial_results]
                    consistency = len(set(answers)) == 1  # All answers the same
                
                example_result = {
                    "example": example,
                    "prompt": prompt,
                    "trials": trial_results,
                    "consistency": consistency,
                    "avg_accuracy": np.mean([r["accuracy"] for r in trial_results]),
                    "avg_reasoning_score": np.mean([r["reasoning_score"] for r in trial_results])
                }
                
                cwe_results["examples"].append(example_result)
                cwe_results["metrics"]["accuracy"].append(example_result["avg_accuracy"])
                cwe_results["metrics"]["reasoning_scores"].append(example_result["avg_reasoning_score"])
                cwe_results["metrics"]["consistency"].append(consistency)
            
            # Calculate CWE-level metrics
            cwe_results["summary"] = {
                "total_examples": len(examples),
                "average_accuracy": np.mean(cwe_results["metrics"]["accuracy"]),
                "average_reasoning_score": np.mean(cwe_results["metrics"]["reasoning_scores"]),
                "consistency_rate": np.mean(cwe_results["metrics"]["consistency"]),
                "accuracy_std": np.std(cwe_results["metrics"]["accuracy"]),
                "reasoning_score_std": np.std(cwe_results["metrics"]["reasoning_scores"])
            }
            
            all_results[cwe] = cwe_results
            
            # Log CWE summary
            summary = cwe_results["summary"]
            logger.info(f"  📊 {cwe.upper()} Results:")
            logger.info(f"    Accuracy: {summary['average_accuracy']:.3f} (±{summary['accuracy_std']:.3f})")
            logger.info(f"    Reasoning: {summary['average_reasoning_score']:.3f} (±{summary['reasoning_score_std']:.3f})")
            logger.info(f"    Consistency: {summary['consistency_rate']:.3f}")
        
        # Calculate overall metrics
        overall_accuracy = np.mean([r["summary"]["average_accuracy"] for r in all_results.values()])
        overall_reasoning = np.mean([r["summary"]["average_reasoning_score"] for r in all_results.values()])
        overall_consistency = np.mean([r["summary"]["consistency_rate"] for r in all_results.values()])
        
        overall_summary = {
            "model": self.config.model_name,
            "timestamp": time.strftime("%Y%m%d_%H%M%S"),
            "config": self.config.__dict__,
            "overall_metrics": {
                "accuracy": overall_accuracy,
                "reasoning_score": overall_reasoning,
                "consistency": overall_consistency
            },
            "per_cwe_results": all_results
        }
        
        # Save results
        results_file = Path(self.config.output_dir) / f"baseline_results_{overall_summary['timestamp']}.json"
        with open(results_file, 'w') as f:
            json.dump(overall_summary, f, indent=2, default=str)
        
        logger.info(f"\n🎉 Baseline Experiment Complete!")
        logger.info(f"📁 Results saved to: {results_file}")
        logger.info(f"📊 Overall Results:")
        logger.info(f"   Accuracy: {overall_accuracy:.3f}")
        logger.info(f"   Reasoning Score: {overall_reasoning:.3f}")
        logger.info(f"   Consistency: {overall_consistency:.3f}")
        
        return overall_summary

def main():
    """Main function to run baseline experiment."""
    # Configuration
    config = BaselineConfig(
        model_name="bigcode/starcoderbase-1b",
        temperature=0.0,  # Paper recommends 0.0 for deterministic results
        max_new_tokens=200,
        num_trials=1,  # Increase for consistency checking
    )
    
    # Create adapter and run experiment
    adapter = SecLLMHolmesBaselineAdapter(config)
    results = adapter.run_baseline_experiment()
    
    return results

if __name__ == "__main__":
    results = main() 