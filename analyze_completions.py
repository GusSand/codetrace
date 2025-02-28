#!/usr/bin/env python3
import datasets
import pandas as pd

# Load the dataset
ds = datasets.load_from_disk('starcoder1_fim_completions')

# Convert to pandas for easier analysis
df = pd.DataFrame(ds)

# Print overall statistics
print("\nOverall Statistics:")
print("-" * 50)
print(f"Total examples: {len(df)}")
print(f"Correct predictions: {df['correct'].sum()}")
print(f"Accuracy: {df['correct'].mean()*100:.2f}%")

# Print some examples
print("\nExample Predictions:")
print("-" * 50)
for i, row in df.iterrows():
    print(f"\nExample {i+1}:")
    print(f"Program: {row['fim_program']}")
    print(f"Expected type: {row['fim_type']}")
    print(f"Generated type: {row['generated_text']}")
    print(f"Correct: {row['correct']}")
    if i >= 4:  # Show first 5 examples
        break

# Analyze error patterns
print("\nError Analysis:")
print("-" * 50)
incorrect_df = df[~df['correct']]
if len(incorrect_df) > 0:
    print("\nIncorrect Predictions:")
    for i, row in incorrect_df.iterrows():
        print(f"\nMisprediction {i+1}:")
        print(f"Program: {row['fim_program']}")
        print(f"Expected: {row['fim_type']}")
        print(f"Generated: {row['generated_text']}") 