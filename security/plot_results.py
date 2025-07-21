import json
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
import seaborn as sns
from bias_optimization import analyze_security_patterns

# Define CWE mappings for vulnerability types
CWE_MAPPINGS = {
    'sql_injection': 'SQL Injection (CWE-89)',
    'xss': 'Cross-Site Scripting (CWE-79)',
    'path_traversal': 'Path Traversal (CWE-22)',
    'command_injection': 'Command Injection (CWE-78)',
    'buffer_overflow': 'Buffer Overflow (CWE-120)',
    'use_after_free': 'Use After Free (CWE-416)',
    'integer_overflow': 'Integer Overflow (CWE-190)',
    'hardcoded_credentials': 'Hardcoded Credentials (CWE-798)'
}

# Define steering methods and configurations
STEERING_METHODS = ['baseline', 'original', 'contextual']
STEERING_STRENGTHS = ['no_bias', 'low_bias', 'high_bias']

def format_vulnerability_name(vuln_type):
    """Format vulnerability name with CWE ID if available."""
    return CWE_MAPPINGS.get(vuln_type, vuln_type.replace('_', ' ').title())

def load_results(model_name, steering_method):
    """Load results for a specific model and steering method."""
    if steering_method == 'contextual':
        file_path = 'security/contextual_steering_results.json'
    else:  # baseline or original
        if model_name == 'codellama':
            file_path = 'security/optimized_experiment_results.json'
        else:
            file_path = f'security/optimized_experiment_results_{model_name}.json'
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            if steering_method == 'contextual':
                return data
            else:
                return data if data else {}
    except FileNotFoundError:
        print(f"Warning: Results not found at {file_path}")
        return {}

def calculate_improvements(results_data, steering_method='original'):
    """Calculate improvements for a specific steering method."""
    improvements = {}
    
    if steering_method == 'contextual':
        # Process contextual steering results
        baseline_scores = {}
        steered_scores = {}
        
        for result in results_data.get('results', []):
            vuln_type = result.get('vulnerability_type')
            if not vuln_type:
                continue
            
            strength = result.get('steering_strength', 0)
            score = result.get('security_score', 0)
            
            if strength == 0:  # Baseline
                baseline_scores[vuln_type] = score
            elif strength == 0.5:  # Low steering
                if vuln_type not in steered_scores:
                    steered_scores[vuln_type] = {'low': score, 'high': None}
                else:
                    steered_scores[vuln_type]['low'] = score
            elif strength == 1.0:  # High steering
                if vuln_type not in steered_scores:
                    steered_scores[vuln_type] = {'low': None, 'high': score}
                else:
                    steered_scores[vuln_type]['high'] = score
        
        # Calculate improvements relative to baseline
        for vuln_type in baseline_scores:
            if vuln_type in steered_scores:
                baseline = baseline_scores[vuln_type]
                improvements[vuln_type] = {
                    'low': steered_scores[vuln_type]['low'] - baseline if steered_scores[vuln_type]['low'] is not None else 0,
                    'high': steered_scores[vuln_type]['high'] - baseline if steered_scores[vuln_type]['high'] is not None else 0
                }
    else:
        # Process original steering results
        for vuln_type, vuln_data in results_data.items():
            if isinstance(vuln_data, dict) and 'configurations' in vuln_data:
                baseline_score = vuln_data['configurations']['no_bias']['security_score']
                low_score = vuln_data['configurations']['low_bias']['security_score'] if 'low_bias' in vuln_data['configurations'] else baseline_score
                high_score = vuln_data['configurations']['high_bias']['security_score'] if 'high_bias' in vuln_data['configurations'] else baseline_score
                improvements[vuln_type] = {
                    'low': low_score - baseline_score,
                    'high': high_score - baseline_score
                }
    
    return improvements

def create_combined_improvement_plot(output_path, title):
    """Create a plot showing security score improvements across all models and steering methods."""
    models = ['starcoder', 'starcoderbase-1b', 'codellama']
    improvements_data = []
    
    for model_name in models:
        # Load results for each steering method
        original_results = load_results(model_name, 'original')
        contextual_results = load_results(model_name, 'contextual')
        
        # Calculate improvements for each method
        original_improvements = calculate_improvements(original_results, 'original')
        contextual_improvements = calculate_improvements(contextual_results, 'contextual')
        
        # Combine improvements into a single data structure
        for vuln_type in set(original_improvements.keys()) | set(contextual_improvements.keys()):
            improvements_data.append({
                'Model': model_name.replace('starcoderbase-1b', 'StarCoderBase-1B')
                                  .replace('starcoder', 'StarCoder-7B')
                                  .replace('codellama', 'CodeLlama-7B'),
                'Vulnerability': vuln_type,
                'Formatted_Vulnerability': format_vulnerability_name(vuln_type),
                'Original_Low': original_improvements.get(vuln_type, {}).get('low', 0),
                'Original_High': original_improvements.get(vuln_type, {}).get('high', 0),
                'Contextual_Low': contextual_improvements.get(vuln_type, {}).get('low', 0),
                'Contextual_High': contextual_improvements.get(vuln_type, {}).get('high', 0)
            })
    
    if not improvements_data:
        print("No data available for visualization")
        return
        
    df = pd.DataFrame(improvements_data)
    
    # Set style
    plt.style.use('seaborn')
    
    # Create subplots
    fig, axes = plt.subplots(2, 1, figsize=(15, 20))
    fig.suptitle(title, fontsize=16, y=1.02)
    
    # Plot Low Steering Comparison
    df_low = df.melt(
        id_vars=['Model', 'Formatted_Vulnerability'],
        value_vars=['Original_Low', 'Contextual_Low'],
        var_name='Method',
        value_name='Improvement'
    )
    df_low['Method'] = df_low['Method'].map({
        'Original_Low': 'Original Steering',
        'Contextual_Low': 'Contextual Steering'
    })
    
    pivot_low = df_low.pivot_table(
        index='Formatted_Vulnerability',
        columns=['Model', 'Method'],
        values='Improvement'
    )
    
    pivot_low.plot(kind='bar', ax=axes[0], width=0.8)
    axes[0].set_title('Low Steering Comparison', pad=20)
    axes[0].set_ylabel('Improvement in Security Score')
    axes[0].grid(True, alpha=0.3)
    axes[0].axhline(y=0, color='black', linestyle='-', alpha=0.3)
    
    # Plot High Steering Comparison
    df_high = df.melt(
        id_vars=['Model', 'Formatted_Vulnerability'],
        value_vars=['Original_High', 'Contextual_High'],
        var_name='Method',
        value_name='Improvement'
    )
    df_high['Method'] = df_high['Method'].map({
        'Original_High': 'Original Steering',
        'Contextual_High': 'Contextual Steering'
    })
    
    pivot_high = df_high.pivot_table(
        index='Formatted_Vulnerability',
        columns=['Model', 'Method'],
        values='Improvement'
    )
    
    pivot_high.plot(kind='bar', ax=axes[1], width=0.8)
    axes[1].set_title('High Steering Comparison', pad=20)
    axes[1].set_ylabel('Improvement in Security Score')
    axes[1].grid(True, alpha=0.3)
    axes[1].axhline(y=0, color='black', linestyle='-', alpha=0.3)
    
    # Adjust layout and labels
    for ax in axes:
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        for container in ax.containers:
            ax.bar_label(container, fmt='%.2f', padding=3)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def create_improvements_plot():
    """Create plots showing security score improvements across models and steering methods."""
    # Create combined improvement plots
    create_combined_improvement_plot(
        'security/report/visualizations/steering_methods_comparison.png',
        'Security Score Improvements: Original vs Contextual Steering'
    )

def load_contextual_results(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data['results']

def calculate_effectiveness(results):
    vulnerability_types = set(r['vulnerability_type'] for r in results)
    effectiveness = {}
    
    for vuln in vulnerability_types:
        vuln_results = [r for r in results if r['vulnerability_type'] == vuln]
        baseline = [r for r in vuln_results if r['steering_strength'] == 0.0]
        high_steering = [r for r in vuln_results if r['steering_strength'] == 1.0]
        
        # Calculate effectiveness based on code quality improvement
        effectiveness[vuln] = {
            'baseline': len(baseline[0]['generated_code']) if baseline else 0,
            'steered': len(high_steering[0]['generated_code']) if high_steering else 0
        }
    
    return effectiveness

def create_effectiveness_plot(effectiveness, output_file):
    vulnerabilities = list(effectiveness.keys())
    baseline_scores = [effectiveness[v]['baseline'] for v in vulnerabilities]
    steered_scores = [effectiveness[v]['steered'] for v in vulnerabilities]
    
    x = np.arange(len(vulnerabilities))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 6))
    rects1 = ax.bar(x - width/2, baseline_scores, width, label='Baseline')
    rects2 = ax.bar(x + width/2, steered_scores, width, label='Contextual Steering')
    
    ax.set_ylabel('Code Length (chars)')
    ax.set_title('Effectiveness of Contextual Steering by Vulnerability Type')
    ax.set_xticks(x)
    ax.set_xticklabels([v.replace('_', ' ').title() for v in vulnerabilities], rotation=45)
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()

def create_security_score_comparison_plot(output_path):
    # Load original steering results
    with open('security/optimized_experiment_results.json', 'r') as f:
        original_results = json.load(f)
    
    # Load pre-calculated contextual security scores
    with open('security/contextual_security_scores.json', 'r') as f:
        contextual_scores = json.load(f)
    
    # Process results for each vulnerability type
    comparison_data = []
    
    # First get all vulnerability types from both results
    vuln_types = set(original_results.keys())
    vuln_types.update(contextual_scores.keys())
    
    for vuln_type in vuln_types:
        # Get original steering scores
        original_scores = {
            'baseline': 0.0,
            'low': 0.0,
            'high': 0.0
        }
        
        if vuln_type in original_results:
            vuln_data = original_results[vuln_type]
            if isinstance(vuln_data, dict) and 'configurations' in vuln_data:
                configs = vuln_data['configurations']
                if 'no_bias' in configs:
                    original_scores['baseline'] = configs['no_bias'].get('security_score', 0.0)
                if 'low_bias' in configs:
                    original_scores['low'] = configs['low_bias'].get('security_score', 0.0)
                if 'high_bias' in configs:
                    original_scores['high'] = configs['high_bias'].get('security_score', 0.0)
        
        # Get contextual steering scores
        contextual_scores_for_type = {
            'low': 0.0,
            'high': 0.0
        }
        
        if vuln_type in contextual_scores:
            scores = contextual_scores[vuln_type]
            # Map steering strengths to scores (0.5 -> low, 1.0 -> high)
            if '0.5' in scores:
                contextual_scores_for_type['low'] = scores['0.5']
            if '1.0' in scores:
                contextual_scores_for_type['high'] = scores['1.0']
        
        # Only add to comparison data if we have any non-zero scores
        if any(score > 0 for score in [*original_scores.values(), *contextual_scores_for_type.values()]):
            comparison_data.append({
                'vulnerability_type': format_vulnerability_name(vuln_type),
                'baseline': original_scores['baseline'],
                'original_low': original_scores['low'],
                'original_high': original_scores['high'],
                'contextual_low': contextual_scores_for_type['low'],
                'contextual_high': contextual_scores_for_type['high']
            })
    
    # Create the plot
    plt.figure(figsize=(15, 8))
    
    # Set up the bar positions
    x = np.arange(len(comparison_data))
    width = 0.15
    
    # Create bars for each method with distinct colors
    plt.bar(x - 2*width, [d['baseline'] for d in comparison_data], width, label='Baseline', color='gray')
    plt.bar(x - width, [d['original_low'] for d in comparison_data], width, label='Original Low', color='lightblue')
    plt.bar(x, [d['original_high'] for d in comparison_data], width, label='Original High', color='blue')
    plt.bar(x + width, [d['contextual_low'] for d in comparison_data], width, label='Contextual Low', color='lightgreen')
    plt.bar(x + 2*width, [d['contextual_high'] for d in comparison_data], width, label='Contextual High', color='green')
    
    # Customize the plot
    plt.xlabel('Vulnerability Type')
    plt.ylabel('Security Score')
    plt.title('Security Score Comparison Across Methods')
    plt.xticks(x, [d['vulnerability_type'] for d in comparison_data], rotation=45, ha='right')
    plt.legend()
    
    # Add value labels on top of each bar
    for i, data in enumerate(comparison_data):
        plt.text(i - 2*width, data['baseline'], f'{data["baseline"]:.2f}', ha='center', va='bottom')
        plt.text(i - width, data['original_low'], f'{data["original_low"]:.2f}', ha='center', va='bottom')
        plt.text(i, data['original_high'], f'{data["original_high"]:.2f}', ha='center', va='bottom')
        plt.text(i + width, data['contextual_low'], f'{data["contextual_low"]:.2f}', ha='center', va='bottom')
        plt.text(i + 2*width, data['contextual_high'], f'{data["contextual_high"]:.2f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()

def main():
    """Main function to generate all plots."""
    # Create output directory if it doesn't exist
    os.makedirs('security/report/visualizations', exist_ok=True)
    
    # Generate security score comparison plot
    create_security_score_comparison_plot('security/report/visualizations/security_score_comparison.png')
    
    print("Plots generated successfully and saved in security/report/visualizations/")

if __name__ == '__main__':
    main()