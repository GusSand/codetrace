import datasets
from pathlib import Path
import re
import argparse

# Define the FIM patterns and the placeholder
FIM_PREFIX = "<fim_prefix>"
FIM_SUFFIX = "<fim_suffix>"
FIM_MIDDLE = "<fim_middle>"
PLACEHOLDER = "<FILL>"

def fim_to_placeholder(program: str) -> str:
    """
    Convert a program from FIM format to placeholder format.
    FIM format: <fim_prefix>prefix<fim_suffix>suffix<fim_middle>
    Placeholder format: prefix<FILL>suffix
    """
    if FIM_PREFIX not in program or FIM_SUFFIX not in program or FIM_MIDDLE not in program:
        raise ValueError(f"Program is not in FIM format! Missing one of the tags: {FIM_PREFIX}, {FIM_SUFFIX}, {FIM_MIDDLE}")
    
    # Extract the parts
    prefix_pattern = re.escape(FIM_PREFIX) + "(.*?)" + re.escape(FIM_SUFFIX)
    suffix_pattern = re.escape(FIM_SUFFIX) + "(.*?)" + re.escape(FIM_MIDDLE)
    
    prefix_match = re.search(prefix_pattern, program, re.DOTALL)
    suffix_match = re.search(suffix_pattern, program, re.DOTALL)
    
    if not prefix_match or not suffix_match:
        raise ValueError("Failed to extract prefix or suffix from FIM format")
    
    prefix = prefix_match.group(1)
    suffix = suffix_match.group(1)
    
    # Combine into placeholder format
    return prefix + PLACEHOLDER + suffix

def main():
    parser = argparse.ArgumentParser(description="Convert dataset from FIM format to placeholder format")
    parser.add_argument("--input-path", type=str, required=True, help="Path to the input dataset in FIM format")
    parser.add_argument("--output-path", type=str, required=True, help="Path to save the converted dataset")
    args = parser.parse_args()
    
    print(f"Loading dataset from {args.input_path}...")
    ds = datasets.load_from_disk(args.input_path)
    
    print("Converting FIM format to placeholder format...")
    
    def convert_example(example):
        try:
            example["original_fim_program"] = example["fim_program"]  # Save the original format
            example["fim_program"] = fim_to_placeholder(example["fim_program"])
            return example
        except ValueError as e:
            print(f"Error converting example: {e}")
            return example
    
    converted_ds = ds.map(convert_example)
    
    # Check conversion results
    successful = sum(1 for ex in converted_ds if ex["fim_program"] != ex["original_fim_program"])
    print(f"Successfully converted {successful}/{len(converted_ds)} examples")
    
    print(f"Saving converted dataset to {args.output_path}...")
    converted_ds.save_to_disk(args.output_path)
    print("Conversion complete!")

if __name__ == "__main__":
    main() 