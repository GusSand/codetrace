#!/usr/bin/env python3
"""
Fast CPU-based completion generation - 25 completions per scenario at temperature 0.6
Optimized for speed with minimal overhead
"""

import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from datetime import datetime
import os
import time
import logging
import sys
import ast
import subprocess
import tempfile
import gc
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Simple logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('completions_generation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class FastCompletionGenerator:
    def __init__(self):
        self.model_name = "bigcode/starcoderbase-1b"
        self.num_completions = 25
        self.temperature = 0.6
        self.device = torch.device("cpu")
        self.tokenizer = None
        self.model = None
        
        # Output file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_file = f"completions_dow_starcoder_t{self.temperature}_{timestamp}.jsonl"
        self.checkpoint_file = f"checkpoint_{timestamp}.json"
        
        # Track progress
        self.completed = []
        self.total_scenarios = 0
        self.start_time = time.time()
    
    def load_checkpoint(self):
        """Load checkpoint if exists"""
        if os.path.exists(self.checkpoint_file):
            with open(self.checkpoint_file, 'r') as f:
                data = json.load(f)
                self.completed = data.get('completed', [])
                logger.info(f"Resuming from {len(self.completed)} completed scenarios")
    
    def save_checkpoint(self):
        """Save checkpoint"""
        with open(self.checkpoint_file, 'w') as f:
            json.dump({'completed': self.completed}, f)
    
    def load_model(self):
        """Load model and tokenizer"""
        logger.info(f"Loading {self.model_name} on CPU...")
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True
        )
        self.model.eval()
        
        logger.info("Model loaded successfully")
    
    def generate_completions(self, prompt, scenario_id):
        """Generate 25 completions for a prompt"""
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
                
                full_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                completion = full_text[len(prompt):]
                
                completions.append({
                    "scenario_id": scenario_id,
                    "completion": completion
                })
                
                # Progress indicator
                if (i + 1) % 5 == 0:
                    logger.info(f"  {scenario_id}: {i+1}/{self.num_completions} completions")
                
            except Exception as e:
                logger.error(f"Error generating completion {i+1}: {e}")
        
        return completions
    
    def process_scenarios(self):
        """Process all scenarios"""
        # Load scenarios
        scenarios = []
        for file in ['data/scenario_dow.jsonl', 'data/scenario_dop.jsonl', 'data/scenario_dod.jsonl']:
            if os.path.exists(file):
                with open(file, 'r') as f:
                    for line in f:
                        scenarios.append(json.loads(line))
        
        self.total_scenarios = len(scenarios)
        logger.info(f"Processing {self.total_scenarios} scenarios")
        
        # Process each scenario
        for idx, scenario in enumerate(scenarios):
            scenario_id = scenario['scenario_id']
            
            # Skip if already done
            if scenario_id in self.completed:
                continue
            
            # Status update
            elapsed = time.time() - self.start_time
            done = len(self.completed)
            rate = done / elapsed if done > 0 else 0
            eta = (self.total_scenarios - done) / rate if rate > 0 else float('inf')
            
            logger.info(f"\n[{done}/{self.total_scenarios}] Processing {scenario_id} "
                       f"(~{eta/3600:.1f}h remaining)")
            
            # Generate completions
            prompt = scenario['prompt']
            completions = self.generate_completions(prompt, scenario_id)
            
            # Save completions
            with open(self.output_file, 'a') as f:
                for comp in completions:
                    f.write(json.dumps(comp) + '\n')
            
            # Update progress
            self.completed.append(scenario_id)
            
            # Save checkpoint every 5 scenarios
            if len(self.completed) % 5 == 0:
                self.save_checkpoint()
                gc.collect()
        
        # Final save
        self.save_checkpoint()
    
    def run(self):
        """Main entry point"""
        logger.info("="*60)
        logger.info(f"Starting fast completion generation")
        logger.info(f"Temperature: {self.temperature}")
        logger.info(f"Completions per scenario: {self.num_completions}")
        logger.info("="*60)
        
        # Load checkpoint
        self.load_checkpoint()
        
        # Load model
        self.load_model()
        
        # Process scenarios
        self.process_scenarios()
        
        # Summary
        total_time = (time.time() - self.start_time) / 60
        logger.info("="*60)
        logger.info(f"COMPLETE!")
        logger.info(f"Generated {len(self.completed) * self.num_completions} completions")
        logger.info(f"Time: {total_time:.1f} minutes")
        logger.info(f"Output: {self.output_file}")
        logger.info("="*60)

if __name__ == "__main__":
    generator = FastCompletionGenerator()
    generator.run()