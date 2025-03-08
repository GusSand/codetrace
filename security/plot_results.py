import json
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np

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

def format_vulnerability_name(vuln_type):
    """Format vulnerability name with CWE ID if available."""
    return CWE_MAPPINGS.get(vuln_type, vuln_type.replace('_', ' ').title())

def load_results(model_name):
    """Load results for a specific model."""
    if model_name == 'codellama':
        results_file = "security/optimized_experiment_results.json"
    else:
        results_file = f"security/optimized_experiment_results_{model_name}.json"
    with open(results_file, 'r') as f:
        return json.load(f)

def calculate_improvements(results_data):
    improvements = {}
    for vuln_type, vuln_data in results_data.items():
        if isinstance(vuln_data, dict) and 'configurations' in vuln_data:
            baseline_score = vuln_data['configurations']['no_bias']['security_score']
            high_score = vuln_data['configurations']['high_bias']['security_score'] if 'high_bias' in vuln_data['configurations'] else baseline_score
            improvements[vuln_type] = high_score - baseline_score
    return improvements

def calculate_improvements_low_steering(results_data):
    improvements = {}
    for vuln_type, vuln_data in results_data.items():
        if isinstance(vuln_data, dict) and 'configurations' in vuln_data:
            baseline_score = vuln_data['configurations']['no_bias']['security_score']
            low_score = vuln_data['configurations']['low_bias']['security_score'] if 'low_bias' in vuln_data['configurations'] else baseline_score
            improvements[vuln_type] = low_score - baseline_score
    return improvements

def create_improvement_plot(results_data, output_path):
    improvements = calculate_improvements(results_data)
    
    # Filter out vulnerabilities with no change
    improvements = {k: v for k, v in improvements.items() if v != 0}
    
    # If there are no improvements left, handle gracefully
    if not improvements:
        plt.figure(figsize=(12, 6))
        plt.text(0.5, 0.5, "No changes in security scores", 
                 ha='center', va='center', fontsize=14)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        return
    
    # Sort vulnerabilities by improvement value
    sorted_vulns = sorted(improvements.items(), key=lambda x: x[1], reverse=True)
    vulns = [format_vulnerability_name(x[0]) for x in sorted_vulns]
    values = [x[1] for x in sorted_vulns]
    
    plt.figure(figsize=(12, 6))
    bars = plt.bar(vulns, values)
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Security Score Improvement')
    plt.title('Security Score Improvements with High Steering')
    
    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom' if height >= 0 else 'top')
    
    # Add zero line for reference
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def create_low_steering_plot(results_data, output_path):
    improvements = calculate_improvements_low_steering(results_data)
    
    # Filter out vulnerabilities with no change
    improvements = {k: v for k, v in improvements.items() if v != 0}
    
    # If there are no improvements left, handle gracefully
    if not improvements:
        plt.figure(figsize=(12, 6))
        plt.text(0.5, 0.5, "No changes in security scores", 
                 ha='center', va='center', fontsize=14)
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()
        return
    
    # Sort vulnerabilities by improvement value
    sorted_vulns = sorted(improvements.items(), key=lambda x: x[1], reverse=True)
    vulns = [format_vulnerability_name(x[0]) for x in sorted_vulns]
    values = [x[1] for x in sorted_vulns]
    
    plt.figure(figsize=(12, 6))
    bars = plt.bar(vulns, values)
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Security Score Improvement')
    plt.title('Security Score Improvements with Low Steering')
    
    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom' if height >= 0 else 'top')
    
    # Add zero line for reference
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def create_combined_improvement_plot(output_path, title, calc_func):
    """Create a plot showing security score improvements across all models."""
    # Load results for each model
    results_starcoder = load_results('starcoder')
    results_codellama = load_results('codellama')
    results_starcoderbase = load_results('starcoderbase-1b')
    
    # Calculate improvements for each model
    improvements_data = []
    
    for model_name, results in [
        ('StarCoder-7B', results_starcoder),
        ('StarCoderBase-1B', results_starcoderbase),
        ('CodeLlama-7B', results_codellama)
    ]:
        improvements = calc_func(results)
        
        for vuln_type, improvement in improvements.items():
            improvements_data.append({
                'Model': model_name,
                'Vulnerability': vuln_type,
                'Formatted_Vulnerability': format_vulnerability_name(vuln_type),
                'Improvement': improvement
            })
    
    if not improvements_data:
        print("No data available for visualization")
        return
        
    df = pd.DataFrame(improvements_data)
    
    # Set style
    plt.style.use('seaborn')
    
    # Create improvements plot
    plt.figure(figsize=(15, 8))
    
    # Filter out vulnerabilities with no change across all models
    # Get unique vulnerabilities
    unique_vulns = df['Vulnerability'].unique()
    vulns_to_keep = []
    
    for vuln in unique_vulns:
        vuln_data = df[df['Vulnerability'] == vuln]
        if any(vuln_data['Improvement'] != 0):
            vulns_to_keep.append(vuln)
    
    if not vulns_to_keep:
        print(f"No improvements to show in {output_path}")
        return
        
    df_filtered = df[df['Vulnerability'].isin(vulns_to_keep)]
    
    # Create pivot table for plotting
    pivot_df = df_filtered.pivot(
        index='Vulnerability',
        columns='Model',
        values='Improvement'
    )
    
    # Sort by average improvement across models
    pivot_df['Avg'] = pivot_df.mean(axis=1)
    pivot_df = pivot_df.sort_values('Avg', ascending=False)
    pivot_df = pivot_df.drop('Avg', axis=1)
    
    # Create a mapping of original index to formatted names
    name_mapping = {vuln: format_vulnerability_name(vuln) for vuln in pivot_df.index}
    
    # Replace underscores with spaces and capitalize for better display
    pivot_df.index = pivot_df.index.map(name_mapping)
    
    # Plot with improved styling
    ax = pivot_df.plot(kind='bar', width=0.8)
    plt.xticks(rotation=45, ha='right')
    plt.title(title, pad=20, fontsize=14)
    plt.ylabel('Improvement in Security Score', fontsize=12)
    plt.xlabel('Vulnerability Type', fontsize=12)
    plt.legend(title='Model')
    plt.grid(True, alpha=0.3)
    
    # Add zero line for reference
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    
    # Add values on top of bars
    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f', padding=3)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def create_improvements_plot():
    """Create a plot showing security score improvements across models."""
    # Load results for each model
    results = load_results('starcoder')
    results_codellama = load_results('codellama')
    results_starcoderbase = load_results('starcoderbase-1b')
    
    # Create high steering improvement plots for each model
    create_improvement_plot(results, 'security/report/visualizations/security_improvements_starcoder.png')
    create_improvement_plot(results_codellama, 'security/report/visualizations/security_improvements_codellama.png')
    create_improvement_plot(results_starcoderbase, 'security/report/visualizations/security_improvements_starcoderbase.png')
    
    # Create low steering improvement plots for each model
    create_low_steering_plot(results, 'security/report/visualizations/low_steering_improvements_starcoder.png')
    create_low_steering_plot(results_codellama, 'security/report/visualizations/low_steering_improvements_codellama.png')
    create_low_steering_plot(results_starcoderbase, 'security/report/visualizations/low_steering_improvements_starcoderbase.png')
    
    # Create combined improvement plots
    create_combined_improvement_plot(
        'security/report/visualizations/all_models_high_steering.png',
        'Security Score Improvements (High Steering vs Baseline)',
        calculate_improvements
    )
    
    create_combined_improvement_plot(
        'security/report/visualizations/all_models_low_steering.png',
        'Security Score Improvements (Low Steering vs Baseline)',
        calculate_improvements_low_steering
    )

if __name__ == '__main__':
    # Create directories if they don't exist
    os.makedirs('security/report/visualizations', exist_ok=True)
    
    # Generate all plots
    create_improvements_plot()
    print("Plots generated successfully in security/report/visualizations/")