#!/usr/bin/env python3
import json
import argparse
import random
from pathlib import Path
from typing import List, Dict, Any

def load_mutation_results(results_file: str) -> List[Dict[Any, Any]]:
    """Load mutation robustness results from JSON file."""
    with open(results_file, 'r') as f:
        return json.load(f)

def prepare_steering_candidates(results: List[Dict[Any, Any]], max_candidates: int = 100) -> List[Dict[Any, Any]]:
    """
    Prepare steering candidates from mutation results.
    We'll use examples where mutations caused type mismatches.
    """
    candidates = []
    
    for result in results:
        # Only use results where mutations caused type mismatches
        if result["mutations"]:
            mutation = result["mutations"][0]  # We stored only type-mismatched mutations
            
            candidate = {
                "index": result["example_id"],
                "original_program": mutation["original_code"],
                "mutated_program": mutation["mutated_code"],
                "expected_type": mutation["expected_fim_type"],
                "generated_type_original": mutation["completion"],
                "generated_type_mutated": mutation["completion_fim_type"],
                "category": "type_mismatch",
                "fim_type": result["fim_type"],
                "prefix": result["prefix"],
                "suffix": result["suffix"],
                "middle": result["middle"]
            }
            candidates.append(candidate)
    
    # Randomly select candidates if we have more than max_candidates
    if len(candidates) > max_candidates:
        candidates = random.sample(candidates, max_candidates)
    
    return candidates

def main():
    parser = argparse.ArgumentParser(description="Prepare steering candidates from mutation results")
    parser.add_argument("--input-file", type=str, required=True,
                        help="Path to mutation robustness results JSON file")
    parser.add_argument("--output-file", type=str, required=True,
                        help="Path to save steering candidates JSON file")
    parser.add_argument("--max-candidates", type=int, default=100,
                        help="Maximum number of steering candidates to create")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed for reproducibility")
    args = parser.parse_args()
    
    # Set random seed
    random.seed(args.seed)
    
    # Load mutation results
    print(f"Loading mutation results from {args.input_file}")
    results = load_mutation_results(args.input_file)
    
    # Prepare steering candidates
    print("Preparing steering candidates...")
    candidates = prepare_steering_candidates(results, args.max_candidates)
    print(f"Created {len(candidates)} steering candidates")
    
    # Save candidates
    output_path = Path(args.output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(candidates, f, indent=2)
    print(f"Saved steering candidates to {args.output_file}")

if __name__ == "__main__":
    main() 