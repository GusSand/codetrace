#!/usr/bin/env python3
"""
Script to add the 'typechecks' field to the mutation_robustness_results_type_mismatches.json dataset.
"""

import json
import os

# Load the dataset
input_file = "data/mutation_robustness_results_type_mismatches.json"
output_file = "data/mutation_robustness_results_with_typechecks.json"

with open(input_file, 'r') as f:
    data = json.load(f)

# Add 'typechecks' field to each item
for item in data:
    item['typechecks'] = True
    # Also ensure each mutation has a 'typechecks' field
    if 'mutations' in item:
        for mutation in item['mutations']:
            mutation['typechecks'] = True

# Save the modified dataset
with open(output_file, 'w') as f:
    json.dump(data, f, indent=2)

print(f"Added 'typechecks' field to dataset and saved to {output_file}") 