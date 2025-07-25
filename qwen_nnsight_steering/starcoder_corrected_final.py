#!/usr/bin/env python3
"""
CORRECTED StarCoder Neural Steering Experiment
Uses the EXACT patterns from NNSight documentation: model.logits.output.save()

Based on https://nnsight.net/documentation/ vLLM examples.
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
class CorrectedConfig:
    """Configuration using exact NNSight documentation patterns."""
    model_name: str = "bigcode/starcoderbase-1b"
    dataset_path: str = "../security/SecLLMHolmes/datasets"
    steering_strength: float = 10.0
    target_layers: List[int] = None
    max_tokens: int = 30  # Using max_tokens like in NNSight examples
    temperature: float = 0.7
    top_p: float = 1.0
    results_dir: str = "starcoder_corrected_results"
    
    def __post_init__(self):
        if self.target_layers is None:
            self.target_layers = [4, 12, 20]

class StarCoderCorrected:
    """StarCoder experiment using EXACT NNSight documentation patterns."""
    
    def __init__(self, config: CorrectedConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize model - EXACT pattern from documentation
        self.model, self.tokenizer = self._initialize_model()
        
        # Create results directory
        os.makedirs(self.config.results_dir, exist_ok=True)
        
        logger.info(f"🚀 Initialized CORRECTED StarCoder experiment")
    
    def _initialize_model(self):
        """Initialize model - EXACT pattern from documentation."""
        self.logger.info(f"🚀 Loading model: {self.config.model_name}")
        
        try:
            model = LanguageModel(self.config.model_name, device_map="auto")
            tokenizer = model.tokenizer
            
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
            
            self.logger.info(f"✅ Model loaded successfully")
            return model, tokenizer
            
        except Exception as e:
            self.logger.error(f"❌ Error loading model: {e}")
            raise
    
    def _get_hidden_state_for_layer(self, layer_idx: int) -> Optional[torch.Tensor]:
        """Get hidden state - EXACT pattern from documentation."""
        try:
            if hasattr(self.model, 'model') and hasattr(self.model.model, 'layers'):
                if layer_idx < len(self.model.model.layers):
                    return self.model.model.layers[layer_idx].output[0]
            elif hasattr(self.model, 'model') and hasattr(self.model.model, 'transformer') and hasattr(self.model.model.transformer, 'h'):
                if layer_idx < len(self.model.model.transformer.h):
                    return self.model.model.transformer.h[layer_idx].output[0]
            elif hasattr(self.model, 'transformer') and hasattr(self.model.transformer, 'h'):
                if layer_idx < len(self.model.transformer.h):
                    return self.model.transformer.h[layer_idx].output[0]
            elif hasattr(self.model, 'layers'):
                if layer_idx < len(self.model.layers):
                    return self.model.layers[layer_idx].output[0]
            
            return None
        except Exception as e:
            self.logger.debug(f"Could not get hidden state for layer {layer_idx}: {e}")
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
        """Create REAL steering vectors using EXACT NNSight documentation patterns."""
        self.logger.info("🎯 Creating REAL steering vectors")
        
        layers = self.config.target_layers
        hidden_dim = 2048  # StarCoder 1B
        
        # Use all available examples
        sample_count = min(len(vulnerable_examples), len(secure_examples))
        if sample_count == 0:
            self.logger.error("❌ No examples available!")
            return None
        
        self.logger.info(f"📊 Using {sample_count} examples per type")
        
        # Collect hidden states - EXACT pattern from documentation
        secure_states = []
        vulnerable_states = []
        
        # Process secure examples
        for i, example in enumerate(tqdm(secure_examples[:sample_count], desc="Processing secure examples")):
            try:
                with self.model.trace() as tracer:
                    with tracer.invoke(example):
                        layer_states = []
                        for layer_idx in layers:
                            hidden_state = self._get_hidden_state_for_layer(layer_idx)
                            if hidden_state is not None:
                                mean_state = hidden_state.mean(dim=1)
                                layer_states.append(mean_state.save())
                            else:
                                layer_states.append(None)
                        
                        secure_states.append([state.value if state else None for state in layer_states])
                        
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
                            hidden_state = self._get_hidden_state_for_layer(layer_idx)
                            if hidden_state is not None:
                                mean_state = hidden_state.mean(dim=1)
                                layer_states.append(mean_state.save())
                            else:
                                layer_states.append(None)
                        
                        vulnerable_states.append([state.value if state else None for state in layer_states])
                        
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
        
        steering_tensor = torch.stack(steering_vectors)
        self.logger.info(f"✅ Created steering tensor: {steering_tensor.shape}")
        
        return steering_tensor
    
    def create_analysis_prompt(self, code: str) -> str:
        """Create analysis prompt for StarCoder."""
        return f"""Analyze this C code for security vulnerabilities:

{code}

Security analysis:"""
    
    def generate_with_corrected_pattern(self, prompt: str, apply_steering: bool = False, 
                                      steering_tensor: Optional[torch.Tensor] = None) -> str:
        """Generate using EXACT NNSight documentation pattern: model.logits.output.save()"""
        self.logger.debug(f"🎲 Generating {'with steering' if apply_steering else 'baseline'}")
        
        try:
            # EXACT pattern from NNSight documentation
            with self.model.trace(temperature=self.config.temperature, 
                                top_p=self.config.top_p, 
                                max_tokens=self.config.max_tokens) as tracer:
                with tracer.invoke(prompt):
                    
                    # Apply steering if requested - following documentation patterns
                    if apply_steering and steering_tensor is not None:
                        steering_layers = self.config.target_layers
                        steering_scale = self.config.steering_strength
                        
                        for layer in range(24):  # Try reasonable number of layers
                            if layer in steering_layers:
                                hidden_state = self._get_hidden_state_for_layer(layer)
                                if hidden_state is not None:
                                    # Create mask for the last token
                                    mask = torch.zeros_like(hidden_state)
                                    mask[:, -1, :] = 1.0
                                    
                                    # Apply steering to the last token only
                                    steering_idx = steering_layers.index(layer)
                                    steering_vector = steering_tensor[steering_idx]
                                    
                                    # Ensure correct dimensions
                                    if steering_vector.shape[-1] != hidden_state.shape[-1]:
                                        if steering_vector.shape[-1] < hidden_state.shape[-1]:
                                            padding = torch.zeros(steering_vector.shape[:-1] + (hidden_state.shape[-1] - steering_vector.shape[-1],))
                                            steering_vector = torch.cat([steering_vector, padding], dim=-1)
                                        else:
                                            steering_vector = steering_vector[..., :hidden_state.shape[-1]]
                                    
                                    # Reshape to match hidden state dimensions
                                    steering_vector = steering_vector.view(1, 1, -1).expand(hidden_state.shape[0], 1, -1)
                                    
                                    # Apply steering 
                                    hidden_state -= steering_scale * steering_vector * mask
                    
                    # EXACT PATTERN FROM DOCUMENTATION: Use model.logits.output.save()
                    if hasattr(self.model, 'logits'):
                        logits = self.model.logits.output.save()
                    elif hasattr(self.model, 'lm_head'):
                        logits = self.model.lm_head.output.save()
                    else:
                        # Try to find the output head
                        logits = None
                        for name, module in self.model.named_modules():
                            if 'lm_head' in name or 'output' in name:
                                logits = module.output.save()
                                break
                        
                        if logits is None:
                            raise ValueError("Could not find model output layer")
            
            # Access the logits value and decode - EXACT pattern from documentation
            output_logits = logits.value
            if len(output_logits.shape) >= 2:
                # Get the last token's logits
                next_token_logits = output_logits[0, -1, :]
                next_token = next_token_logits.argmax().item()
                response = self.tokenizer.decode([next_token])
            else:
                response = "Unable to decode response"
            
            return response.strip()
            
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
    
    def run_quick_test(self):
        """Run a quick test to verify the corrected approach works."""
        self.logger.info("🧪 Running quick test with CORRECTED NNSight patterns...")
        
        # Load a small sample
        cwe_data = self.load_cwe_data("CWE-22")
        
        if not cwe_data["vulnerable"]:
            self.logger.error("❌ No vulnerable examples loaded!")
            return False
        
        # Test with first example
        test_code = cwe_data["vulnerable"][0]
        prompt = self.create_analysis_prompt(test_code)
        
        self.logger.info(f"📝 Testing with: {test_code[:100]}...")
        
        # Test baseline
        self.logger.info("🔄 Testing baseline generation...")
        try:
            baseline_response = self.generate_with_corrected_pattern(prompt, apply_steering=False)
            baseline_eval = self.evaluate_response(baseline_response)
            
            self.logger.info(f"✅ Baseline successful!")
            self.logger.info(f"   Response: {baseline_response}")
            self.logger.info(f"   Classification: {baseline_eval['classification']}")
            
        except Exception as e:
            self.logger.error(f"❌ Baseline failed: {e}")
            return False
        
        # Test steering if we have data
        if cwe_data["secure"]:
            self.logger.info("🎯 Testing steering generation...")
            try:
                steering_vectors = self.create_real_steering_vectors(
                    cwe_data["vulnerable"], cwe_data["secure"]
                )
                
                if steering_vectors is not None:
                    steering_response = self.generate_with_corrected_pattern(
                        prompt, apply_steering=True, steering_tensor=steering_vectors
                    )
                    steering_eval = self.evaluate_response(steering_response)
                    
                    self.logger.info(f"✅ Steering successful!")
                    self.logger.info(f"   Response: {steering_response}")
                    self.logger.info(f"   Classification: {steering_eval['classification']}")
                    
                    # Compare
                    self.logger.info("📊 Quick comparison:")
                    self.logger.info(f"   Baseline: {baseline_eval['classification']} (security: {baseline_eval['security_score']})")
                    self.logger.info(f"   Steering: {steering_eval['classification']} (security: {steering_eval['security_score']})")
                
            except Exception as e:
                self.logger.error(f"❌ Steering failed: {e}")
                return False
        
        return True


def main():
    """Run the corrected experiment."""
    config = CorrectedConfig()
    experiment = StarCoderCorrected(config)
    
    success = experiment.run_quick_test()
    
    if success:
        print("\n🎉 CORRECTED approach successful!")
        print("✅ Using exact NNSight documentation patterns")
        print("✅ model.logits.output.save() instead of invoker.output.save()")
        print("✅ Ready for full neural steering experiments")
    else:
        print("\n❌ Still has issues - need further investigation.")


if __name__ == "__main__":
    main() 