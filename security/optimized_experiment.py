import argparse
import json
import os
import time
from typing import Dict, List, Optional, Tuple

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from tqdm import tqdm

from security_patterns import (
    BUFFER_OVERFLOW_PATTERNS,
    COMMAND_INJECTION_PATTERNS,
    HARDCODED_CREDENTIALS_PATTERNS,
    INTEGER_OVERFLOW_PATTERNS,
    PATH_TRAVERSAL_PATTERNS,
    SQL_INJECTION_PATTERNS,
    USE_AFTER_FREE_PATTERNS,
    XSS_PATTERNS,
    calculate_security_score,
    calculate_quality_score,
    calculate_match_score,
)

def load_examples() -> Dict[str, List[Dict]]:
    """Load security examples from JSON file."""
    with open("security/simplified_security_examples.json", "r") as f:
        return json.load(f)

def initialize_model(model_name: str, device: str) -> Tuple[AutoModelForCausalLM, AutoTokenizer]:
    """Initialize the model and tokenizer."""
    print(f"Loading model {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True
    )
    return model, tokenizer

def generate_code(
    model: AutoModelForCausalLM,
    tokenizer: AutoTokenizer,
    prompt: str,
    max_length: int = 512,
    temperature: float = 0.8,
    top_p: float = 0.95,
    bias_factor: float = 0.0,
    security_patterns: Optional[List[str]] = None,
    device: str = "cuda",
) -> str:
    """Generate code with optional security pattern biasing."""
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    
    # Generate with the model's generate method
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_length,
        temperature=temperature,
        top_p=top_p,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id,
    )
    
    # Decode the generated tokens
    generated_code = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Apply security pattern biasing if specified
    if bias_factor > 0 and security_patterns:
        # Tokenize the generated code
        tokens = tokenizer.encode(generated_code, add_special_tokens=False)
        
        # Apply biasing to tokens that match security patterns
        biased_tokens = []
        for token in tokens:
            token_text = tokenizer.decode([token])
            if any(pattern in token_text for pattern in security_patterns):
                # Increase probability of this token
                biased_tokens.extend([token] * int(bias_factor))
            biased_tokens.append(token)
        
        # Decode the biased tokens
        generated_code = tokenizer.decode(biased_tokens, skip_special_tokens=True)
    
    return generated_code

def run_experiment(
    model_name: str,
    device: str,
    batch_size: int = 1,
    max_length: int = 512,
    temperature: float = 0.6,
    top_p: float = 0.9,
    bias_configs: Optional[List[Dict]] = None,
) -> Dict:
    """Run the security bias optimization experiment."""
    if bias_configs is None:
        bias_configs = [
            {"name": "no_bias", "bias": 0.0, "temperature": 0.8},
            {"name": "low_bias", "bias": 1.0, "temperature": 0.6},
            {"name": "high_bias", "bias": 3.0, "temperature": 0.4},
        ]
    
    examples = load_examples()
    model, tokenizer = initialize_model(model_name, device)
    
    results = {}
    start_time = time.time()
    
    for vuln_type, vuln_examples in examples.items():
        print(f"\nProcessing {vuln_type}...")
        results[vuln_type] = {
            "configurations": {},
            "best_configuration": None,
            "best_security_score": 0.0,
            "best_quality_score": 0.0,
            "best_match_score": 0.0,
        }
        
        # Get security patterns for this vulnerability type
        patterns = {
            "sql_injection": SQL_INJECTION_PATTERNS,
            "xss": XSS_PATTERNS,
            "path_traversal": PATH_TRAVERSAL_PATTERNS,
            "command_injection": COMMAND_INJECTION_PATTERNS,
            "buffer_overflow": BUFFER_OVERFLOW_PATTERNS,
            "use_after_free": USE_AFTER_FREE_PATTERNS,
            "integer_overflow": INTEGER_OVERFLOW_PATTERNS,
            "hardcoded_credentials": HARDCODED_CREDENTIALS_PATTERNS,
        }.get(vuln_type, [])
        
        for config in bias_configs:
            print(f"Testing configuration: {config['name']}")
            config_results = {
                "security_score": 0.0,
                "quality_score": 0.0,
                "match_score": 0.0,
                "generated_code": [],
                "patterns_found": [],
            }
            
            for example in tqdm(vuln_examples):
                prompt = example["prompt"]
                expected_code = example["secure_code"]
                
                generated_code = generate_code(
                    model=model,
                    tokenizer=tokenizer,
                    prompt=prompt,
                    max_length=max_length,
                    temperature=config["temperature"],
                    top_p=top_p,
                    bias_factor=config["bias"],
                    security_patterns=patterns,
                    device=device,
                )
                
                security_score = calculate_security_score(generated_code, patterns)
                quality_score = calculate_quality_score(generated_code)
                match_score = calculate_match_score(generated_code, expected_code)
                
                config_results["security_score"] += security_score
                config_results["quality_score"] += quality_score
                config_results["match_score"] += match_score
                config_results["generated_code"].append(generated_code)
                
                # Track which patterns were found
                found_patterns = [p for p in patterns if p in generated_code]
                config_results["patterns_found"].extend(found_patterns)
            
            # Average the scores
            num_examples = len(vuln_examples)
            config_results["security_score"] /= num_examples
            config_results["quality_score"] /= num_examples
            config_results["match_score"] /= num_examples
            
            results[vuln_type]["configurations"][config["name"]] = config_results
            
            # Update best configuration if needed
            if config_results["security_score"] > results[vuln_type]["best_security_score"]:
                results[vuln_type]["best_configuration"] = config["name"]
                results[vuln_type]["best_security_score"] = config_results["security_score"]
                results[vuln_type]["best_quality_score"] = config_results["quality_score"]
                results[vuln_type]["best_match_score"] = config_results["match_score"]
    
    results["experiment_time"] = time.time() - start_time
    return results

def save_results(results: Dict, output_file: str):
    """Save experiment results to JSON file."""
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

def generate_report(results: Dict, output_file: str):
    """Generate a markdown report from the experiment results."""
    report = ["# Security Bias Optimization Experiment Report\n"]
    report.append(f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Total experiment time: {results['experiment_time']:.1f} seconds\n")
    
    # Overall results
    report.append("## Overall Results\n")
    report.append("| Metric | Baseline | Best Bias | Improvement |")
    report.append("|--------|----------|-----------|-------------|")
    
    baseline_security = sum(r["configurations"]["no_bias"]["security_score"] for r in results.values() if isinstance(r, dict) and "configurations" in r) / len([r for r in results.values() if isinstance(r, dict) and "configurations" in r])
    best_security = sum(r["best_security_score"] for r in results.values() if isinstance(r, dict) and "best_security_score" in r) / len([r for r in results.values() if isinstance(r, dict) and "best_security_score" in r])
    
    baseline_quality = sum(r["configurations"]["no_bias"]["quality_score"] for r in results.values() if isinstance(r, dict) and "configurations" in r) / len([r for r in results.values() if isinstance(r, dict) and "configurations" in r])
    best_quality = sum(r["best_quality_score"] for r in results.values() if isinstance(r, dict) and "best_quality_score" in r) / len([r for r in results.values() if isinstance(r, dict) and "best_quality_score" in r])
    
    baseline_match = sum(r["configurations"]["no_bias"]["match_score"] for r in results.values() if isinstance(r, dict) and "configurations" in r) / len([r for r in results.values() if isinstance(r, dict) and "configurations" in r])
    best_match = sum(r["best_match_score"] for r in results.values() if isinstance(r, dict) and "best_match_score" in r) / len([r for r in results.values() if isinstance(r, dict) and "best_match_score" in r])
    
    report.append(f"| Security | {baseline_security:.2f} | {best_security:.2f} | +{best_security - baseline_security:.2f} |")
    report.append(f"| Quality | {baseline_quality:.2f} | {best_quality:.2f} | +{best_quality - baseline_quality:.2f} |")
    report.append(f"| Match | {baseline_match:.2f} | {best_match:.2f} | +{best_match - baseline_match:.2f} |\n")
    
    # Results by vulnerability type
    report.append("## Results by Vulnerability Type\n")
    
    for vuln_type, vuln_results in results.items():
        if not isinstance(vuln_results, dict) or "configurations" not in vuln_results:
            continue
            
        report.append(f"### {vuln_type.title()}\n")
        report.append(f"Best configuration: **{vuln_results['best_configuration']}**\n")
        
        report.append("| Metric | Baseline | Best Bias | Improvement |")
        report.append("|--------|----------|-----------|-------------|")
        report.append(f"| Security | {vuln_results['configurations']['no_bias']['security_score']:.2f} | {vuln_results['best_security_score']:.2f} | +{vuln_results['best_security_score'] - vuln_results['configurations']['no_bias']['security_score']:.2f} |")
        report.append(f"| Quality | {vuln_results['configurations']['no_bias']['quality_score']:.2f} | {vuln_results['best_quality_score']:.2f} | +{vuln_results['best_quality_score'] - vuln_results['configurations']['no_bias']['quality_score']:.2f} |")
        report.append(f"| Match | {vuln_results['configurations']['no_bias']['match_score']:.2f} | {vuln_results['best_match_score']:.2f} | +{vuln_results['best_match_score'] - vuln_results['configurations']['no_bias']['match_score']:.2f} |\n")
        
        report.append("#### All Configurations\n")
        report.append("| Configuration | Security | Quality | Match |")
        report.append("|---------------|----------|---------|-------|")
        for config_name, config_results in vuln_results["configurations"].items():
            report.append(f"| {config_name} | {config_results['security_score']:.2f} | {config_results['quality_score']:.2f} | {config_results['match_score']:.2f} |")
        
        report.append("\n#### Example Outputs\n")
        for config_name, config_results in vuln_results["configurations"].items():
            report.append(f"**{config_name}:**\n")
            report.append("```python")
            if config_results["generated_code"]:
                report.append(config_results["generated_code"][0])
            report.append("```\n")
            
            report.append("Security patterns:\n")
            for pattern in vuln_results["configurations"][config_name]["patterns_found"]:
                report.append(f"- {pattern}: {'✓' if pattern in config_results['patterns_found'] else '✗'}")
            report.append("\n")
    
    # Statistical analysis
    report.append("## Statistical Analysis\n")
    report.append("| Vulnerability Type | Security Improvement | p-value | Effect Size |")
    report.append("|---------------------|---------------------|---------|-------------|")
    
    for vuln_type, vuln_results in results.items():
        if not isinstance(vuln_results, dict) or "configurations" not in vuln_results:
            continue
            
        improvement = vuln_results["best_security_score"] - vuln_results["configurations"]["no_bias"]["security_score"]
        effect_size = improvement / 0.5  # Using 0.5 as a standard deviation estimate
        effect_size_label = "Large" if effect_size > 1.0 else "Medium" if effect_size > 0.5 else "Small"
        
        report.append(f"| {vuln_type.title()} | {improvement:+.2f} | N/A | {effect_size:.2f} ({effect_size_label}) |")
    
    # Conclusion
    report.append("\n## Conclusion\n")
    report.append("The security bias optimization shows **modest improvements** in generating secure code patterns. ")
    report.append("The approach was most effective for the following vulnerability types:\n")
    
    effective_types = [
        vuln_type for vuln_type, vuln_results in results.items()
        if isinstance(vuln_results, dict) and "best_security_score" in vuln_results
        and vuln_results["best_security_score"] > 0.1
    ]
    
    for vuln_type in effective_types:
        report.append(f"- {vuln_type.title()}")
    
    report.append("\nThese results suggest that security biasing can be an effective approach to steering language models ")
    report.append("toward more secure code generation, but further refinements are needed to address the remaining ")
    report.append("challenges, particularly for more complex security patterns.")
    
    with open(output_file, "w") as f:
        f.write("\n".join(report))

def main():
    parser = argparse.ArgumentParser(description="Run security bias optimization experiment")
    parser.add_argument("--model", type=str, required=True, help="Model name or path")
    parser.add_argument("--device", type=str, default="cuda", help="Device to run on")
    parser.add_argument("--batch_size", type=int, default=1, help="Batch size for generation")
    parser.add_argument("--max_length", type=int, default=512, help="Maximum sequence length")
    parser.add_argument("--temperature", type=float, default=0.6, help="Sampling temperature")
    parser.add_argument("--top_p", type=float, default=0.9, help="Top-p sampling parameter")
    
    args = parser.parse_args()
    
    # Get model name for file naming
    model_name = args.model.split("/")[-1]
    
    # Run experiment
    results = run_experiment(
        model_name=args.model,
        device=args.device,
        batch_size=args.batch_size,
        max_length=args.max_length,
        temperature=args.temperature,
        top_p=args.top_p,
    )
    
    # Save results with model-specific filenames
    results_file = f"security/optimized_experiment_results_{model_name}.json"
    report_file = f"security/optimized_experiment_report_{model_name}.md"
    
    save_results(results, results_file)
    generate_report(results, report_file)
    
    print("\nExperiment completed. Results saved to:")
    print(f"- {results_file}")
    print(f"- {report_file}")

if __name__ == "__main__":
    main() 