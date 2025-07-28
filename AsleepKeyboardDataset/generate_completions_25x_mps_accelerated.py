#!/usr/bin/env python3
"""
MPS-accelerated 25x completion generation with transformers patch
Continues from existing progress
"""

import json
import torch
import os
import time
import logging
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForCausalLM
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Enable MPS fallback
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

# ==================== MPS PATCH ====================
def apply_mps_patch():
    """Apply the MPS compatibility patch for transformers"""
    
    def fixed_isin_mps_friendly(elements, test_elements):
        """Fixed version that handles all MPS edge cases"""
        
        # Convert non-tensor to tensor
        if not isinstance(test_elements, torch.Tensor):
            test_elements = torch.tensor(test_elements, device=elements.device, dtype=elements.dtype)
        
        # Check PyTorch version
        try:
            major, minor = map(int, torch.__version__.split('.')[:2])
            is_torch_2_4_plus = (major > 2) or (major == 2 and minor >= 4)
        except:
            is_torch_2_4_plus = False
        
        # Use native torch.isin for newer versions or non-MPS
        if elements.device.type != "mps" or is_torch_2_4_plus:
            return torch.isin(elements, test_elements)
        
        # MPS workaround
        if test_elements.dim() == 0:
            test_elements = test_elements.unsqueeze(0)
        
        elements_flat = elements.flatten()
        test_elements_flat = test_elements.flatten()
        
        if elements_flat.numel() == 0 or test_elements_flat.numel() == 0:
            return torch.zeros_like(elements, dtype=torch.bool)
        
        result = torch.zeros_like(elements_flat, dtype=torch.bool)
        
        # Use loop for small test sets (more stable on MPS)
        if test_elements_flat.numel() <= 10:
            for test_val in test_elements_flat:
                result = result | (elements_flat == test_val)
        else:
            # Use broadcasting for larger sets
            elements_expanded = elements_flat.unsqueeze(1)
            test_expanded = test_elements_flat.unsqueeze(0)
            matches = elements_expanded == test_expanded
            result = matches.any(dim=1)
        
        return result.reshape(elements.shape)
    
    # Apply patch
    import transformers.pytorch_utils
    transformers.pytorch_utils.isin_mps_friendly = fixed_isin_mps_friendly
    print("✅ Applied MPS compatibility patch")

# Apply patch before importing transformers
apply_mps_patch()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('completions_generation_mps.log'),
        logging.StreamHandler()
    ]
)

class MPSCompletionGenerator:
    def __init__(self):
        self.model_name = "bigcode/starcoderbase-1b"
        self.temperature = 0.6
        self.num_completions = 25
        self.device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
        
        # Continue from existing file
        self.output_file = "completions_dow_starcoder_t0.6_20250727_113842.jsonl"
        self.progress_file = "mps_generation_progress.json"
        
        # Track completed scenarios
        self.completed_scenarios = set()
        self.load_progress()
        
        logging.info(f"Device: {self.device}")
        logging.info(f"MPS available: {torch.backends.mps.is_available()}")
        
    def load_progress(self):
        """Load existing completions to determine where to continue"""
        if os.path.exists(self.output_file):
            with open(self.output_file, 'r') as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        scenario_id = data['scenario_id']
                        if scenario_id not in self.completed_scenarios:
                            self.completed_scenarios.add(scenario_id)
                    except:
                        pass
            
            # Count completions per scenario
            scenario_counts = {}
            with open(self.output_file, 'r') as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        scenario_id = data['scenario_id']
                        scenario_counts[scenario_id] = scenario_counts.get(scenario_id, 0) + 1
                    except:
                        pass
            
            # Mark as completed only if we have 25 completions
            self.completed_scenarios = {s for s, count in scenario_counts.items() if count >= 25}
            
        logging.info(f"Found {len(self.completed_scenarios)} completed scenarios")
    
    def load_model(self):
        """Load model on MPS"""
        logging.info(f"Loading {self.model_name} on {self.device}...")
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16 if self.device.type == "mps" else torch.float32,
            low_cpu_mem_usage=True
        ).to(self.device)
        
        self.model.eval()
        logging.info("Model loaded successfully")
    
    def generate_completions(self, prompt, scenario_id):
        """Generate 25 completions for a prompt"""
        completions = []
        
        # Tokenize once
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
        input_ids = inputs["input_ids"].to(self.device)
        attention_mask = inputs.get("attention_mask")
        if attention_mask is not None:
            attention_mask = attention_mask.to(self.device)
        
        for i in range(self.num_completions):
            try:
                with torch.no_grad():
                    outputs = self.model.generate(
                        input_ids=input_ids,
                        attention_mask=attention_mask,
                        max_new_tokens=256,
                        temperature=self.temperature,
                        do_sample=True,
                        pad_token_id=self.tokenizer.pad_token_id,
                        use_cache=True  # Can use cache with fixed MPS
                    )
                
                completion = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                completion = completion[len(prompt):]
                
                completions.append({
                    "scenario_id": scenario_id,
                    "completion": completion
                })
                
                # Progress logging
                if (i + 1) % 5 == 0:
                    logging.info(f"  {scenario_id}: {i+1}/{self.num_completions} completions")
                
            except Exception as e:
                logging.error(f"Error generating completion {i+1} for {scenario_id}: {e}")
        
        return completions
    
    def process_scenarios(self):
        """Process all scenarios"""
        # Load scenarios
        scenario_files = ['data/scenario_dow.jsonl']
        scenarios = []
        
        for file in scenario_files:
            if os.path.exists(file):
                with open(file, 'r') as f:
                    for line in f:
                        try:
                            scenarios.append(json.loads(line))
                        except:
                            pass
        
        logging.info(f"Processing {len(scenarios)} scenarios")
        logging.info(f"Skipping {len(self.completed_scenarios)} already completed")
        
        # Filter out completed scenarios
        remaining_scenarios = [s for s in scenarios if s['scenario_id'] not in self.completed_scenarios]
        
        if not remaining_scenarios:
            logging.info("All scenarios already completed!")
            return
        
        # Process remaining scenarios
        start_time = time.time()
        initial_completed = len(self.completed_scenarios)
        
        with open(self.output_file, 'a') as outfile:
            for idx, scenario in enumerate(remaining_scenarios):
                scenario_id = scenario['scenario_id']
                prompt = scenario['prompt']
                
                elapsed = time.time() - start_time
                completed_count = len(self.completed_scenarios) - initial_completed + idx
                if completed_count > 0:
                    avg_time = elapsed / completed_count
                    remaining_scenarios_count = len(remaining_scenarios) - idx - 1
                    eta = remaining_scenarios_count * avg_time / 3600
                else:
                    eta = float('inf')
                
                current_total = initial_completed + idx
                logging.info(f"\n[{current_total}/{len(scenarios)}] Processing {scenario_id} (~{eta:.1f}h remaining)")
                
                # Generate completions
                completions = self.generate_completions(prompt, scenario_id)
                
                # Save completions
                for completion_data in completions:
                    outfile.write(json.dumps(completion_data) + '\n')
                    outfile.flush()
                
                self.completed_scenarios.add(scenario_id)
                
                # Save progress every 5 scenarios
                if (idx + 1) % 5 == 0:
                    self.save_progress()
                
                # Clear cache periodically
                if self.device.type == "mps" and (idx + 1) % 10 == 0:
                    torch.mps.empty_cache()
        
        self.save_progress()
        
        total_time = time.time() - start_time
        scenarios_processed = len(remaining_scenarios)
        logging.info(f"\nCompleted {scenarios_processed} scenarios in {total_time/3600:.1f} hours")
        logging.info(f"Average time per scenario: {total_time/scenarios_processed:.1f} seconds")
    
    def save_progress(self):
        """Save progress checkpoint"""
        with open(self.progress_file, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "completed_scenarios": list(self.completed_scenarios),
                "total_completed": len(self.completed_scenarios)
            }, f, indent=2)

def main():
    logging.info("="*60)
    logging.info("Starting MPS-accelerated completion generation")
    logging.info(f"Temperature: 0.6")
    logging.info(f"Completions per scenario: 25")
    logging.info("="*60)
    
    generator = MPSCompletionGenerator()
    generator.load_model()
    generator.process_scenarios()
    
    logging.info("\nGeneration complete!")

if __name__ == "__main__":
    main()