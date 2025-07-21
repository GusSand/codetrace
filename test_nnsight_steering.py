import torch
from nnsight import LanguageModel
import logging

logging.basicConfig(level=logging.INFO)

def test_steering():
    # Initialize model
    model = LanguageModel("gpt2", device_map="auto")
    n_layers = len(model.transformer.h)
    start_layer = n_layers - 5  # Use last 5 layers
    
    logging.info(f"Model has {n_layers} layers, using layers {start_layer} to {n_layers-1}")
    
    # Test prompts
    positive_prompts = [
        "The capital of France is Paris",
        "The capital of Spain is Madrid"
    ]
    negative_prompts = [
        "The capital of France is London",
        "The capital of Spain is Lisbon"
    ]
    
    # Collect hidden states for positive and negative examples
    with model.trace() as tracer:
        # Get positive examples
        with tracer.invoke(positive_prompts):
            pos_hidden_states = [
                model.transformer.h[layer].output[0].save()
                for layer in range(start_layer, n_layers)
            ]
        
        # Get negative examples
        with tracer.invoke(negative_prompts):
            neg_hidden_states = [
                model.transformer.h[layer].output[0].save()
                for layer in range(start_layer, n_layers)
            ]
    
    # Create steering vectors (difference between positive and negative)
    steering_vectors = {}
    for i, layer in enumerate(range(start_layer, n_layers)):
        # Mean over batch and sequence length for more stable steering
        pos_mean = torch.mean(pos_hidden_states[i], dim=(0,1))  # Mean over batch and sequence
        neg_mean = torch.mean(neg_hidden_states[i], dim=(0,1))  # Mean over batch and sequence
        
        # Compute steering vector as difference of means
        steering_vector = pos_mean - neg_mean
        
        # Normalize
        norm = torch.norm(steering_vector)
        if norm > 0:
            steering_vector = steering_vector / norm
        
        steering_vectors[layer] = steering_vector
        
        logging.info(f"Layer {layer} steering vector stats:")
        logging.info(f"  Mean: {torch.mean(steering_vector).item():.4f}")
        logging.info(f"  Std: {torch.std(steering_vector).item():.4f}")
        logging.info(f"  Norm: {torch.norm(steering_vector).item():.4f}")
    
    # Test steering on a new prompt
    test_prompt = "The capital of Italy is"
    
    with model.trace() as tracer:
        # Original prediction
        with tracer.invoke(test_prompt):
            original_hidden = model.transformer.h[n_layers-1].output[0].save()
            original_logits = model.lm_head.output.save()
        
        # Apply steering
        with tracer.invoke(test_prompt):
            for layer in range(start_layer, n_layers):
                current_hidden = model.transformer.h[layer].output[0]
                steering_vector = steering_vectors[layer].to(current_hidden.device)
                
                # Apply steering with strength
                strength = 1.0
                # Expand steering vector to match hidden state dimensions
                steering_expanded = steering_vector.view(1, 1, -1).expand(current_hidden.shape)
                steered = current_hidden + strength * steering_expanded
                
                # Replace hidden states
                model.transformer.h[layer].output[0][:] = steered
            
            steered_hidden = model.transformer.h[n_layers-1].output[0].save()
            steered_logits = model.lm_head.output.save()
    
    # Compare results
    logging.info("\nOriginal prediction:")
    top_tokens = torch.topk(original_logits[0, -1], k=5)
    for i, (score, token) in enumerate(zip(top_tokens.values, top_tokens.indices)):
        logging.info(f"  {i+1}. {model.tokenizer.decode([token.item()])} ({score.item():.2f})")
    
    logging.info("\nSteered prediction:")
    top_tokens = torch.topk(steered_logits[0, -1], k=5)
    for i, (score, token) in enumerate(zip(top_tokens.values, top_tokens.indices)):
        logging.info(f"  {i+1}. {model.tokenizer.decode([token.item()])} ({score.item():.2f})")

if __name__ == "__main__":
    test_steering() 