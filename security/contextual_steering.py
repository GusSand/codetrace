import torch
import numpy as np
from transformers import AutoTokenizer, AutoModel
import json
import os
from tqdm import tqdm
import argparse
from typing import List, Dict, Tuple, Any
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("contextual_steering.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Define vulnerability types and their CWE IDs
VULNERABILITY_TYPES = {
    'sql_injection': 'CWE-89',
    'xss': 'CWE-79',
    'path_traversal': 'CWE-22',
    'command_injection': 'CWE-78',
    'buffer_overflow': 'CWE-120',
    'use_after_free': 'CWE-416',
    'integer_overflow': 'CWE-190',
    'hardcoded_credentials': 'CWE-798'
}

class ContextualSteering:
    def __init__(self, model_name="microsoft/codebert-base", target_dim=2048):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()
        self.steering_vectors = None
        
        # Add projection layer from CodeBERT dim (768) to target model dim
        self.projection = torch.nn.Linear(768, target_dim)
        self.projection.to(self.device)
        
    def get_steering_vector(self, vulnerability_type):
        """Get the steering vector for a specific vulnerability type."""
        if self.steering_vectors is None:
            # Load code examples and compute steering vectors if not already done
            dataset = load_code_examples()
            self.steering_vectors = self.compute_steering_vectors(dataset)
        
        steering_vector = self.steering_vectors.get(vulnerability_type)
        if steering_vector is not None:
            # Project the steering vector to target dimension
            with torch.no_grad():
                steering_vector = torch.tensor(steering_vector, device=self.device)
                steering_vector = self.projection(steering_vector)
                steering_vector = steering_vector.cpu().numpy()
        
        return steering_vector
        
    def get_embeddings(self, code_examples):
        """Extract embeddings from code examples using CodeBERT."""
        embeddings = []
        
        for code in tqdm(code_examples, desc="Extracting embeddings"):
            # Tokenize and encode
            inputs = self.tokenizer(
                code,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Get embeddings from last hidden state
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            # Use [CLS] token embedding as code representation
            embedding = outputs.last_hidden_state[:, 0, :].cpu().numpy()
            embeddings.append(embedding)
        
        return np.vstack(embeddings)
    
    def compute_steering_vectors(self, dataset):
        """Compute steering vectors for each vulnerability type."""
        steering_vectors = {}
        
        for vuln_type, cwe_id in tqdm(VULNERABILITY_TYPES.items(), desc="Computing steering vectors"):
            if vuln_type not in dataset:
                print(f"Warning: No examples found for {vuln_type}")
                continue
                
            # Get embeddings for secure and vulnerable examples
            secure_embeddings = self.get_embeddings(dataset[vuln_type]["secure"])
            vulnerable_embeddings = self.get_embeddings(dataset[vuln_type]["vulnerable"])
            
            # Compute centroid vectors
            secure_centroid = np.mean(secure_embeddings, axis=0)
            vulnerable_centroid = np.mean(vulnerable_embeddings, axis=0)
            
            # Compute steering vector as difference
            steering_vector = secure_centroid - vulnerable_centroid
            
            # Normalize the vector
            steering_vector = steering_vector / np.linalg.norm(steering_vector)
            
            steering_vectors[vuln_type] = steering_vector
            
        return steering_vectors
    
    def apply_steering(self, hidden_states, steering_vector, strength=1.0):
        """Apply steering vector to hidden states."""
        # Apply dot product with steering vector
        steering = torch.matmul(hidden_states, steering_vector.to(hidden_states.device)) * strength
        
        # Return adjusted hidden states
        return hidden_states + steering.unsqueeze(-1) * steering_vector.to(hidden_states.device)

def load_code_examples():
    """Load secure and vulnerable code examples for each vulnerability type."""
    dataset = {}
    
    # Load examples from JSON files
    for vuln_type in VULNERABILITY_TYPES:
        secure_file = f"security/examples/{vuln_type}_secure.json"
        vulnerable_file = f"security/examples/{vuln_type}_vulnerable.json"
        
        if os.path.exists(secure_file) and os.path.exists(vulnerable_file):
            with open(secure_file, 'r') as f:
                secure_examples = json.load(f)
            with open(vulnerable_file, 'r') as f:
                vulnerable_examples = json.load(f)
            
            dataset[vuln_type] = {
                "secure": secure_examples,
                "vulnerable": vulnerable_examples
            }
        else:
            print(f"Warning: Example files not found for {vuln_type}")
    
    return dataset

def save_steering_vectors(steering_vectors, output_file="security/steering_vectors.json"):
    """Save computed steering vectors to a file."""
    # Convert numpy arrays to lists for JSON serialization
    serializable_vectors = {
        vuln_type: vector.tolist()
        for vuln_type, vector in steering_vectors.items()
    }
    
    with open(output_file, 'w') as f:
        json.dump(serializable_vectors, f, indent=2)

def main():
    # Load code examples
    print("Loading code examples...")
    dataset = load_code_examples()
    
    # Initialize contextual steering
    print("Initializing CodeBERT...")
    steering = ContextualSteering()
    
    # Compute steering vectors
    print("Computing steering vectors...")
    steering_vectors = steering.compute_steering_vectors(dataset)
    
    # Save steering vectors
    print("Saving steering vectors...")
    save_steering_vectors(steering_vectors)
    
    print("Done!")

if __name__ == "__main__":
    main() 