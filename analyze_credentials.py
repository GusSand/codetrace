import json

print('HARDCODED CREDENTIALS SCORES AND IMPROVEMENTS:')

print('\nStarCoder:')
starcoder = json.load(open('security/optimized_experiment_results_starcoder.json'))
baseline_score = starcoder['hardcoded_credentials']['configurations']['no_bias']['security_score']
high_score = starcoder['hardcoded_credentials']['configurations']['high_bias']['security_score']
print(f'Baseline: {baseline_score}')
print(f'High Steering: {high_score}')
print(f'Improvement: {high_score - baseline_score}')

print('\nCodeLlama:')
codellama = json.load(open('security/optimized_experiment_results.json'))
baseline_score = codellama['hardcoded_credentials']['configurations']['no_bias']['security_score']
high_score = codellama['hardcoded_credentials']['configurations']['high_bias']['security_score']
print(f'Baseline: {baseline_score}')
print(f'High Steering: {high_score}')
print(f'Improvement: {high_score - baseline_score}')

print('\nStarCoderBase-1B:')
starcoderbase = json.load(open('security/optimized_experiment_results_starcoderbase-1b.json'))
baseline_score = starcoderbase['hardcoded_credentials']['configurations']['no_bias']['security_score']
high_score = starcoderbase['hardcoded_credentials']['configurations']['high_bias']['security_score']
print(f'Baseline: {baseline_score}')
print(f'High Steering: {high_score}')
print(f'Improvement: {high_score - baseline_score}') 