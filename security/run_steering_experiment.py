#!/usr/bin/env python3
"""
Run steering strength experiment with different scales and layer configurations.
This tests steering strengths of 5, 10, and 20 (much more reasonable than 100).
"""

import sys
import os
from pathlib import Path
import json
from datetime import datetime

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from security.steering_strength_experiment import ExperimentConfig, SteeringStrengthExperiment

def create_experiment_config():
    """Create experiment configuration with reasonable steering strengths."""
    
    # More reasonable steering strengths (literature typically uses 0.1-5.0)
    steering_scales = [5.0, 10.0, 20.0]  # Much more reasonable than 100.0
    
    # Layer configurations - not applying to all layers
    layer_configs = [
        [4],           # Single early layer
        [8],           # Single middle layer  
        [12],          # Single late layer
        [4, 8],        # Two layers
        [8, 12],       # Two layers (middle-late)
        [4, 8, 12],    # Three layers (distributed)
    ]
    
    config = ExperimentConfig(
        model_name="bigcode/starcoderbase-1b",  # Use the same model as our previous experiments
        steering_scales=steering_scales,
        layer_configs=layer_configs,
        max_new_tokens=30,           # Reasonable generation length
        temperature=0.7,
        max_retries=2,               # Retry on failures
        timeout_seconds=60,          # Reasonable timeout
        save_intermediate=True,      # Save progress
        debug_mode=True              # Enable tracing
    )
    
    return config

def main():
    """Run the steering strength experiment."""
    print("🚀 Starting steering strength experiment...")
    print("📊 Testing steering scales: 5.0, 10.0, 20.0")
    print("🎯 Testing layer configurations: single layers and small combinations")
    
    try:
        # Create configuration
        config = create_experiment_config()
        print(f"✅ Created experiment configuration")
        
        # Initialize experiment
        experiment = SteeringStrengthExperiment(config)
        print(f"✅ Initialized experiment with model: {config.model_name}")
        
        # Run experiment
        print("🔄 Running experiment...")
        results = experiment.run_experiment()
        
        # Analyze results
        print("📈 Analyzing results...")
        analysis = experiment.analyze_results(results)
        
        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_filename = f"steering_strength_results_{timestamp}.json"
        analysis_filename = f"steering_strength_analysis_{timestamp}.json"
        
        experiment.save_results(results, analysis, results_filename)
        
        print(f"✅ Experiment completed successfully!")
        print(f"📁 Results saved to: {results_filename}")
        print(f"📁 Analysis saved to: {analysis_filename}")
        
        # Print key findings
        print("\n🔍 Key Findings:")
        print(f"- Total experiments: {len(results.get('results', []))}")
        print(f"- Best security score: {analysis.get('best_security_score', 0):.3f}")
        print(f"- Best quality score: {analysis.get('best_quality_score', 0):.3f}")
        print(f"- Optimal steering scale: {analysis.get('optimal_steering_scale', 0)}")
        print(f"- Optimal layer config: {analysis.get('optimal_layer_config', [])}")
        
        # Recommendations
        recommendations = analysis.get('recommendations', [])
        if recommendations:
            print("\n💡 Recommendations:")
            for i, rec in enumerate(recommendations[:5], 1):  # Show top 5
                print(f"  {i}. {rec}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Experiment failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit(main()) 