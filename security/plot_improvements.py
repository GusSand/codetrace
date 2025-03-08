import json
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np

def load_results(model_name):
    """Load results for a specific model."""
    if model_name == 'codellama':
        results_file = "security/optimized_experiment_results.json"
    else:
        results_file = f"security/optimized_experiment_results_{model_name}.json"
    with open(results_file, 'r') as f:
        return json.load(f)

def calculate_improvements(results):
    """Calculate improvements from baseline to high steering configuration."""
    improvements = {}
    for vuln_type, vuln_results in results.items():
        if isinstance(vuln_results, dict) and 'configurations' in vuln_results:
            baseline = vuln_results['configurations']['no_bias']
            high_steering = vuln_results['configurations']['high_bias']
            improvements[vuln_type] = {
                'Security Score': high_steering['security_score'] - baseline['security_score'],
                'Quality Score': high_steering['quality_score'] - baseline['quality_score'],
                'Match Score': high_steering['match_score'] - baseline['match_score']
            }
    return improvements

def create_improvements_plot():
    """Create a plot showing improvements from baseline to high steering configuration."""
    models = ['starcoder', 'starcoderbase-1b', 'codellama']
    improvements_data = []
    
    for model in models:
        try:
            results = load_results(model)
            improvements = calculate_improvements(results)
            
            for vuln_type, scores in improvements.items():
                improvements_data.append({
                    'Model': model,
                    'Vulnerability': vuln_type,
                    'Security Score': scores['Security Score'],
                    'Quality Score': scores['Quality Score'],
                    'Match Score': scores['Match Score']
                })
        except FileNotFoundError:
            print(f"Results not found for {model}")
    
    if not improvements_data:
        print("No data available for visualization")
        return
        
    df = pd.DataFrame(improvements_data)
    
    # Set style
    plt.style.use('seaborn')
    
    # Create improvements plot
    plt.figure(figsize=(15, 8))
    pivot_df = df.pivot(
        index='Vulnerability',
        columns='Model',
        values='Security Score'
    )
    
    # Sort by maximum improvement
    pivot_df['max_improvement'] = pivot_df.max(axis=1)
    pivot_df = pivot_df.sort_values('max_improvement', ascending=True)
    pivot_df = pivot_df.drop('max_improvement', axis=1)
    
    # Create the bar plot
    ax = pivot_df.plot(kind='bar', figsize=(15, 8))
    
    # Add value labels on the bars
    for container in ax.containers:
        ax.bar_label(container, fmt='%.2f', padding=3)
    
    # Customize the plot
    plt.title('Security Score Improvements\n(High Steering vs Baseline)', pad=20)
    plt.ylabel('Improvement in Security Score\n(Positive = Better)')
    plt.xlabel('Vulnerability Type')
    plt.legend(title='Model', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    
    # Add zero line with label
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3, label='No Change')
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the plot
    os.makedirs('security/report/visualizations', exist_ok=True)
    plt.savefig('security/report/visualizations/security_improvements_clear.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    create_improvements_plot() 