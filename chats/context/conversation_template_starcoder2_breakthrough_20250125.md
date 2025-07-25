# Conversation Template: Universal Architecture Support for Neural Steering

**Template ID**: `conversation_template_starcoder2_breakthrough_20250125`  
**Created**: January 25, 2025  
**Use Case**: Implementing neural steering across different model architectures  
**Status**: ✅ Production Ready  

## 📋 **TEMPLATE OVERVIEW**

This template provides the proven patterns for implementing universal neural steering support across different model architectures, specifically validated with StarCoder 1B and StarCoder2 15B.

## 🔧 **CORE IMPLEMENTATION PATTERNS**

### **1. Universal Architecture Detection**

```python
def _debug_model_structure(self):
    """Universal architecture detection for neural steering."""
    
    # Pattern 1: transformer.h (StarCoder 1B, GPT-style)
    if hasattr(self.model, 'transformer') and hasattr(self.model.transformer, 'h'):
        num_layers = len(self.model.transformer.h)
        self.layer_access_pattern = "transformer.h"
        self.num_layers = num_layers
        
    # Pattern 2: model.layers (StarCoder2 15B, Qwen2.5 style)
    elif hasattr(self.model, 'model') and hasattr(self.model.model, 'layers'):
        num_layers = len(self.model.model.layers)
        self.layer_access_pattern = "model.layers" 
        self.num_layers = num_layers
        
    # Pattern 3: model.transformer.h (Alternative wrapping)
    elif hasattr(self.model, 'model') and hasattr(self.model.model, 'transformer'):
        if hasattr(self.model.model.transformer, 'h'):
            num_layers = len(self.model.model.transformer.h)
            self.layer_access_pattern = "model.transformer.h"
            self.num_layers = num_layers
    
    # Auto-configure steering layers based on detected architecture
    if self.num_layers > 0:
        final_layers = [self.num_layers - 3, self.num_layers - 2, self.num_layers - 1]
        self.steering_layers = final_layers
```

### **2. Universal Hidden State Access**

```python
def _get_hidden_state_optimized(self, layer_idx: int):
    """Get hidden state using universal pattern."""
    try:
        if self.layer_access_pattern == "transformer.h":
            if layer_idx < len(self.model.transformer.h):
                return self.model.transformer.h[layer_idx].output[0]
                
        elif self.layer_access_pattern == "model.layers":
            if layer_idx < len(self.model.model.layers):
                return self.model.model.layers[layer_idx].output[0]
                
        elif self.layer_access_pattern == "model.transformer.h":
            if layer_idx < len(self.model.model.transformer.h):
                return self.model.model.transformer.h[layer_idx].output[0]
        
        return None
        
    except Exception as e:
        self.logger.error(f"Hidden state access failed for layer {layer_idx}: {e}")
        return None
```

### **3. Dynamic Dimension Detection**

```python
def detect_model_dimensions(self, model_name: str) -> int:
    """Detect hidden dimensions based on model architecture."""
    
    # Known model configurations
    dimension_map = {
        "starcoder2-15b": 6144,
        "starcoder2-7b": 4096, 
        "starcoderbase-1b": 2048,
        "qwen2.5-14b": 5120,
        "qwen2.5-7b": 4096,
        "qwen2.5-1.5b": 1536
    }
    
    for model_key, hidden_dim in dimension_map.items():
        if model_key in model_name.lower():
            return hidden_dim
    
    # Default fallback
    return 2048
```

### **4. Memory-Optimized Processing**

```python
def get_memory_optimization_config(self, model_name: str) -> dict:
    """Configure memory optimization based on model size."""
    
    if "15b" in model_name.lower() or "14b" in model_name.lower():
        return {
            "max_samples_per_cwe": 2,
            "batch_size": 1,
            "gradient_checkpointing": True
        }
    elif "7b" in model_name.lower():
        return {
            "max_samples_per_cwe": 3,
            "batch_size": 2,
            "gradient_checkpointing": False
        }
    else:  # 1B-3B models
        return {
            "max_samples_per_cwe": 5,
            "batch_size": 4,
            "gradient_checkpointing": False
        }
```

### **5. Universal Steering Vector Application**

```python
def apply_steering_universal(self, layer_idx: int, steering_vector: torch.Tensor):
    """Apply steering vector using universal architecture support."""
    
    hidden_state = self._get_hidden_state_optimized(layer_idx)
    if hidden_state is not None:
        # Get last token's hidden state
        last_token_state = hidden_state[-1]
        steered_hidden = last_token_state + self.steering_scale * steering_vector
        
        # Apply back using universal pattern
        if self.layer_access_pattern == "transformer.h":
            self.model.transformer.h[layer_idx].output[0][-1] = steered_hidden
        elif self.layer_access_pattern == "model.layers":
            self.model.model.layers[layer_idx].output[0][-1] = steered_hidden
        elif self.layer_access_pattern == "model.transformer.h":
            self.model.model.transformer.h[layer_idx].output[0][-1] = steered_hidden
```

## 🧪 **EVALUATION PATTERNS**

### **SecLLMHolmes-Style Binary Classification**

```python
def evaluate_secllmholmes_response(self, response: str, expected_vulnerable: bool) -> dict:
    """Evaluate using SecLLMHolmes methodology."""
    
    vulnerable_indicators = [
        "contains security vulnerabilities", "vulnerable", "security vulnerability", 
        "security flaw", "security issue", "unsafe", "exploitable", "attack",
        "injection", "overflow", "traversal", "dangerous"
    ]
    
    secure_indicators = [
        "is secure", "secure", "safe", "no vulnerabilities", "no security issues",
        "properly validated", "sanitized", "protected", "no security problems"
    ]
    
    response_lower = response.lower()
    vulnerable_count = sum(1 for indicator in vulnerable_indicators if indicator in response_lower)
    secure_count = sum(1 for indicator in secure_indicators if indicator in response_lower)
    
    if vulnerable_count > secure_count:
        predicted_vulnerable = True
        confidence = vulnerable_count / (vulnerable_count + secure_count + 1)
    elif secure_count > vulnerable_count:
        predicted_vulnerable = False
        confidence = secure_count / (vulnerable_count + secure_count + 1)
    else:
        predicted_vulnerable = False  # Conservative default
        confidence = 0.5
    
    return {
        "predicted_vulnerable": predicted_vulnerable,
        "expected_vulnerable": expected_vulnerable,
        "is_correct": predicted_vulnerable == expected_vulnerable,
        "confidence": confidence,
        "raw_response": response
    }
```

## 🚨 **CRITICAL LESSONS LEARNED**

### **1. Architecture Compatibility Issues**
- **Problem**: Different models use different layer access patterns
- **Solution**: Implement universal detection and access patterns
- **Validation**: Test on multiple architectures before deployment

### **2. Dimension Mismatches**
- **Problem**: Hidden dimensions vary significantly between models (2048 vs 6144)
- **Solution**: Dynamic dimension detection based on model name/config
- **Critical**: Always verify tensor shapes before steering vector application

### **3. Memory Management**
- **Problem**: Larger models (15B+) cause OOM errors with default settings
- **Solution**: Implement memory optimization based on model size
- **Best Practice**: Monitor memory usage and adjust batch sizes accordingly

### **4. Vulnerability Bias Persistence**
- **Finding**: StarCoder family models have fundamental vulnerability bias (50% accuracy)
- **Implication**: Neural steering alone cannot overcome architectural biases
- **Research Direction**: Need novel approaches beyond current steering techniques

## 📊 **EXPECTED RESULTS PATTERNS**

### **Architecture Detection Success Indicators**
```
✅ "Found [pattern] with [N] layers"
✅ "Architecture pattern: [pattern_name]"  
✅ "Updated steering layers to final layers: [X, Y, Z]"
✅ "Created steering tensor: torch.Size([3, hidden_dim])"
```

### **Steering Application Success Indicators**
```
✅ Non-zero steering vectors created
✅ No dimension mismatch errors
✅ Generation completes without errors
✅ Measurable token/response differences
```

### **Research Validation Indicators**
```
✅ Consistent accuracy patterns across CWE types
✅ Reproducible results across multiple runs
✅ Clear baseline vs steering comparisons
✅ Statistical significance in measured differences
```

## 🔄 **REUSABLE COMPONENTS**

### **Model Initialization Template**
```python
class UniversalSteeringExperiment:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model, self.tokenizer = self._initialize_model()
        self._debug_model_structure()
        self.memory_config = self.get_memory_optimization_config(model_name)
        self.hidden_dim = self.detect_model_dimensions(model_name)
```

### **Experiment Configuration Template**
```python
@dataclass
class UniversalSteeringConfig:
    model_name: str
    steering_layers: List[int] = None  # Auto-detected
    steering_scale: float = 100.0
    max_new_tokens: int = 50
    hidden_dim: int = None  # Auto-detected
    memory_optimized: bool = None  # Auto-detected
    
    def __post_init__(self):
        # Auto-configuration will be set by the experiment class
        pass
```

## 🎯 **USAGE GUIDELINES**

### **When to Use This Template**
- ✅ Testing neural steering on new model architectures
- ✅ Implementing cross-model compatibility
- ✅ Scaling experiments across different model sizes
- ✅ Research requiring architecture-agnostic steering

### **Prerequisites**
- ✅ NNSight library installed and configured
- ✅ Sufficient GPU memory for target model
- ✅ SecLLMHolmes dataset or equivalent evaluation data
- ✅ Understanding of the model's architecture patterns

### **Success Criteria**
- ✅ Successful architecture detection
- ✅ Non-zero steering vector creation
- ✅ Measurable differences between baseline and steered outputs
- ✅ Reproducible experimental results

---

## 📝 **TEMPLATE VALIDATION**

**Tested Architectures**: StarCoder 1B (transformer.h), StarCoder2 15B (model.layers)  
**Validation Status**: ✅ Production Ready  
**Last Updated**: January 25, 2025  
**Maintainer**: Neural Steering Research Team 