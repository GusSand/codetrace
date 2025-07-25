#!/usr/bin/env python3
"""
CWE Steering Results Visualization Script

Creates research-quality charts comparing baseline vs steered performance
across different CWE types for the neural steering experiment.

Usage:
    python create_results_charts.py

Author: AI Assistant
Date: 2025-01-24
"""

import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from pathlib import Path
import pandas as pd
from datetime import datetime

# Set style for research paper quality
plt.style.use('default')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3
sns.set_palette("husl")

def load_results(results_file):
    """Load the experiment results."""
    with open(results_file, 'r') as f:
        return json.load(f)

def create_cwe_comparison_chart(data, save_path):
    """Create a comparison chart showing baseline vs steered accuracy per CWE."""
    
    cwe_names = []
    baseline_accs = []
    steered_accs = []
    
    for cwe, results in data['cwe_results'].items():
        cwe_names.append(cwe.replace('CWE-', ''))  # Shorter labels
        baseline_accs.append(results['baseline_accuracy'] * 100)  # Convert to percentage
        steered_accs.append(results['steered_accuracy'] * 100)
    
    x = np.arange(len(cwe_names))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    bars1 = ax.bar(x - width/2, baseline_accs, width, label='Baseline', alpha=0.8, color='#2E86C1')
    bars2 = ax.bar(x + width/2, steered_accs, width, label='Steered', alpha=0.8, color='#E74C3C')
    
    ax.set_xlabel('CWE Type', fontsize=12, fontweight='bold')
    ax.set_ylabel('Accuracy (%)', fontsize=12, fontweight='bold')
    ax.set_title('CWE-Specific Neural Steering Results\nBaseline vs Steered Performance Comparison', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(cwe_names, rotation=45, ha='right')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.0f}%',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),  # 3 points vertical offset
                       textcoords="offset points",
                       ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return fig

def create_improvement_chart(data, save_path):
    """Create a chart showing improvement/decline per CWE."""
    
    cwe_names = []
    improvements = []
    colors = []
    
    for cwe, results in data['cwe_results'].items():
        cwe_names.append(cwe.replace('CWE-', ''))
        improvement = results['average_improvement']
        improvements.append(improvement)
        
        # Color coding: positive=green, negative=red, zero=gray
        if improvement > 0:
            colors.append('#27AE60')  # Green
        elif improvement < 0:
            colors.append('#E74C3C')  # Red
        else:
            colors.append('#95A5A6')  # Gray
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    bars = ax.bar(cwe_names, improvements, color=colors, alpha=0.8)
    
    ax.set_xlabel('CWE Type', fontsize=12, fontweight='bold')
    ax.set_ylabel('Average Improvement Score', fontsize=12, fontweight='bold')
    ax.set_title('Neural Steering Improvement Analysis by CWE\n(Positive = Better with Steering, Negative = Worse)', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax.grid(True, alpha=0.3)
    
    # Rotate x-axis labels
    plt.xticks(rotation=45, ha='right')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.3f}',
                   xy=(bar.get_x() + bar.get_width() / 2, height),
                   xytext=(0, 3 if height >= 0 else -15),
                   textcoords="offset points",
                   ha='center', va='bottom' if height >= 0 else 'top', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return fig

def create_summary_metrics_chart(data, save_path):
    """Create a summary chart showing key experiment metrics."""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
    
    # 1. Overall Accuracy Comparison
    metrics = ['Baseline', 'Steered']
    values = [data['overall_metrics']['baseline_accuracy'] * 100, 
              data['overall_metrics']['steered_accuracy'] * 100]
    
    ax1.bar(metrics, values, color=['#2E86C1', '#E74C3C'], alpha=0.8)
    ax1.set_ylabel('Accuracy (%)')
    ax1.set_title('Overall Performance')
    ax1.set_ylim(0, 100)
    for i, v in enumerate(values):
        ax1.text(i, v + 1, f'{v:.1f}%', ha='center', fontweight='bold')
    
    # 2. Success Rate Pie Chart
    success_rate = data['success_summary']['success_rate'] * 100
    failure_rate = 100 - success_rate
    
    ax2.pie([success_rate, failure_rate], labels=['Successful', 'Failed'], 
            colors=['#27AE60', '#E74C3C'], autopct='%1.1f%%', startangle=90)
    ax2.set_title('CWE Processing Success Rate')
    
    # 3. Examples Distribution
    cwe_names = [cwe.replace('CWE-', '') for cwe in data['cwe_results'].keys()]
    example_counts = [results['total_examples'] for results in data['cwe_results'].values()]
    
    ax3.bar(cwe_names, example_counts, color='#8E44AD', alpha=0.8)
    ax3.set_ylabel('Number of Examples')
    ax3.set_title('Examples Tested per CWE')
    ax3.tick_params(axis='x', rotation=45)
    for i, v in enumerate(example_counts):
        ax3.text(i, v + 0.1, str(v), ha='center', fontweight='bold')
    
    # 4. Change Distribution
    positive_changes = sum(results['positive_improvements'] for results in data['cwe_results'].values())
    negative_changes = sum(results['negative_improvements'] for results in data['cwe_results'].values())
    no_changes = sum(results['no_change'] for results in data['cwe_results'].values())
    
    categories = ['Improved', 'Declined', 'No Change']
    counts = [positive_changes, negative_changes, no_changes]
    colors = ['#27AE60', '#E74C3C', '#95A5A6']
    
    ax4.bar(categories, counts, color=colors, alpha=0.8)
    ax4.set_ylabel('Number of Examples')
    ax4.set_title('Steering Effect Distribution')
    for i, v in enumerate(counts):
        ax4.text(i, v + 0.5, str(v), ha='center', fontweight='bold')
    
    plt.suptitle('CWE Neural Steering Experiment Summary', fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return fig

def create_detailed_breakdown_chart(data, save_path):
    """Create a detailed breakdown chart showing all metrics per CWE."""
    
    # Prepare data for grouped bar chart
    cwe_names = [cwe.replace('CWE-', '') for cwe in data['cwe_results'].keys()]
    
    baseline_acc = [results['baseline_accuracy'] * 100 for results in data['cwe_results'].values()]
    steered_acc = [results['steered_accuracy'] * 100 for results in data['cwe_results'].values()]
    positive_imp = [results['positive_improvements'] for results in data['cwe_results'].values()]
    negative_imp = [results['negative_improvements'] for results in data['cwe_results'].values()]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Top chart: Accuracy comparison
    x = np.arange(len(cwe_names))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, baseline_acc, width, label='Baseline Accuracy', 
                    color='#2E86C1', alpha=0.8)
    bars2 = ax1.bar(x + width/2, steered_acc, width, label='Steered Accuracy', 
                    color='#E74C3C', alpha=0.8)
    
    ax1.set_xlabel('CWE Type')
    ax1.set_ylabel('Accuracy (%)')
    ax1.set_title('Detailed CWE Performance Analysis: Accuracy Comparison')
    ax1.set_xticks(x)
    ax1.set_xticklabels(cwe_names)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 100)
    
    # Bottom chart: Improvement distribution
    bars3 = ax2.bar(x - width/2, positive_imp, width, label='Positive Changes', 
                    color='#27AE60', alpha=0.8)
    bars4 = ax2.bar(x + width/2, negative_imp, width, label='Negative Changes', 
                    color='#E74C3C', alpha=0.8)
    
    ax2.set_xlabel('CWE Type')
    ax2.set_ylabel('Number of Examples')
    ax2.set_title('Change Distribution: Examples that Improved vs Declined')
    ax2.set_xticks(x)
    ax2.set_xticklabels(cwe_names, rotation=45, ha='right')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return fig

def create_research_summary_table(data, save_path):
    """Create a research-quality summary table."""
    
    # Prepare data for DataFrame
    table_data = []
    for cwe, results in data['cwe_results'].items():
        table_data.append({
            'CWE': cwe,
            'Examples': results['total_examples'],
            'Baseline Acc (%)': f"{results['baseline_accuracy']*100:.1f}",
            'Steered Acc (%)': f"{results['steered_accuracy']*100:.1f}",
            'Avg Improvement': f"{results['average_improvement']:+.3f}",
            'Positive/Negative/Unchanged': f"{results['positive_improvements']}/{results['negative_improvements']}/{results['no_change']}"
        })
    
    df = pd.DataFrame(table_data)
    
    # Create table visualization
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.axis('tight')
    ax.axis('off')
    
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.8)
    
    # Style the table
    for i in range(len(df.columns)):
        table[(0, i)].set_facecolor('#34495E')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    for i in range(1, len(df) + 1):
        for j in range(len(df.columns)):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#ECF0F1')
    
    plt.title('CWE Neural Steering Experiment: Detailed Results Summary', 
              fontsize=14, fontweight='bold', pad=20)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return fig

def main():
    """Main function to generate all charts."""
    
    print("🎨 Creating CWE Steering Results Visualizations...")
    
    # Load results
    results_file = "results_final_working/cwe_steering_final_working_20250724_224717.json"
    data = load_results(results_file)
    
    # Create output directory
    output_dir = Path("charts")
    output_dir.mkdir(exist_ok=True)
    
    # Generate charts
    print("📊 Creating CWE comparison chart...")
    create_cwe_comparison_chart(data, output_dir / "cwe_comparison_chart.png")
    
    print("📈 Creating improvement analysis chart...")
    create_improvement_chart(data, output_dir / "improvement_analysis_chart.png")
    
    print("📋 Creating summary metrics chart...")
    create_summary_metrics_chart(data, output_dir / "summary_metrics_chart.png")
    
    print("🔍 Creating detailed breakdown chart...")
    create_detailed_breakdown_chart(data, output_dir / "detailed_breakdown_chart.png")
    
    print("📑 Creating research summary table...")
    create_research_summary_table(data, output_dir / "research_summary_table.png")
    
    # Print summary
    print(f"\n✅ All charts created successfully!")
    print(f"📁 Output directory: {output_dir.absolute()}")
    print(f"📊 Charts generated:")
    for chart_file in output_dir.glob("*.png"):
        print(f"   - {chart_file.name}")
    
    # Print key findings
    print(f"\n🔍 KEY FINDINGS:")
    print(f"   • Successfully processed {data['overall_metrics']['cwes_tested']} CWEs")
    print(f"   • Created steering vectors for all {data['success_summary']['successful_cwes']} CWEs")
    print(f"   • Overall baseline accuracy: {data['overall_metrics']['baseline_accuracy']:.1%}")
    print(f"   • Overall steered accuracy: {data['overall_metrics']['steered_accuracy']:.1%}")
    print(f"   • Total examples tested: {data['overall_metrics']['total_examples']}")
    print(f"   • Experiment duration: {data['duration_seconds']:.1f} seconds")

if __name__ == "__main__":
    main() 