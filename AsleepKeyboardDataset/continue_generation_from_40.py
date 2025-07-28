#!/usr/bin/env python3
"""
Continue generation from scenario 40 (DoW/CWE-78-0)
"""

import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import time
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('completions_generation.log', mode='a'),
        logging.StreamHandler()
    ]
)

class ContinuedCompletionGenerator:
    def __init__(self):
        self.model_name = "bigcode/starcoderbase-1b"
        self.temperature = 0.6
        self.num_completions = 25
        self.output_file = "completions_dow_starcoder_t0.6_20250727_113842.jsonl"
        
    def load_model(self):
        logging.info(f"Loading {self.model_name} on CPU...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True
        )
        logging.info("Model loaded successfully")
    
    def generate_completions(self, prompt, scenario_id):
        completions = []
        
        # Tokenize once
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
        
        for i in range(self.num_completions):
            try:
                with torch.no_grad():
                    outputs = self.model.generate(
                        **inputs,
                        max_new_tokens=256,
                        temperature=self.temperature,
                        do_sample=True,
                        pad_token_id=self.tokenizer.pad_token_id
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
    
    def run(self):
        # Load scenarios
        with open('data/scenario_dow.jsonl', 'r') as f:
            scenarios = [json.loads(line) for line in f]
        
        # Start from scenario 40 (index 40)
        remaining_scenarios = scenarios[40:]  # DoW/CWE-78-0 onwards
        
        logging.info(f"Continuing from scenario 40/89")
        logging.info(f"Processing {len(remaining_scenarios)} remaining scenarios")
        
        start_time = time.time()
        
        with open(self.output_file, 'a') as outfile:
            for idx, scenario in enumerate(remaining_scenarios):
                scenario_id = scenario['scenario_id']
                prompt = scenario['prompt']
                
                # Calculate timing
                elapsed = time.time() - start_time
                if idx > 0:
                    avg_time = elapsed / idx
                    eta = (len(remaining_scenarios) - idx) * avg_time / 3600
                else:
                    eta = float('inf')
                
                current_scenario_num = 40 + idx
                logging.info(f"\n[{current_scenario_num}/89] Processing {scenario_id} (~{eta:.1f}h remaining)")
                
                # Generate completions
                completions = self.generate_completions(prompt, scenario_id)
                
                # Save completions
                for completion_data in completions:
                    outfile.write(json.dumps(completion_data) + '\n')
                    outfile.flush()

def main():
    generator = ContinuedCompletionGenerator()
    generator.load_model()
    generator.run()

if __name__ == "__main__":
    main()