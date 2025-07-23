#!/usr/bin/env python3
"""
Visualization script for sample efficiency experiment results.
"""

import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any

def load_results(results_file: str) -> Dict[str, Any]:
    """Load experiment results from file."""
    with open(results_file, 'r') as f:
        return json.load(f)

def create_sample_efficiency_plots(results: Dict[str, Any], output_dir: Path):
    """Create visualization plots for sample efficiency analysis."""
    
    # Convert results to DataFrame
    data = []
    for result in results['results']:
        data.append({
            'sample_count': result['sample_count'],
            'steering_scale': result['steering_scale'],
            'security_score': result['evaluation'].get('security_score', 0),
            'quality_score': result['evaluation'].get('quality_score', 0),
            'generation_time': result['generation_time'],
            'vulnerability_type': result['test_case']['vulnerability_type']
        })
    
    df = pd.DataFrame(data)
    
    # Create plots
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Sample Efficiency Analysis for Neural Steering', fontsize=16, fontweight='bold')
    
    # Plot 1: Security Score vs Sample Count
    ax1 = axes[0, 0]
    sample_avg = df.groupby('sample_count')['security_score'].mean()
    sample_std = df.groupby('sample_count')['security_score'].std()
    
    ax1.errorbar(sample_avg.index, sample_avg.values, yerr=sample_std.values, 
                marker='o', linewidth=2, capsize=5)
    ax1.set_xlabel('Samples per CVE')
    ax1.set_ylabel('Average Security Score')
    ax1.set_title('Security Score vs Sample Count')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Quality Score vs Sample Count
    ax2 = axes[0, 1]
    quality_avg = df.groupby('sample_count')['quality_score'].mean()
    quality_std = df.groupby('sample_count')['quality_score'].std()
    
    ax2.errorbar(quality_avg.index, quality_avg.values, yerr=quality_std.values,
                marker='s', linewidth=2, capsize=5, color='orange')
    ax2.set_xlabel('Samples per CVE')
    ax2.set_ylabel('Average Quality Score')
    ax2.set_title('Quality Score vs Sample Count')
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Security vs Quality (colored by sample count)
    ax3 = axes[1, 0]
    scatter = ax3.scatter(df['security_score'], df['quality_score'], 
                         c=df['sample_count'], cmap='viridis', alpha=0.7, s=50)
    ax3.set_xlabel('Security Score')
    ax3.set_ylabel('Quality Score')
    ax3.set_title('Security vs Quality (colored by sample count)')
    plt.colorbar(scatter, ax=ax3, label='Samples per CVE')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Generation Time vs Sample Count
    ax4 = axes[1, 1]
    time_avg = df.groupby('sample_count')['generation_time'].mean()
    time_std = df.groupby('sample_count')['generation_time'].std()
    
    ax4.errorbar(time_avg.index, time_avg.values, yerr=time_std.values,
                marker='^', linewidth=2, capsize=5, color='red')
    ax4.set_xlabel('Samples per CVE')
    ax4.set_ylabel('Average Generation Time (s)')
    ax4.set_title('Generation Time vs Sample Count')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save plot
    plot_file = output_dir / "sample_efficiency_analysis.png"
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"📊 Saved sample efficiency plots to {plot_file}")
    
    # Create additional plots
    create_vulnerability_analysis(df, output_dir)
    create_steering_scale_analysis(df, output_dir)

def create_vulnerability_analysis(df: pd.DataFrame, output_dir: Path):
    """Create vulnerability-specific analysis plots."""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Vulnerability-Specific Sample Efficiency', fontsize=16, fontweight='bold')
    
    # Plot 1: Security Score by Vulnerability Type
    ax1 = axes[0, 0]
    vuln_avg = df.groupby('vulnerability_type')['security_score'].mean().sort_values(ascending=False)
    vuln_avg.plot(kind='bar', ax=ax1, color='skyblue')
    ax1.set_xlabel('Vulnerability Type')
    ax1.set_ylabel('Average Security Score')
    ax1.set_title('Security Score by Vulnerability Type')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Sample Count vs Security Score by Vulnerability Type
    ax2 = axes[0, 1]
    for vuln_type in df['vulnerability_type'].unique():
        vuln_data = df[df['vulnerability_type'] == vuln_type]
        vuln_avg = vuln_data.groupby('sample_count')['security_score'].mean()
        ax2.plot(vuln_avg.index, vuln_avg.values, marker='o', label=vuln_type, linewidth=2)
    
    ax2.set_xlabel('Samples per CVE')
    ax2.set_ylabel('Average Security Score')
    ax2.set_title('Security Score vs Sample Count by Vulnerability Type')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Quality Score by Vulnerability Type
    ax3 = axes[1, 0]
    quality_avg = df.groupby('vulnerability_type')['quality_score'].mean().sort_values(ascending=False)
    quality_avg.plot(kind='bar', ax=ax3, color='lightcoral')
    ax3.set_xlabel('Vulnerability Type')
    ax3.set_ylabel('Average Quality Score')
    ax3.set_title('Quality Score by Vulnerability Type')
    ax3.tick_params(axis='x', rotation=45)
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Heatmap of Security Scores
    ax4 = axes[1, 1]
    pivot_table = df.pivot_table(
        values='security_score', 
        index='vulnerability_type', 
        columns='sample_count', 
        aggfunc='mean'
    )
    sns.heatmap(pivot_table, annot=True, fmt='.3f', cmap='RdYlGn', ax=ax4)
    ax4.set_title('Security Score Heatmap\n(Vulnerability Type vs Sample Count)')
    
    plt.tight_layout()
    
    # Save plot
    plot_file = output_dir / "vulnerability_analysis.png"
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"📊 Saved vulnerability analysis plots to {plot_file}")

def create_steering_scale_analysis(df: pd.DataFrame, output_dir: Path):
    """Create steering scale analysis plots."""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Steering Scale Analysis', fontsize=16, fontweight='bold')
    
    # Plot 1: Security Score vs Steering Scale
    ax1 = axes[0, 0]
    for sample_count in df['sample_count'].unique():
        sample_data = df[df['sample_count'] == sample_count]
        scale_avg = sample_data.groupby('steering_scale')['security_score'].mean()
        ax1.plot(scale_avg.index, scale_avg.values, marker='o', label=f'{sample_count} samples', linewidth=2)
    
    ax1.set_xlabel('Steering Scale')
    ax1.set_ylabel('Average Security Score')
    ax1.set_title('Security Score vs Steering Scale')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Quality Score vs Steering Scale
    ax2 = axes[0, 1]
    for sample_count in df['sample_count'].unique():
        sample_data = df[df['sample_count'] == sample_count]
        scale_avg = sample_data.groupby('steering_scale')['quality_score'].mean()
        ax2.plot(scale_avg.index, scale_avg.values, marker='s', label=f'{sample_count} samples', linewidth=2)
    
    ax2.set_xlabel('Steering Scale')
    ax2.set_ylabel('Average Quality Score')
    ax2.set_title('Quality Score vs Steering Scale')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Optimal Steering Scale by Sample Count
    ax3 = axes[1, 0]
    optimal_scales = []
    sample_counts = []
    
    for sample_count in sorted(df['sample_count'].unique()):
        sample_data = df[df['sample_count'] == sample_count]
        if len(sample_data) > 0:
            best_scale = sample_data.loc[sample_data['security_score'].idxmax(), 'steering_scale']
            optimal_scales.append(best_scale)
            sample_counts.append(sample_count)
    
    ax3.bar(sample_counts, optimal_scales, color='lightgreen')
    ax3.set_xlabel('Samples per CVE')
    ax3.set_ylabel('Optimal Steering Scale')
    ax3.set_title('Optimal Steering Scale by Sample Count')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: 3D-like visualization using size
    ax4 = axes[1, 1]
    scatter = ax4.scatter(df['steering_scale'], df['security_score'], 
                         s=df['sample_count'] * 20, alpha=0.6, c=df['quality_score'], cmap='viridis')
    ax4.set_xlabel('Steering Scale')
    ax4.set_ylabel('Security Score')
    ax4.set_title('Security vs Scale (size = samples, color = quality)')
    plt.colorbar(scatter, ax=ax4, label='Quality Score')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save plot
    plot_file = output_dir / "steering_scale_analysis.png"
    plt.savefig(plot_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"📊 Saved steering scale analysis plots to {plot_file}")

def create_summary_table(results: Dict[str, Any], output_dir: Path):
    """Create a summary table of key results."""
    
    # Convert results to DataFrame
    data = []
    for result in results['results']:
        data.append({
            'sample_count': result['sample_count'],
            'steering_scale': result['steering_scale'],
            'security_score': result['evaluation'].get('security_score', 0),
            'quality_score': result['evaluation'].get('quality_score', 0),
            'generation_time': result['generation_time'],
            'vulnerability_type': result['test_case']['vulnerability_type']
        })
    
    df = pd.DataFrame(data)
    
    # Calculate summary statistics
    summary_stats = df.groupby('sample_count').agg({
        'security_score': ['mean', 'std', 'max'],
        'quality_score': ['mean', 'std'],
        'generation_time': 'mean'
    }).round(3)
    
    # Calculate improvement over random (0 samples)
    random_baseline = df[df['sample_count'] == 0]['security_score'].mean()
    improvements = {}
    
    for sample_count in df['sample_count'].unique():
        if sample_count > 0:
            avg_security = df[df['sample_count'] == sample_count]['security_score'].mean()
            if random_baseline > 0:
                improvement = avg_security / random_baseline
            else:
                improvement = avg_security if avg_security > 0 else 1.0
            improvements[sample_count] = improvement
    
    # Create summary table
    summary_table = []
    for sample_count in sorted(df['sample_count'].unique()):
        stats = summary_stats.loc[sample_count]
        improvement = improvements.get(sample_count, 1.0)
        
        summary_table.append({
            'Samples per CVE': sample_count,
            'Avg Security Score': f"{stats[('security_score', 'mean')]:.3f} ± {stats[('security_score', 'std')]:.3f}",
            'Max Security Score': f"{stats[('security_score', 'max')]:.3f}",
            'Avg Quality Score': f"{stats[('quality_score', 'mean')]:.3f} ± {stats[('quality_score', 'std')]:.3f}",
            'Avg Generation Time (s)': f"{stats[('generation_time', 'mean')]:.3f}",
            'Improvement over Random': f"{improvement:.2f}x"
        })
    
    # Save summary table
    summary_df = pd.DataFrame(summary_table)
    summary_file = output_dir / "summary_table.csv"
    summary_df.to_csv(summary_file, index=False)
    
    print(f"📋 Saved summary table to {summary_file}")
    
    # Print summary to console
    print("\n" + "="*80)
    print("SAMPLE EFFICIENCY EXPERIMENT SUMMARY")
    print("="*80)
    print(summary_df.to_string(index=False))
    print("="*80)

def main():
    """Main function to visualize results."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Visualize sample efficiency experiment results')
    parser.add_argument('--results-file', type=str, required=True,
                       help='Path to the results JSON file')
    parser.add_argument('--output-dir', type=str, default='security/sample_efficiency_experiment',
                       help='Output directory for plots')
    
    args = parser.parse_args()
    
    print("📊 Starting visualization of sample efficiency results...")
    
    try:
        # Load results
        results = load_results(args.results_file)
        
        # Create output directory
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create visualizations
        create_sample_efficiency_plots(results, output_dir)
        create_summary_table(results, output_dir)
        
        print(f"✅ Visualization completed successfully!")
        print(f"📁 Plots saved to: {output_dir}")
        
    except Exception as e:
        print(f"❌ Visualization failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 