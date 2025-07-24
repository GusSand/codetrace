#!/usr/bin/env python3
"""
Analysis script for SecLLMHolmes baseline experiment results.
Provides comprehensive analysis and visualization of the StarCoder1B baseline performance.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

def load_results(results_file: str) -> Dict[str, Any]:
    """Load baseline results from JSON file."""
    with open(results_file, 'r') as f:
        return json.load(f)

def analyze_overall_performance(results: Dict[str, Any]) -> None:
    """Analyze overall baseline performance."""
    print("🎯 SECLLMHOLMES BASELINE ANALYSIS")
    print("=" * 60)
    print(f"Model: {results['model']}")
    print(f"Timestamp: {results['timestamp']}")
    print(f"Temperature: {results['config']['temperature']}")
    print(f"Max New Tokens: {results['config']['max_new_tokens']}")
    
    overall = results['overall_metrics']
    print(f"\n📊 OVERALL PERFORMANCE:")
    print(f"   🎯 Accuracy: {overall['accuracy']:.3f} ({overall['accuracy']*100:.1f}%)")
    print(f"   💭 Reasoning Score: {overall['reasoning_score']:.3f}")
    print(f"   🔄 Consistency: {overall['consistency']:.3f}")
    
    print(f"\n📈 PERFORMANCE INTERPRETATION:")
    if overall['accuracy'] < 0.2:
        acc_level = "Very Low"
    elif overall['accuracy'] < 0.4:
        acc_level = "Low"
    elif overall['accuracy'] < 0.6:
        acc_level = "Moderate"
    elif overall['accuracy'] < 0.8:
        acc_level = "Good"
    else:
        acc_level = "Excellent"
    
    print(f"   • Accuracy Level: {acc_level}")
    print(f"   • Model correctly identifies vulnerabilities {overall['accuracy']*100:.1f}% of the time")
    print(f"   • Reasoning quality is {'poor' if overall['reasoning_score'] < 0.3 else 'moderate' if overall['reasoning_score'] < 0.6 else 'good'}")
    print(f"   • Model is {'highly consistent' if overall['consistency'] > 0.9 else 'moderately consistent' if overall['consistency'] > 0.7 else 'inconsistent'}")

def analyze_per_cwe_performance(results: Dict[str, Any]) -> pd.DataFrame:
    """Analyze performance by CWE type."""
    print(f"\n🔍 PER-CWE PERFORMANCE ANALYSIS:")
    print("-" * 60)
    
    cwe_data = []
    per_cwe = results['per_cwe_results']
    
    # CWE name mappings for better readability
    cwe_names = {
        "cwe-22": "Path Traversal",
        "cwe-77": "Command Injection", 
        "cwe-79": "Cross-site Scripting",
        "cwe-89": "SQL Injection",
        "cwe-190": "Integer Overflow",
        "cwe-416": "Use After Free",
        "cwe-476": "NULL Pointer Dereference", 
        "cwe-787": "Out-of-bounds Write"
    }
    
    for cwe, data in per_cwe.items():
        summary = data['summary']
        cwe_data.append({
            'CWE': cwe.upper(),
            'Name': cwe_names.get(cwe, cwe),
            'Examples': summary['total_examples'],
            'Accuracy': summary['average_accuracy'],
            'Accuracy_Std': summary['accuracy_std'],
            'Reasoning': summary['average_reasoning_score'],
            'Reasoning_Std': summary['reasoning_score_std'],
            'Consistency': summary['consistency_rate']
        })
        
        print(f"📋 {cwe.upper()} ({cwe_names.get(cwe, cwe)}):")
        print(f"   🎯 Accuracy: {summary['average_accuracy']:.3f} ± {summary['accuracy_std']:.3f}")
        print(f"   💭 Reasoning: {summary['average_reasoning_score']:.3f} ± {summary['reasoning_score_std']:.3f}")
        print(f"   🔄 Consistency: {summary['consistency_rate']:.3f}")
        print(f"   📊 Examples: {summary['total_examples']}")
        
        # Performance interpretation per CWE
        if summary['average_accuracy'] == 0:
            perf = "Failed to detect any vulnerabilities"
        elif summary['average_accuracy'] < 0.3:
            perf = "Poor detection"
        elif summary['average_accuracy'] < 0.7:
            perf = "Moderate detection"
        else:
            perf = "Good detection"
        print(f"   💡 Assessment: {perf}")
        print()
    
    return pd.DataFrame(cwe_data)

def analyze_failure_patterns(results: Dict[str, Any]) -> None:
    """Analyze common failure patterns."""
    print(f"\n🔍 FAILURE PATTERN ANALYSIS:")
    print("-" * 60)
    
    total_examples = 0
    total_correct = 0
    vulnerable_correct = 0
    secure_correct = 0
    vulnerable_total = 0
    secure_total = 0
    
    response_patterns = defaultdict(int)
    
    for cwe, data in results['per_cwe_results'].items():
        for example_result in data['examples']:
            total_examples += 1
            example = example_result['example']
            trial = example_result['trials'][0]  # Single trial per config
            
            is_vulnerable = example['is_vulnerable']
            accuracy = trial['accuracy']
            predicted_answer = trial['predicted_answer']
            
            if is_vulnerable:
                vulnerable_total += 1
                if accuracy == 1.0:
                    vulnerable_correct += 1
            else:
                secure_total += 1
                if accuracy == 1.0:
                    secure_correct += 1
            
            if accuracy == 1.0:
                total_correct += 1
            
            # Track response patterns
            response_patterns[predicted_answer] += 1
    
    print(f"📊 DETECTION BREAKDOWN:")
    print(f"   • Total Examples: {total_examples}")
    print(f"   • Vulnerable Examples: {vulnerable_total}")
    print(f"   • Secure Examples: {secure_total}")
    print(f"   • Vulnerable Detected: {vulnerable_correct}/{vulnerable_total} ({vulnerable_correct/vulnerable_total*100 if vulnerable_total > 0 else 0:.1f}%)")
    print(f"   • Secure Identified: {secure_correct}/{secure_total} ({secure_correct/secure_total*100 if secure_total > 0 else 0:.1f}%)")
    
    print(f"\n🔤 RESPONSE PATTERNS:")
    for pattern, count in sorted(response_patterns.items(), key=lambda x: x[1], reverse=True):
        print(f"   • '{pattern}': {count} times ({count/total_examples*100:.1f}%)")
    
    # Analysis insights
    print(f"\n💡 KEY INSIGHTS:")
    if vulnerable_correct < vulnerable_total * 0.5:
        print(f"   ⚠️  Model struggles to identify vulnerable code ({vulnerable_correct/vulnerable_total*100:.1f}% success)")
    if secure_correct < secure_total * 0.5:
        print(f"   ⚠️  Model struggles to identify secure code ({secure_correct/secure_total*100:.1f}% success)")
    if response_patterns.get('n/a', 0) > total_examples * 0.3:
        print(f"   ⚠️  Model frequently gives ambiguous responses ({response_patterns['n/a']}/{total_examples} cases)")
    
    # Recommendations
    print(f"\n🎯 RECOMMENDATIONS FOR IMPROVEMENT:")
    if overall_accuracy := total_correct / total_examples < 0.3:
        print(f"   • Consider using larger models or fine-tuning")
        print(f"   • Improve prompt engineering for clearer instructions")
    if response_patterns.get('n/a', 0) > total_examples * 0.2:
        print(f"   • Enhance structured output parsing")
        print(f"   • Use more explicit prompting for yes/no answers")

def create_visualization(df: pd.DataFrame, output_dir: str) -> None:
    """Create visualizations of the results."""
    print(f"\n📊 CREATING VISUALIZATIONS...")
    
    # Set up the plotting style
    plt.style.use('default')
    sns.set_palette("husl")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('SecLLMHolmes Baseline Results - StarCoder1B', fontsize=16, fontweight='bold')
    
    # 1. Accuracy by CWE
    axes[0, 0].bar(df['CWE'], df['Accuracy'], yerr=df['Accuracy_Std'], capsize=5)
    axes[0, 0].set_title('Accuracy by CWE Type')
    axes[0, 0].set_ylabel('Accuracy')
    axes[0, 0].set_ylim(0, 1)
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # Add accuracy values on bars
    for i, (cwe, acc) in enumerate(zip(df['CWE'], df['Accuracy'])):
        axes[0, 0].text(i, acc + 0.05, f'{acc:.2f}', ha='center', va='bottom')
    
    # 2. Reasoning Score by CWE
    axes[0, 1].bar(df['CWE'], df['Reasoning'], yerr=df['Reasoning_Std'], capsize=5, color='orange')
    axes[0, 1].set_title('Reasoning Score by CWE Type')
    axes[0, 1].set_ylabel('Reasoning Score')
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    # 3. Accuracy vs Reasoning Score
    axes[1, 0].scatter(df['Accuracy'], df['Reasoning'], s=100, alpha=0.7)
    for i, cwe in enumerate(df['CWE']):
        axes[1, 0].annotate(cwe, (df['Accuracy'][i], df['Reasoning'][i]), 
                           xytext=(5, 5), textcoords='offset points', fontsize=8)
    axes[1, 0].set_xlabel('Accuracy')
    axes[1, 0].set_ylabel('Reasoning Score')
    axes[1, 0].set_title('Accuracy vs Reasoning Score')
    
    # 4. Consistency by CWE
    axes[1, 1].bar(df['CWE'], df['Consistency'], color='green', alpha=0.7)
    axes[1, 1].set_title('Consistency by CWE Type')
    axes[1, 1].set_ylabel('Consistency')
    axes[1, 1].set_ylim(0, 1.1)
    axes[1, 1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    
    # Save the plot
    plot_path = Path(output_dir) / 'baseline_analysis.png'
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"   📊 Visualization saved to: {plot_path}")
    
    plt.show()

def generate_summary_report(results: Dict[str, Any], df: pd.DataFrame, output_dir: str) -> None:
    """Generate a comprehensive summary report."""
    report_path = Path(output_dir) / 'baseline_summary_report.md'
    
    with open(report_path, 'w') as f:
        f.write("# SecLLMHolmes Baseline Experiment Report\n\n")
        f.write(f"**Model:** {results['model']}\n")
        f.write(f"**Date:** {results['timestamp']}\n")
        f.write(f"**Configuration:** Temperature={results['config']['temperature']}, Max Tokens={results['config']['max_new_tokens']}\n\n")
        
        f.write("## Overall Performance\n\n")
        overall = results['overall_metrics']
        f.write(f"- **Accuracy:** {overall['accuracy']:.3f} ({overall['accuracy']*100:.1f}%)\n")
        f.write(f"- **Reasoning Score:** {overall['reasoning_score']:.3f}\n") 
        f.write(f"- **Consistency:** {overall['consistency']:.3f}\n\n")
        
        f.write("## Per-CWE Results\n\n")
        f.write("| CWE | Vulnerability Type | Accuracy | Reasoning | Consistency |\n")
        f.write("|-----|-------------------|----------|-----------|-------------|\n")
        
        for _, row in df.iterrows():
            f.write(f"| {row['CWE']} | {row['Name']} | {row['Accuracy']:.3f} | {row['Reasoning']:.3f} | {row['Consistency']:.3f} |\n")
        
        f.write(f"\n## Key Findings\n\n")
        f.write(f"1. **Overall Performance:** The model achieved {overall['accuracy']*100:.1f}% accuracy across all vulnerability types.\n")
        f.write(f"2. **Best Performance:** {df.loc[df['Accuracy'].idxmax(), 'Name']} (CWE-{df.loc[df['Accuracy'].idxmax(), 'CWE'][4:]}) with {df['Accuracy'].max():.1f}% accuracy.\n")
        f.write(f"3. **Worst Performance:** {df.loc[df['Accuracy'].idxmin(), 'Name']} (CWE-{df.loc[df['Accuracy'].idxmin(), 'CWE'][4:]}) with {df['Accuracy'].min():.1f}% accuracy.\n")
        f.write(f"4. **Consistency:** Model showed high consistency with {overall['consistency']:.1f} consistency rate.\n\n")
        
        # Add improvement recommendations
        f.write("## Recommendations\n\n")
        if overall['accuracy'] < 0.3:
            f.write("- Consider using larger models or implementing fine-tuning\n")
            f.write("- Improve prompt engineering for better vulnerability detection\n")
        f.write("- Implement neural steering techniques to improve security awareness\n")
        f.write("- Consider ensemble methods combining multiple models\n")
    
    print(f"📄 Summary report saved to: {report_path}")

def main():
    """Main analysis function."""
    # Find the most recent results file
    results_dir = Path("security/final/baseline_results")
    if not results_dir.exists():
        print("❌ Results directory not found. Please run the baseline experiment first.")
        return
    
    results_files = list(results_dir.glob("baseline_results_*.json"))
    if not results_files:
        print("❌ No results files found. Please run the baseline experiment first.")
        return
    
    # Use the most recent file
    latest_file = max(results_files, key=lambda x: x.stat().st_mtime)
    print(f"📁 Loading results from: {latest_file}")
    
    # Load and analyze results
    results = load_results(latest_file)
    
    # Perform analyses
    analyze_overall_performance(results)
    df = analyze_per_cwe_performance(results)
    analyze_failure_patterns(results)
    
    # Create output directory for analysis
    analysis_dir = results_dir / "analysis"
    analysis_dir.mkdir(exist_ok=True)
    
    # Generate visualizations and reports
    try:
        create_visualization(df, str(analysis_dir))
    except ImportError:
        print("⚠️  Matplotlib/Seaborn not available for visualizations")
    
    generate_summary_report(results, df, str(analysis_dir))
    
    print(f"\n🎉 Analysis complete! Check {analysis_dir} for detailed results.")

if __name__ == "__main__":
    main() 