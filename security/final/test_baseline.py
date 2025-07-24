#!/usr/bin/env python3
"""
Quick test script for the SecLLMHolmes baseline to verify setup before running full experiment.
"""

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from baseline import BaselineConfig, SecLLMHolmesBaselineAdapter

def test_baseline_setup():
    """Test that baseline setup works correctly."""
    print("🧪 Testing SecLLMHolmes Baseline Setup")
    print("=" * 50)
    
    # Create test config with minimal settings
    config = BaselineConfig(
        model_name="bigcode/starcoderbase-1b",
        temperature=0.0,
        max_new_tokens=50,  # Shorter for testing
        num_trials=1,
        cwe_list=["cwe-89"]  # Just test SQL injection
    )
    
    print(f"✅ Config created: {config.model_name}")
    
    try:
        # Test adapter creation
        adapter = SecLLMHolmesBaselineAdapter(config)
        print("✅ Adapter created successfully")
        
        # Test model loading
        print("🔄 Loading model (this may take a moment)...")
        adapter.load_model()
        print("✅ Model loaded successfully")
        
        # Test dataset loading
        print("🔄 Loading SecLLMHolmes dataset...")
        dataset = adapter.load_secllmholmes_data()
        
        if dataset:
            total_examples = sum(len(examples) for examples in dataset.values())
            print(f"✅ Dataset loaded: {total_examples} examples across {len(dataset)} CWEs")
            
            # Show first example for each CWE
            for cwe, examples in dataset.items():
                if examples:
                    example = examples[0]
                    print(f"  📋 {cwe}: {len(examples)} examples")
                    print(f"    First example: {example['file_name']} ({example['language']})")
                    
            # Test a quick generation
            if dataset:
                cwe, examples = next(iter(dataset.items()))
                example = examples[0]
                
                print(f"\n🧪 Testing generation with first {cwe} example:")
                prompt = adapter.prepare_prompt(example, prompt_type="Question")
                print(f"📝 Prompt: {prompt[:200]}...")
                
                response = adapter.generate_response(prompt)
                print(f"🤖 Response: {response[:200]}...")
                
                answer, reason = adapter.parse_structured_output(response, example["cwe_name"])
                print(f"📊 Parsed Answer: {answer}")
                print(f"📊 Parsed Reason: {reason[:100]}...")
                
                accuracy = adapter.evaluate_accuracy(answer, example)
                print(f"📊 Accuracy: {accuracy}")
                
        else:
            print("❌ No dataset loaded - check SecLLMHolmes path")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n🎉 Baseline test completed successfully!")
    print("✅ Ready to run full experiment with: python baseline.py")
    return True

if __name__ == "__main__":
    success = test_baseline_setup()
    if not success:
        sys.exit(1) 