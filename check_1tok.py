#!/usr/bin/env python3
import datasets
from transformers import AutoTokenizer

# Load tokenizer and dataset
tokenizer = AutoTokenizer.from_pretrained('bigcode/starcoder')
ds = datasets.load_dataset('nuprl-staging/py_typeinf_fim')['train']

# Define 1-token filter
def is_1tok(fim_type):
    return len(tokenizer(fim_type, add_special_tokens=False)['input_ids']) == 1

# Filter and count
filtered = ds.filter(lambda x: is_1tok(x['fim_type']))

print(f'Original examples: {len(ds)}')
print(f'After 1-token filter: {len(filtered)}')

# Show some examples of types that pass and fail the filter
print("\nSome 1-token types:")
one_tok = filtered.select(range(5))
for ex in one_tok:
    print(f"- {ex['fim_type']}")

print("\nSome multi-token types:")
multi_tok = ds.filter(lambda x: not is_1tok(x['fim_type'])).select(range(5))
for ex in multi_tok:
    print(f"- {ex['fim_type']}") 