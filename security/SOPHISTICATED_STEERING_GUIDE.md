# Sophisticated Security Steering Guide

## Problem with Token Biasing

The current `final_security_steering.py` uses **token-level biasing**, which has major limitations:

```python
# Token biasing - BRITTLE APPROACH
security_terms = {
    "%s": 10.0,           # What if they use f-strings?
    "sanitize": 5.0,      # What about "clean", "validate", "filter"?  
    "parameterized": 10.0 # What about "prepared", "bound", "safe"?
}
```

**Problems:**
- Can't enumerate all security-relevant tokens
- Misses semantic relationships 
- Brittle to different coding styles
- No understanding of context

## Solution: Activation Steering

**Activation steering** modifies the model's internal representations (hidden states) rather than just token probabilities.

### Key Advantages

| Aspect | Token Biasing | Activation Steering |
|--------|---------------|-------------------|
| **Scope** | Individual tokens | Semantic concepts |
| **Robustness** | Brittle to synonyms | Handles variations naturally |
| **Context** | No context awareness | Context-aware |
| **Generalization** | Limited to known tokens | Generalizes to new patterns |
| **Integration** | Surface-level | Deep model integration |

### How It Works

1. **Create Paired Examples:**
```python
secure_examples = [
    "cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))",
    "stmt = conn.prepare('SELECT name FROM users WHERE age > ?')"
]

insecure_examples = [
    "cursor.execute('SELECT * FROM users WHERE id = ' + user_id)",
    "query = f'SELECT name FROM users WHERE age > {min_age}'"
]
```

2. **Extract Hidden State Differences:**
```python
# Get model's internal representations
secure_hidden_states = model.encode(secure_examples)
insecure_hidden_states = model.encode(insecure_examples)

# Create steering vector as difference
steering_vector = secure_hidden_states.mean() - insecure_hidden_states.mean()
```

3. **Apply During Generation:**
```python
# Modify hidden states during generation
hidden_states[:, -1, :] += steering_vector * scale
```

## Implementation Options

### Option 1: Use Existing SteeringManager

Integrate with codetrace's sophisticated infrastructure:

```python
from codetrace.steering import SteeringManager

# Create security dataset in expected format
security_dataset = create_security_dataset_for_steering("sql_injection")

# Use SteeringManager for sophisticated steering
steering_manager = SteeringManager(
    model=model,
    cache_dir=cache_dir,
    candidates_ds=security_dataset,
    only_collect_layers=[8, 12, 16, 20]  # Multi-layer steering
)

# Create steering vectors from semantic differences
steering_tensor = steering_manager.create_steering_tensor(batch_size=2)

# Apply sophisticated steering during generation
results = steering_manager.steer(
    split="test",
    layers_to_steer=[12, 16],
    batch_size=1
)
```

### Option 2: Custom Contextual Embeddings

Build your own sophisticated approach:

```python
def create_contextual_steering_vectors(model, secure_examples, insecure_examples):
    """Create steering vectors from contextual embeddings."""
    
    # Extract embeddings from multiple layers
    secure_embeddings = extract_multilayer_embeddings(model, secure_examples)
    insecure_embeddings = extract_multilayer_embeddings(model, insecure_examples)
    
    # Compute semantic difference vectors
    steering_vectors = []
    for layer in range(num_layers):
        secure_mean = secure_embeddings[layer].mean(dim=0)
        insecure_mean = insecure_embeddings[layer].mean(dim=0)
        steering_vector = secure_mean - insecure_mean
        steering_vectors.append(steering_vector)
    
    return torch.stack(steering_vectors)
```

## Examples Provided

### 1. `sophisticated_security_steering.py`
- **Custom implementation** of contextual embedding steering
- Shows how to extract semantic security concepts
- Demonstrates multi-layer steering application
- Includes security pattern analysis

### 2. `steeringmanager_security_example.py`  
- **Integrates with existing codetrace** infrastructure
- Uses SteeringManager for sophisticated steering
- Handles multiple vulnerability types
- Production-ready approach

## Key Results Expected

With sophisticated activation steering, you should see:

1. **Better Generalization:**
   - Handles `"SELECT * FROM users WHERE id = ?"` AND `"query = conn.prepare('SELECT...')`
   - Works with different SQL libraries and coding styles

2. **Semantic Understanding:**
   - Recognizes parameterized queries regardless of exact syntax
   - Understands input validation patterns beyond specific function names

3. **Context Awareness:**
   - Considers surrounding code context
   - Makes appropriate security choices based on context

4. **Robustness:**
   - Works with novel security patterns not in training data
   - Less brittle to adversarial inputs

## Migration Strategy

To upgrade from token biasing to activation steering:

1. **Replace token dictionaries** with paired secure/insecure examples
2. **Use SteeringManager** or implement custom contextual embeddings  
3. **Apply steering at hidden state level** instead of logit level
4. **Test across multiple vulnerability types** to ensure robustness

This approach should achieve the **6-13x security improvements** mentioned in the executive summary through sophisticated semantic steering rather than brittle token manipulation.