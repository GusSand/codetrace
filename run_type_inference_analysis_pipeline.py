#!/usr/bin/env python3
import os
import argparse
import subprocess
import json
from pathlib import Path
import time

def run_command(command, description):
    """Run a command and print its output in real-time."""
    print(f"\n{'='*80}\n{description}\n{'='*80}")
    print(f"Running command: {' '.join(command)}")
    
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    # Print output in real-time
    for line in process.stdout:
        print(line, end='')
    
    process.wait()
    return process.returncode

def main():
    parser = argparse.ArgumentParser(description="Run the complete type inference analysis pipeline")
    parser.add_argument("--original-dataset", type=str, default="starcoder1_fim_completions",
                        help="Path to the original dataset")
    parser.add_argument("--output-dir", type=str, default="type_inference_pipeline",
                        help="Directory to save all results")
    parser.add_argument("--model-id", type=str, default="bigcode/starcoderbase-1b",
                        help="Model ID to use for completions")
    parser.add_argument("--max-samples", type=int, default=10,
                        help="Maximum number of examples to process for each step")
    parser.add_argument("--steering-strength", type=float, default=0.5,
                        help="Strength of the steering vector (0.0 to 1.0)")
    parser.add_argument("--skip-mutations", action="store_true",
                        help="Skip the mutation creation step")
    parser.add_argument("--skip-completions", action="store_true",
                        help="Skip the completions step")
    parser.add_argument("--skip-analysis", action="store_true",
                        help="Skip the analysis step")
    parser.add_argument("--skip-steering", action="store_true",
                        help="Skip the steering step")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed for reproducibility")
    args = parser.parse_args()
    
    # Create the output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Set paths for all steps
    mutated_dataset = os.path.join(args.output_dir, "mutated_dataset")
    original_results = os.path.join(args.output_dir, "original_results")
    mutated_results = os.path.join(args.output_dir, "mutated_results")
    analysis_dir = os.path.join(args.output_dir, "analysis")
    steering_dir = os.path.join(args.output_dir, "steering")
    steering_candidates = os.path.join(analysis_dir, "steering_candidates.json")
    
    # Save the pipeline configuration
    config = vars(args)
    config_path = os.path.join(args.output_dir, "pipeline_config.json")
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"Pipeline configuration saved to {config_path}")
    
    # Record start time
    start_time = time.time()
    
    # Step 1: Create mutated dataset
    if not args.skip_mutations:
        status = run_command(
            [
                "python", "create_type_inference_mutations.py",
                "--input-path", args.original_dataset,
                "--output-path", mutated_dataset,
                "--mutation-types", "vars",
                "--max-samples", str(args.max_samples),
                "--seed", str(args.seed)
            ],
            "Step 1: Creating mutated dataset"
        )
        if status != 0:
            print("Error creating mutated dataset. Exiting.")
            return status
    else:
        print("Skipping mutation creation step.")
    
    # Step 2: Run completions on both datasets
    if not args.skip_completions:
        status = run_command(
            [
                "python", "run_type_completions.py",
                "--original-path", args.original_dataset,
                "--mutated-path", mutated_dataset,
                "--original-output", original_results,
                "--mutated-output", mutated_results,
                "--model-id", args.model_id,
                "--max-samples", str(args.max_samples),
                "--seed", str(args.seed)
            ],
            "Step 2: Running completions on both datasets"
        )
        if status != 0:
            print("Error running completions. Exiting.")
            return status
    else:
        print("Skipping completions step.")
    
    # Step 3: Analyze results
    if not args.skip_analysis:
        status = run_command(
            [
                "python", "analyze_type_inference_results.py",
                "--original-results", original_results,
                "--mutated-results", mutated_results,
                "--output-dir", analysis_dir,
                "--steering-candidates", steering_candidates,
                "--max-candidates", str(args.max_samples)
            ],
            "Step 3: Analyzing results"
        )
        if status != 0:
            print("Error analyzing results. Exiting.")
            return status
    else:
        print("Skipping analysis step.")
    
    # Step 4: Run steering
    if not args.skip_steering:
        status = run_command(
            [
                "python", "run_steering_vectors.py",
                "--candidates-file", steering_candidates,
                "--model-id", args.model_id,
                "--output-dir", steering_dir,
                "--max-examples", str(args.max_samples),
                "--strength", str(args.steering_strength),
                "--seed", str(args.seed)
            ],
            "Step 4: Running steering vectors"
        )
        if status != 0:
            print("Error running steering vectors. Exiting.")
            return status
    else:
        print("Skipping steering step.")
    
    # Record end time and calculate duration
    end_time = time.time()
    duration = end_time - start_time
    
    # Generate summary report
    print(f"\n{'='*80}\nPipeline Summary\n{'='*80}")
    print(f"Total execution time: {duration:.2f} seconds ({duration/60:.2f} minutes)")
    
    # Check if all results are available and create a summary
    results_summary = {
        "pipeline_duration_seconds": duration,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "configuration": config
    }
    
    # Add accuracy results if available
    try:
        if not args.skip_completions and os.path.exists(original_results):
            with open(os.path.join(original_results, "inference_results.json"), 'r') as f:
                original_data = json.load(f)
                results_summary["original_accuracy"] = original_data.get("accuracy", "N/A")
        
        if not args.skip_completions and os.path.exists(mutated_results):
            with open(os.path.join(mutated_results, "inference_results.json"), 'r') as f:
                mutated_data = json.load(f)
                results_summary["mutated_accuracy"] = mutated_data.get("accuracy", "N/A")
        
        if not args.skip_steering and os.path.exists(steering_dir):
            steering_result_files = list(Path(steering_dir).glob("steered_results_*.json"))
            if steering_result_files:
                with open(steering_result_files[0], 'r') as f:
                    steering_data = json.load(f)
                    results_summary["steering_accuracy"] = steering_data.get("accuracy", "N/A")
    except Exception as e:
        print(f"Error gathering results: {str(e)}")
    
    # Save summary
    summary_path = os.path.join(args.output_dir, "pipeline_summary.json")
    with open(summary_path, 'w') as f:
        json.dump(results_summary, f, indent=2)
    
    print(f"\nPipeline summary saved to {summary_path}")
    
    # Print key metrics
    print("\nKey Results:")
    if "original_accuracy" in results_summary:
        print(f"Original dataset accuracy: {results_summary['original_accuracy']*100:.2f}%")
    if "mutated_accuracy" in results_summary:
        print(f"Mutated dataset accuracy: {results_summary['mutated_accuracy']*100:.2f}%")
    if "steering_accuracy" in results_summary:
        print(f"Steering accuracy: {results_summary['steering_accuracy']*100:.2f}%")
    
    print("\nPipeline completed successfully!")
    return 0

if __name__ == "__main__":
    main() 