import json
import torch
import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer
from tqdm import tqdm
import os
from contextual_steering import ContextualSteering

# Define vulnerability types
VULNERABILITY_TYPES = [
    'sql_injection',
    'xss',
    'path_traversal',
    'command_injection',
    'buffer_overflow',
    'use_after_free',
    'integer_overflow',
    'hardcoded_credentials'
]

class ContextualSteeringExperiment:
    def __init__(self, model_name, device="cuda"):
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
        self.steering = ContextualSteering()
        
    def generate_code(self, prompt, vulnerability_type, steering_strength=1.0):
        """Generate code with contextual steering."""
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        # Get steering vector for the vulnerability type
        steering_vector = self.steering.get_steering_vector(vulnerability_type)
        if steering_vector is None:
            print(f"Warning: No steering vector found for {vulnerability_type}")
            return None
            
        # Convert steering vector to tensor
        steering_vector = torch.tensor(steering_vector, device=self.device)
        
        # Set up generation config
        gen_config = {
            "max_length": 512,
            "num_return_sequences": 1,
            "do_sample": True,
            "temperature": 0.7,
            "pad_token_id": self.tokenizer.eos_token_id
        }
        
        # Generate with steering
        def steering_hook(module, input, output):
            if isinstance(output, tuple):
                hidden_states = output[0]
                steered_states = self.steering.apply_steering(hidden_states, steering_vector, steering_strength)
                return (steered_states,) + output[1:]
            else:
                return self.steering.apply_steering(output, steering_vector, steering_strength)
        
        # Register hook on the last layer
        handle = self.model.transformer.h[-1].register_forward_hook(steering_hook)
        
        try:
            outputs = self.model.generate(**inputs, **gen_config)
            generated_code = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return generated_code
        finally:
            handle.remove()
    
    def run_experiment(self, prompts_file, output_file):
        """Run experiment with different steering strengths."""
        # Load prompts
        with open(prompts_file, 'r') as f:
            prompts = json.load(f)
        
        results = []
        
        for vuln_type in tqdm(VULNERABILITY_TYPES, desc="Running experiments"):
            if vuln_type not in prompts:
                print(f"Warning: No prompts found for {vuln_type}")
                continue
                
            for example in prompts[vuln_type]:
                prompt = example["prompt"]  # Extract the prompt from the example object
                
                # Generate with different steering strengths
                for strength in [0.0, 0.5, 1.0]:  # Baseline, low steering, high steering
                    generated_code = self.generate_code(
                        prompt,
                        vuln_type,
                        steering_strength=strength
                    )
                    
                    if generated_code is not None:
                        results.append({
                            "vulnerability_type": vuln_type,
                            "prompt": prompt,
                            "steering_strength": strength,
                            "generated_code": generated_code
                        })
        
        # Save results
        with open(output_file, 'w') as f:
            json.dump({"results": results}, f, indent=2)

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True,
                       help="Model name (e.g., 'bigcode/starcoderbase-1b')")
    parser.add_argument("--device", type=str, default="cuda",
                       help="Device to run on (cuda or cpu)")
    parser.add_argument("--prompts_file", type=str,
                       default="security/prompts.json",
                       help="Path to prompts file")
    parser.add_argument("--output_file", type=str,
                       default="security/contextual_steering_results.json",
                       help="Path to save results")
    
    args = parser.parse_args()
    
    # Initialize experiment
    experiment = ContextualSteeringExperiment(args.model, args.device)
    
    # Run experiment
    experiment.run_experiment(args.prompts_file, args.output_file)

if __name__ == "__main__":
    main() 