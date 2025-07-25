#!/usr/bin/env python3
"""
Test script for Qwen + NNSight integration
Validates steering vector creation with sample vulnerability data
"""

import os
import sys
import torch
import logging
from pathlib import Path

# Add parent directory for imports
sys.path.append(str(Path(__file__).parent.parent))

from qwen_steering_integration import QwenNNSightSteering, QwenSteeringConfig, check_nnsight_compatibility

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Sample vulnerability data for testing
SAMPLE_VULNERABLE_EXAMPLES = [
    {
        "content": '''def process_file(filename):
    # Vulnerable: Path traversal vulnerability
    file_path = "/var/www/uploads/" + filename
    with open(file_path, 'r') as f:
        return f.read()''',
        "label": "vulnerable",
        "cwe": "CWE-22"
    },
    {
        "content": '''import os
def execute_command(user_input):
    # Vulnerable: Command injection
    command = "ls " + user_input
    os.system(command)
    return "Command executed"''',
        "label": "vulnerable", 
        "cwe": "CWE-77"
    },
    {
        "content": '''def search_users(query):
    # Vulnerable: SQL injection
    sql = "SELECT * FROM users WHERE name = '" + query + "'"
    cursor.execute(sql)
    return cursor.fetchall()''',
        "label": "vulnerable",
        "cwe": "CWE-89"
    }
]

SAMPLE_SECURE_EXAMPLES = [
    {
        "content": '''import os
def process_file(filename):
    # Secure: Proper path validation
    if not filename or '..' in filename or '/' in filename:
        raise ValueError("Invalid filename")
    file_path = os.path.join("/var/www/uploads/", filename)
    with open(file_path, 'r') as f:
        return f.read()''',
        "label": "secure",
        "cwe": "CWE-22"
    },
    {
        "content": '''import subprocess
def execute_command(user_input):
    # Secure: Using subprocess with shell=False
    allowed_commands = ['ls', 'pwd', 'date']
    if user_input not in allowed_commands:
        raise ValueError("Command not allowed")
    result = subprocess.run([user_input], capture_output=True, text=True)
    return result.stdout''',
        "label": "secure",
        "cwe": "CWE-77" 
    },
    {
        "content": '''def search_users(query):
    # Secure: Parameterized query
    sql = "SELECT * FROM users WHERE name = %s"
    cursor.execute(sql, (query,))
    return cursor.fetchall()''',
        "label": "secure",
        "cwe": "CWE-89"
    }
]

def test_compatibility():
    """Test NNSight compatibility and basic setup."""
    logger.info("🔍 Testing NNSight compatibility...")
    
    api_type = check_nnsight_compatibility()
    
    if api_type == "not_installed":
        logger.error("❌ NNSight not installed - please run: pip install nnsight")
        return False
    elif api_type == "tuple_api":
        logger.info("✅ NNSight 0.4.x detected - using tuple handling patterns")
    elif api_type == "tensor_api":
        logger.warning("⚠️ NNSight 0.2.x detected - may have compatibility issues")
    else:
        logger.warning("❓ Unknown NNSight version - proceeding with caution")
    
    return True

def test_model_loading(use_small_model: bool = False):
    """Test Qwen model loading with memory management."""
    logger.info("🚀 Testing Qwen model loading...")
    
    # Use smaller model for testing if requested
    config = QwenSteeringConfig()
    if use_small_model:
        # Switch to smaller model for testing
        config.model_name = "Qwen/Qwen2.5-1.5B-Instruct"
        config.hidden_dim = 1536  # Adjust for smaller model
        config.target_layers = [4, 8, 12, 23]  # Adjust for 24-layer model
        logger.info(f"🔧 Using smaller model for testing: {config.model_name}")
    
    try:
        steerer = QwenNNSightSteering(config)
        
        logger.info("📦 Loading model...")
        steerer.load_model()
        
        logger.info("✅ Model loaded successfully!")
        logger.info(f"📊 Model: {config.model_name}")
        logger.info(f"🎯 Target layers: {config.target_layers}")
        
        return steerer
        
    except Exception as e:
        logger.error(f"❌ Model loading failed: {e}")
        logger.info("💡 Try setting use_small_model=True for testing")
        return None

def test_steering_vector_creation(steerer: QwenNNSightSteering):
    """Test steering vector creation with sample data."""
    logger.info("🎯 Testing steering vector creation...")
    
    try:
        # Create steering vectors using sample data
        steering_vectors = steerer.create_steering_vectors(
            vulnerable_examples=SAMPLE_VULNERABLE_EXAMPLES,
            secure_examples=SAMPLE_SECURE_EXAMPLES,
            cwe_type="test-mixed"
        )
        
        if steering_vectors:
            logger.info(f"🎉 Successfully created {len(steering_vectors)} steering vectors!")
            
            # Analyze vector properties
            for layer_name, vector in steering_vectors.items():
                norm = torch.norm(vector).item()
                logger.info(f"📊 {layer_name}: shape={vector.shape}, norm={norm:.4f}")
            
            # Save test vectors
            output_path = "vectors/test_steering_vectors.pt"
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            metadata = {
                "test_type": "mixed_cwe_sample",
                "vulnerable_examples": len(SAMPLE_VULNERABLE_EXAMPLES),
                "secure_examples": len(SAMPLE_SECURE_EXAMPLES),
                "creation_timestamp": torch.cuda.Event().record() if torch.cuda.is_available() else "cpu"
            }
            
            steerer.save_steering_vectors(steering_vectors, output_path, metadata)
            
            return True
        else:
            logger.error("❌ No steering vectors created")
            return False
            
    except Exception as e:
        logger.error(f"❌ Steering vector creation failed: {e}")
        return False

def test_vector_loading():
    """Test loading saved steering vectors."""
    logger.info("📂 Testing steering vector loading...")
    
    try:
        config = QwenSteeringConfig()
        steerer = QwenNNSightSteering(config)
        
        vectors, metadata = steerer.load_steering_vectors("vectors/test_steering_vectors.pt")
        
        logger.info(f"✅ Loaded {len(vectors)} steering vectors")
        logger.info(f"📋 Metadata: {metadata}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Vector loading failed: {e}")
        return False

def run_comprehensive_test(use_small_model: bool = False):
    """Run comprehensive test suite."""
    logger.info("🧪 Starting comprehensive Qwen + NNSight integration test...")
    
    tests = [
        ("Compatibility Check", test_compatibility),
        ("Model Loading", lambda: test_model_loading(use_small_model)),
        ("Steering Vector Creation", test_steering_vector_creation), 
        ("Vector Loading", test_vector_loading)
    ]
    
    results = {}
    steerer = None
    
    for test_name, test_func in tests:
        logger.info(f"\n{'='*50}")
        logger.info(f"🔬 Running: {test_name}")
        logger.info(f"{'='*50}")
        
        try:
            if test_name == "Model Loading":
                result = test_func()
                if result:
                    steerer = result
                    results[test_name] = True
                else:
                    results[test_name] = False
            elif test_name == "Steering Vector Creation" and steerer:
                results[test_name] = test_func(steerer)
            elif test_name in ["Compatibility Check", "Vector Loading"]:
                results[test_name] = test_func()
            else:
                if test_name == "Steering Vector Creation" and not steerer:
                    logger.warning("⚠️ Skipping steering vector creation - model not loaded")
                    results[test_name] = False
                else:
                    results[test_name] = test_func()
                    
        except Exception as e:
            logger.error(f"❌ Test {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    logger.info(f"\n{'='*50}")
    logger.info("📊 TEST SUMMARY")
    logger.info(f"{'='*50}")
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status} {test_name}")
    
    logger.info(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Qwen + NNSight integration is working correctly.")
    else:
        logger.warning("⚠️ Some tests failed. Check logs above for details.")
    
    return results

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Qwen + NNSight integration")
    parser.add_argument("--small-model", action="store_true", 
                       help="Use smaller Qwen model for testing (less GPU memory)")
    parser.add_argument("--test", choices=["compatibility", "loading", "vectors", "all"],
                       default="all", help="Which test to run")
    
    args = parser.parse_args()
    
    if args.test == "all":
        run_comprehensive_test(use_small_model=args.small_model)
    elif args.test == "compatibility":
        test_compatibility()
    elif args.test == "loading":
        test_model_loading(use_small_model=args.small_model)
    elif args.test == "vectors":
        steerer = test_model_loading(use_small_model=args.small_model)
        if steerer:
            test_steering_vector_creation(steerer)
    
    logger.info("🏁 Test execution completed.") 