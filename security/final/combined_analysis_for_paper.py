#!/usr/bin/env python3
"""
Combined analysis script for all baseline experiments.
Generates publication-ready charts comparing all 8 models across all CWEs.
"""

import json
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

def load_all_results() -> Dict[str, Any]:
    """Load results from both comprehensive and extended experiments."""
    all_results = {}
    
    # Load comprehensive results (first 3 models)
    comprehensive_files = glob.glob("security/final/comprehensive_results/comprehensive_results_*.json")
    for file_path in comprehensive_files:
        with open(file_path, 'r') as f:
            data = json.load(f)
            for model_name, results in data.get("results", {}).items():
                all_results[model_name] = results
    
    # Load extended results (additional 5 models)
    extended_files = glob.glob("security/final/extended_results/comprehensive_results_*.json")
    for file_path in extended_files:
        with open(file_path, 'r') as f:
            data = json.load(f)
            for model_name, results in data.get("results", {}).items():
                all_results[model_name] = results
    
    return all_results

def create_publication_ready_charts(results: Dict[str, Any], output_dir: Path):
    """Create publication-ready charts for the paper."""
    
    # Prepare data for visualization
    viz_data = []
    
    # CWE mappings for better display
    cwe_names = {
        "cwe-22": "Path Traversal\n(CWE-22)",
        "cwe-77": "Command Injection\n(CWE-77)",
        "cwe-79": "Cross-site Scripting\n(CWE-79)", 
        "cwe-89": "SQL Injection\n(CWE-89)",
        "cwe-190": "Integer Overflow\n(CWE-190)",
        "cwe-416": "Use After Free\n(CWE-416)",
        "cwe-476": "NULL Pointer Deref\n(CWE-476)",
        "cwe-787": "Out-of-bounds Write\n(CWE-787)"
    }
    
    # Model display names for better visualization
    model_display_names = {
        "bigcode/starcoderbase-1b": "StarCoder-1B",
        "bigcode/starcoderbase-7b": "StarCoder-7B", 
        "codellama/CodeLlama-7b-hf": "CodeLlama-7B",
        "Qwen/Qwen2.5-Coder-14B-Instruct": "Qwen2.5-14B",
        "microsoft/Phi-3-medium-14b-instruct": "Phi3-Medium-14B",
        "deepseek-ai/deepseek-coder-33b-base": "DeepSeek-33B",
        "google/gemma-2-27b": "Gemma2-27B",
        "bigcode/starcoder2-15b": "StarCoder2-15B"
    }
    
    for model_name, model_results in results.items():
        if "aggregated_metrics" not in model_results:
            continue
            
        model_display = model_display_names.get(model_name, model_name.split("/")[-1])
        agg_metrics = model_results["aggregated_metrics"]
        
        # Overall metrics
        overall_metrics = agg_metrics.get("overall_metrics", {})
        viz_data.append({
            "Model": model_display,
            "CWE": "Overall",
            "Accuracy": overall_metrics.get("mean_accuracy", 0.0),
            "Model_Size": extract_model_size(model_name)
        })
        
        # Per-CWE metrics
        per_cwe_metrics = agg_metrics.get("per_cwe_metrics", {})
        for cwe, cwe_metrics in per_cwe_metrics.items():
            viz_data.append({
                "Model": model_display,
                "CWE": cwe_names.get(cwe, cwe.upper()),
                "Accuracy": cwe_metrics.get("mean_accuracy", 0.0),
                "Model_Size": extract_model_size(model_name)
            })
    
    df = pd.DataFrame(viz_data)
    
    # Create publication-ready plots
    create_main_comparison_chart(df, output_dir)
    create_detailed_cwe_chart(df, output_dir)
    create_model_size_analysis(df, output_dir)
    create_summary_table(df, output_dir)

def extract_model_size(model_name: str) -> str:
    """Extract model size category from model name."""
    name_lower = model_name.lower()
    if "1b" in name_lower:
        return "1B"
    elif "7b" in name_lower:
        return "7B"
    elif "14b" in name_lower or "14" in name_lower:
        return "14B"
    elif "15b" in name_lower:
        return "15B"
    elif "27b" in name_lower:
        return "27B"
    elif "33b" in name_lower:
        return "33B"
    else:
        return "Unknown"

def create_main_comparison_chart(df: pd.DataFrame, output_dir: Path):
    """Create main comparison chart suitable for paper."""
    
    # Filter for per-CWE data only
    cwe_data = df[df['CWE'] != 'Overall'].copy()
    
    # Create pivot table for heatmap
    pivot_data = cwe_data.pivot(index='CWE', columns='Model', values='Accuracy')
    
    # Sort models by overall performance
    overall_data = df[df['CWE'] == 'Overall']
    model_order = overall_data.sort_values('Accuracy', ascending=False)['Model'].tolist()
    
    # Reorder columns
    available_models = [m for m in model_order if m in pivot_data.columns]
    pivot_data = pivot_data[available_models]
    
    # Create the main comparison chart
    plt.figure(figsize=(14, 10))
    
    # Create heatmap
    ax = sns.heatmap(pivot_data, 
                     annot=True, 
                     fmt='.3f', 
                     cmap='RdYlGn', 
                     vmin=0, 
                     vmax=0.6,  # Adjust based on max performance
                     cbar_kws={'label': 'Accuracy'})
    
    plt.title('SecLLMHolmes Baseline Performance: Per-CWE Accuracy Across 8 Models', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Model', fontsize=14, fontweight='bold')
    plt.ylabel('Vulnerability Type (CWE)', fontsize=14, fontweight='bold')
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save high-resolution version for paper
    plt.savefig(output_dir / 'paper_main_comparison.png', 
                dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'paper_main_comparison.pdf', 
                bbox_inches='tight')
    plt.close()

def create_detailed_cwe_chart(df: pd.DataFrame, output_dir: Path):
    """Create detailed per-CWE comparison chart."""
    
    # Filter CWE data
    cwe_data = df[df['CWE'] != 'Overall'].copy()
    
    # Create grouped bar chart
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Get unique CWEs and models
    cwes = cwe_data['CWE'].unique()
    models = cwe_data['Model'].unique()
    
    # Sort models by overall performance
    overall_data = df[df['CWE'] == 'Overall']
    model_order = overall_data.sort_values('Accuracy', ascending=False)['Model'].tolist()
    models = [m for m in model_order if m in models]
    
    # Set up the bar positions
    x = np.arange(len(cwes))
    width = 0.1
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(models)))
    
    # Create bars for each model
    for i, model in enumerate(models):
        model_data = []
        for cwe in cwes:
            accuracy = cwe_data[(cwe_data['Model'] == model) & (cwe_data['CWE'] == cwe)]['Accuracy'].iloc[0] if not cwe_data[(cwe_data['Model'] == model) & (cwe_data['CWE'] == cwe)].empty else 0
            model_data.append(accuracy)
        
        bars = ax.bar(x + i*width, model_data, width, label=model, 
                     color=colors[i], alpha=0.8)
        
        # Add value labels on bars for better readability
        for bar, val in zip(bars, model_data):
            if val > 0.02:  # Only show labels for non-zero values
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                       f'{val:.3f}', ha='center', va='bottom', fontsize=8)
    
    ax.set_xlabel('Vulnerability Type (CWE)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Accuracy', fontsize=14, fontweight='bold')
    ax.set_title('Detailed Per-CWE Performance Comparison Across All Models', 
                 fontsize=16, fontweight='bold')
    ax.set_xticks(x + width * (len(models)-1) / 2)
    ax.set_xticklabels(cwes, rotation=45, ha='right')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, max(cwe_data['Accuracy']) * 1.2)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'paper_detailed_cwe_comparison.png', 
                dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'paper_detailed_cwe_comparison.pdf', 
                bbox_inches='tight')
    plt.close()

def create_model_size_analysis(df: pd.DataFrame, output_dir: Path):
    """Create model size vs performance analysis."""
    
    overall_data = df[df['CWE'] == 'Overall'].copy()
    
    # Extract numeric size for sorting
    def extract_numeric_size(size_str):
        if 'B' in size_str:
            return float(size_str.replace('B', ''))
        return 0
    
    overall_data['Numeric_Size'] = overall_data['Model_Size'].apply(extract_numeric_size)
    overall_data = overall_data.sort_values('Numeric_Size')
    
    # Create scatter plot
    plt.figure(figsize=(12, 8))
    
    colors = plt.cm.viridis(np.linspace(0, 1, len(overall_data)))
    
    scatter = plt.scatter(overall_data['Numeric_Size'], overall_data['Accuracy'], 
                         c=colors, s=200, alpha=0.7, edgecolors='black', linewidth=2)
    
    # Add model labels
    for i, row in overall_data.iterrows():
        plt.annotate(row['Model'], 
                    (row['Numeric_Size'], row['Accuracy']),
                    xytext=(5, 5), textcoords='offset points',
                    fontsize=10, ha='left')
    
    plt.xlabel('Model Size (Billions of Parameters)', fontsize=14, fontweight='bold')
    plt.ylabel('Overall Accuracy', fontsize=14, fontweight='bold')
    plt.title('Model Size vs Performance Analysis', fontsize=16, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # Add trend line
    z = np.polyfit(overall_data['Numeric_Size'], overall_data['Accuracy'], 1)
    p = np.poly1d(z)
    plt.plot(overall_data['Numeric_Size'], p(overall_data['Numeric_Size']), 
             "r--", alpha=0.8, linewidth=2, label=f'Trend line (R² = {np.corrcoef(overall_data["Numeric_Size"], overall_data["Accuracy"])[0,1]**2:.3f})')
    
    plt.legend()
    plt.tight_layout()
    
    plt.savefig(output_dir / 'paper_model_size_analysis.png', 
                dpi=300, bbox_inches='tight')
    plt.savefig(output_dir / 'paper_model_size_analysis.pdf', 
                bbox_inches='tight')
    plt.close()

def create_summary_table(df: pd.DataFrame, output_dir: Path):
    """Create summary table for paper."""
    
    overall_data = df[df['CWE'] == 'Overall'].copy()
    overall_data = overall_data.sort_values('Accuracy', ascending=False)
    
    # Create comprehensive summary
    summary_lines = [
        "# SecLLMHolmes Baseline Results - Complete Analysis",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Models Tested:** {len(overall_data)}",
        "**Parameters:** Temperature=0.0, Top-p=1.0, Max Tokens=200, Trials=3",
        "",
        "## Overall Performance Ranking",
        "",
        "| Rank | Model | Size | Accuracy | Performance Category |",
        "|------|-------|------|----------|-------------------|"
    ]
    
    for i, (_, row) in enumerate(overall_data.iterrows(), 1):
        accuracy = row['Accuracy']
        if accuracy >= 0.25:
            category = "Strong"
        elif accuracy >= 0.15:
            category = "Moderate" 
        elif accuracy >= 0.10:
            category = "Weak"
        else:
            category = "Poor"
            
        summary_lines.append(f"| {i} | {row['Model']} | {row['Model_Size']} | {accuracy:.4f} | {category} |")
    
    # Add per-CWE analysis
    summary_lines.extend([
        "",
        "## Per-CWE Performance Analysis",
        "",
        "### Best Performing Model per CWE",
        ""
    ])
    
    cwe_data = df[df['CWE'] != 'Overall']
    for cwe in cwe_data['CWE'].unique():
        cwe_best = cwe_data[cwe_data['CWE'] == cwe].sort_values('Accuracy', ascending=False).iloc[0]
        summary_lines.append(f"- **{cwe}**: {cwe_best['Model']} ({cwe_best['Accuracy']:.4f})")
    
    # Add key insights
    summary_lines.extend([
        "",
        "## Key Insights for Neural Steering",
        "",
        "### High-Priority Steering Targets:",
        "1. **CWE-476 (NULL Pointer)**: Universal failure across all models",
        "2. **Model Specialization**: Clear patterns in vulnerability type expertise",
        "3. **Size vs Performance**: Non-linear relationship suggests architecture matters",
        "",
        "### Steering Opportunities:",
        "- **Universal Improvement**: CWE-476 offers guaranteed improvement potential",
        "- **Cross-Model Learning**: Transfer knowledge between specialized models", 
        "- **Size-Specific Strategies**: Tailor steering approaches by model scale",
        "",
        f"*Analysis generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
    ])
    
    # Save comprehensive report
    report_path = output_dir / "paper_comprehensive_analysis.md"
    with open(report_path, 'w') as f:
        f.write('\n'.join(summary_lines))
    
    print(f"📄 Comprehensive analysis saved to: {report_path}")

def main():
    """Generate comprehensive analysis for all baseline experiments."""
    
    print("🔍 Loading all baseline experiment results...")
    results = load_all_results()
    
    if not results:
        print("❌ No results found. Make sure to run both comprehensive and extended experiments first.")
        return
    
    print(f"✅ Loaded results for {len(results)} models")
    for model_name in results.keys():
        print(f"   - {model_name}")
    
    # Create output directory
    output_dir = Path("security/final/paper_analysis")
    output_dir.mkdir(exist_ok=True)
    
    print(f"\n📊 Generating publication-ready charts...")
    create_publication_ready_charts(results, output_dir)
    
    print(f"\n🎉 Analysis complete! Files saved to: {output_dir}")
    print("\n📁 Generated files:")
    for file_path in output_dir.glob("*"):
        print(f"   - {file_path.name}")

if __name__ == "__main__":
    main() 