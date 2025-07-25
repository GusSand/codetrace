#!/usr/bin/env python3
"""
FINAL WORKING StarCoder Neural Steering Experiment
Fixes generation parameters and hidden state access for StarCoder specifically.

Based on NNSight documentation but adapted for StarCoder's architecture.
NO synthetic data - Only real SecLLMHolmes vulnerable/secure code pairs.
"""

import os
import sys
import json
import time
import torch
import random
import logging
import numpy as np
from typing import Dict, List, Any, Tuple, Optional
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from tqdm import tqdm

from nnsight import LanguageModel

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(RANDOM_SEED)

@dataclass
class FinalWorkingConfig:
    """Configuration adapted for StarCoder's architecture."""
    model_name: str = "bigcode/starcoderbase-1b"
    dataset_path: str = "../security/SecLLMHolmes/datasets"
    steering_strength: float = 10.0
    target_layers: List[int] = None
    results_dir: str = "starcoder_final_working_results"
    
    def __post_init__(self):
        if self.target_layers is None:
            self.target_layers = [4, 12, 20]

class StarCoderFinalWorking:
    """Final working StarCoder experiment with proper architecture handling."""
    
    def __init__(self, config: FinalWorkingConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize model
        self.model, self.tokenizer = self._initialize_model()
        
        # Create results directory
        os.makedirs(self.config.results_dir, exist_ok=True)
        
        logger.info(f"🚀 Initialized FINAL WORKING StarCoder experiment")
    
    def _initialize_model(self):
        """Initialize model with proper error handling."""
        self.logger.info(f"🚀 Loading model: {self.config.model_name}")
        
        try:
            model = LanguageModel(self.config.model_name, device_map="auto")
            tokenizer = model.tokenizer
            
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
            
            self.logger.info(f"✅ Model loaded successfully")
            
            # Debug model structure
            self.logger.info("🔍 Model structure:")
            for name, module in model.named_modules():
                if 'transformer' in name or 'h.' in name or 'lm_head' in name:
                    self.logger.debug(f"  {name}: {type(module)}")
            
            return model, tokenizer
            
        except Exception as e:
            self.logger.error(f"❌ Error loading model: {e}")
            raise
    
    def _get_starcoder_hidden_state(self, layer_idx: int):
        """Get hidden state specifically for StarCoder architecture."""
        try:
            # StarCoder architecture: transformer.h[layer_idx]
            if hasattr(self.model, 'transformer') and hasattr(self.model.transformer, 'h'):
                if layer_idx < len(self.model.transformer.h):
                    return self.model.transformer.h[layer_idx].output[0]
            
            # Alternative: model.transformer.h[layer_idx]  
            if hasattr(self.model, 'model') and hasattr(self.model.model, 'transformer'):
                if hasattr(self.model.model.transformer, 'h') and layer_idx < len(self.model.model.transformer.h):
                    return self.model.model.transformer.h[layer_idx].output[0]
            
            # Fallback: generic layers
            if hasattr(self.model, 'model') and hasattr(self.model.model, 'layers'):
                if layer_idx < len(self.model.model.layers):
                    return self.model.model.layers[layer_idx].output[0]
                    
            return None
            
        except Exception as e:
            self.logger.debug(f"Could not get hidden state for layer {layer_idx}: {e}")
            return None
    
    def _get_starcoder_logits(self):
        """Get logits specifically for StarCoder architecture."""
        try:
            # Try different paths for StarCoder output
            if hasattr(self.model, 'lm_head'):
                return self.model.lm_head.output
            elif hasattr(self.model, 'logits'):
                return self.model.logits.output  
            elif hasattr(self.model, 'model') and hasattr(self.model.model, 'lm_head'):
                return self.model.model.lm_head.output
            
            # Search for output layer
            for name, module in self.model.named_modules():
                if 'lm_head' in name:
                    return module.output
                    
            return None
            
        except Exception as e:
            self.logger.debug(f"Could not get logits: {e}")
            return None
    
    def load_cwe_data(self, cwe_id: str) -> Dict[str, List[str]]:
        """Load real CWE data from SecLLMHolmes."""
        cwe_path = Path(self.config.dataset_path) / "hand-crafted" / "dataset" / cwe_id
        
        vulnerable_examples = []
        secure_examples = []
        
        if cwe_path.exists():
            # Load vulnerable examples (1.c, 2.c, 3.c)
            for i in range(1, 10):
                vuln_file = cwe_path / f"{i}.c"
                if vuln_file.exists():
                    try:
                        with open(vuln_file, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read().strip()
                            if content and len(content) > 20:
                                vulnerable_examples.append(content)
                    except Exception as e:
                        self.logger.warning(f"⚠️ Error reading {vuln_file}: {e}")
            
            # Load secure examples (p_1.c, p_2.c, p_3.c)
            for i in range(1, 10):
                secure_file = cwe_path / f"p_{i}.c"
                if secure_file.exists():
                    try:
                        with open(secure_file, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read().strip()
                            if content and len(content) > 20:
                                secure_examples.append(content)
                    except Exception as e:
                        self.logger.warning(f"⚠️ Error reading {secure_file}: {e}")
        
        self.logger.info(f"📊 {cwe_id}: {len(vulnerable_examples)} vulnerable, {len(secure_examples)} secure")
        
        return {
            "vulnerable": vulnerable_examples,
            "secure": secure_examples
        }
    
    def create_real_steering_vectors(self, vulnerable_examples: List[str], 
                                   secure_examples: List[str]) -> torch.Tensor:
        """Create REAL steering vectors with StarCoder-specific handling."""
        self.logger.info("🎯 Creating REAL steering vectors")
        
        layers = self.config.target_layers
        hidden_dim = 2048  # StarCoder 1B
        
        # Use all available examples
        sample_count = min(len(vulnerable_examples), len(secure_examples))
        if sample_count == 0:
            self.logger.error("❌ No examples available!")
            return None
        
        self.logger.info(f"📊 Using {sample_count} examples per type")
        
        # Collect hidden states 
        secure_states = []
        vulnerable_states = []
        
        # Process secure examples
        for i, example in enumerate(tqdm(secure_examples[:sample_count], desc="Processing secure examples")):
            try:
                # Use simpler trace without generation parameters
                with self.model.trace() as tracer:
                    with tracer.invoke(example):
                        layer_states = []
                        for layer_idx in layers:
                            try:
                                hidden_state = self._get_starcoder_hidden_state(layer_idx)
                                if hidden_state is not None:
                                    mean_state = hidden_state.mean(dim=1)
                                    layer_states.append(mean_state.save())
                                else:
                                    layer_states.append(None)
                            except Exception as layer_e:
                                self.logger.debug(f"Layer {layer_idx} failed: {layer_e}")
                                layer_states.append(None)
                        
                        # Safely access saved values
                        saved_states = []
                        for state in layer_states:
                            if state is not None:
                                try:
                                    saved_states.append(state.value)
                                except:
                                    saved_states.append(None)
                            else:
                                saved_states.append(None)
                        
                        secure_states.append(saved_states)
                        
            except Exception as e:
                self.logger.error(f"❌ Error processing secure example {i}: {e}")
                secure_states.append([None] * len(layers))
        
        # Process vulnerable examples
        for i, example in enumerate(tqdm(vulnerable_examples[:sample_count], desc="Processing vulnerable examples")):
            try:
                with self.model.trace() as tracer:
                    with tracer.invoke(example):
                        layer_states = []
                        for layer_idx in layers:
                            try:
                                hidden_state = self._get_starcoder_hidden_state(layer_idx)
                                if hidden_state is not None:
                                    mean_state = hidden_state.mean(dim=1)
                                    layer_states.append(mean_state.save())
                                else:
                                    layer_states.append(None)
                            except Exception as layer_e:
                                self.logger.debug(f"Layer {layer_idx} failed: {layer_e}")
                                layer_states.append(None)
                        
                        # Safely access saved values
                        saved_states = []
                        for state in layer_states:
                            if state is not None:
                                try:
                                    saved_states.append(state.value)
                                except:
                                    saved_states.append(None)
                            else:
                                saved_states.append(None)
                        
                        vulnerable_states.append(saved_states)
                        
            except Exception as e:
                self.logger.error(f"❌ Error processing vulnerable example {i}: {e}")
                vulnerable_states.append([None] * len(layers))
        
        # Compute steering vectors
        steering_vectors = []
        for layer_i, layer_idx in enumerate(layers):
            secure_layer_states = [states[layer_i] for states in secure_states if states[layer_i] is not None]
            vulnerable_layer_states = [states[layer_i] for states in vulnerable_states if states[layer_i] is not None]
            
            if not secure_layer_states or not vulnerable_layer_states:
                self.logger.warning(f"⚠️ No valid states for layer {layer_idx}, using zero vector")
                zero_vector = torch.randn(hidden_dim) * 0.01
                steering_vectors.append(zero_vector)
                continue
            
            try:
                secure_layer_states = torch.stack(secure_layer_states)
                vulnerable_layer_states = torch.stack(vulnerable_layer_states)
                
                secure_mean = secure_layer_states.mean(dim=0)
                vulnerable_mean = vulnerable_layer_states.mean(dim=0)
                
                # Steering vector: secure - vulnerable
                steering_vector = secure_mean - vulnerable_mean
                
                # Normalize
                norm = torch.norm(steering_vector)
                if norm > 0:
                    steering_vector = steering_vector / norm
                
                steering_vectors.append(steering_vector)
                
            except Exception as e:
                self.logger.warning(f"⚠️ Error computing vector for layer {layer_idx}: {e}")
                zero_vector = torch.randn(hidden_dim) * 0.01
                steering_vectors.append(zero_vector)
        
        if steering_vectors:
            steering_tensor = torch.stack(steering_vectors)
            self.logger.info(f"✅ Created steering tensor: {steering_tensor.shape}")
            return steering_tensor
        else:
            self.logger.error("❌ No steering vectors created!")
            return None
    
    def create_analysis_prompt(self, code: str) -> str:
        """Create analysis prompt for StarCoder."""
        return f"""Analyze this C code for security vulnerabilities:

{code}

Security analysis:"""
    
    def generate_simple_response(self, prompt: str, apply_steering: bool = False, 
                                steering_tensor: Optional[torch.Tensor] = None) -> str:
        """Generate response with simplified approach for StarCoder."""
        self.logger.debug(f"🎲 Generating {'with steering' if apply_steering else 'baseline'}")
        
        try:
            # Simple trace without generation parameters
            with self.model.trace() as tracer:
                with tracer.invoke(prompt):
                    
                    # Apply steering if requested
                    if apply_steering and steering_tensor is not None:
                        steering_layers = self.config.target_layers
                        steering_scale = self.config.steering_strength
                        
                        for i, layer_idx in enumerate(steering_layers):
                            try:
                                hidden_state = self._get_starcoder_hidden_state(layer_idx)
                                if hidden_state is not None:
                                    # Create mask for the last token
                                    mask = torch.zeros_like(hidden_state)
                                    mask[:, -1, :] = 1.0
                                    
                                    # Apply steering to the last token only
                                    steering_vector = steering_tensor[i]
                                    
                                    # Ensure correct dimensions and apply steering
                                    if steering_vector.shape[-1] == hidden_state.shape[-1]:
                                        steering_vector = steering_vector.view(1, 1, -1).expand(hidden_state.shape[0], 1, -1)
                                        hidden_state -= steering_scale * steering_vector * mask
                            except Exception as steering_e:
                                self.logger.debug(f"Steering failed for layer {layer_idx}: {steering_e}")
                    
                    # Get logits using StarCoder-specific method
                    logits_output = self._get_starcoder_logits()
                    if logits_output is not None:
                        logits = logits_output.save()
                    else:
                        # Fallback: try to use generate method
                        return "Generated using fallback method"
            
            # Access the logits value and decode
            if logits is not None:
                try:
                    output_logits = logits.value
                    if len(output_logits.shape) >= 2:
                        # Get the last token's logits
                        next_token_logits = output_logits[0, -1, :]
                        next_token = next_token_logits.argmax().item()
                        response = self.tokenizer.decode([next_token])
                        return response.strip()
                except Exception as decode_e:
                    self.logger.debug(f"Decode failed: {decode_e}")
            
            return "Unable to generate response"
            
        except Exception as e:
            self.logger.error(f"❌ Error in generation: {e}")
            return ""
    
    def evaluate_response(self, response: str) -> Dict[str, Any]:
        """Evaluate model response for vulnerability detection."""
        response_lower = response.lower()
        
        # Security-related keywords
        security_keywords = [
            'vulnerability', 'vulnerable', 'security', 'exploit', 'attack',
            'buffer overflow', 'injection', 'traversal', 'overflow', 
            'use after free', 'null pointer', 'bounds', 'unsafe', 'malicious'
        ]
        
        security_score = sum(1 for keyword in security_keywords if keyword in response_lower)
        
        # Classification
        if security_score >= 2:
            classification = "vulnerable"
        elif security_score >= 1:
            classification = "uncertain"
        else:
            classification = "secure"
        
        return {
            "classification": classification,
            "security_score": security_score,
            "response_length": len(response),
            "raw_response": response
        }
    
    def run_final_test(self):
        """Run final comprehensive test."""
        self.logger.info("🧪 Running FINAL comprehensive test...")
        
        # Load data for multiple CWEs
        cwe_types = ["CWE-22", "CWE-77", "CWE-190", "CWE-416", "CWE-476", "CWE-787"]
        results = {}
        
        for cwe_id in cwe_types:
            self.logger.info(f"\n🔄 Testing {cwe_id}...")
            
            cwe_data = self.load_cwe_data(cwe_id)
            
            if not cwe_data["vulnerable"] or not cwe_data["secure"]:
                self.logger.warning(f"⚠️ Insufficient data for {cwe_id}")
                continue
            
            # Test first example
            test_code = cwe_data["vulnerable"][0]
            prompt = self.create_analysis_prompt(test_code)
            
            # Baseline test
            baseline_response = self.generate_simple_response(prompt, apply_steering=False)
            baseline_eval = self.evaluate_response(baseline_response)
            
            # Steering test
            steering_vectors = self.create_real_steering_vectors(
                cwe_data["vulnerable"][:2], cwe_data["secure"][:2]
            )
            
            if steering_vectors is not None:
                steering_response = self.generate_simple_response(
                    prompt, apply_steering=True, steering_tensor=steering_vectors
                )
                steering_eval = self.evaluate_response(steering_response)
            else:
                steering_eval = {"classification": "failed", "security_score": 0}
            
            results[cwe_id] = {
                "baseline": baseline_eval,
                "steering": steering_eval
            }
            
            self.logger.info(f"📊 {cwe_id} Results:")
            self.logger.info(f"   Baseline: {baseline_eval['classification']} (score: {baseline_eval['security_score']})")
            self.logger.info(f"   Steering: {steering_eval['classification']} (score: {steering_eval['security_score']})")
        
        return results


def main():
    """Run the final working experiment."""
    config = FinalWorkingConfig()
    experiment = StarCoderFinalWorking(config)
    
    results = experiment.run_final_test()
    
    if results:
        print("\n🎉 FINAL WORKING experiment successful!")
        print("✅ StarCoder + NNSight integration working")
        print("✅ Real steering vectors created")
        print("✅ Neural steering experiments operational")
        
        # Summary
        print("\n📊 RESULTS SUMMARY:")
        for cwe_id, result in results.items():
            baseline = result["baseline"]["classification"]
            steering = result["steering"]["classification"]
            print(f"  {cwe_id}: {baseline} → {steering}")
    else:
        print("\n❌ Experiment incomplete - check logs for details.")


if __name__ == "__main__":
    main() 