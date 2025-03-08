#!/usr/bin/env python3
import sys
import os
import json
import torch
import datasets
from pathlib import Path

# Add the parent directory to the path so we can import from codetrace
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    """Examine the steering results."""
    results_dir = Path("security_steering_results")
    
    # Load the test steering results
    try:
        test_results = datasets.load_from_disk(str(results_dir / "test_steering_results"))
        print(f"Loaded test results dataset with {len(test_results)} examples")
    except Exception as e:
        print(f"Error loading test results: {e}")
        return
    
    # Display the results
    print("\n=== TEST STEERING RESULTS ===\n")
    for i, example in enumerate(test_results):
        print(f"\n--- Example {i+1} ---\n")
        
        # Display original prompt (FIM program)
        print("Original FIM Program:")
        print(example["fim_program"])
        print("\n")
        
        # Display expected secure implementation (FIM type)
        print("Expected Secure Implementation (FIM Type):")
        print(example["fim_type"])
        print("\n")
        
        # Display steered prediction
        print("Steered Prediction:")
        print(example["steered_predictions"])
        print("\n")
        
        # Check if steered prediction matches expected
        match = example["steered_predictions"] == example["fim_type"]
        print(f"Match: {match}")
        print("-" * 80)
    
    # Also load and display the results from the steer split
    try:
        steer_results = datasets.load_from_disk(str(results_dir / "steer_steering_results"))
        print(f"\n\nLoaded steer results dataset with {len(steer_results)} examples")
    except Exception as e:
        print(f"Error loading steer results: {e}")
        return
    
    # Display the steer results
    print("\n=== STEER SPLIT RESULTS ===\n")
    for i, example in enumerate(steer_results):
        print(f"\n--- Example {i+1} ---\n")
        
        # Display original prompt (FIM program)
        print("Original FIM Program:")
        print(example["fim_program"])
        print("\n")
        
        # Display expected secure implementation (FIM type)
        print("Expected Secure Implementation (FIM Type):")
        print(example["fim_type"])
        print("\n")
        
        # Display steered prediction
        print("Steered Prediction:")
        print(example["steered_predictions"])
        print("\n")
        
        # Check if steered prediction matches expected
        match = example["steered_predictions"] == example["fim_type"]
        print(f"Match: {match}")
        print("-" * 80)
    
    # Check the outputs file for more details
    print("\n=== RAW OUTPUTS ===\n")
    try:
        with open(results_dir / "outputs_test", "r") as f:
            outputs = json.load(f)
            print("Test Outputs:")
            print(json.dumps(outputs, indent=2))
    except Exception as e:
        print(f"Error loading outputs file: {e}")
    
    try:
        with open(results_dir / "outputs_steer", "r") as f:
            outputs = json.load(f)
            print("\nSteer Outputs:")
            print(json.dumps(outputs, indent=2))
    except Exception as e:
        print(f"Error loading steer outputs file: {e}")

if __name__ == "__main__":
    main() 