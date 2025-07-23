#!/usr/bin/env python3
"""
Simple test script to verify the steering experiment setup works correctly.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from security.steering_strength_experiment import ExperimentConfig, SteeringStrengthExperiment

def test_experiment_setup():
    """Test that the experiment can be initialized correctly."""
    print("🚀 Starting steering experiment tests...")
    
    # Create a minimal config for testing
    config = ExperimentConfig(
        model_name="bigcode/starcoderbase-1b",  # Use the same model as our previous experiments
        steering_scales=[1.0, 2.0],  # Just 2 scales for testing
        layer_configs=[[4], [6]],    # Just 2 layer configs for testing
        max_new_tokens=10,           # Small for testing
        temperature=0.7,
        max_retries=1,
        timeout_seconds=30,
        save_intermediate=False,
        debug_mode=True
    )
    
    print("✅ Testing experiment setup...")
    try:
        experiment = SteeringStrengthExperiment(config)
        print("✅ Experiment setup successful!")
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_logging():
    """Test that logging works correctly."""
    print("✅ Testing logging setup...")
    try:
        from security.steering_strength_experiment import TracingLogger
        from pathlib import Path
        
        # Create logs directory
        log_dir = Path("security/logs")
        log_dir.mkdir(exist_ok=True)
        
        logger = TracingLogger(
            str(log_dir / "test_log.log"),
            debug_mode=True
        )
        
        logger.logger.info("Test log message")
        print("✅ Logging test successful!")
        return True
    except Exception as e:
        print(f"❌ Logging test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🧪 Running steering experiment tests...")
    
    tests = [
        ("Logging Setup", test_logging),
        ("Experiment Setup", test_experiment_setup),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if test_func():
            passed += 1
            print(f"✅ {test_name} passed")
        else:
            print(f"❌ {test_name} failed")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The experiment setup is working correctly.")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()