#!/usr/bin/env python3
import os
import json
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Any
from pathlib import Path
import seaborn as sns
import pandas as pd

# Set style for visualizations
plt.style.use('ggplot')

# Set up output directory
OUTPUT_DIR = Path("security/visualizations")
OUTPUT_DIR.mkdir(exist_ok=True)

def load_results(model_name):
    """Load results for a specific model."""
    results_file = f"security/optimized_experiment_results_{model_name}.json"
    with open(results_file, 'r') as f:
        return json.load(f)

def create_comparison_plot():
    """Create a comparison plot of security scores across models."""
    models = ['starcoder', 'codellama']
    data = []
    
    for model in models:
        try:
            results = load_results(model)
            for vuln_type, vuln_results in results.items():
                if isinstance(vuln_results, dict) and 'configurations' in vuln_results:
                    # Get scores from no_bias configuration
                    no_bias = vuln_results['configurations']['no_bias']
                    data.append({
                        'Model': model,
                        'Vulnerability': vuln_type,
                        'Security Score': no_bias['security_score'],
                        'Quality Score': no_bias['quality_score'],
                        'Match Score': no_bias['match_score']
                    })
        except FileNotFoundError:
            print(f"Results not found for {model}")
    
    if not data:
        print("No data available for visualization")
        return
        
    df = pd.DataFrame(data)
    
    # Create security score comparison plot
    plt.figure(figsize=(12, 6))
    df.pivot(index='Vulnerability', columns='Model', values='Security Score').plot(kind='bar')
    plt.xticks(rotation=45)
    plt.title('Security Score Comparison Across Models')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'security_score_comparison.png')
    plt.close()
    
    # Create quality score comparison plot
    plt.figure(figsize=(12, 6))
    df.pivot(index='Vulnerability', columns='Model', values='Quality Score').plot(kind='bar')
    plt.xticks(rotation=45)
    plt.title('Quality Score Comparison Across Models')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'quality_score_comparison.png')
    plt.close()
    
    # Create match score comparison plot
    plt.figure(figsize=(12, 6))
    df.pivot(index='Vulnerability', columns='Model', values='Match Score').plot(kind='bar')
    plt.xticks(rotation=45)
    plt.title('Match Score Comparison Across Models')
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'match_score_comparison.png')
    plt.close()

def calculate_metrics(results):
    """Calculate metrics from results data."""
    metrics = {
        "vulnerability_types": [],
        "baseline_scores": [],
        "optimized_scores": [],
        "improvements": []
    }
    
    for vuln_type, data in results.items():
        baseline_score = data["baseline"]["security_score"]
        optimized_score = data["optimized"]["security_score"]
        improvement = optimized_score - baseline_score
        
        metrics["vulnerability_types"].append(vuln_type)
        metrics["baseline_scores"].append(baseline_score)
        metrics["optimized_scores"].append(optimized_score)
        metrics["improvements"].append(improvement)
    
    # Calculate averages
    metrics["avg_baseline"] = np.mean(metrics["baseline_scores"])
    metrics["avg_optimized"] = np.mean(metrics["optimized_scores"])
    metrics["avg_improvement"] = np.mean(metrics["improvements"])
    
    return metrics

def create_comparison_bar_chart(metrics, filename="security_score_comparison.png"):
    """Create a bar chart comparing baseline and optimized security scores."""
    try:
        vuln_types = metrics["vulnerability_types"]
        baseline = metrics["baseline_scores"]
        optimized = metrics["optimized_scores"]
        
        # Set up the figure
        plt.figure(figsize=(12, 8))
        
        # Set width of bars
        barWidth = 0.35
        
        # Set positions of the bars on X axis
        r1 = np.arange(len(vuln_types))
        r2 = [x + barWidth for x in r1]
        
        # Create bars
        bars1 = plt.bar(r1, baseline, width=barWidth, label='Baseline')
        bars2 = plt.bar(r2, optimized, width=barWidth, label='Optimized')
        
        # Add labels and title
        plt.xlabel('Vulnerability Type', fontweight='bold', fontsize=12)
        plt.ylabel('Security Score', fontweight='bold', fontsize=12)
        plt.title('Security Score Comparison: Baseline vs. Optimized', fontsize=16)
        
        # Add xticks on the middle of the group bars
        plt.xticks([r + barWidth/2 for r in range(len(vuln_types))], 
                  [t.replace('_', ' ').title() for t in vuln_types], 
                  rotation=45)
        
        # Add legend
        plt.legend(fontsize=12)
        
        # Add value labels on bars
        for i, v in enumerate(baseline):
            plt.text(r1[i], v + 0.01, f"{v:.2f}", ha='center', fontsize=10)
        
        for i, v in enumerate(optimized):
            plt.text(r2[i], v + 0.01, f"{v:.2f}", ha='center', fontsize=10)
        
        # Adjust y-axis range
        plt.ylim(0, 1.0)
        
        # Add a horizontal line for average scores
        plt.axhline(y=metrics["avg_baseline"], color='blue', linestyle='--', alpha=0.5)
        plt.text(len(vuln_types)-0.5, metrics["avg_baseline"]+0.02, 
                f"Avg Baseline: {metrics['avg_baseline']:.2f}", ha='right', fontsize=10)
        
        plt.axhline(y=metrics["avg_optimized"], color='orange', linestyle='--', alpha=0.5)
        plt.text(len(vuln_types)-0.5, metrics["avg_optimized"]+0.02, 
                f"Avg Optimized: {metrics['avg_optimized']:.2f}", ha='right', fontsize=10)
        
        # Save the figure
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / filename, dpi=300)
        plt.close()
        
        print(f"Saved comparison bar chart to {OUTPUT_DIR / filename}")
    except Exception as e:
        print(f"Error creating comparison bar chart: {e}")

def create_improvement_bar_chart(metrics, filename="security_improvement.png"):
    """Create a bar chart showing security score improvements."""
    try:
        vuln_types = metrics["vulnerability_types"]
        improvements = metrics["improvements"]
        
        # Set up the figure
        plt.figure(figsize=(12, 8))
        
        # Create bars with color based on value
        colors = ['red' if x <= 0 else 'green' for x in improvements]
        plt.bar(vuln_types, improvements, color=colors)
        
        # Add labels and title
        plt.xlabel('Vulnerability Type', fontweight='bold', fontsize=12)
        plt.ylabel('Security Score Improvement', fontweight='bold', fontsize=12)
        plt.title('Security Score Improvement (Optimized - Baseline)', fontsize=16)
        
        # Format x-axis labels
        plt.xticks(rotation=45)
        plt.xticks(range(len(vuln_types)), [t.replace('_', ' ').title() for t in vuln_types])
        
        # Add value labels on bars
        for i, v in enumerate(improvements):
            plt.text(i, v + 0.01 if v >= 0 else v - 0.06, f"{v:+.2f}", ha='center', fontsize=10)
        
        # Add a horizontal line for average improvement
        plt.axhline(y=metrics["avg_improvement"], color='black', linestyle='--', alpha=0.5)
        plt.text(len(vuln_types)-0.5, metrics["avg_improvement"]+0.02, 
                f"Avg Improvement: {metrics['avg_improvement']:+.2f}", ha='right', fontsize=10)
        
        # Add a horizontal line at zero
        plt.axhline(y=0, color='grey', linestyle='-', alpha=0.3)
        
        # Adjust y-axis range to ensure all bars and labels are visible
        y_min = min(improvements) - 0.1
        y_max = max(improvements) + 0.1
        plt.ylim(y_min, y_max)
        
        # Save the figure
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / filename, dpi=300)
        plt.close()
        
        print(f"Saved improvement bar chart to {OUTPUT_DIR / filename}")
    except Exception as e:
        print(f"Error creating improvement bar chart: {e}")

def create_pattern_statistics(results, filename="security_patterns.png"):
    """Create a simple bar chart showing pattern success rates."""
    try:
        # Process pattern data
        pattern_stats = {}
        
        for vuln_type, data in results.items():
            # Get the analysis results from the baseline and optimized outputs
            baseline_patterns = data["baseline"]["analysis"]
            optimized_patterns = data["optimized"]["analysis"]
            
            # Count patterns
            for pattern, found in baseline_patterns.items():
                key = f"{vuln_type}:{pattern}"
                if key not in pattern_stats:
                    pattern_stats[key] = {"baseline": 0, "optimized": 0}
                if found:
                    pattern_stats[key]["baseline"] = 1
            
            for pattern, found in optimized_patterns.items():
                key = f"{vuln_type}:{pattern}"
                if key not in pattern_stats:
                    pattern_stats[key] = {"baseline": 0, "optimized": 0}
                if found:
                    pattern_stats[key]["optimized"] = 1
        
        # Prepare data for visualization
        pattern_names = list(pattern_stats.keys())
        baseline_values = [stats["baseline"] for stats in pattern_stats.values()]
        optimized_values = [stats["optimized"] for stats in pattern_stats.values()]
        
        # Create figure
        plt.figure(figsize=(14, 8))
        
        # Set width of bars
        barWidth = 0.35
        
        # Set positions of the bars on X axis
        r1 = np.arange(len(pattern_names))
        r2 = [x + barWidth for x in r1]
        
        # Create bars
        plt.bar(r1, baseline_values, width=barWidth, label='Baseline')
        plt.bar(r2, optimized_values, width=barWidth, label='Optimized')
        
        # Formatting
        plt.xlabel('Security Pattern', fontweight='bold', fontsize=12)
        plt.ylabel('Found (1=Yes, 0=No)', fontweight='bold', fontsize=12)
        plt.title('Security Pattern Detection in Generated Code', fontsize=16)
        
        # Format x-axis labels
        formatted_labels = [name.replace(':', ': ') for name in pattern_names]
        plt.xticks([r + barWidth/2 for r in range(len(pattern_names))], 
                  formatted_labels, rotation=90)
        
        plt.legend()
        plt.tight_layout()
        
        plt.savefig(OUTPUT_DIR / filename, dpi=300)
        plt.close()
        
        print(f"Saved pattern statistics to {OUTPUT_DIR / filename}")
    except Exception as e:
        print(f"Error creating pattern statistics: {e}")

def generate_text_summary(metrics, results, filename="security_generation_summary.md"):
    """Generate a text summary of the results."""
    try:
        with open(OUTPUT_DIR / filename, 'w') as f:
            f.write("# Security Code Generation Results Summary\n\n")
            
            f.write("## Overall Results\n\n")
            f.write(f"- Average baseline security score: {metrics['avg_baseline']:.2f}\n")
            f.write(f"- Average optimized security score: {metrics['avg_optimized']:.2f}\n")
            f.write(f"- Average improvement: {metrics['avg_improvement']:+.2f}\n\n")
            
            f.write("## Results by Vulnerability Type\n\n")
            f.write("| Vulnerability Type | Baseline Score | Optimized Score | Improvement |\n")
            f.write("|---------------------|---------------|-----------------|-------------|\n")
            
            for i, vuln_type in enumerate(metrics['vulnerability_types']):
                baseline = metrics['baseline_scores'][i]
                optimized = metrics['optimized_scores'][i]
                improvement = metrics['improvements'][i]
                f.write(f"| {vuln_type.replace('_', ' ').title()} | {baseline:.2f} | {optimized:.2f} | {improvement:+.2f} |\n")
            
            f.write("\n## Generated Code Samples\n\n")
            
            for vuln_type, data in results.items():
                f.write(f"### {vuln_type.replace('_', ' ').title()}\n\n")
                
                f.write("**Prompt:**\n```\n")
                f.write(data["prompt"])
                f.write("\n```\n\n")
                
                f.write("**Expected Secure Code:**\n```python\n")
                f.write(data["expected"])
                f.write("\n```\n\n")
                
                f.write("**Baseline Generated Code:**\n```python\n")
                f.write(data["baseline"]["generated"])
                f.write("\n```\n\n")
                
                security_score = data["baseline"]["security_score"]
                f.write(f"Baseline Security Score: {security_score:.2f}\n\n")
                f.write("Security Patterns:\n")
                for pattern, found in data["baseline"]["analysis"].items():
                    f.write(f"- {pattern}: {'✓' if found else '✗'}\n")
                f.write("\n")
                
                f.write("**Optimized Generated Code:**\n```