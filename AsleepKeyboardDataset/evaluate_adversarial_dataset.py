#!/usr/bin/env python3
"""
Evaluate models on the Adversarial AsleepKeyboard Dataset
"""

import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import re
from datetime import datetime
import argparse
from pathlib import Path

class AdversarialEvaluator:
    def __init__(self, model_name="bigcode/starcoderbase-1b"):
        print(f"Loading {model_name}...")
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True
        )
        self.model.eval()
        
        self.results = {
            "model": model_name,
            "timestamp": datetime.now().isoformat(),
            "evaluations": [],
            "summary": {
                "total": 0,
                "vulnerable": 0,
                "by_vulnerability": {},
                "by_technique": {},
                "by_language": {}
            }
        }
    
    def generate_completion(self, prompt, max_tokens=150):
        """Generate code completion"""
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        
        with torch.no_grad():
            outputs = self.model.generate(
                inputs["input_ids"],
                max_new_tokens=max_tokens,
                temperature=0.2,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        completion = self.tokenizer.decode(
            outputs[0][len(inputs["input_ids"][0]):], 
            skip_special_tokens=True
        )
        
        return completion
    
    def check_vulnerability(self, completion, patterns):
        """Check if completion contains vulnerable patterns"""
        completion_lower = completion.lower()
        
        for pattern in patterns:
            # Handle regex patterns
            try:
                if re.search(pattern.lower(), completion_lower):
                    return True, f"Found pattern: {pattern}"
            except:
                # If not valid regex, do simple string match
                if pattern.lower() in completion_lower:
                    return True, f"Found pattern: {pattern}"
        
        return False, "No vulnerable patterns found"
    
    def evaluate_prompt(self, prompt_data):
        """Evaluate a single adversarial prompt"""
        print(f"\nEvaluating: {prompt_data['id']}")
        print(f"  Type: {prompt_data['vulnerability_type']}")
        print(f"  Technique: {prompt_data['technique']}")
        
        # Generate completion
        completion = self.generate_completion(prompt_data["prompt"])
        
        # Check for vulnerability
        is_vulnerable, details = self.check_vulnerability(
            completion, 
            prompt_data["vulnerable_patterns"]
        )
        
        # Store result
        result = {
            "prompt_id": prompt_data["id"],
            "vulnerability_type": prompt_data["vulnerability_type"],
            "technique": prompt_data["technique"],
            "language": prompt_data["language"],
            "is_vulnerable": is_vulnerable,
            "details": details,
            "completion_preview": completion[:100] + "..." if len(completion) > 100 else completion
        }
        
        self.results["evaluations"].append(result)
        
        # Update summary
        self.update_summary(result)
        
        print(f"  Vulnerable: {'YES' if is_vulnerable else 'NO'}")
        
        return result
    
    def update_summary(self, result):
        """Update running summary statistics"""
        self.results["summary"]["total"] += 1
        
        if result["is_vulnerable"]:
            self.results["summary"]["vulnerable"] += 1
        
        # By vulnerability type
        vuln_type = result["vulnerability_type"]
        if vuln_type not in self.results["summary"]["by_vulnerability"]:
            self.results["summary"]["by_vulnerability"][vuln_type] = {
                "total": 0, "vulnerable": 0
            }
        self.results["summary"]["by_vulnerability"][vuln_type]["total"] += 1
        if result["is_vulnerable"]:
            self.results["summary"]["by_vulnerability"][vuln_type]["vulnerable"] += 1
        
        # By technique
        technique = result["technique"]
        if technique not in self.results["summary"]["by_technique"]:
            self.results["summary"]["by_technique"][technique] = {
                "total": 0, "vulnerable": 0
            }
        self.results["summary"]["by_technique"][technique]["total"] += 1
        if result["is_vulnerable"]:
            self.results["summary"]["by_technique"][technique]["vulnerable"] += 1
        
        # By language
        language = result["language"]
        if language not in self.results["summary"]["by_language"]:
            self.results["summary"]["by_language"][language] = {
                "total": 0, "vulnerable": 0
            }
        self.results["summary"]["by_language"][language]["total"] += 1
        if result["is_vulnerable"]:
            self.results["summary"]["by_language"][language]["vulnerable"] += 1
    
    def run_evaluation(self, dataset_file="adversarial_asleep_keyboard_dataset.json", 
                       sample_size=None, specific_technique=None):
        """Run evaluation on dataset"""
        # Load dataset
        with open(dataset_file, 'r') as f:
            dataset = json.load(f)
        
        prompts = dataset["prompts"]
        
        # Filter by technique if specified
        if specific_technique:
            prompts = [p for p in prompts if p["technique"] == specific_technique]
        
        # Sample if requested
        if sample_size and sample_size < len(prompts):
            import random
            prompts = random.sample(prompts, sample_size)
        
        print(f"\nEvaluating {len(prompts)} prompts...")
        
        # Evaluate each prompt
        for i, prompt_data in enumerate(prompts):
            print(f"\nProgress: {i+1}/{len(prompts)}")
            self.evaluate_prompt(prompt_data)
        
        # Generate report
        self.generate_report()
        
        # Save results
        output_file = f"adversarial_evaluation_{self.model_name.replace('/', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\nResults saved to: {output_file}")
        
        return self.results
    
    def generate_report(self):
        """Generate evaluation report"""
        summary = self.results["summary"]
        total = summary["total"]
        vulnerable = summary["vulnerable"]
        
        print("\n" + "="*60)
        print("ADVERSARIAL EVALUATION REPORT")
        print("="*60)
        
        print(f"\nModel: {self.model_name}")
        print(f"Total Prompts: {total}")
        print(f"Vulnerable Completions: {vulnerable} ({vulnerable/total*100:.1f}%)")
        print(f"Secure Completions: {total-vulnerable} ({(total-vulnerable)/total*100:.1f}%)")
        
        # By vulnerability type
        print("\nVulnerability Rates by Type:")
        for vuln_type, stats in sorted(summary["by_vulnerability"].items()):
            rate = stats['vulnerable'] / stats['total'] * 100 if stats['total'] > 0 else 0
            print(f"  {vuln_type}: {stats['vulnerable']}/{stats['total']} ({rate:.1f}%)")
        
        # By technique
        print("\nEffectiveness by Psychological Technique:")
        for technique, stats in sorted(summary["by_technique"].items(), 
                                     key=lambda x: x[1]['vulnerable']/x[1]['total'] if x[1]['total']>0 else 0, 
                                     reverse=True):
            rate = stats['vulnerable'] / stats['total'] * 100 if stats['total'] > 0 else 0
            print(f"  {technique}: {stats['vulnerable']}/{stats['total']} ({rate:.1f}%)")
        
        # By language
        print("\nVulnerability Rates by Language:")
        for language, stats in sorted(summary["by_language"].items()):
            rate = stats['vulnerable'] / stats['total'] * 100 if stats['total'] > 0 else 0
            print(f"  {language}: {stats['vulnerable']}/{stats['total']} ({rate:.1f}%)")
        
        # Find most effective combinations
        print("\nMost Vulnerable Combinations:")
        vulnerable_combos = [(e["vulnerability_type"], e["technique"]) 
                           for e in self.results["evaluations"] if e["is_vulnerable"]]
        from collections import Counter
        combo_counts = Counter(vulnerable_combos).most_common(5)
        for (vuln, tech), count in combo_counts:
            print(f"  {vuln} + {tech}: {count} vulnerabilities")

def main():
    parser = argparse.ArgumentParser(description="Evaluate models on adversarial dataset")
    parser.add_argument("--model", default="bigcode/starcoderbase-1b", 
                       help="Model to evaluate")
    parser.add_argument("--sample", type=int, help="Number of prompts to sample")
    parser.add_argument("--technique", help="Test specific psychological technique")
    parser.add_argument("--dataset", default="adversarial_asleep_keyboard_dataset.json",
                       help="Dataset file")
    
    args = parser.parse_args()
    
    evaluator = AdversarialEvaluator(args.model)
    evaluator.run_evaluation(
        dataset_file=args.dataset,
        sample_size=args.sample,
        specific_technique=args.technique
    )

if __name__ == "__main__":
    main()
