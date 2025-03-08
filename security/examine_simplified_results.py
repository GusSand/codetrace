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
    """Examine the simplified security examples steering results."""
    results_dir = Path("simplified_security_results")
    
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
    
    # Check the outputs file for more details
    print("\n=== RAW OUTPUTS ===\n")
    try:
        with open(results_dir / "outputs_test", "r") as f:
            outputs = json.load(f)
            print("Test Outputs:")
            print(json.dumps(outputs, indent=2))
    except Exception as e:
        print(f"Error loading outputs file: {e}")
    
    # Compare with the results from original approach
    try:
        with open(results_dir / "test_results.json", "r") as f:
            results = json.load(f)
            print("\nTest Results Summary:")
            print(json.dumps(results, indent=2))
    except Exception as e:
        print(f"Error loading results file: {e}")
    
    # Display overall statistics
    print("\n=== OVERALL STATISTICS ===\n")
    success_rates = []
    
    try:
        with open(results_dir / "test_results.json", "r") as f:
            results = json.load(f)
            success_rates.append(("Test", results["mean_succ"]))
    except Exception:
        pass
    
    try:
        with open(results_dir / "test_results_rand.json", "r") as f:
            results = json.load(f)
            success_rates.append(("Random", results["mean_succ"]))
    except Exception:
        pass
    
    try:
        with open(results_dir / "steer_results.json", "r") as f:
            results = json.load(f)
            success_rates.append(("Steer", results["mean_succ"]))
    except Exception:
        pass
    
    print("Success Rates:")
    for name, rate in success_rates:
        print(f" - {name}: {rate * 100:.1f}%")
    
    # Check if any of the predictions match any part of the expected output
    print("\n=== PARTIAL MATCHES ===\n")
    
    for i, example in enumerate(test_results):
        print(f"Example {i+1}:")
        predicted = example["steered_predictions"]
        expected = example["fim_type"]
        
        # Check for partial matches
        partial_matches = []
        for line in expected.split("\n"):
            line = line.strip()
            if line and len(line) > 10 and line in predicted:
                partial_matches.append(line)
        
        if partial_matches:
            print(f" - Found {len(partial_matches)} partial matches:")
            for match in partial_matches:
                print(f"   * {match}")
        else:
            print(" - No meaningful partial matches found")
    
    print("\n=== SUGGESTIONS FOR NEXT STEPS ===\n")
    print("1. Try with a larger model like StarCoder-7B")
    print("2. Experiment with simultaneous steering of multiple layers (e.g., layers 6, 7, and 8)")
    print("3. Consider amplifying the steering vector by a scaling factor")
    print("4. Investigate using a proper generative approach rather than single-token prediction")
    print("5. Fine-tune a model on security examples instead of using steering")

if __name__ == "__main__":
    main() 