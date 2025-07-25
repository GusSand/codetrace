# NNSight 0.4.x Working Code Patterns for Neural Steering
# Date: 2025-01-24
# Status: PROVEN WORKING - Use these patterns for future steering experiments

import torch
from nnsight import LanguageModel

def create_steering_vectors_nnsight_04x(model, vulnerable_examples, secure_examples, layer_idx, model_name):
    """
    PROVEN WORKING pattern for NNSight 0.4.x steering vector creation.
    
    KEY FIX: Handle tuple outputs from layer.output.save()
    """
    vulnerable_activations = []
    secure_activations = []
    
    # Process vulnerable examples
    for ex in vulnerable_examples:
        prompt = create_vulnerability_prompt(ex['content'])
        
        with model.trace() as tracer:
            with tracer.invoke(prompt):
                # Model-specific layer access patterns
                if "starcoder" in model_name.lower():
                    layer_output = model.transformer.h[layer_idx].output.save()
                elif "qwen" in model_name.lower():
                    layer_output = model.model.layers[layer_idx].output.save()
                else:
                    # Generic transformer pattern
                    layer_output = model.transformer.h[layer_idx].output.save()
        
        # 🔧 CRITICAL FIX: Handle NNSight 0.4.x tuple outputs
        if layer_output is not None:
            if isinstance(layer_output, tuple) and len(layer_output) > 0:
                # Extract hidden states (first element of tuple)
                hidden_states = layer_output[0]
                if len(hidden_states.shape) >= 3:  # [batch, seq_len, hidden_dim]
                    # Take last token activation
                    activation = hidden_states[0, -1, :].detach().cpu()
                    vulnerable_activations.append(activation)
            
            # Fallback for direct tensor case (if API sometimes returns non-tuples)
            elif hasattr(layer_output, 'shape') and len(layer_output.shape) >= 3:
                activation = layer_output[0, -1, :].detach().cpu()
                vulnerable_activations.append(activation)
    
    # Process secure examples (same pattern)
    for ex in secure_examples:
        prompt = create_vulnerability_prompt(ex['content'])
        
        with model.trace() as tracer:
            with tracer.invoke(prompt):
                if "starcoder" in model_name.lower():
                    layer_output = model.transformer.h[layer_idx].output.save()
                elif "qwen" in model_name.lower():
                    layer_output = model.model.layers[layer_idx].output.save()
                else:
                    layer_output = model.transformer.h[layer_idx].output.save()
        
        # Same tuple handling logic
        if layer_output is not None:
            if isinstance(layer_output, tuple) and len(layer_output) > 0:
                hidden_states = layer_output[0]
                if len(hidden_states.shape) >= 3:
                    activation = hidden_states[0, -1, :].detach().cpu()
                    secure_activations.append(activation)
            elif hasattr(layer_output, 'shape') and len(layer_output.shape) >= 3:
                activation = layer_output[0, -1, :].detach().cpu()
                secure_activations.append(activation)
    
    # Create steering vector if sufficient activations
    if len(vulnerable_activations) > 0 and len(secure_activations) > 0:
        vulnerable_mean = torch.stack(vulnerable_activations).mean(dim=0).cuda()
        secure_mean = torch.stack(secure_activations).mean(dim=0).cuda()
        
        # Steering direction: From vulnerable toward secure
        steering_vector = (secure_mean - vulnerable_mean).detach()
        
        # Normalize for consistent application
        norm = torch.norm(steering_vector)
        if norm > 0:
            steering_vector = steering_vector / norm  # ||v||₂ = 1.0
        
        return steering_vector
    
    return None

def create_vulnerability_prompt(code):
    """Proven effective prompt template for vulnerability assessment."""
    return f"""<instruction>
Analyze the following code for security vulnerabilities.

Code:
{code[:500]}

Question: Does this code have security vulnerabilities?
Answer: """

# Model Architecture Specifications
MODEL_SPECS = {
    "bigcode/starcoderbase-1b": {
        "layer_access": "model.transformer.h[i].output",
        "hidden_dim": 2048,
        "total_layers": 24,
        "recommended_layers": [4, 12, 20]
    },
    "Qwen/Qwen2.5-14B-Instruct": {
        "layer_access": "model.model.layers[i].output", 
        "hidden_dim": 5120,
        "total_layers": 48,
        "recommended_layers": [12, 24, 47]
    }
}

# Steering Configuration
STEERING_CONFIG = {
    "steering_strength": 20.0,  # Proven effective
    "normalization": True,      # Always normalize: ||v||₂ = 1.0
    "examples_per_type": 2-3,   # Minimum for stable vectors
    "layers": "multi_layer",    # Use multiple layers for robustness
}

# API Compatibility Check
def check_nnsight_compatibility():
    """Check NNSight version and API compatibility."""
    import nnsight
    version = nnsight.__version__
    
    if version.startswith("0.4"):
        print(f"✅ NNSight {version} - Use tuple handling patterns")
        return "tuple_api"
    elif version.startswith("0.2"):
        print(f"⚠️ NNSight {version} - Use direct tensor patterns") 
        return "tensor_api"
    else:
        print(f"❓ NNSight {version} - Unknown API, test carefully")
        return "unknown"

# Expected Results
EXPECTED_RESULTS = {
    "starcoderbase-1b": {
        "steering_vector_shape": "torch.Size([2048])",
        "typical_norm": "10-30 (before normalization)",
        "status": "PROVEN WORKING"
    },
    "qwen2.5-14b": {
        "steering_vector_shape": "torch.Size([5120])",
        "typical_norm": "15-50 (before normalization)", 
        "status": "EXPECTED WORKING (same API)"
    }
} 