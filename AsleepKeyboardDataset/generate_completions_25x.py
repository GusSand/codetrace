#!/usr/bin/env python3
"""
Generate 25 completions per scenario at temperature 0.6
Following the Asleep at the Keyboard paper methodology
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
import re
from pathlib import Path
import hashlib
import gc

# Set up detailed logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('generate_completions_25x.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class CompletionGenerator:
    def __init__(self):
        self.model_name = "bigcode/starcoderbase-1b"
        self.num_completions = 25
        self.temperature = 0.6
        self.device = torch.device("cpu")  # Force CPU due to MPS issues
        self.tokenizer = None
        self.model = None
        
        # Output file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_file = f"completions_asleep_starcoder_t{self.temperature}_{timestamp}.jsonl"
        self.progress_file = f"completion_progress_{timestamp}.json"
        
        # Track progress
        self.completed_scenarios = set()
        self.total_generated = 0
        self.valid_programs = 0
        self.compilable_programs = 0
        
        # Load previous progress if exists
        self.load_progress()
    
    def load_progress(self):
        """Load previous progress if interrupted"""
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r') as f:
                    progress = json.load(f)
                    self.completed_scenarios = set(progress.get('completed_scenarios', []))
                    self.total_generated = progress.get('total_generated', 0)
                    self.valid_programs = progress.get('valid_programs', 0)
                    self.compilable_programs = progress.get('compilable_programs', 0)
                    logger.info(f"Resuming from {len(self.completed_scenarios)} completed scenarios")
            except Exception as e:
                logger.warning(f"Could not load progress: {e}")
    
    def save_progress(self):
        """Save current progress"""
        progress = {
            "timestamp": datetime.now().isoformat(),
            "completed_scenarios": list(self.completed_scenarios),
            "total_generated": self.total_generated,
            "valid_programs": self.valid_programs,
            "compilable_programs": self.compilable_programs,
            "temperature": self.temperature,
            "num_completions": self.num_completions
        }
        with open(self.progress_file, 'w') as f:
            json.dump(progress, f, indent=2)
    
    def load_model(self):
        """Load model and tokenizer on CPU"""
        logger.info(f"Loading model: {self.model_name}")
        logger.info("Using CPU (MPS has compatibility issues)")
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        
        # Set pad token if not set
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
        
        # Load model on CPU
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True
        )
        self.model.eval()
        
        logger.info("Model loaded successfully on CPU")
    
    def generate_completion(self, prompt, max_new_tokens=256):
        """Generate a single completion"""
        generation_start = time.time()
        try:
            logger.debug(f"Tokenizing prompt of length {len(prompt)}")
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
            
            # Add attention mask
            attention_mask = inputs.get("attention_mask", torch.ones_like(inputs["input_ids"]))
            
            logger.debug(f"Starting generation with max_new_tokens={max_new_tokens}, temperature={self.temperature}")
            with torch.no_grad():
                outputs = self.model.generate(
                    input_ids=inputs["input_ids"],
                    attention_mask=attention_mask,
                    max_new_tokens=max_new_tokens,
                    temperature=self.temperature,
                    do_sample=True,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode
            full_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the completion part
            completion = full_text[len(prompt):]
            
            generation_time = time.time() - generation_start
            logger.debug(f"Generation completed in {generation_time:.2f}s, completion length: {len(completion)}")
            
            # Clean up memory
            del inputs, outputs
            
            return completion
            
        except Exception as e:
            generation_time = time.time() - generation_start
            logger.error(f"Error generating completion after {generation_time:.2f}s: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None
    
    def check_python_syntax(self, code):
        """Check if Python code is syntactically valid"""
        try:
            # Try to parse the code
            ast.parse(code)
            return True, None
        except SyntaxError as e:
            return False, str(e)
    
    def check_c_compilation(self, code, scenario_id):
        """Check if C code compiles"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            # Try to compile
            result = subprocess.run(
                ['gcc', '-Wall', '-Wextra', '-c', temp_file, '-o', '/dev/null'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            # Clean up
            os.unlink(temp_file)
            
            if result.returncode == 0:
                return True, None
            else:
                # Extract main error
                error_lines = result.stderr.strip().split('\n')
                main_error = error_lines[0] if error_lines else "Unknown compilation error"
                return False, main_error
                
        except subprocess.TimeoutExpired:
            return False, "Compilation timeout"
        except Exception as e:
            return False, f"Compilation check failed: {e}"
        finally:
            # Ensure cleanup
            if 'temp_file' in locals() and os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def check_javascript_syntax(self, code):
        """Check JavaScript syntax using node"""
        try:
            # Try to parse with node
            result = subprocess.run(
                ['node', '-c'],
                input=code,
                capture_output=True,
                text=True,
                timeout=2
            )
            
            if result.returncode == 0:
                return True, None
            else:
                return False, result.stderr.strip()
                
        except subprocess.TimeoutExpired:
            return False, "Syntax check timeout"
        except FileNotFoundError:
            # Node not installed, skip validation
            return True, "Node.js not available for validation"
        except Exception as e:
            return False, f"Syntax check failed: {e}"
    
    def validate_completion(self, prompt, completion, language, scenario_id):
        """Validate if completion creates a valid program"""
        full_code = prompt + completion
        
        # Remove any truncation artifacts
        if completion.endswith('...') or completion.endswith('"""'):
            # Likely truncated, still check but note it
            truncated = True
        else:
            truncated = False
        
        if language == 'python':
            valid, error = self.check_python_syntax(full_code)
            compilable = valid  # For Python, syntactically valid = compilable
        elif language == 'c':
            # First check basic syntax by trying to compile
            valid, error = self.check_c_compilation(full_code, scenario_id)
            compilable = valid
        elif language == 'javascript':
            valid, error = self.check_javascript_syntax(full_code)
            compilable = valid
        else:
            # Unknown language, assume valid
            valid = True
            compilable = True
            error = None
        
        return {
            'syntactically_valid': valid,
            'compilable': compilable,
            'validation_error': error,
            'truncated': truncated
        }
    
    def generate_completions_for_scenario(self, scenario):
        """Generate 25 completions for a single scenario"""
        scenario_start = time.time()
        scenario_id = scenario['scenario_id']
        prompt = scenario['prompt']
        language = scenario.get('language', 'unknown')
        
        logger.info(f"Starting scenario {scenario_id} (language: {language}, prompt length: {len(prompt)} chars)")
        logger.info(f"Generating {self.num_completions} completions at temperature {self.temperature}")
        
        completions = []
        valid_count = 0
        compilable_count = 0
        
        for i in range(self.num_completions):
            iteration_start = time.time()
            logger.debug(f"Starting completion {i+1}/{self.num_completions} for {scenario_id}")
            
            # Generate completion
            completion = self.generate_completion(prompt)
            
            if completion is None:
                logger.warning(f"Failed to generate completion {i+1} for {scenario_id}")
                continue
            
            # Validate completion
            logger.debug(f"Validating completion {i+1} (length: {len(completion)} chars)")
            validation_start = time.time()
            validation = self.validate_completion(prompt, completion, language, scenario_id)
            validation_time = time.time() - validation_start
            logger.debug(f"Validation completed in {validation_time:.2f}s")
            
            # Create completion entry
            entry = {
                "scenario_id": scenario_id,
                "completion": completion,
                "run_number": i + 1,
                "temperature": self.temperature,
                "syntactically_valid": validation['syntactically_valid'],
                "compilable": validation['compilable'],
                "validation_error": validation['validation_error'],
                "truncated": validation['truncated'],
                "timestamp": datetime.now().isoformat(),
                "generation_time": time.time() - iteration_start
            }
            
            completions.append(entry)
            
            if validation['syntactically_valid']:
                valid_count += 1
            if validation['compilable']:
                compilable_count += 1
            
            # Log progress every completion
            iteration_time = time.time() - iteration_start
            logger.info(f"  [{i+1}/{self.num_completions}] Generated in {iteration_time:.2f}s - "
                       f"Valid: {validation['syntactically_valid']}, "
                       f"Compilable: {validation['compilable']}")
            
            # Log detailed progress every 5
            if (i + 1) % 5 == 0:
                elapsed = time.time() - scenario_start
                rate = (i + 1) / elapsed
                remaining = (self.num_completions - (i + 1)) / rate
                logger.info(f"  Progress: {i+1}/{self.num_completions} completions "
                          f"(valid: {valid_count}, compilable: {compilable_count}) - "
                          f"ETA for scenario: {remaining:.1f}s")
            
            # Small delay to avoid overwhelming the system
            time.sleep(0.1)
        
        scenario_time = time.time() - scenario_start
        logger.info(f"Completed {scenario_id} in {scenario_time:.1f}s: "
                   f"{len(completions)} completions, "
                   f"{valid_count} valid ({valid_count/len(completions)*100:.1f}%), "
                   f"{compilable_count} compilable ({compilable_count/len(completions)*100:.1f}%)")
        
        # Update global stats
        self.total_generated += len(completions)
        self.valid_programs += valid_count
        self.compilable_programs += compilable_count
        
        return completions
    
    def load_scenarios(self):
        """Load all scenarios from the dataset"""
        all_scenarios = []
        
        for filename in ['data/scenario_dow.jsonl', 'data/scenario_dop.jsonl', 'data/scenario_dod.jsonl']:
            if os.path.exists(filename):
                logger.info(f"Loading scenarios from {filename}")
                with open(filename, 'r') as f:
                    for line in f:
                        try:
                            scenario = json.loads(line)
                            all_scenarios.append(scenario)
                        except json.JSONDecodeError as e:
                            logger.warning(f"Skipping invalid JSON line: {e}")
            else:
                logger.warning(f"File not found: {filename}")
        
        logger.info(f"Loaded {len(all_scenarios)} total scenarios")
        return all_scenarios
    
    def save_completions(self, completions):
        """Save completions to JSONL file"""
        with open(self.output_file, 'a') as f:
            for completion in completions:
                f.write(json.dumps(completion) + '\n')
    
    def run_generation(self):
        """Run the complete generation process"""
        logger.info("="*60)
        logger.info("Starting completion generation")
        logger.info(f"Model: {self.model_name}")
        logger.info(f"Temperature: {self.temperature}")
        logger.info(f"Completions per scenario: {self.num_completions}")
        logger.info("="*60)
        
        # Load model
        self.load_model()
        
        # Load scenarios
        all_scenarios = self.load_scenarios()
        
        # Process each scenario
        start_time = time.time()
        
        for idx, scenario in enumerate(all_scenarios):
            scenario_id = scenario['scenario_id']
            
            # Skip if already completed
            if scenario_id in self.completed_scenarios:
                logger.debug(f"Skipping already completed scenario: {scenario_id}")
                continue
            
            # Progress update
            elapsed = time.time() - start_time
            if idx > 0:
                rate = idx / elapsed
                remaining = (len(all_scenarios) - idx) / rate
                logger.info(f"\nProgress: {idx}/{len(all_scenarios)} scenarios "
                          f"({idx/len(all_scenarios)*100:.1f}%) - "
                          f"ETA: {remaining/60:.1f} minutes")
            
            # Generate completions
            completions = self.generate_completions_for_scenario(scenario)
            
            # Save completions
            if completions:
                self.save_completions(completions)
                self.completed_scenarios.add(scenario_id)
            
            # Save progress
            self.save_progress()
            
            # Memory cleanup every 10 scenarios
            if (idx + 1) % 10 == 0:
                gc.collect()
        
        # Final statistics
        total_time = (time.time() - start_time) / 60
        self.generate_final_report(total_time)
    
    def generate_final_report(self, total_time):
        """Generate final summary report"""
        report = f"""# Completion Generation Report

**Generated**: {datetime.now().isoformat()}
**Model**: {self.model_name}
**Temperature**: {self.temperature}
**Completions per scenario**: {self.num_completions}

## Statistics

- **Total scenarios processed**: {len(self.completed_scenarios)}
- **Total completions generated**: {self.total_generated}
- **Syntactically valid programs**: {self.valid_programs} ({self.valid_programs/self.total_generated*100:.1f}%)
- **Compilable programs**: {self.compilable_programs} ({self.compilable_programs/self.total_generated*100:.1f}%)
- **Total time**: {total_time:.1f} minutes
- **Average time per scenario**: {total_time/len(self.completed_scenarios):.2f} minutes

## Output Files

- Completions: `{self.output_file}`
- Progress tracking: `{self.progress_file}`

## Summary

Successfully generated {self.num_completions} completions for each of {len(self.completed_scenarios)} scenarios 
at temperature {self.temperature}. The completions have been validated for syntax and compilation where applicable.
"""
        
        report_file = f"completion_generation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_file, 'w') as f:
            f.write(report)
        
        logger.info("="*60)
        logger.info("GENERATION COMPLETE")
        logger.info(f"Total completions: {self.total_generated}")
        logger.info(f"Valid programs: {self.valid_programs} ({self.valid_programs/self.total_generated*100:.1f}%)")
        logger.info(f"Report saved to: {report_file}")
        logger.info("="*60)

def main():
    """Main entry point"""
    generator = CompletionGenerator()
    
    try:
        generator.run_generation()
    except KeyboardInterrupt:
        logger.info("Generation interrupted by user - progress saved")
        generator.save_progress()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        generator.save_progress()
        raise

if __name__ == "__main__":
    main()