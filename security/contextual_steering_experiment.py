import torch
import json
import argparse
import logging
import os
from tqdm import tqdm
import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import List, Dict, Any, Optional
import random
import time
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"contextual_steering_experiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ContextualSteeringExperiment:
    """
    Runs experiments using contextual embedding-based steering vectors.
    """
    def __init__(
        self,
        model_name: str,
        steering_vectors_file: str,
        device: str = "cuda",
        batch_size: int = 1
    ):
        """
        Initialize the experiment.
        
        Args:
            model_name: Name of the model to use
            steering_vectors_file: Path to the JSON file containing steering vectors
            device: Device to run the model on
            batch_size: Batch size for generation
        """
        self.device = device
        self.batch_size = batch_size
        
        # Load the model and tokenizer
        logger.info(f"Loading model {model_name} on {device}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map=device
        )
        
        # Load steering vectors
        logger.info(f"Loading steering vectors from {steering_vectors_file}")
        with open(steering_vectors_file, 'r') as f:
            self.steering_vectors = json.load(f)
            
        # Convert steering vectors from lists to numpy arrays
        self.steering_vectors = {k: np.array(v) for k, v in self.steering_vectors.items()}
        
        # Load prompts
        self.prompts = self._load_prompts()
        
    def _load_prompts(self) -> Dict[str, List[str]]:
        """
        Load prompts for each vulnerability type.
        
        Returns:
            Dictionary mapping vulnerability types to lists of prompts
        """
        prompts = {}
        
        # Define prompts for each vulnerability type
        prompts["sql_injection"] = [
            "Write a function that safely queries a database with user input:",
            "Create a function that prevents SQL injection when querying a database:",
            "Implement a secure database query function that handles user input:"
        ]
        
        prompts["xss"] = [
            "Write a function that safely renders user input in HTML:",
            "Create a function that prevents XSS when displaying user content:",
            "Implement a secure HTML rendering function that handles user input:"
        ]
        
        prompts["path_traversal"] = [
            "Write a function that safely reads files based on user input:",
            "Create a function that prevents path traversal when accessing files:",
            "Implement a secure file access function that handles user input:"
        ]
        
        prompts["command_injection"] = [
            "Write a function that safely executes system commands with user input:",
            "Create a function that prevents command injection when running commands:",
            "Implement a secure command execution function that handles user input:"
        ]
        
        prompts["hardcoded_credentials"] = [
            "Write a function that securely handles authentication credentials:",
            "Create a function that avoids hardcoding credentials in the code:",
            "Implement a secure authentication function that doesn't use hardcoded credentials:"
        ]
        
        prompts["integer_overflow"] = [
            "Write a function that safely performs arithmetic operations:",
            "Create a function that prevents integer overflow in calculations:",
            "Implement a secure arithmetic function that handles large numbers:"
        ]
        
        return prompts
    
    def apply_steering(self, hidden_states: torch.Tensor, steering_vector: np.ndarray, strength: float = 1.0) -> torch.Tensor:
        """
        Apply steering vector to the hidden states.
        
        Args:
            hidden_states: Hidden states from the model
            steering_vector: Steering vector to apply
            strength: Strength of the steering
            
        Returns:
            Modified hidden states
        """
        # Convert steering vector to tensor
        steering_tensor = torch.tensor(steering_vector, dtype=hidden_states.dtype, device=self.device)
        
        # Reshape steering vector to match hidden states
        steering_tensor = steering_tensor.view(1, 1, -1)
        
        # Apply steering to the last hidden layer
        # We're modifying the hidden states at the final layer
        modified_hidden_states = hidden_states.clone()
        modified_hidden_states[:, -1, :] += strength * steering_tensor
        
        return modified_hidden_states
    
    def generate_with_steering(
        self,
        prompt: str,
        vulnerability_type: str,
        steering_strength: float = 1.0,
        max_length: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.95,
        num_return_sequences: int = 1
    ) -> List[str]:
        """
        Generate code with steering applied.
        
        Args:
            prompt: Prompt to generate from
            vulnerability_type: Type of vulnerability to steer for
            steering_strength: Strength of the steering
            max_length: Maximum length of the generated sequence
            temperature: Sampling temperature
            top_p: Top-p sampling parameter
            num_return_sequences: Number of sequences to return
            
        Returns:
            List of generated sequences
        """
        # Get the steering vector for this vulnerability type
        if vulnerability_type not in self.steering_vectors:
            logger.warning(f"No steering vector found for {vulnerability_type}, using no steering")
            steering_vector = np.zeros(768)  # Default size for CodeBERT
        else:
            steering_vector = self.steering_vectors[vulnerability_type]
        
        # Tokenize the prompt
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        # Create a custom forward function that applies steering
        def custom_forward(*args, **kwargs):
            # Get the original outputs
            outputs = self.model(*args, **kwargs)
            
            # Apply steering to the hidden states
            if hasattr(outputs, 'hidden_states') and outputs.hidden_states is not None:
                # If the model returns hidden states, apply steering to the last layer
                modified_hidden_states = []
                for hidden_state in outputs.hidden_states:
                    modified_hidden_states.append(self.apply_steering(hidden_state, steering_vector, steering_strength))
                outputs.hidden_states = modified_hidden_states
            
            return outputs
        
        # Monkey patch the model's forward method
        original_forward = self.model.forward
        self.model.forward = custom_forward
        
        try:
            # Generate with the modified model
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                num_return_sequences=num_return_sequences,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            # Decode the outputs
            generated_texts = [self.tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
            
            # Remove the prompt from the generated texts
            generated_texts = [text[len(prompt):] for text in generated_texts]
            
            return generated_texts
        finally:
            # Restore the original forward method
            self.model.forward = original_forward
    
    def run_experiment(
        self,
        vulnerability_types: Optional[List[str]] = None,
        steering_strengths: List[float] = [0.0, 0.5, 1.0],
        num_samples: int = 5
    ) -> Dict[str, Any]:
        """
        Run the experiment with different steering strengths.
        
        Args:
            vulnerability_types: List of vulnerability types to test
            steering_strengths: List of steering strengths to test
            num_samples: Number of samples to generate for each configuration
            
        Returns:
            Dictionary containing the results
        """
        if vulnerability_types is None:
            vulnerability_types = list(self.prompts.keys())
        
        results = {
            "model": self.model.config.name_or_path,
            "steering_method": "contextual_embedding",
            "timestamp": datetime.now().isoformat(),
            "results": []
        }
        
        for vuln_type in vulnerability_types:
            logger.info(f"Testing {vuln_type}")
            
            if vuln_type not in self.prompts:
                logger.warning(f"No prompts found for {vuln_type}, skipping")
                continue
                
            prompts = self.prompts[vuln_type]
            
            for strength in steering_strengths:
                logger.info(f"Testing {vuln_type} with steering strength {strength}")
                
                for i, prompt in enumerate(prompts):
                    if i >= num_samples:
                        break
                        
                    logger.info(f"Generating sample {i+1}/{num_samples} for {vuln_type} with strength {strength}")
                    
                    try:
                        generated_texts = self.generate_with_steering(
                            prompt=prompt,
                            vulnerability_type=vuln_type,
                            steering_strength=strength
                        )
                        
                        for j, text in enumerate(generated_texts):
                            result = {
                                "vulnerability_type": vuln_type,
                                "steering_strength": strength,
                                "prompt": prompt,
                                "generated_code": text,
                                "sample_id": f"{vuln_type}_{strength}_{i}_{j}"
                            }
                            
                            results["results"].append(result)
                    except Exception as e:
                        logger.error(f"Error generating for {vuln_type} with strength {strength}: {e}")
        
        return results
    
    def save_results(self, results: Dict[str, Any], output_file: str):
        """
        Save the results to a JSON file.
        
        Args:
            results: Results dictionary
            output_file: Path to the output file
        """
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Saved results to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Run experiments with contextual embedding-based steering vectors")
    parser.add_argument("--model", type=str, required=True, help="Name of the model to use")
    parser.add_argument("--steering_vectors", type=str, default="security/contextual_steering_vectors.json",
                        help="Path to the JSON file containing steering vectors")
    parser.add_argument("--output", type=str, default="security/contextual_steering_results.json",
                        help="Path to the output JSON file for results")
    parser.add_argument("--device", type=str, default="cuda", help="Device to run the model on")
    parser.add_argument("--batch_size", type=int, default=1, help="Batch size for generation")
    parser.add_argument("--vulnerability_types", type=str, nargs="+", default=None,
                        help="List of vulnerability types to test")
    parser.add_argument("--steering_strengths", type=float, nargs="+", default=[0.0, 0.5, 1.0],
                        help="List of steering strengths to test")
    parser.add_argument("--num_samples", type=int, default=5, help="Number of samples to generate for each configuration")
    
    args = parser.parse_args()
    
    # Initialize the experiment
    experiment = ContextualSteeringExperiment(
        model_name=args.model,
        steering_vectors_file=args.steering_vectors,
        device=args.device,
        batch_size=args.batch_size
    )
    
    # Run the experiment
    results = experiment.run_experiment(
        vulnerability_types=args.vulnerability_types,
        steering_strengths=args.steering_strengths,
        num_samples=args.num_samples
    )
    
    # Save the results
    experiment.save_results(results, args.output)

if __name__ == "__main__":
    main() 