#!/usr/bin/env python3
"""
Script to add the 'mutated_program' field to the dataset using the existing mutations.
"""

import json
import os

# Load the dataset
input_file = "data/mutation_robustness_results_with_typechecks.json"
output_file = "data/mutation_robustness_results_complete.json"

with open(input_file, 'r') as f:
    data = json.load(f)

# Add 'mutated_program' field to each item
for item in data:
    # Check if the item has mutations
    if 'mutations' in item and len(item['mutations']) > 0:
        # Use the first mutation's mutated_code as the mutated_program
        item['mutated_program'] = item['mutations'][0]['mutated_code']
    else:
        # If there are no mutations, use the original program
        item['mutated_program'] = item['fim_program']

# Save the modified dataset
with open(output_file, 'w') as f:
    json.dump(data, f, indent=2)

print(f"Added 'mutated_program' field to dataset and saved to {output_file}") 