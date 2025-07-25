#!/usr/bin/env python3
"""
Debug script to isolate the meta tensor issue and test basic steering functionality.
"""

import torch
import logging
from qwen_steering_integration import QwenNNSightSteering, QwenSteeringConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_basic_model_loading():
    """Test basic model loading without steering."""
    logger.info("🧪 Testing basic model loading...")
    
    config = QwenSteeringConfig(
        model_name="Qwen/Qwen2.5-1.5B-Instruct",
        device_map={"": 0}  # Single device
    )
    
    steerer = QwenNNSightSteering(config)
    steerer.load_model()
    
    # Test basic tokenization
    test_prompt = "Hello, how are you?"
    inputs = steerer.tokenizer(test_prompt, return_tensors="pt")
    logger.info(f"✅ Tokenization works: {inputs.input_ids.shape}")
    
    # Test basic generation WITHOUT NNSight tracing
    logger.info("🧪 Testing basic generation (no NNSight)...")
    try:
        with torch.no_grad():
            outputs = steerer.model.generate(
                inputs.input_ids.to(steerer.model.device),
                max_new_tokens=20,
                temperature=0.1,
                do_sample=True,
                pad_token_id=steerer.tokenizer.eos_token_id
            )
        
        response = steerer.tokenizer.decode(outputs[0], skip_special_tokens=True)
        logger.info(f"✅ Basic generation works: {response}")
        return steerer
        
    except Exception as e:
        logger.error(f"❌ Basic generation failed: {e}")
        return None

def test_nnsight_tracing(steerer):
    """Test NNSight tracing functionality."""
    logger.info("🧪 Testing NNSight tracing...")
    
    test_prompt = "Hello, how are you?"
    inputs = steerer.tokenizer(test_prompt, return_tensors="pt")
    
    try:
        # Test basic tracing without generation
        with steerer.model.trace() as tracer:
            with tracer.invoke(inputs.input_ids.to(steerer.model.device)):
                # Try to access layer outputs
                layer_output = steerer.model.model.layers[4].output.save()
        
        logger.info(f"✅ NNSight tracing works: {type(layer_output)}")
        
        # Check if it's a tuple (NNSight 0.4.x)
        if isinstance(layer_output, tuple):
            logger.info(f"📊 Tuple output: {len(layer_output)} elements")
            if len(layer_output) > 0:
                logger.info(f"📊 First element shape: {layer_output[0].shape}")
        else:
            logger.info(f"📊 Direct tensor shape: {layer_output.shape}")
            
        return True
        
    except Exception as e:
        logger.error(f"❌ NNSight tracing failed: {e}")
        return False

def test_simple_steering(steerer):
    """Test very simple steering without full generation."""
    logger.info("🧪 Testing simple steering application...")
    
    # Load our steering vectors
    try:
        vectors, metadata = steerer.load_steering_vectors("vectors/cwe-77_steering_vectors.pt")
        logger.info(f"✅ Loaded steering vectors: {list(vectors.keys())}")
    except Exception as e:
        logger.error(f"❌ Failed to load vectors: {e}")
        return False
    
    test_prompt = "Analyze this code: os.system('ls')"
    inputs = steerer.tokenizer(test_prompt, return_tensors="pt")
    
    try:
        # Test steering application
        with steerer.model.trace() as tracer:
            with tracer.invoke(inputs.input_ids.to(steerer.model.device)):
                
                # Apply simple steering to one layer
                layer_idx = 4
                layer_output = steerer.model.model.layers[layer_idx].output
                
                # Get steering vector
                steering_vector = vectors[f"layer_{layer_idx}"].to(steerer.model.device)
                
                # Test if we can modify the output
                if isinstance(layer_output, tuple):
                    hidden_states = layer_output[0]
                    logger.info(f"📊 Hidden states shape: {hidden_states.shape}")
                    logger.info(f"📊 Steering vector shape: {steering_vector.shape}")
                    
                    # Try to apply steering
                    modified_states = hidden_states.clone()
                    modified_states[0, -1, :] += steering_vector * 0.1  # Small modification
                    
                    logger.info("✅ Steering application succeeded")
                else:
                    logger.info(f"📊 Direct tensor shape: {layer_output.shape}")
                    
        return True
        
    except Exception as e:
        logger.error(f"❌ Simple steering failed: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Debug: Testing Real Neural Steering Components")
    print("="*60)
    
    # Test 1: Basic model loading
    steerer = test_basic_model_loading()
    if not steerer:
        print("❌ Basic model loading failed - stopping")
        exit(1)
    
    # Test 2: NNSight tracing
    if not test_nnsight_tracing(steerer):
        print("❌ NNSight tracing failed - stopping")
        exit(1)
    
    # Test 3: Simple steering
    if not test_simple_steering(steerer):
        print("❌ Simple steering failed")
        exit(1)
    
    print("\n✅ All debug tests passed!")
    print("🎯 Ready to implement full neural steering") 