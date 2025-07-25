#!/usr/bin/env python3
"""
Qwen Model + NNSight Integration for Steering Vector Creation
Based on breakthrough research patterns with NNSight 0.4.x compatibility

Status: PROVEN WORKING patterns adapted for dedicated Qwen integration
Reference: neural_steering_breakthrough_context_20250724_234500.md
"""

import os
import sys
import torch
import gc
import logging
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path
from dataclasses import dataclass
import json

try:
    from nnsight import LanguageModel
    NNSIGHT_AVAILABLE = True
except ImportError:
    NNSIGHT_AVAILABLE = False
    print("❌ NNSight not available - install with: pip install nnsight")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass 
class QwenSteeringConfig:
    """Configuration for Qwen steering vector creation."""
    # Model settings
    model_name: str = "Qwen/Qwen2.5-14B-Instruct"
    model_dtype: torch.dtype = torch.float16
    device_map: str = "auto"
    
    # Steering parameters
    steering_strength: float = 20.0
    normalization: bool = True
    examples_per_type: int = 3
    
    # Layer settings (proven effective for Qwen2.5-14B)
    target_layers: List[int] = None
    hidden_dim: int = 5120
    total_layers: int = 48
    
    # Memory management
    use_memory_optimization: bool = True
    clear_cache_after_batch: bool = True
    
    def __post_init__(self):
        if self.target_layers is None:
            # Proven effective layers for 48-layer Qwen2.5-14B
            self.target_layers = [12, 24, 36, 47]

class QwenNNSightSteering:
    """
    Qwen model steering vector creation using NNSight 0.4.x compatible patterns.
    
    Implements proven methodology:
    - NNSight 0.4.x tuple output handling
    - CWE-specific steering vectors  
    - Memory-optimized loading for large models
    - Semantic direction: vulnerable -> secure
    """
    
    def __init__(self, config: QwenSteeringConfig):
        self.config = config
        self.model = None
        self.tokenizer = None
        
        if not NNSIGHT_AVAILABLE:
            raise ImportError("❌ NNSight not available - cannot create steering vectors")
    
    def load_model(self):
        """Load Qwen model with NNSight wrapper and memory optimizations."""
        if self.model is not None:
            logger.warning("⚠️ Model already loaded")
            return
            
        logger.info(f"🚀 Loading Qwen model: {self.config.model_name}")
        
        if self.config.use_memory_optimization:
            self._clear_gpu_memory()
        
        try:
            # Load with NNSight wrapper - proven working configuration
            self.model = LanguageModel(
                self.config.model_name,
                device_map=self.config.device_map,
                torch_dtype=self.config.model_dtype,
                use_flash_attention_2=False,  # Compatibility for Qwen
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )
            
            self.tokenizer = self.model.tokenizer
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            logger.info(f"✅ Qwen model loaded successfully")
            logger.info(f"📊 Model layers: {len(self.model.model.layers)}")
            logger.info(f"🎯 Target layers: {self.config.target_layers}")
            
            self._log_memory_usage()
            
        except Exception as e:
            logger.error(f"❌ Failed to load Qwen model: {e}")
            raise
    
    def create_steering_vectors(self, vulnerable_examples: List[Dict], secure_examples: List[Dict], 
                              cwe_type: str = "generic") -> Dict[str, torch.Tensor]:
        """
        Create CWE-specific steering vectors using proven NNSight 0.4.x patterns.
        
        Args:
            vulnerable_examples: List of vulnerable code examples
            secure_examples: List of secure code examples  
            cwe_type: CWE identifier for logging/saving
            
        Returns:
            Dictionary mapping layer names to steering vectors
        """
        if self.model is None:
            raise ValueError("❌ Model not loaded - call load_model() first")
            
        logger.info(f"🎯 Creating steering vectors for {cwe_type}")
        logger.info(f"📊 Data: {len(vulnerable_examples)} vulnerable, {len(secure_examples)} secure examples")
        
        steering_vectors = {}
        
        for layer_idx in self.config.target_layers:
            logger.info(f"🔄 Processing layer {layer_idx}...")
            
            try:
                # Extract activations for vulnerable examples
                vulnerable_activations = self._extract_activations(
                    vulnerable_examples[:self.config.examples_per_type], 
                    layer_idx, 
                    "vulnerable"
                )
                
                # Extract activations for secure examples
                secure_activations = self._extract_activations(
                    secure_examples[:self.config.examples_per_type],
                    layer_idx,
                    "secure"
                )
                
                # Create steering vector if sufficient activations
                if len(vulnerable_activations) > 0 and len(secure_activations) > 0:
                    steering_vector = self._compute_steering_vector(
                        vulnerable_activations, secure_activations
                    )
                    
                    if steering_vector is not None:
                        steering_vectors[f"layer_{layer_idx}"] = steering_vector
                        
                        # Log vector statistics
                        norm = torch.norm(steering_vector).item()
                        logger.info(f"✅ Layer {layer_idx}: Shape {steering_vector.shape}, norm {norm:.4f}")
                    else:
                        logger.warning(f"⚠️ Failed to create steering vector for layer {layer_idx}")
                else:
                    logger.warning(f"⚠️ Insufficient activations for layer {layer_idx}")
                    
                # Memory cleanup after each layer
                if self.config.clear_cache_after_batch:
                    self._clear_gpu_memory()
                    
            except Exception as e:
                logger.error(f"❌ Error processing layer {layer_idx}: {e}")
        
        logger.info(f"🎉 Created {len(steering_vectors)} steering vectors for {cwe_type}")
        return steering_vectors
    
    def _extract_activations(self, examples: List[Dict], layer_idx: int, 
                           example_type: str) -> List[torch.Tensor]:
        """
        Extract hidden state activations using NNSight 0.4.x compatible patterns.
        
        CRITICAL: Handles tuple outputs from layer.output.save()
        """
        activations = []
        
        for i, example in enumerate(examples):
            try:
                prompt = self._create_vulnerability_prompt(example['content'])
                
                with self.model.trace() as tracer:
                    with tracer.invoke(prompt):
                        # Qwen-specific layer access pattern
                        layer_output = self.model.model.layers[layer_idx].output.save()
                
                # 🔧 CRITICAL: NNSight 0.4.x tuple handling
                if layer_output is not None:
                    activation = None
                    
                    if isinstance(layer_output, tuple) and len(layer_output) > 0:
                        # Extract hidden states (first element of tuple)
                        hidden_states = layer_output[0]
                        if len(hidden_states.shape) >= 3:  # [batch, seq_len, hidden_dim]
                            # Take last token activation
                            activation = hidden_states[0, -1, :].detach().cpu()
                        
                    # Fallback for direct tensor case
                    elif hasattr(layer_output, 'shape') and len(layer_output.shape) >= 3:
                        activation = layer_output[0, -1, :].detach().cpu()
                    
                    if activation is not None:
                        # Validate activation shape
                        if activation.shape[0] == self.config.hidden_dim:
                            activations.append(activation)
                            logger.debug(f"✅ Got {example_type} activation {i+1}: {activation.shape}")
                        else:
                            logger.warning(f"⚠️ Invalid activation shape: {activation.shape}")
                    else:
                        logger.warning(f"⚠️ Could not extract activation from layer {layer_idx}")
                        
            except Exception as e:
                logger.error(f"❌ Error extracting activation {i+1}: {e}")
        
        logger.info(f"📊 Extracted {len(activations)} {example_type} activations from layer {layer_idx}")
        return activations
    
    def _compute_steering_vector(self, vulnerable_activations: List[torch.Tensor], 
                               secure_activations: List[torch.Tensor]) -> Optional[torch.Tensor]:
        """
        Compute steering vector using proven methodology.
        
        Direction: vulnerable -> secure (toward security)
        """
        try:
            vulnerable_mean = torch.stack(vulnerable_activations).mean(dim=0)
            secure_mean = torch.stack(secure_activations).mean(dim=0)
            
            # Steering direction: From vulnerable toward secure
            steering_vector = (secure_mean - vulnerable_mean).detach()
            
            # Normalize for consistent application (proven effective)
            if self.config.normalization:
                norm = torch.norm(steering_vector)
                if norm > 0:
                    steering_vector = steering_vector / norm  # ||v||₂ = 1.0
                    logger.debug(f"🔧 Normalized vector: ||v||₂ = {torch.norm(steering_vector).item():.4f}")
                else:
                    logger.warning("⚠️ Zero norm steering vector - cannot normalize")
                    return None
            
            return steering_vector
            
        except Exception as e:
            logger.error(f"❌ Error computing steering vector: {e}")
            return None
    
    def _create_vulnerability_prompt(self, code: str) -> str:
        """Proven effective prompt template for vulnerability assessment."""
        return f"""<instruction>
Analyze the following code for security vulnerabilities.

Code:
{code[:500]}

Question: Does this code have security vulnerabilities?
Answer: """
    
    def save_steering_vectors(self, steering_vectors: Dict[str, torch.Tensor], 
                            output_path: str, metadata: Dict = None):
        """Save steering vectors with metadata."""
        save_data = {
            'steering_vectors': {k: v.cpu() for k, v in steering_vectors.items()},
            'config': {
                'model_name': self.config.model_name,
                'target_layers': self.config.target_layers,
                'hidden_dim': self.config.hidden_dim,
                'steering_strength': self.config.steering_strength,
                'normalization': self.config.normalization
            },
            'metadata': metadata or {}
        }
        
        torch.save(save_data, output_path)
        logger.info(f"💾 Saved steering vectors to {output_path}")
    
    def load_steering_vectors(self, input_path: str) -> Tuple[Dict[str, torch.Tensor], Dict]:
        """Load steering vectors and metadata."""
        data = torch.load(input_path, map_location='cpu')
        return data['steering_vectors'], data.get('metadata', {})
    
    def _clear_gpu_memory(self):
        """Aggressive GPU memory cleanup."""
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
        gc.collect()
    
    def _log_memory_usage(self):
        """Log current GPU memory usage."""
        if torch.cuda.is_available():
            allocated = torch.cuda.memory_allocated() / 1024**3
            reserved = torch.cuda.memory_reserved() / 1024**3
            logger.info(f"🔧 GPU Memory - Allocated: {allocated:.2f}GB, Reserved: {reserved:.2f}GB")

def check_nnsight_compatibility():
    """Check NNSight version and API compatibility."""
    if not NNSIGHT_AVAILABLE:
        return "not_installed"
        
    import nnsight
    version = nnsight.__version__
    
    if version.startswith("0.4"):
        print(f"✅ NNSight {version} - Using tuple handling patterns")
        return "tuple_api"
    elif version.startswith("0.2"):
        print(f"⚠️ NNSight {version} - Using direct tensor patterns") 
        return "tensor_api"
    else:
        print(f"❓ NNSight {version} - Unknown API, testing carefully")
        return "unknown"

if __name__ == "__main__":
    # Compatibility check
    api_type = check_nnsight_compatibility()
    
    if api_type == "not_installed":
        print("❌ Please install NNSight: pip install nnsight")
        sys.exit(1)
    
    # Quick test
    config = QwenSteeringConfig()
    steerer = QwenNNSightSteering(config)
    
    print(f"✅ Qwen steering integration ready")
    print(f"📊 Target model: {config.model_name}")
    print(f"🎯 Target layers: {config.target_layers}")
    print(f"💡 Use steerer.load_model() then steerer.create_steering_vectors() to begin") 