#!/usr/bin/env python3
"""
Working Neural Steering Implementation
This bypasses the meta tensor issues and implements real steering.
"""

import torch
import logging
import gc
from typing import Dict, List, Optional
from pathlib import Path

try:
    from nnsight import LanguageModel
    NNSIGHT_AVAILABLE = True
except ImportError:
    NNSIGHT_AVAILABLE = False

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WorkingNeuralSteering:
    """
    Working neural steering implementation that actually applies vectors during generation.
    
    This uses a simpler approach to avoid meta tensor issues.
    """
    
    def __init__(self, model_name: str = "Qwen/Qwen2.5-1.5B-Instruct"):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.steering_vectors = {}
        
    def load_model(self):
        """Load model with proper configuration to avoid meta tensors."""
        logger.info(f"🚀 Loading {self.model_name} for real neural steering...")
        
        # Clear GPU memory
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            
        try:
            # Load with NNSight using minimal configuration
            self.model = LanguageModel(
                self.model_name,
                device_map=None,  # Don't use device_map
                torch_dtype=torch.float16,
                trust_remote_code=True
            )
            
            # Move to GPU manually
            if torch.cuda.is_available():
                self.model = self.model.cuda()
            
            self.tokenizer = self.model.tokenizer
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
            logger.info("✅ Model loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Model loading failed: {e}")
            return False
    
    def load_steering_vectors(self, vector_file: str) -> bool:
        """Load steering vectors from file."""
        if not Path(vector_file).exists():
            logger.error(f"❌ Vector file not found: {vector_file}")
            return False
            
        try:
            data = torch.load(vector_file, map_location='cpu', weights_only=False)
            self.steering_vectors = data['steering_vectors']
            metadata = data.get('metadata', {})
            
            logger.info(f"✅ Loaded steering vectors: {list(self.steering_vectors.keys())}")
            logger.info(f"📋 Metadata: {metadata}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to load steering vectors: {e}")
            return False
    
    def generate_with_steering(self, prompt: str, steering_strength: float = 1.0) -> str:
        """Generate text with real neural steering applied using proper NNSight hooks."""
        if not self.steering_vectors:
            raise ValueError("❌ No steering vectors loaded")
            
        logger.info("🎯 Generating with REAL neural steering...")
        
        try:
            # Tokenize
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
            if torch.cuda.is_available():
                inputs = {k: v.cuda() for k, v in inputs.items()}
            
            # Apply steering using NNSight hooks - proper approach
            with self.model.trace() as tracer:
                # Define hook function for steering
                def create_steering_hook(layer_idx, steering_vector, strength):
                    def apply_steering(hidden_states):
                        """Apply steering to hidden states."""
                        # Handle NNSight 0.4.x tuple format
                        if isinstance(hidden_states, tuple):
                            states = hidden_states[0]
                        else:
                            states = hidden_states
                        
                        # Clone to avoid in-place modification issues
                        modified_states = states.clone()
                        
                        # CRITICAL FIX: Apply steering in correct direction for vulnerability detection
                        # Vector points vulnerable→secure, but we want better vulnerability detection
                        # So we steer in the OPPOSITE direction (secure→vulnerable detection)
                        steering_vector_device = steering_vector.to(states.device)
                        modified_states[:, -1, :] -= strength * steering_vector_device  # FLIPPED SIGN!
                        
                        logger.debug(f"🎯 Applied steering to layer {layer_idx}")
                        
                        # Return in the same format as input
                        if isinstance(hidden_states, tuple):
                            return (modified_states,) + hidden_states[1:]
                        else:
                            return modified_states
                    
                    return apply_steering
                
                # Register hooks for each steering vector
                for layer_name, steering_vector in self.steering_vectors.items():
                    layer_idx = int(layer_name.split('_')[1])
                    
                    # Create and register the hook
                    hook_fn = create_steering_hook(layer_idx, steering_vector, steering_strength)
                    
                    # Register hook at the layer output
                    tracer.hooks.modify_at(
                        f"model.layers.{layer_idx}.output",
                        hook_fn
                    )
                
                # Generate with steering applied
                with tracer.invoke(inputs['input_ids']):
                    # Use the model's generate method with steering hooks active
                    outputs = self.model.generate(
                        **inputs,
                        max_new_tokens=50,
                        temperature=0.1,
                        do_sample=True,
                        top_p=0.9,
                        pad_token_id=self.tokenizer.eos_token_id
                    )
            
            # Get the generated tokens (everything after the input)
            generated_tokens = outputs[0][inputs['input_ids'].shape[1]:]
            
            # Decode result
            response = self.tokenizer.decode(generated_tokens, skip_special_tokens=True)
            logger.info(f"✅ Steered generation: '{response}'")
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Steering generation failed: {e}")
            logger.error(f"❌ Error type: {type(e).__name__}")
            import traceback
            logger.error(f"❌ Traceback: {traceback.format_exc()}")
            return f"ERROR: {str(e)}"
    
    def generate_baseline(self, prompt: str) -> str:
        """Generate without steering for comparison."""
        logger.info("📊 Generating baseline (no steering)...")
        
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
            if torch.cuda.is_available():
                inputs = {k: v.cuda() for k, v in inputs.items()}
            
            # Standard generation
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs['input_ids'],
                    max_new_tokens=50,
                    temperature=0.1,
                    do_sample=True,
                    top_p=0.9,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode
            input_length = inputs['input_ids'].shape[1]
            response = self.tokenizer.decode(outputs[0][input_length:], skip_special_tokens=True)
            
            logger.info(f"✅ Baseline generation: '{response[:100]}...'")
            return response
            
        except Exception as e:
            logger.error(f"❌ Baseline generation failed: {e}")
            return f"ERROR: {str(e)}"
    
    def compare_approaches(self, test_code: str) -> Dict[str, str]:
        """Compare baseline vs enhanced prompting vs real steering."""
        logger.info("🔬 Comparing all approaches...")
        
        # Basic prompt
        basic_prompt = f"Analyze this code for vulnerabilities:\n{test_code}\nIs it vulnerable?"
        
        # Enhanced prompt (what "breakthrough" did)
        enhanced_prompt = f"""You are a security expert specializing in vulnerability detection.
Focus on command injection, shell execution, and system call vulnerabilities.

Analyze this code with heightened security awareness:
{test_code}

Is this code vulnerable? Provide a thorough security assessment:"""
        
        results = {}
        
        # Test baseline
        try:
            results['baseline'] = self.generate_baseline(basic_prompt)
        except Exception as e:
            results['baseline'] = f"ERROR: {e}"
        
        # Test enhanced prompting
        try:
            results['enhanced_prompting'] = self.generate_baseline(enhanced_prompt)
        except Exception as e:
            results['enhanced_prompting'] = f"ERROR: {e}"
        
        # Test real steering
        try:
            results['real_steering'] = self.generate_with_steering(basic_prompt, steering_strength=1.0)
        except Exception as e:
            results['real_steering'] = f"ERROR: {e}"
        
        return results

def test_working_steering():
    """Test the working neural steering implementation."""
    logger.info("🧪 Testing Working Neural Steering Implementation")
    
    # Initialize
    steerer = WorkingNeuralSteering()
    
    # Load model
    if not steerer.load_model():
        logger.error("❌ Failed to load model")
        return
    
    # Load steering vectors
    if not steerer.load_steering_vectors("vectors/cwe-77_steering_vectors.pt"):
        logger.error("❌ Failed to load steering vectors")
        return
    
    # Test vulnerable code
    test_code = '''def execute_command(user_input):
    command = "ls " + user_input
    os.system(command)
    return "done"'''
    
    # Compare approaches
    results = steerer.compare_approaches(test_code)
    
    print("\n" + "="*80)
    print("🎯 REAL NEURAL STEERING COMPARISON RESULTS")
    print("="*80)
    
    for approach, response in results.items():
        print(f"\n📊 {approach.upper()}:")
        print(f"Response: {response[:200]}...")
        
    print("\n✅ Working neural steering test complete!")
    print("🎯 This demonstrates actual neural steering vs enhanced prompting")

if __name__ == "__main__":
    if not NNSIGHT_AVAILABLE:
        print("❌ NNSight not available")
        exit(1)
        
    test_working_steering() 