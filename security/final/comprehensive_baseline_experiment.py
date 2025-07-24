#!/usr/bin/env python3
"""
Comprehensive baseline experiment framework for SecLLMHolmes dataset.
Runs multiple trials across different models with systematic data collection and analysis.
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
from dataclasses import dataclass, asdict
from collections import defaultdict
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

from transformers import AutoTokenizer, AutoModelForCausalLM
from tqdm import tqdm

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ExperimentConfig:
    """Configuration for comprehensive baseline experiments."""
    # Model configurations
    models: List[str] = None
    
    # Generation parameters (fixed per paper)
    temperature: float = 0.0
    top_p: float = 1.0
    max_new_tokens: int = 200
    
    # Experiment parameters
    num_trials: int = 5  # Multiple runs for statistical significance
    batch_size: int = 1
    
    # Dataset paths
    secllmholmes_base: str = "../SecLLMHolmes/datasets"
    output_dir: str = "security/final/comprehensive_results"
    
    # CWE list
    cwe_list: List[str] = None
    
    def __post_init__(self):
        if self.models is None:
            self.models = [
                "bigcode/starcoderbase-1b",
                "bigcode/starcoderbase-7b", 
                "codellama/CodeLlama-7b-hf"
            ]
        
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

class ComprehensiveSecLLMHolmesExperiment:
    """Comprehensive experiment runner for multiple models and trials."""
    
    def __init__(self, config: ExperimentConfig):
        self.config = config
        self.results = {}
        self.experiment_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
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
        
    def load_secllmholmes_data(self) -> Dict[str, List[Dict]]:
        """Load SecLLMHolmes dataset for each CWE."""
        logger.info("Loading SecLLMHolmes dataset...")
        
        dataset = defaultdict(list)
        
        for cwe in self.config.cwe_list:
            cwe_upper = cwe.upper()
            
            # Try different dataset types: hand-crafted first
            for dataset_type in ["hand-crafted"]:
                dataset_path = Path(self.config.secllmholmes_base) / dataset_type / "dataset" / cwe_upper
                
                if not dataset_path.exists():
                    continue
                    
                logger.info(f"Loading {dataset_type} examples for {cwe_upper}")
                
                # Load all files in the CWE directory
                for file_path in dataset_path.glob("*"):
                    if file_path.is_file() and file_path.suffix in ['.c', '.py', '.java', '.js']:
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                code_content = f.read()
                            
                            # Determine if vulnerable based on filename
                            is_vulnerable = not file_path.name.startswith("p_")
                            
                            example = {
                                "cwe": cwe,
                                "cwe_name": self.cwe_names[cwe],
                                "code": code_content,
                                "file_name": file_path.name,
                                "is_vulnerable": is_vulnerable,
                                "dataset_type": dataset_type,
                                "language": file_path.suffix[1:]  # Remove the dot
                            }
                            
                            dataset[cwe].append(example)
                            
                        except Exception as e:
                            logger.warning(f"Error loading {file_path}: {e}")
                            continue
        
        # Log dataset statistics
        total_examples = sum(len(examples) for examples in dataset.values())
        logger.info(f"Loaded {total_examples} total examples across {len(dataset)} CWEs")
        for cwe, examples in dataset.items():
            vulnerable = sum(1 for ex in examples if ex["is_vulnerable"])
            secure = len(examples) - vulnerable
            logger.info(f"  {cwe.upper()}: {len(examples)} examples ({vulnerable} vulnerable, {secure} secure)")
        
        return dict(dataset)
    
    def format_prompt(self, example: Dict[str, Any]) -> str:
        """Format the prompt for vulnerability detection."""
        return f'''Code: """
{example["code"]}
"""
Does this code contain instances of the security vulnerability known as {example["cwe_name"]}?'''
    
    def parse_response(self, response: str) -> Tuple[str, str]:
        """Parse model response to extract answer and reasoning."""
        # Clean the response
        response = response.strip()
        
        # Try to extract structured answer
        answer_patterns = [
            r'(?i)\b(yes|no)\b(?:\s*[,.]|\s*$)',
            r'(?i)answer:\s*(yes|no)\b',
            r'(?i)the answer is\s*(yes|no)\b'
        ]
        
        predicted_answer = "n/a"
        for pattern in answer_patterns:
            match = re.search(pattern, response)
            if match:
                predicted_answer = match.group(1).lower()
                break
        
        return predicted_answer, response
    
    def run_model_experiment(self, model_name: str, dataset: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Run experiment for a single model across all trials."""
        logger.info(f"Starting experiment for model: {model_name}")
        
        # Load model and tokenizer
        logger.info(f"Loading model: {model_name}")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True
        )
        
        model_results = {
            "model_name": model_name,
            "config": asdict(self.config),
            "trials": []
        }
        
        # Run multiple trials
        for trial_num in range(1, self.config.num_trials + 1):
            logger.info(f"Running trial {trial_num}/{self.config.num_trials} for {model_name}")
            
            trial_results = {
                "trial": trial_num,
                "per_cwe_results": {},
                "start_time": time.time()
            }
            
            # Process each CWE
            for cwe, examples in dataset.items():
                cwe_results = {
                    "examples": []
                }
                
                # Process each example
                for example in tqdm(examples, desc=f"Processing {cwe.upper()}"):
                    prompt = self.format_prompt(example)
                    
                    # Tokenize and generate
                    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
                    inputs = {k: v.to(model.device) for k, v in inputs.items()}
                    
                    with torch.no_grad():
                        outputs = model.generate(
                            **inputs,
                            temperature=self.config.temperature,
                            top_p=self.config.top_p,
                            max_new_tokens=self.config.max_new_tokens,
                            pad_token_id=tokenizer.eos_token_id,
                            do_sample=False  # Deterministic with temp=0.0
                        )
                    
                    # Decode response
                    generated_tokens = outputs[0][inputs['input_ids'].shape[1]:]
                    raw_response = tokenizer.decode(generated_tokens, skip_special_tokens=True)
                    
                    # Parse response
                    predicted_answer, predicted_reason = self.parse_response(raw_response)
                    
                    # Calculate accuracy
                    ground_truth = "yes" if example["is_vulnerable"] else "no"
                    accuracy = 1.0 if predicted_answer == ground_truth else 0.0
                    
                    # Store results
                    example_results = {
                        "example": example,
                        "prompt": prompt,
                        "raw_response": raw_response,
                        "predicted_answer": predicted_answer,
                        "predicted_reason": predicted_reason,
                        "accuracy": accuracy
                    }
                    
                    cwe_results["examples"].append(example_results)
                
                # Calculate CWE-level metrics
                accuracies = [ex["accuracy"] for ex in cwe_results["examples"]]
                cwe_results["accuracy"] = np.mean(accuracies)
                cwe_results["std_accuracy"] = np.std(accuracies)
                cwe_results["num_examples"] = len(accuracies)
                
                trial_results["per_cwe_results"][cwe] = cwe_results
            
            # Calculate trial-level metrics
            trial_results["end_time"] = time.time()
            trial_results["duration"] = trial_results["end_time"] - trial_results["start_time"]
            
            # Overall accuracy across all CWEs for this trial
            all_accuracies = []
            for cwe_results in trial_results["per_cwe_results"].values():
                all_accuracies.extend([ex["accuracy"] for ex in cwe_results["examples"]])
            
            trial_results["overall_accuracy"] = np.mean(all_accuracies)
            trial_results["overall_std"] = np.std(all_accuracies)
            
            model_results["trials"].append(trial_results)
            
            # Save intermediate results
            self.save_intermediate_results(model_name, trial_num, trial_results)
        
        # Calculate model-level aggregated metrics
        model_results["aggregated_metrics"] = self.calculate_aggregated_metrics(model_results["trials"])
        
        # Clean up model to free memory
        del model
        del tokenizer
        torch.cuda.empty_cache()
        
        return model_results
    
    def calculate_aggregated_metrics(self, trials: List[Dict]) -> Dict[str, Any]:
        """Calculate aggregated metrics across all trials."""
        aggregated = {
            "per_cwe_metrics": {},
            "overall_metrics": {}
        }
        
        # Aggregate per-CWE metrics
        for cwe in self.config.cwe_list:
            cwe_accuracies = []
            for trial in trials:
                if cwe in trial["per_cwe_results"]:
                    cwe_accuracies.append(trial["per_cwe_results"][cwe]["accuracy"])
            
            if cwe_accuracies:
                aggregated["per_cwe_metrics"][cwe] = {
                    "mean_accuracy": np.mean(cwe_accuracies),
                    "std_accuracy": np.std(cwe_accuracies),
                    "min_accuracy": np.min(cwe_accuracies),
                    "max_accuracy": np.max(cwe_accuracies),
                    "num_trials": len(cwe_accuracies)
                }
        
        # Aggregate overall metrics
        overall_accuracies = [trial["overall_accuracy"] for trial in trials]
        aggregated["overall_metrics"] = {
            "mean_accuracy": np.mean(overall_accuracies),
            "std_accuracy": np.std(overall_accuracies),
            "min_accuracy": np.min(overall_accuracies),
            "max_accuracy": np.max(overall_accuracies),
            "num_trials": len(overall_accuracies)
        }
        
        return aggregated
    
    def save_intermediate_results(self, model_name: str, trial_num: int, trial_results: Dict):
        """Save intermediate results after each trial."""
        model_safe_name = model_name.replace("/", "_").replace("-", "_")
        filename = f"{model_safe_name}_trial_{trial_num}_{self.experiment_id}.json"
        filepath = Path(self.config.output_dir) / filename
        
        with open(filepath, 'w') as f:
            json.dump(trial_results, f, indent=2, default=str)
        
        logger.info(f"Saved intermediate results: {filepath}")
    
    def run_comprehensive_experiment(self):
        """Run comprehensive experiments across all models."""
        logger.info("Starting comprehensive baseline experiments")
        logger.info(f"Models: {self.config.models}")
        logger.info(f"Trials per model: {self.config.num_trials}")
        logger.info(f"CWEs: {self.config.cwe_list}")
        
        # Load dataset once
        dataset = self.load_secllmholmes_data()
        
        # Run experiments for each model
        for model_name in self.config.models:
            try:
                model_results = self.run_model_experiment(model_name, dataset)
                self.results[model_name] = model_results
                
                # Save model results
                self.save_model_results(model_name, model_results)
                
            except Exception as e:
                logger.error(f"Error running experiment for {model_name}: {e}")
                continue
        
        # Save comprehensive results
        self.save_comprehensive_results()
        
        # Generate visualizations
        self.generate_comprehensive_visualizations()
        
        logger.info("Comprehensive experiments completed!")
    
    def save_model_results(self, model_name: str, model_results: Dict):
        """Save complete results for a single model."""
        model_safe_name = model_name.replace("/", "_").replace("-", "_")
        filename = f"{model_safe_name}_complete_{self.experiment_id}.json"
        filepath = Path(self.config.output_dir) / filename
        
        with open(filepath, 'w') as f:
            json.dump(model_results, f, indent=2, default=str)
        
        logger.info(f"Saved complete model results: {filepath}")
    
    def save_comprehensive_results(self):
        """Save comprehensive results across all models."""
        comprehensive_results = {
            "experiment_id": self.experiment_id,
            "timestamp": datetime.now().isoformat(),
            "config": asdict(self.config),
            "results": self.results
        }
        
        filename = f"comprehensive_results_{self.experiment_id}.json"
        filepath = Path(self.config.output_dir) / filename
        
        with open(filepath, 'w') as f:
            json.dump(comprehensive_results, f, indent=2, default=str)
        
        logger.info(f"Saved comprehensive results: {filepath}")
    
    def generate_comprehensive_visualizations(self):
        """Generate comprehensive visualizations comparing all models."""
        logger.info("Generating comprehensive visualizations...")
        
        # Create analysis directory
        analysis_dir = Path(self.config.output_dir) / "analysis"
        analysis_dir.mkdir(exist_ok=True)
        
        # Prepare data for visualization
        viz_data = []
        
        for model_name, model_results in self.results.items():
            model_display_name = model_name.split("/")[-1] if "/" in model_name else model_name
            
            # Overall metrics
            agg_metrics = model_results["aggregated_metrics"]
            viz_data.append({
                "Model": model_display_name,
                "CWE": "Overall",
                "Mean_Accuracy": agg_metrics["overall_metrics"]["mean_accuracy"],
                "Std_Accuracy": agg_metrics["overall_metrics"]["std_accuracy"],
                "Num_Trials": agg_metrics["overall_metrics"]["num_trials"]
            })
            
            # Per-CWE metrics
            for cwe, cwe_metrics in agg_metrics["per_cwe_metrics"].items():
                viz_data.append({
                    "Model": model_display_name,
                    "CWE": cwe.upper(),
                    "Mean_Accuracy": cwe_metrics["mean_accuracy"],
                    "Std_Accuracy": cwe_metrics["std_accuracy"],
                    "Num_Trials": cwe_metrics["num_trials"]
                })
        
        df = pd.DataFrame(viz_data)
        
        # Generate visualizations
        self.create_comparison_plots(df, analysis_dir)
        self.create_detailed_analysis_report(df, analysis_dir)
        
        logger.info(f"Visualizations saved to: {analysis_dir}")
    
    def create_comparison_plots(self, df: pd.DataFrame, output_dir: Path):
        """Create comparison plots between models."""
        plt.style.use('default')
        
        # 1. Overall accuracy comparison
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle(f'SecLLMHolmes Baseline Comparison - {self.experiment_id}', fontsize=16, fontweight='bold')
        
        # Overall accuracy bar plot with error bars
        overall_data = df[df['CWE'] == 'Overall']
        ax1 = axes[0, 0]
        bars = ax1.bar(overall_data['Model'], overall_data['Mean_Accuracy'], 
                      yerr=overall_data['Std_Accuracy'], capsize=5, 
                      alpha=0.7, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
        ax1.set_title('Overall Accuracy Comparison', fontweight='bold')
        ax1.set_ylabel('Accuracy')
        ax1.set_ylim(0, 1)
        ax1.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, val, std in zip(bars, overall_data['Mean_Accuracy'], overall_data['Std_Accuracy']):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + std + 0.01,
                    f'{val:.3f}±{std:.3f}', ha='center', va='bottom', fontsize=10)
        
        # Per-CWE heatmap
        ax2 = axes[0, 1]
        cwe_data = df[df['CWE'] != 'Overall']
        pivot_data = cwe_data.pivot(index='CWE', columns='Model', values='Mean_Accuracy')
        sns.heatmap(pivot_data, annot=True, fmt='.3f', cmap='RdYlGn', 
                   vmin=0, vmax=1, ax=ax2, cbar_kws={'label': 'Accuracy'})
        ax2.set_title('Per-CWE Accuracy Heatmap', fontweight='bold')
        
        # Box plot showing accuracy distribution
        ax3 = axes[1, 0]
        cwe_data_plot = cwe_data[cwe_data['CWE'] != 'Overall']
        models = cwe_data_plot['Model'].unique()
        box_data = [cwe_data_plot[cwe_data_plot['Model'] == model]['Mean_Accuracy'].values for model in models]
        ax3.boxplot(box_data, labels=models)
        ax3.set_title('Accuracy Distribution Across CWEs', fontweight='bold')
        ax3.set_ylabel('Accuracy')
        ax3.grid(True, alpha=0.3)
        
        # Performance ranking by CWE
        ax4 = axes[1, 1]
        cwe_grouped = cwe_data.groupby('Model')['Mean_Accuracy'].mean().sort_values(ascending=True)
        bars = ax4.barh(range(len(cwe_grouped)), cwe_grouped.values, 
                       color=['#1f77b4', '#ff7f0e', '#2ca02c'])
        ax4.set_yticks(range(len(cwe_grouped)))
        ax4.set_yticklabels(cwe_grouped.index)
        ax4.set_xlabel('Mean Accuracy Across All CWEs')
        ax4.set_title('Model Ranking', fontweight='bold')
        ax4.grid(True, alpha=0.3)
        
        # Add value labels
        for i, (bar, val) in enumerate(zip(bars, cwe_grouped.values)):
            ax4.text(val + 0.005, bar.get_y() + bar.get_height()/2,
                    f'{val:.3f}', ha='left', va='center', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(output_dir / f'comprehensive_comparison_{self.experiment_id}.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Detailed per-CWE comparison
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Grouped bar plot for each CWE
        cwe_list = [cwe for cwe in self.config.cwe_list]
        x = np.arange(len(cwe_list))
        width = 0.25
        
        models = df[df['CWE'] != 'Overall']['Model'].unique()
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        
        for i, model in enumerate(models):
            model_data = []
            model_std = []
            for cwe in cwe_list:
                cwe_row = df[(df['Model'] == model) & (df['CWE'] == cwe.upper())]
                if not cwe_row.empty:
                    model_data.append(cwe_row['Mean_Accuracy'].iloc[0])
                    model_std.append(cwe_row['Std_Accuracy'].iloc[0])
                else:
                    model_data.append(0)
                    model_std.append(0)
            
            bars = ax.bar(x + i*width, model_data, width, 
                         label=model, alpha=0.8, color=colors[i % len(colors)],
                         yerr=model_std, capsize=3)
        
        ax.set_xlabel('CWE Type', fontweight='bold')
        ax.set_ylabel('Accuracy', fontweight='bold')
        ax.set_title('Detailed Per-CWE Performance Comparison', fontweight='bold')
        ax.set_xticks(x + width)
        ax.set_xticklabels([cwe.upper() for cwe in cwe_list], rotation=45)
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 1)
        
        plt.tight_layout()
        plt.savefig(output_dir / f'detailed_cwe_comparison_{self.experiment_id}.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_detailed_analysis_report(self, df: pd.DataFrame, output_dir: Path):
        """Create detailed analysis report."""
        report_lines = [
            f"# Comprehensive SecLLMHolmes Baseline Experiment Report",
            f"",
            f"**Experiment ID:** {self.experiment_id}",
            f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Models Tested:** {', '.join(self.config.models)}",
            f"**Trials per Model:** {self.config.num_trials}",
            f"**Parameters:** Temperature={self.config.temperature}, Top-p={self.config.top_p}, Max Tokens={self.config.max_new_tokens}",
            f"",
            f"## Overall Performance Summary",
            f""
        ]
        
        # Overall results table
        overall_data = df[df['CWE'] == 'Overall'].sort_values('Mean_Accuracy', ascending=False)
        report_lines.extend([
            "| Model | Mean Accuracy | Std Dev | Trials |",
            "|-------|---------------|---------|--------|"
        ])
        
        for _, row in overall_data.iterrows():
            report_lines.append(f"| {row['Model']} | {row['Mean_Accuracy']:.4f} | {row['Std_Accuracy']:.4f} | {row['Num_Trials']} |")
        
        report_lines.extend([
            "",
            "## Per-CWE Performance Analysis",
            ""
        ])
        
        # Per-CWE analysis
        for cwe in self.config.cwe_list:
            cwe_data = df[df['CWE'] == cwe.upper()].sort_values('Mean_Accuracy', ascending=False)
            if not cwe_data.empty:
                report_lines.extend([
                    f"### {cwe.upper()} ({self.cwe_names.get(cwe, cwe)})",
                    "",
                    "| Model | Mean Accuracy | Std Dev |",
                    "|-------|---------------|---------|"
                ])
                
                for _, row in cwe_data.iterrows():
                    report_lines.append(f"| {row['Model']} | {row['Mean_Accuracy']:.4f} | {row['Std_Accuracy']:.4f} |")
                
                report_lines.append("")
        
        # Key findings
        report_lines.extend([
            "## Key Findings",
            ""
        ])
        
        # Best performing model overall
        best_model = overall_data.iloc[0]
        worst_model = overall_data.iloc[-1]
        
        report_lines.extend([
            f"1. **Best Overall Performance:** {best_model['Model']} with {best_model['Mean_Accuracy']:.4f} accuracy",
            f"2. **Worst Overall Performance:** {worst_model['Model']} with {worst_model['Mean_Accuracy']:.4f} accuracy",
            f"3. **Performance Gap:** {best_model['Mean_Accuracy'] - worst_model['Mean_Accuracy']:.4f} accuracy difference",
            ""
        ])
        
        # Best CWE for each model
        report_lines.append("### Best CWE Performance by Model")
        report_lines.append("")
        
        for model in df[df['CWE'] != 'Overall']['Model'].unique():
            model_data = df[(df['Model'] == model) & (df['CWE'] != 'Overall')]
            best_cwe = model_data.loc[model_data['Mean_Accuracy'].idxmax()]
            report_lines.append(f"- **{model}:** {best_cwe['CWE']} ({best_cwe['Mean_Accuracy']:.4f} accuracy)")
        
        report_lines.extend([
            "",
            "## Statistical Significance",
            "",
            f"All results are based on {self.config.num_trials} independent trials per model.",
            "Standard deviations indicate variability across trials.",
            "",
            "---",
            f"*Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
        ])
        
        # Save report
        report_path = output_dir / f"comprehensive_analysis_report_{self.experiment_id}.md"
        with open(report_path, 'w') as f:
            f.write('\n'.join(report_lines))
        
        logger.info(f"Analysis report saved: {report_path}")

def main():
    """Run comprehensive baseline experiments."""
    # Configuration
    config = ExperimentConfig(
        models=[
            "bigcode/starcoderbase-1b",
            "bigcode/starcoderbase-7b", 
            "codellama/CodeLlama-7b-hf"
        ],
        num_trials=3,  # Start with 3 trials, can increase later
        temperature=0.0,
        top_p=1.0,
        max_new_tokens=200
    )
    
    # Run experiments
    experiment = ComprehensiveSecLLMHolmesExperiment(config)
    experiment.run_comprehensive_experiment()

if __name__ == "__main__":
    main() 