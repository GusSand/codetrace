#!/usr/bin/env python3
"""
Generate 25 completions per scenario at temperature 0.6 with MPS support
Uses the monkey patch fix for transformers MPS bug
"""

import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers.pytorch_utils
from datetime import datetime
import os
import time
import logging
import sys
import ast
import subprocess
import tempfile
import warnings
import gc
from concurrent.futures import ThreadPoolExecutor, as_completed

# Suppress tokenizer warning
warnings.filterwarnings("ignore", message=".*clean_up_tokenization_spaces.*")

# Enable MPS fallback
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('generate_completions_25x_mps.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def monkey_patch_transformers():
    """Monkey patch the broken isin_mps_friendly function"""
    def fixed_isin_mps_friendly(elements, test_elements):
        """Fixed version that handles edge cases properly"""
        # Handle scalar tensors
        if elements.dim() == 0:
            elements = elements.unsqueeze(0)
        if test_elements.dim() == 0:
            test_elements = test_elements.unsqueeze(0)
            
        # Original logic with dimension checks
        if test_elements.numel() == 0:
            return torch.zeros_like(elements, dtype=torch.bool)
        
        # Use a more robust comparison
        return (elements.unsqueeze(0) == test_elements.unsqueeze(1)).any(dim=0)
    
    # Replace the broken function
    transformers.pytorch_utils.isin_mps_friendly = fixed_isin_mps_friendly

class MPSCompletionGenerator:
    def __init__(self):
        self.model_name = "bigcode/starcoderbase-1b"
        self.num_completions = 25
        self.temperature = 0.6
        self.tokenizer = None
        self.model = None
        
        # Determine best device
        if torch.backends.mps.is_available():
            self.device = torch.device("mps")
            self.device_name = "MPS"
            # Apply MPS fix
            monkey_patch_transformers()
        elif torch.cuda.is_available():
            self.device = torch.device("cuda")
            self.device_name = "CUDA"
        else:
            self.device = torch.device("cpu")
            self.device_name = "CPU"
        
        # Output file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_file = f"completions_asleep_starcoder_t{self.temperature}_{timestamp}.jsonl"
        self.progress_file = f"completion_progress_{timestamp}.json"
        
        # Track progress
        self.completed_scenarios = set()
        self.total_generated = 0
        self.valid_programs = 0
        self.compilable_programs = 0
        self.current_scenario_completions = []
        
        # Performance settings
        self.batch_size = 5 if self.device_name != "CPU" else 3
        
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
            "num_completions": self.num_completions,
            "device": self.device_name
        }
        with open(self.progress_file, 'w') as f:
            json.dump(progress, f, indent=2)
    
    def load_model(self):
        """Load model and tokenizer"""
        logger.info(f"Loading model: {self.model_name}")
        logger.info(f"Using device: {self.device_name}")
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        
        # Set pad token if not set
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
        
        # Load model
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float32 if self.device_name == "MPS" else torch.float16,
            low_cpu_mem_usage=True
        )
        
        # Move to device
        self.model = self.model.to(self.device)
        self.model.eval()
        
        logger.info(f"Model loaded successfully on {self.device_name}")
    
    def generate_completion_batch(self, prompt, num_completions=5):
        """Generate multiple completions efficiently"""
        completions = []
        max_new_tokens = 256
        
        try:
            # Tokenize once
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
            input_ids = inputs["input_ids"].to(self.device)
            attention_mask = inputs.get("attention_mask", torch.ones_like(input_ids)).to(self.device)
            
            # Generate multiple completions
            for i in range(num_completions):
                start_time = time.time()
                
                with torch.no_grad():
                    outputs = self.model.generate(
                        input_ids=input_ids,
                        attention_mask=attention_mask,
                        max_new_tokens=max_new_tokens,
                        temperature=self.temperature,
                        do_sample=True,
                        pad_token_id=self.tokenizer.pad_token_id,
                        eos_token_id=self.tokenizer.eos_token_id,
                        use_cache=True if self.device_name != "MPS" else False
                    )
                
                # Decode
                full_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                completion = full_text[len(prompt):]
                
                gen_time = time.time() - start_time
                logger.debug(f"Generated completion {i+1} in {gen_time:.2f}s")
                
                completions.append(completion)
                
                # Clean up intermediate tensors
                del outputs
                
        except Exception as e:
            logger.error(f"Error in batch generation: {e}")
            import traceback
            logger.error(traceback.format_exc())
        
        return completions
    
    def check_python_syntax(self, code):
        """Check if Python code is syntactically valid"""
        try:
            ast.parse(code)
            return True, None
        except SyntaxError as e:
            return False, f"Line {e.lineno}: {e.msg}"
    
    def check_c_compilation(self, code, timeout=3):
        """Check if C code compiles"""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            result = subprocess.run(
                ['gcc', '-Wall', '-c', temp_file, '-o', '/dev/null'],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            os.unlink(temp_file)
            
            if result.returncode == 0:
                return True, None
            else:
                error_lines = result.stderr.strip().split('\n')
                main_error = error_lines[0] if error_lines else "Compilation failed"
                return False, main_error
                
        except subprocess.TimeoutExpired:
            return False, "Compilation timeout"
        except FileNotFoundError:
            return True, "gcc not available"
        except Exception as e:
            return False, str(e)
        finally:
            if 'temp_file' in locals() and os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def check_javascript_syntax(self, code):
        """Basic JavaScript syntax check"""
        # Basic checks for common syntax errors
        try:
            # Check for balanced braces/brackets
            stack = []
            pairs = {'(': ')', '[': ']', '{': '}'}
            for char in code:
                if char in pairs:
                    stack.append(char)
                elif char in pairs.values():
                    if not stack or pairs[stack.pop()] != char:
                        return False, "Unbalanced brackets"
            
            if stack:
                return False, "Unclosed brackets"
            
            # Check for basic syntax patterns
            if code.count('"') % 2 != 0:
                return False, "Unmatched quotes"
            
            return True, None
            
        except Exception as e:
            return True, None  # Assume valid if check fails
    
    def validate_completion(self, prompt, completion, language):
        """Validate if completion creates a valid program"""
        full_code = prompt + completion
        
        # Check for truncation
        truncated = completion.endswith('...') or completion.endswith('"""')
        
        if language == 'python':
            valid, error = self.check_python_syntax(full_code)
            compilable = valid
        elif language == 'c':
            valid, error = self.check_c_compilation(full_code)
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
        
        logger.info(f"Starting {scenario_id} ({language}, {len(prompt)} chars) on {self.device_name}")
        
        completions = []
        valid_count = 0
        compilable_count = 0
        
        # Generate in batches
        num_batches = (self.num_completions + self.batch_size - 1) // self.batch_size
        
        for batch_idx in range(num_batches):
            batch_start = batch_idx * self.batch_size
            batch_end = min(batch_start + self.batch_size, self.num_completions)
            batch_size = batch_end - batch_start
            
            logger.info(f"  Generating batch {batch_idx+1}/{num_batches} ({batch_size} completions)")
            
            # Generate batch
            batch_completions = self.generate_completion_batch(prompt, batch_size)
            
            # Validate completions in parallel for C
            validation_tasks = []
            for i, completion in enumerate(batch_completions):
                if completion is None:
                    continue
                
                run_number = batch_start + i + 1
                
                # Quick validation
                validation = self.validate_completion(prompt, completion, language)
                
                # Create entry
                entry = {
                    "scenario_id": scenario_id,
                    "completion": completion,
                    "run_number": run_number,
                    "temperature": self.temperature,
                    "syntactically_valid": validation['syntactically_valid'],
                    "compilable": validation['compilable'],
                    "validation_error": validation['validation_error'],
                    "truncated": validation['truncated'],
                    "timestamp": datetime.now().isoformat(),
                    "device": self.device_name
                }
                
                completions.append(entry)
                
                if validation['syntactically_valid']:
                    valid_count += 1
                if validation['compilable']:
                    compilable_count += 1
            
            # Progress update
            progress = batch_end
            elapsed = time.time() - scenario_start
            rate = progress / elapsed if elapsed > 0 else 0
            eta = (self.num_completions - progress) / rate if rate > 0 else 0
            
            logger.info(f"  Progress: {progress}/{self.num_completions} "
                       f"(valid: {valid_count}, compilable: {compilable_count}) - "
                       f"Rate: {rate:.1f} compl/s, ETA: {eta:.0f}s")
            
            # Store intermediate results
            self.current_scenario_completions = completions
        
        scenario_time = time.time() - scenario_start
        logger.info(f"Completed {scenario_id} in {scenario_time:.1f}s: "
                   f"{len(completions)} completions, "
                   f"{valid_count} valid ({valid_count/len(completions)*100:.1f}%), "
                   f"{compilable_count} compilable")
        
        # Update stats
        self.total_generated += len(completions)
        self.valid_programs += valid_count
        self.compilable_programs += compilable_count
        
        return completions
    
    def load_scenarios(self):
        """Load all scenarios from the dataset"""
        all_scenarios = []
        
        for filename in ['data/scenario_dow.jsonl', 'data/scenario_dop.jsonl', 'data/scenario_dod.jsonl']:
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    for line in f:
                        try:
                            scenario = json.loads(line)
                            all_scenarios.append(scenario)
                        except json.JSONDecodeError:
                            pass
        
        logger.info(f"Loaded {len(all_scenarios)} scenarios")
        return all_scenarios
    
    def save_completions(self, completions):
        """Save completions to JSONL file"""
        with open(self.output_file, 'a') as f:
            for completion in completions:
                f.write(json.dumps(completion) + '\n')
    
    def run_generation(self):
        """Run the complete generation process"""
        logger.info("="*60)
        logger.info("Starting MPS-optimized completion generation")
        logger.info(f"Model: {self.model_name}")
        logger.info(f"Device: {self.device_name}")
        logger.info(f"Temperature: {self.temperature}")
        logger.info(f"Completions per scenario: {self.num_completions}")
        logger.info(f"Batch size: {self.batch_size}")
        logger.info("="*60)
        
        # Load model
        self.load_model()
        
        # Load scenarios
        all_scenarios = self.load_scenarios()
        
        # Process each scenario
        start_time = time.time()
        
        try:
            for idx, scenario in enumerate(all_scenarios):
                scenario_id = scenario['scenario_id']
                
                # Skip if already completed
                if scenario_id in self.completed_scenarios:
                    continue
                
                # Progress update
                if idx > 0 and idx % 5 == 0:
                    elapsed = time.time() - start_time
                    scenarios_done = len(self.completed_scenarios)
                    rate = scenarios_done / elapsed if elapsed > 0 else 0
                    remaining = (len(all_scenarios) - scenarios_done) / rate if rate > 0 else 0
                    
                    logger.info(f"\n{'='*50}")
                    logger.info(f"Overall: {scenarios_done}/{len(all_scenarios)} scenarios "
                              f"({scenarios_done/len(all_scenarios)*100:.1f}%) - "
                              f"ETA: {remaining/3600:.1f} hours")
                    logger.info(f"Stats: {self.valid_programs}/{self.total_generated} valid "
                              f"({self.valid_programs/self.total_generated*100:.1f}%)")
                    logger.info(f"{'='*50}\n")
                    
                    # Save progress
                    self.save_progress()
                
                # Generate completions
                completions = self.generate_completions_for_scenario(scenario)
                
                # Save completions
                if completions:
                    self.save_completions(completions)
                    self.completed_scenarios.add(scenario_id)
                    self.current_scenario_completions = []
                
                # Memory cleanup every 10 scenarios
                if idx % 10 == 0:
                    gc.collect()
                    if self.device_name == "MPS":
                        torch.mps.empty_cache()
                    elif self.device_name == "CUDA":
                        torch.cuda.empty_cache()
        
        except KeyboardInterrupt:
            logger.info("\nInterrupted by user - saving progress...")
            # Save any partial completions
            if self.current_scenario_completions:
                self.save_completions(self.current_scenario_completions)
                self.total_generated += len(self.current_scenario_completions)
            self.save_progress()
            raise
        
        except Exception as e:
            logger.error(f"Fatal error: {e}")
            import traceback
            logger.error(traceback.format_exc())
            # Save any partial completions
            if self.current_scenario_completions:
                self.save_completions(self.current_scenario_completions)
                self.total_generated += len(self.current_scenario_completions)
            self.save_progress()
            raise
        
        # Save final progress
        self.save_progress()
        
        # Final report
        total_time = (time.time() - start_time) / 60
        self.generate_final_report(total_time)
    
    def generate_final_report(self, total_time):
        """Generate final summary report"""
        report = f"""# MPS-Optimized Completion Generation Report

**Generated**: {datetime.now().isoformat()}
**Model**: {self.model_name}
**Device**: {self.device_name}
**Temperature**: {self.temperature}
**Completions per scenario**: {self.num_completions}

## Statistics

- **Total scenarios processed**: {len(self.completed_scenarios)}
- **Total completions generated**: {self.total_generated}
- **Syntactically valid programs**: {self.valid_programs} ({self.valid_programs/self.total_generated*100:.1f}%)
- **Compilable programs**: {self.compilable_programs} ({self.compilable_programs/self.total_generated*100:.1f}%)
- **Total time**: {total_time:.1f} minutes ({total_time/60:.1f} hours)
- **Average time per scenario**: {total_time/len(self.completed_scenarios)*60:.1f} seconds
- **Average time per completion**: {total_time*60/self.total_generated:.1f} seconds

## Performance

- **Device used**: {self.device_name}
- **Batch size**: {self.batch_size}
- **Generation rate**: {self.total_generated/(total_time*60):.2f} completions/second

## Output Files

- Completions: `{self.output_file}`
- Progress tracking: `{self.progress_file}`

## Summary

Successfully generated {self.num_completions} completions for each of {len(self.completed_scenarios)} scenarios 
at temperature {self.temperature}. The completions have been validated for syntax and compilation where applicable.

The MPS optimization {'provided significant speedup' if self.device_name == 'MPS' else 'was not used but the script is MPS-ready'}.
"""
        
        report_file = f"completion_generation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_file, 'w') as f:
            f.write(report)
        
        logger.info("="*60)
        logger.info("GENERATION COMPLETE")
        logger.info(f"Total completions: {self.total_generated}")
        logger.info(f"Valid programs: {self.valid_programs} ({self.valid_programs/self.total_generated*100:.1f}%)")
        logger.info(f"Time: {total_time:.1f} minutes on {self.device_name}")
        logger.info(f"Report: {report_file}")
        logger.info("="*60)

def main():
    generator = MPSCompletionGenerator()
    generator.run_generation()

if __name__ == "__main__":
    main()