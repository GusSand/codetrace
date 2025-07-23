## Neural Steering Security Experiments - Enhanced Context Summary

### Key Achievements
- Successfully implemented real nnsight steering vectors for security improvement
- Achieved security score of 0.125 with only 5 training examples
- Developed comprehensive visualization and analysis tools
- Created chat management system for conversation persistence

### Technical Learnings
- Real steering vectors outperform synthetic ones for security tasks
- Layer configurations [4,12,20] with scale 20.0 work well for security
- Proper dimension matching and context handling are crucial
- Memory usage scales with steering parameters

### Important Files
- `security/sample_efficiency_experiment/real_steering_experiment.py` - Working experiment
- `security/visualize_steering_strength.py` - Analysis and visualization
- `chats/chat_manager.py` - Conversation management
- `steering_strength_results_*.json` - Experiment results

### Code Patterns & Implementation Hints

#### ✅ Correct NNSight Usage Pattern
```python
# CRITICAL: This is the working pattern from real_steering_experiment.py
with model.trace() as tracer:
    with tracer.invoke(current_input) as invoker:
        # Apply steering to specified layers
        for layer_idx in steering_layers:
            if layer_idx < len(layers):
                # Get current hidden state
                hidden_state = layers[layer_idx].output[0][-1]
                # Apply steering
                steered_hidden = hidden_state + steering_scale * steering_tensor
                # Replace the hidden state
                layers[layer_idx].output[0][-1] = steered_hidden
        
        # Get logits for next token
        logits = model.lm_head.output[0][-1].save()
```

#### ✅ Security Evaluation Pattern
```python
def evaluate_security(generated_code, vulnerability_type):
    secure_patterns = SECURITY_PATTERNS[vulnerability_type]['secure']
    vulnerable_patterns = SECURITY_PATTERNS[vulnerability_type]['vulnerable']
    
    secure_count = sum(1 for pattern in secure_patterns if pattern in generated_code)
    vulnerable_count = sum(1 for pattern in vulnerable_patterns if pattern in generated_code)
    
    # Avoid division by zero
    security_score = secure_count / (secure_count + vulnerable_count + 1)
    return security_score
```

#### ✅ Memory Monitoring
```python
import psutil
import os

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # MB

# Monitor during experiments
memory_before = get_memory_usage()
# Run steering experiment
memory_after = get_memory_usage()
memory_delta = memory_after - memory_before
```

#### ✅ Steering Vector Loading
```python
def load_steering_vectors(model_name, layer_config):
    vectors = {}
    for layer_idx in layer_config:
        vector_path = f"steering_vectors/{model_name}/layer_{layer_idx}.npy"
        vectors[layer_idx] = np.load(vector_path)
    return vectors
```

### Common Issues & Solutions

#### ❌ Invoker Attribute Error
- **Cause**: Accessing proxy values after generation completes
- **Fix**: Access hidden states before `invoker.next()`
- **Pattern**: Always access `layers[layer_idx].output[0]` before generation

#### ❌ Dimension Mismatch
- **Cause**: Steering vector shape ≠ hidden state shape
- **Fix**: Check dimensions with `assert steering_vector.shape == hidden_states.shape`
- **Pattern**: Always verify tensor shapes before applying steering

#### ❌ Memory Errors
- **Cause**: Too many layers or high steering scale
- **Fix**: Use specific layer configs like `[4,12,20]` and monitor memory
- **Pattern**: Start with small layer configs and scale up gradually

### Best Practices Checklist

- ✅ Use layer configurations `[4,12,20]` for security tasks
- ✅ Apply steering scales between `10-50`
- ✅ Access hidden states BEFORE generation
- ✅ Check steering vector dimensions before applying
- ✅ Monitor memory usage during experiments
- ✅ Use pattern-based security evaluation
- ✅ Save experiment results with metadata

### File-Specific Implementation Details

#### `real_steering_experiment.py`
- Contains the **working steering vector application pattern**
- Uses `model.trace()` and `tracer.invoke()` correctly
- Applies steering to specific layers only
- Includes proper error handling and logging

#### `visualize_steering_strength.py`
- Comprehensive analysis and plotting functions
- Memory usage tracking
- Performance metrics calculation
- Statistical summaries and heatmaps

#### `security_patterns.py`
- Defines SQL injection, XSS, path traversal patterns
- Pattern-based security evaluation
- Secure vs vulnerable pattern matching

#### `test_nnsight_steering.py`
- Basic working example for reference
- Simple steering vector application
- Good starting point for new experiments

### Next Steps
- Extend to more vulnerability types and models
- Optimize steering parameters automatically
- Develop real-time quality assessment
- Create interactive visualization dashboard

This enhanced context includes detailed code patterns, debugging solutions, and implementation hints for continuing neural steering research and development.