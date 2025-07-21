import json
import numpy as np
from bias_optimization import analyze_security_patterns

# Load contextual results
with open('security/contextual_steering_results.json', 'r') as f:
    contextual_results = json.load(f)['results']

# Load original results for comparison
with open('security/optimized_experiment_results.json', 'r') as f:
    original_results = json.load(f)

# Calculate scores for each vulnerability type
vulnerability_types = [
    'sql_injection', 'xss', 'path_traversal', 'command_injection',
    'buffer_overflow', 'use_after_free', 'integer_overflow', 'hardcoded_credentials'
]

# Store calculated scores
calculated_scores = {}

for vuln_type in vulnerability_types:
    # Get contextual results for this vulnerability type
    vuln_results = [r for r in contextual_results if r['vulnerability_type'] == vuln_type]
    
    if not vuln_results:
        print(f"No contextual results found for {vuln_type}")
        continue
    
    # Group by steering strength
    steering_strengths = sorted(set(r['steering_strength'] for r in vuln_results))
    
    # Calculate scores for each steering strength
    scores = {}
    for strength in steering_strengths:
        # Get all results for this steering strength
        strength_results = [r for r in vuln_results if r['steering_strength'] == strength]
        
        # Calculate average security score
        total_score = 0
        for result in strength_results:
            analysis = analyze_security_patterns(result['generated_code'], vuln_type)
            score = sum(1 for found in analysis.values() if found) / len(analysis)
            total_score += score
        
        avg_score = total_score / len(strength_results) if strength_results else 0
        scores[strength] = avg_score
    
    # Store the scores
    calculated_scores[vuln_type] = scores

# Save calculated scores to a file
with open('security/contextual_security_scores.json', 'w') as f:
    json.dump(calculated_scores, f, indent=2)

print("Security scores calculated and saved to security/contextual_security_scores.json") 