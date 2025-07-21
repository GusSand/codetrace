import json

print('HARDCODED CREDENTIALS SCORES - LOW STEERING COMPARISON:')

print('\nStarCoder:')
starcoder = json.load(open('security/optimized_experiment_results_starcoder.json'))
baseline_score = starcoder['hardcoded_credentials']['configurations']['no_bias']['security_score']
low_score = starcoder['hardcoded_credentials']['configurations']['low_bias']['security_score']
print(f'Baseline: {baseline_score}')
print(f'Low Steering: {low_score}')
print(f'Improvement: {low_score - baseline_score}')

print('\nCodeLlama:')
codellama = json.load(open('security/optimized_experiment_results.json'))
baseline_score = codellama['hardcoded_credentials']['configurations']['no_bias']['security_score']
low_score = codellama['hardcoded_credentials']['configurations']['low_bias']['security_score']
print(f'Baseline: {baseline_score}')
print(f'Low Steering: {low_score}')
print(f'Improvement: {low_score - baseline_score}')

print('\nStarCoderBase-1B:')
starcoderbase = json.load(open('security/optimized_experiment_results_starcoderbase-1b.json'))
baseline_score = starcoderbase['hardcoded_credentials']['configurations']['no_bias']['security_score']
low_score = starcoderbase['hardcoded_credentials']['configurations']['low_bias']['security_score']
print(f'Baseline: {baseline_score}')
print(f'Low Steering: {low_score}')
print(f'Improvement: {low_score - baseline_score}')

# Now let's also print a summary of all vulnerabilities to see patterns
print('\n\nALL VULNERABILITIES WITH LOW STEERING IMPROVEMENTS:')

for model_name, model_file in [
    ('StarCoder', 'security/optimized_experiment_results_starcoder.json'),
    ('CodeLlama', 'security/optimized_experiment_results.json'),
    ('StarCoderBase-1B', 'security/optimized_experiment_results_starcoderbase-1b.json')
]:
    print(f'\n{model_name}:')
    model_data = json.load(open(model_file))
    improvements = {}
    
    for vuln_type, vuln_data in model_data.items():
        if isinstance(vuln_data, dict) and 'configurations' in vuln_data:
            if 'no_bias' in vuln_data['configurations'] and 'low_bias' in vuln_data['configurations']:
                baseline = vuln_data['configurations']['no_bias']['security_score']
                low = vuln_data['configurations']['low_bias']['security_score']
                improvements[vuln_type] = low - baseline
    
    # Sort by improvement value
    sorted_improvements = sorted(improvements.items(), key=lambda x: x[1], reverse=True)
    for vuln, improvement in sorted_improvements:
        if improvement != 0:  # Only show those with changes
            print(f'  {vuln}: {improvement:.2f}') 