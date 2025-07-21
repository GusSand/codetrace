import torch
import torch.nn as nn
from transformers import AutoModelForCausalLM

class SteeredModel(AutoModelForCausalLM):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def forward(self, *args, **kwargs):
        # Get steering parameters
        steering_vector = kwargs.pop('steering_vector', None)
        steering_strength = kwargs.pop('steering_strength', 0.0)
        
        # Get model outputs
        outputs = super().forward(*args, **kwargs)
        
        if steering_vector is not None and steering_strength > 0:
            # Apply steering to the last hidden state
            last_hidden_state = outputs.last_hidden_state
            batch_size = last_hidden_state.shape[0]
            
            # Reshape steering vector to match hidden state dimensions
            steering_vector = torch.tensor(steering_vector, device=last_hidden_state.device)
            steering_vector = steering_vector.view(1, 1, -1).expand(batch_size, -1, -1)
            
            # Apply steering
            steered_hidden = last_hidden_state + steering_strength * steering_vector
            
            # Update outputs
            outputs.last_hidden_state = steered_hidden
            
        return outputs
    
    def generate(self, *args, **kwargs):
        # Get steering parameters
        steering_vector = kwargs.pop('steering_vector', None)
        steering_strength = kwargs.pop('steering_strength', 0.0)
        
        if steering_vector is not None and steering_strength > 0:
            # Add steering parameters to generation config
            if 'generation_config' not in kwargs:
                kwargs['generation_config'] = {}
            kwargs['generation_config']['steering_vector'] = steering_vector
            kwargs['generation_config']['steering_strength'] = steering_strength
        
        return super().generate(*args, **kwargs) 