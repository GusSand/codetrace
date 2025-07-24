#!/usr/bin/env python3
"""
Test script for comprehensive baseline experiment.
Tests with 1 model and 2 trials to verify setup before full run.
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from comprehensive_baseline_experiment import ComprehensiveSecLLMHolmesExperiment, ExperimentConfig

def test_comprehensive_experiment():
    """Test comprehensive experiment with minimal configuration."""
    print("🧪 Testing Comprehensive SecLLMHolmes Experiment")
    print("=" * 60)
    
    # Test configuration - start small
    config = ExperimentConfig(
        models=[
            "bigcode/starcoderbase-1b"  # Start with just 1 model
        ],
        num_trials=2,  # Just 2 trials for testing
        temperature=0.0,
        top_p=1.0,
        max_new_tokens=50,  # Shorter for testing
        cwe_list=["cwe-89", "cwe-79"]  # Test with just 2 CWEs
    )
    
    print(f"📋 Test Configuration:")
    print(f"   Models: {config.models}")
    print(f"   Trials: {config.num_trials}")
    print(f"   CWEs: {config.cwe_list}")
    print(f"   Max tokens: {config.max_new_tokens}")
    print()
    
    # Run test experiment
    try:
        experiment = ComprehensiveSecLLMHolmesExperiment(config)
        experiment.run_comprehensive_experiment()
        
        print("✅ Test completed successfully!")
        print(f"📁 Results saved to: {config.output_dir}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_comprehensive_experiment() 