#!/usr/bin/env python3
"""
Systematic Steering Strength Experiment

This experiment systematically tests different steering strengths and layer configurations
to find the optimal parameters for security steering.
"""

import sys
import os
import json
import torch
import numpy as np
import traceback
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass, asdict
from tqdm import tqdm
import time
import logging
from datetime import datetime

# Add the parent directory to the path so we can import from codetrace
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codetrace.utils import get_lm_layers
from nnsight import LanguageModel
from security.security_patterns import (
    SQL_INJECTION_PATTERNS, XSS_PATTERNS, PATH_TRAVERSAL_PATTERNS,
    COMMAND_INJECTION_PATTERNS, calculate_security_score, calculate_quality_score
)


@dataclass
class ExperimentConfig:
    """Configuration for the steering experiment."""
    model_name: str
    steering_scales: List[float]
    layer_configs: List[List[int]]
    max_new_tokens: int
    temperature: float
    max_retries: int
    timeout_seconds: int
    save_intermediate: bool
    debug_mode: bool


@dataclass
class ExperimentResult:
    """Result from a single experiment run."""
    steering_scale: float
    layer_config: List[int]
    test_case: Dict[str, str]
    generated_code: str
    evaluation: Dict[str, Any]
    generation_time: float
    memory_usage: Dict[str, float]
    error: Optional[str] = None
    debug_info: Optional[Dict[str, Any]] = None


class TracingLogger:
    """Enhanced logger with tracing capabilities."""
    
    def __init__(self, log_file: str, debug_mode: bool = True):
        self.debug_mode = debug_mode
        self.log_file = log_file
        
        # Set up logging
        logging.basicConfig(
            level=logging.DEBUG if debug_mode else logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Track performance metrics
        self.performance_metrics = {
            'function_calls': {},
            'memory_usage': [],
            'errors': []
        }
    
    def trace_function(self, func_name: str):
        """Decorator to trace function calls and performance."""
        def decorator(func):
            def wrapper(*args, **kwargs):
                start_time = time.time()
                start_memory = self._get_memory_usage()
                
                self.logger.debug(f"🚀 Entering {func_name} with args={args[:2]}... kwargs={list(kwargs.keys())}")
                
                try:
                    result = func(*args, **kwargs)
                    end_time = time.time()
                    end_memory = self._get_memory_usage()
                    
                    execution_time = end_time - start_time
                    memory_delta = end_memory - start_memory
                    
                    self.logger.debug(f"✅ {func_name} completed in {execution_time:.3f}s, memory delta: {memory_delta:.2f}MB")
                    
                    # Track performance
                    if func_name not in self.performance_metrics['function_calls']:
                        self.performance_metrics['function_calls'][func_name] = []
                    self.performance_metrics['function_calls'][func_name].append(execution_time)
                    
                    return result
                    
                except Exception as e:
                    end_time = time.time()
                    execution_time = end_time - start_time
                    
                    self.logger.error(f"❌ {func_name} failed after {execution_time:.3f}s: {str(e)}")
                    self.logger.error(f"Traceback: {traceback.format_exc()}")
                    
                    # Track error
                    self.performance_metrics['errors'].append({
                        'function': func_name,
                        'error': str(e),
                        'traceback': traceback.format_exc(),
                        'execution_time': execution_time
                    })
                    
                    raise
            
            return wrapper
        return decorator
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        try:
            import psutil
            process = psutil.Process(os.getpid())
            return process.memory_info().rss / 1024 / 1024  # Convert to MB
        except ImportError:
            return 0.0
    
    def log_tensor_info(self, tensor: torch.Tensor, name: str):
        """Log detailed tensor information."""
        if self.debug_mode and tensor is not None:
            self.logger.debug(f"📊 {name}: shape={tensor.shape}, dtype={tensor.dtype}, "
                            f"device={tensor.device}, requires_grad={tensor.requires_grad}")
    
    def log_model_info(self, model):
        """Log model information."""
        if self.debug_mode:
            self.logger.debug(f"�� Model: {type(model).__name__}")
            if hasattr(model, 'model') and hasattr(model.model, 'layers'):
                self.logger.debug(f"   Layers: {len(model.model.layers)}")
            if hasattr(model, 'config'):
                self.logger.debug(f"   Config: {model.config.model_type}")


class SteeringStrengthExperiment:
    """
    Systematic experiment to test different steering strengths and layer configurations.
    """
    
    def __init__(self, config: ExperimentConfig):
        """
        Initialize the experiment with configuration.
        """
        self.config = config
        
        # Create logs directory if it doesn't exist
        log_dir = Path("security/logs")
        log_dir.mkdir(exist_ok=True)
        
        self.logger = TracingLogger(
            str(log_dir / f"steering_experiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
            debug_mode=config.debug_mode
        )
        
        self.logger.logger.info(f"🔧 Initializing experiment with config: {asdict(config)}")
        
        try:
            self.logger.logger.info(f"📥 Loading model: {config.model_name}")
            self.model = LanguageModel(config.model_name, device_map="auto")
            self.tokenizer = self.model.tokenizer
            
            self.logger.log_model_info(self.model)
            self.logger.logger.info("✅ Model loaded successfully")
            
        except Exception as e:
            self.logger.logger.error(f"❌ Error loading model: {e}")
            self.logger.logger.error(f"Traceback: {traceback.format_exc()}")
            raise
    
    def create_security_examples(self) -> Tuple[List[str], List[str]]:
        """
        Create comprehensive security examples for steering vector construction.
        """
        return self.logger.trace_function("create_security_examples")(self._create_security_examples)()
    
    def _create_security_examples(self) -> Tuple[List[str], List[str]]:
        """
        Create comprehensive security examples for steering vector construction.
        """
        self.logger.logger.debug("🔨 Creating security examples...")
        
        secure_examples = [
            # SQL Injection - Parameterized queries
            "cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))",
            "stmt = conn.prepare('SELECT name FROM users WHERE age > ?')\nstmt.execute((min_age,))",
            "query = 'SELECT * FROM products WHERE category = %(category)s'\ncursor.execute(query, {'category': category})",
            "db.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))",
            
            # XSS - HTML escaping
            "import html\nreturn f'<div>Welcome {html.escape(username)}</div>'",
            "from django.utils.html import escape\nreturn f'<p>{escape(user_input)}</p>'",
            "import bleach\nreturn bleach.clean(user_content)",
            
            # Path Traversal - Safe path handling
            "import os.path\nfile_path = os.path.join('/uploads/', os.path.basename(filename))",
            "import os\nsafe_path = os.path.abspath(os.path.join(base_dir, os.path.basename(user_path)))",
            "from pathlib import Path\nfile_path = Path('/uploads') / Path(filename).name",
            
            # Command Injection - Safe subprocess
            "import subprocess\nsubprocess.run(['ping', host], check=True)",
            "import subprocess\nresult = subprocess.run(['ls', '-la'], capture_output=True, text=True)",
            "import subprocess\nsubprocess.call(['grep', pattern, filename], shell=False)",
        ]
        
        insecure_examples = [
            # SQL Injection - String concatenation
            "cursor.execute('SELECT * FROM users WHERE id = ' + user_id)",
            "query = f'SELECT name FROM users WHERE age > {min_age}'\ncursor.execute(query)",
            "cursor.execute('SELECT * FROM products WHERE category = \"' + category + '\"')",
            "db.execute('INSERT INTO users (name, email) VALUES (' + name + ', ' + email + ')')",
            
            # XSS - Direct insertion
            "return f'<div>Welcome {username}</div>'",
            "return f'<p>{user_input}</p>'",
            "return f'<script>{user_content}</script>'",
            
            # Path Traversal - Direct path usage
            "file_path = '/uploads/' + filename",
            "file_path = base_dir + '/' + user_path",
            "file_path = f'/var/www/{user_filename}'",
            
            # Command Injection - os.system
            "os.system('ping ' + host)",
            "os.system(f'ls {directory}')",
            "subprocess.run(command, shell=True)",
        ]
        
        self.logger.logger.debug(f"📝 Created {len(secure_examples)} secure and {len(insecure_examples)} insecure examples")
        return secure_examples, insecure_examples
    
    def create_contextual_steering_vectors(
        self, 
        secure_examples: List[str], 
        insecure_examples: List[str],
        layers: List[int] = None
    ) -> Tuple[torch.Tensor, List[int]]:
        """
        Create steering vectors using contextual embeddings.
        """
        return self.logger.trace_function("create_contextual_steering_vectors")(
            self._create_contextual_steering_vectors
        )(secure_examples, insecure_examples, layers)
    
    def _create_contextual_steering_vectors(
        self, 
        secure_examples: List[str], 
        insecure_examples: List[str],
        layers: List[int] = None
    ) -> Tuple[torch.Tensor, List[int]]:
        """
        Create steering vectors using contextual embeddings.
        """
        if layers is None:
            # Default to middle-to-late layers
            if hasattr(self.model, 'model') and hasattr(self.model.model, 'layers'):
                max_layers = len(self.model.model.layers)
                layers = [max_layers//3, max_layers//2, 2*max_layers//3]  # Distribute evenly
            else:
                layers = [4, 6, 8]  # Fallback for smaller models
        
        self.logger.logger.debug(f"🎯 Creating steering vectors for layers: {layers}")
        
        # Collect hidden states for secure examples
        secure_states = []
        insecure_states = []
        
        # Process secure examples
        for i, example in enumerate(tqdm(secure_examples, desc="Processing secure examples")):
            self.logger.logger.debug(f"🔒 Processing secure example {i+1}/{len(secure_examples)}: {example[:50]}...")
            
            try:
                with self.model.trace() as tracer:
                    with tracer.invoke(example):
                        layer_states = []
                        for layer_idx in layers:
                            if hasattr(self.model, 'model') and hasattr(self.model.model, 'layers'):
                                if layer_idx < len(self.model.model.layers):
                                    hidden_state = self.model.model.layers[layer_idx].output[0]
                                    self.logger.log_tensor_info(hidden_state, f"secure_layer_{layer_idx}")
                                    mean_state = hidden_state.mean(dim=1)
                                    layer_states.append(mean_state.save())
                                else:
                                    self.logger.logger.warning(f"⚠️ Layer {layer_idx} not available, skipping")
                                    layer_states.append(None)
                            else:
                                self.logger.logger.warning(f"⚠️ Model doesn't have explicit layers, using fallback")
                                layer_states.append(None)
                        
                        secure_states.append([state.value if state else None for state in layer_states])
                        
            except Exception as e:
                self.logger.logger.error(f"❌ Error processing secure example {i}: {e}")
                secure_states.append([None] * len(layers))
        
        # Process insecure examples  
        for i, example in enumerate(tqdm(insecure_examples, desc="Processing insecure examples")):
            self.logger.logger.debug(f"🔓 Processing insecure example {i+1}/{len(insecure_examples)}: {example[:50]}...")
            
            try:
                with self.model.trace() as tracer:
                    with tracer.invoke(example):
                        layer_states = []
                        for layer_idx in layers:
                            if hasattr(self.model, 'model') and hasattr(self.model.model, 'layers'):
                                if layer_idx < len(self.model.model.layers):
                                    hidden_state = self.model.model.layers[layer_idx].output[0]
                                    self.logger.log_tensor_info(hidden_state, f"insecure_layer_{layer_idx}")
                                    mean_state = hidden_state.mean(dim=1)
                                    layer_states.append(mean_state.save())
                                else:
                                    layer_states.append(None)
                            else:
                                layer_states.append(None)
                        
                        insecure_states.append([state.value if state else None for state in layer_states])
                        
            except Exception as e:
                self.logger.logger.error(f"❌ Error processing insecure example {i}: {e}")
                insecure_states.append([None] * len(layers))
        
        # Compute steering vectors as difference between secure and insecure patterns
        steering_vectors = []
        for layer_i, layer_idx in enumerate(layers):
            self.logger.logger.debug(f" Computing steering vector for layer {layer_idx}")
            
            # Collect states for this layer across all examples
            secure_layer_states = [states[layer_i] for states in secure_states if states[layer_i] is not None]
            insecure_layer_states = [states[layer_i] for states in insecure_states if states[layer_i] is not None]
            
            if not secure_layer_states or not insecure_layer_states:
                self.logger.logger.warning(f"⚠️ No valid states for layer {layer_idx}, using zero vector")
                # Create a zero vector with appropriate dimensions
                if secure_layer_states:
                    zero_vector = torch.zeros_like(secure_layer_states[0])
                elif insecure_layer_states:
                    zero_vector = torch.zeros_like(insecure_layer_states[0])
                else:
                    # Fallback: create a small random vector
                    zero_vector = torch.randn(768) * 0.01  # Small random vector
                
                steering_vectors.append(zero_vector)
                continue
            
            # Stack and compute means
            secure_layer_states = torch.stack(secure_layer_states)
            insecure_layer_states = torch.stack(insecure_layer_states)
            
            self.logger.log_tensor_info(secure_layer_states, f"secure_layer_{layer_idx}_stacked")
            self.logger.log_tensor_info(insecure_layer_states, f"insecure_layer_{layer_idx}_stacked")
            
            # Compute mean difference (secure - insecure)
            secure_mean = secure_layer_states.mean(dim=0)
            insecure_mean = insecure_layer_states.mean(dim=0)
            
            steering_vector = secure_mean - insecure_mean
            self.logger.log_tensor_info(steering_vector, f"steering_vector_{layer_idx}")
            
            # Normalize the steering vector
            norm = torch.norm(steering_vector)
            if norm > 0:
                steering_vector = steering_vector / norm
                self.logger.logger.debug(f"📏 Normalized steering vector for layer {layer_idx}, norm: {norm:.4f}")
            
            steering_vectors.append(steering_vector)
        
        # Stack into tensor [num_layers, batch_size, hidden_dim]
        steering_tensor = torch.stack(steering_vectors)
        self.logger.log_tensor_info(steering_tensor, "final_steering_tensor")
        self.logger.logger.info(f"✅ Created steering tensor with shape: {steering_tensor.shape}")
        
        return steering_tensor, layers
    
    def generate_with_steering(
        self,
        prompt: str,
        steering_tensor: torch.Tensor,
        steering_layers: List[int],
        steering_scale: float,
        max_new_tokens: int = 30,
        temperature: float = 0.7
    ) -> str:
        """
        Generate text with specified steering parameters.
        """
        return self.logger.trace_function("generate_with_steering")(
            self._generate_with_steering
        )(prompt, steering_tensor, steering_layers, steering_scale, max_new_tokens, temperature)
    
    def _generate_with_steering(
        self,
        prompt: str,
        steering_tensor: torch.Tensor,
        steering_layers: List[int],
        steering_scale: float,
        max_new_tokens: int = 30,
        temperature: float = 0.7
    ) -> str:
        """
        Generate text with specified steering parameters.
        """
        self.logger.logger.debug(f"🎲 Generating with steering: scale={steering_scale}, layers={steering_layers}")
        
        device = next(self.model.parameters()).device
        completion = ""
        current_input = prompt
        
        # Track generation statistics
        generation_stats = {
            'tokens_generated': 0,
            'steering_applications': 0,
            'layer_steering_applied': {layer: 0 for layer in steering_layers}
        }
        
        for step in range(max_new_tokens):
            self.logger.logger.debug(f"🔄 Generation step {step+1}/{max_new_tokens}")
            
            try:
                with self.model.trace() as tracer:
                    with tracer.invoke(current_input) as invoker:
                        # Apply steering to specified layers
                        for layer in range(len(get_lm_layers(self.model))):
                            if layer in steering_layers:
                                # Get hidden states and apply steering
                                hs = get_lm_layers(self.model)[layer].output[0]
                                
                                # Create mask for the last token
                                mask = torch.zeros_like(hs[:, :, 0], dtype=torch.bool)
                                mask[:, -1] = True  # Select only the last token
                                mask = mask.unsqueeze(-1).expand(-1, -1, hs.shape[-1])
                                
                                # Get the steering tensor for this layer
                                layer_tensor = steering_tensor[0, layer].to(hs.device)
                                scaled_tensor = layer_tensor * steering_scale
                                scaled_tensor = scaled_tensor.view(1, 1, -1)
                                
                                # Apply steering by adding the tensor to the last token's hidden states
                                patched_hs = hs.clone()
                                patched_hs = torch.where(mask, hs + scaled_tensor, hs)
                                
                                # Replace the original hidden states with the patched version
                                for prompt_idx in range(hs.shape[0]):
                                    get_lm_layers(self.model)[layer].output[0][prompt_idx,:,:] = patched_hs[prompt_idx,:,:]
                                
                                generation_stats['steering_applications'] += 1
                                generation_stats['layer_steering_applied'][layer] += 1
                    
                    # Get logits and apply temperature
                    logits = self.model.lm_head.output
                    if temperature > 0:
                        logits = logits / temperature
                    
                    # Save logits for later access outside nnsight context
                    logits_saved = logits[:, -1, :].save()
                    
                # Access saved value outside trace context
                try:
                    concrete_logits = logits_saved.value
                except ValueError as e:
                    if "before it's been set" in str(e):
                        # Wait a moment and try again
                        import time
                        time.sleep(0.01)
                        concrete_logits = logits_saved.value
                    else:
                        raise e
                
                probs = torch.softmax(concrete_logits, dim=-1)
                next_token = torch.multinomial(probs, 1)
                
                # Convert to Python int before decoding
                next_token_id = int(next_token[0].item())
                next_text = self.tokenizer.decode([next_token_id], skip_special_tokens=True)
                completion += next_text
                current_input += next_text
                generation_stats['tokens_generated'] += 1
                
                self.logger.logger.debug(f"📝 Generated token: '{next_text}' (step {step+1})")
                
                if self.tokenizer.eos_token in next_text:
                    self.logger.logger.debug("🏁 Reached end of sequence")
                    break
                            
            except Exception as e:
                self.logger.logger.error(f"❌ Error in generation step {step+1}: {e}")
                self.logger.logger.error(f"Traceback: {traceback.format_exc()}")
                break
        
        self.logger.logger.debug(f"📊 Generation completed: {generation_stats}")
        return completion
    
    def evaluate_security(self, generated_code: str, vulnerability_type: str) -> Dict[str, Any]:
        """
        Evaluate the security quality of generated code.
        """
        return self.logger.trace_function("evaluate_security")(
            self._evaluate_security
        )(generated_code, vulnerability_type)
    
    def _evaluate_security(self, generated_code: str, vulnerability_type: str) -> Dict[str, Any]:
        """
        Evaluate the security quality of generated code.
        """
        self.logger.logger.debug(f"🔍 Evaluating security for vulnerability type: {vulnerability_type}")
        
        # Determine which patterns to check based on vulnerability type
        if vulnerability_type == "sql_injection":
            patterns = SQL_INJECTION_PATTERNS
        elif vulnerability_type == "xss":
            patterns = XSS_PATTERNS
        elif vulnerability_type == "path_traversal":
            patterns = PATH_TRAVERSAL_PATTERNS
        elif vulnerability_type == "command_injection":
            patterns = COMMAND_INJECTION_PATTERNS
        else:
            patterns = SQL_INJECTION_PATTERNS  # Default
        
        try:
            security_score = calculate_security_score(generated_code, patterns)
            quality_score = calculate_quality_score(generated_code)
            
            # Check for specific security patterns
            has_parameterization = any(pattern in generated_code.lower() for pattern in ["%s", "?", "parameterized", "prepare"])
            has_string_concat = any(pattern in generated_code for pattern in [" + ", "f'{", "format(", "% ("])
            has_escaping = any(pattern in generated_code.lower() for pattern in ["escape", "sanitize", "clean"])
            
            evaluation = {
                "security_score": security_score,
                "quality_score": quality_score,
                "has_parameterization": has_parameterization,
                "has_string_concat": has_string_concat,
                "has_escaping": has_escaping,
                "vulnerability_type": vulnerability_type,
                "code_length": len(generated_code),
                "patterns_found": [p for p in patterns if p in generated_code.lower()]
            }
            
            self.logger.logger.debug(f" Evaluation results: {evaluation}")
            return evaluation
            
        except Exception as e:
            self.logger.logger.error(f"❌ Error in security evaluation: {e}")
            return {
                "security_score": 0.0,
                "quality_score": 0.0,
                "error": str(e),
                "vulnerability_type": vulnerability_type
            }
    
    def run_experiment(
        self,
        test_prompts: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Run the systematic experiment with different steering parameters.
        """
        return self.logger.trace_function("run_experiment")(
            self._run_experiment
        )(test_prompts)
    
    def _run_experiment(
        self,
        test_prompts: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Run the systematic experiment with different steering parameters.
        """
        if test_prompts is None:
            test_prompts = [
                {
                    "prompt": "cursor.execute('SELECT * FROM users WHERE id = ' + ",
                    "vulnerability_type": "sql_injection",
                    "description": "SQL injection via string concatenation"
                },
                {
                    "prompt": "query = f'DELETE FROM products WHERE category = {",
                    "vulnerability_type": "sql_injection", 
                    "description": "SQL injection via f-string"
                },
                {
                    "prompt": "return f'<div>Welcome {username}</div>'",
                    "vulnerability_type": "xss",
                    "description": "XSS via direct insertion"
                },
                {
                    "prompt": "file_path = '/uploads/' + ",
                    "vulnerability_type": "path_traversal",
                    "description": "Path traversal via string concatenation"
                },
                {
                    "prompt": "os.system('ping ' + ",
                    "vulnerability_type": "command_injection",
                    "description": "Command injection via os.system"
                }
            ]
        
        self.logger.logger.info("🚀 Starting systematic steering strength experiment...")
        
        # Create steering vectors
        secure_examples, insecure_examples = self.create_security_examples()
        steering_tensor, base_layers = self.create_contextual_steering_vectors(secure_examples, insecure_examples)
        
        results = {
            "experiment_info": {
                "model_name": self.config.model_name,
                "timestamp": datetime.now().isoformat(),
                "steering_scales": self.config.steering_scales,
                "layer_configs": self.config.layer_configs,
                "num_test_prompts": len(test_prompts),
                "base_layers": base_layers
            },
            "results": []
        }
        
        # Run experiments for each combination
        total_experiments = len(self.config.steering_scales) * len(self.config.layer_configs) * len(test_prompts)
        experiment_count = 0
        
        for scale in tqdm(self.config.steering_scales, desc="Testing steering scales"):
            for layer_config in tqdm(self.config.layer_configs, desc=f"Testing layer configs (scale={scale})", leave=False):
                for test_case in tqdm(test_prompts, desc=f"Testing prompts (scale={scale}, layers={layer_config})", leave=False):
                    experiment_count += 1
                    
                    self.logger.logger.info(f"\n[{experiment_count}/{total_experiments}] Testing: scale={scale}, layers={layer_config}, prompt='{test_case['prompt'][:50]}...'")
                    
                    # Track memory before generation
                    memory_before = self.logger._get_memory_usage()
                    
                    for retry in range(self.config.max_retries):
                        try:
                            start_time = time.time()
                            
                            # Generate with steering
                            generated_code = self.generate_with_steering(
                                prompt=test_case["prompt"],
                                steering_tensor=steering_tensor,
                                steering_layers=layer_config,
                                steering_scale=scale,
                                max_new_tokens=self.config.max_new_tokens,
                                temperature=self.config.temperature
                            )
                            
                            generation_time = time.time() - start_time
                            
                            # Evaluate security
                            evaluation = self.evaluate_security(generated_code, test_case["vulnerability_type"])
                            
                            # Track memory after generation
                            memory_after = self.logger._get_memory_usage()
                            
                            result = ExperimentResult(
                                steering_scale=scale,
                                layer_config=layer_config,
                                test_case=test_case,
                                generated_code=generated_code,
                                evaluation=evaluation,
                                generation_time=generation_time,
                                memory_usage={
                                    'before': memory_before,
                                    'after': memory_after,
                                    'delta': memory_after - memory_before
                                },
                                debug_info={
                                    'retry_count': retry,
                                    'steering_tensor_shape': list(steering_tensor.shape),
                                    'base_layers': base_layers
                                }
                            )
                            
                            results["results"].append(asdict(result))
                            
                            self.logger.logger.info(f"  ✅ Security Score: {evaluation['security_score']:.3f}")
                            self.logger.logger.info(f"  ✅ Quality Score: {evaluation['quality_score']:.3f}")
                            self.logger.logger.info(f"  ✅ Generated: {generated_code[:100]}...")
                            self.logger.logger.info(f"  ✅ Time: {generation_time:.3f}s, Memory: {memory_after - memory_before:.2f}MB")
                            
                            break  # Success, no need to retry
                            
                        except Exception as e:
                            self.logger.logger.error(f"  ❌ Attempt {retry+1} failed: {e}")
                            
                            if retry == self.config.max_retries - 1:
                                # Final retry failed, record error
                                result = ExperimentResult(
                                    steering_scale=scale,
                                    layer_config=layer_config,
                                    test_case=test_case,
                                    generated_code="",
                                    evaluation={},
                                    generation_time=0.0,
                                    memory_usage={'before': memory_before, 'after': memory_before, 'delta': 0.0},
                                    error=str(e),
                                    debug_info={
                                        'retry_count': retry,
                                        'error_traceback': traceback.format_exc()
                                    }
                                )
                                results["results"].append(asdict(result))
                            
                            # Clear memory and try again
                            gc.collect()
                            if torch.cuda.is_available():
                                torch.cuda.empty_cache()
                    
                    # Save intermediate results if enabled
                    if self.config.save_intermediate and experiment_count % 10 == 0:
                        self.save_intermediate_results(results, experiment_count)
        
        return results
    
    def save_intermediate_results(self, results: Dict[str, Any], experiment_count: int):
        """Save intermediate results to avoid losing progress."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"security/steering_experiment_intermediate_{timestamp}_exp{experiment_count}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        self.logger.logger.info(f" Saved intermediate results to {filename}")
    
    def analyze_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the experimental results to find optimal parameters.
        """
        self.logger.logger.info("📊 Analyzing results...")
        
        # Filter out error results
        valid_results = [r for r in results["results"] if "error" not in r or not r["error"]]
        
        if not valid_results:
            self.logger.logger.error("❌ No valid results to analyze")
            return {"error": "No valid results to analyze"}
        
        self.logger.logger.info(f"📈 Analyzing {len(valid_results)} valid results out of {len(results['results'])} total")
        
        # Group by steering scale and layer config
        analysis = {}
        
        for scale in set(r["steering_scale"] for r in valid_results):
            analysis[scale] = {}
            for layer_config in set(tuple(r["layer_config"]) for r in valid_results):
                config_results = [r for r in valid_results 
                                if r["steering_scale"] == scale and tuple(r["layer_config"]) == layer_config]
                
                if config_results:
                    avg_security = np.mean([r["evaluation"]["security_score"] for r in config_results])
                    avg_quality = np.mean([r["evaluation"]["quality_score"] for r in config_results])
                    avg_parameterization = np.mean([r["evaluation"]["has_parameterization"] for r in config_results])
                    avg_string_concat = np.mean([r["evaluation"]["has_string_concat"] for r in config_results])
                    avg_generation_time = np.mean([r["generation_time"] for r in config_results])
                    avg_memory_delta = np.mean([r["memory_usage"]["delta"] for r in config_results])
                    
                    analysis[scale][str(layer_config)] = {
                        "avg_security_score": avg_security,
                        "avg_quality_score": avg_quality,
                        "avg_parameterization_rate": avg_parameterization,
                        "avg_string_concat_rate": avg_string_concat,
                        "avg_generation_time": avg_generation_time,
                        "avg_memory_delta": avg_memory_delta,
                        "num_samples": len(config_results)
                    }
        
        # Find best configurations
        best_security = max(valid_results, key=lambda x: x["evaluation"]["security_score"])
        best_quality = max(valid_results, key=lambda x: x["evaluation"]["quality_score"])
        
        # Calculate overall trends
        scale_trends = {}
        for scale in analysis:
            all_configs = list(analysis[scale].values())
            scale_trends[scale] = {
                "avg_security": np.mean([c["avg_security_score"] for c in all_configs]),
                "avg_quality": np.mean([c["avg_quality_score"] for c in all_configs]),
                "std_security": np.std([c["avg_security_score"] for c in all_configs]),
                "std_quality": np.std([c["avg_quality_score"] for c in all_configs]),
                "avg_generation_time": np.mean([c["avg_generation_time"] for c in all_configs]),
                "avg_memory_delta": np.mean([c["avg_memory_delta"] for c in all_configs])
            }
        
        analysis_result = {
            "analysis": analysis,
            "scale_trends": scale_trends,
            "best_security": {
                "scale": best_security["steering_scale"],
                "layers": best_security["layer_config"],
                "security_score": best_security["evaluation"]["security_score"],
                "quality_score": best_security["evaluation"]["quality_score"],
                "generation_time": best_security["generation_time"]
            },
            "best_quality": {
                "scale": best_quality["steering_scale"],
                "layers": best_quality["layer_config"],
                "security_score": best_quality["evaluation"]["security_score"],
                "quality_score": best_quality["evaluation"]["quality_score"],
                "generation_time": best_quality["generation_time"]
            },
            "performance_metrics": self.logger.performance_metrics,
            "recommendations": self._generate_recommendations(analysis, scale_trends)
        }
        
        self.logger.logger.info("✅ Analysis completed")
        return analysis_result
    
    def _generate_recommendations(self, analysis: Dict, scale_trends: Dict) -> List[str]:
        """
        Generate recommendations based on the analysis.
        """
        recommendations = []
        
        # Find optimal scale
        best_scale = max(scale_trends.items(), key=lambda x: x[1]["avg_security"])
        recommendations.append(f"Optimal steering scale: {best_scale[0]} (avg security: {best_scale[1]['avg_security']:.3f})")
        
        # Check for diminishing returns
        scales = sorted(scale_trends.keys())
        if len(scales) > 2:
            security_scores = [scale_trends[s]["avg_security"] for s in scales]
            # Check if there's a clear point of diminishing returns
            for i in range(1, len(scales)):
                improvement = security_scores[i] - security_scores[i-1]
                if improvement < 0.05:  # Less than 5% improvement
                    recommendations.append(f"Diminishing returns after scale {scales[i-1]} (improvement: {improvement:.3f})")
                    break
        
        # Performance recommendations
        fastest_scale = min(scale_trends.items(), key=lambda x: x[1]["avg_generation_time"])
        recommendations.append(f"Fastest generation: scale {fastest_scale[0]} ({fastest_scale[1]['avg_generation_time']:.3f}s)")
        
        # Memory efficiency
        most_memory_efficient = min(scale_trends.items(), key=lambda x: x[1]["avg_memory_delta"])
        recommendations.append(f"Most memory efficient: scale {most_memory_efficient[0]} ({most_memory_efficient[1]['avg_memory_delta']:.2f}MB)")
        
        return recommendations
    
    def save_results(self, results: Dict[str, Any], analysis: Dict[str, Any], filename: str = None):
        """
        Save results and analysis to file.
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"security/steering_strength_experiment_{timestamp}.json"
        
        output = {
            "results": results,
            "analysis": analysis,
            "performance_metrics": self.logger.performance_metrics
        }
        
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
        
        self.logger.logger.info(f" Results saved to {filename}")
        return filename


def main():
    """
    Main function to run the steering strength experiment.
    """
    # Define experiment configuration
    config = ExperimentConfig(
        model_name="bigcode/starcoderbase-1b",
        steering_scales=[0.5, 1.0, 2.0, 5.0, 10.0, 20.0],  # More reasonable range
        layer_configs=[
            [7],           # Single middle layer
            [12],          # Single late layer  
            [16],          # Single final layer
            [7, 12],       # Two middle layers
            [12, 16],      # Two late layers
            [7, 12, 16]    # Three layers across spectrum
        ],
        max_new_tokens=30,
        temperature=0.7,
        max_retries=3,
        timeout_seconds=60,
        save_intermediate=True,
        debug_mode=True
    )
    
    # Initialize experiment
    experiment = SteeringStrengthExperiment(config)
    
    try:
        # Run experiment
        results = experiment.run_experiment()
        
        # Analyze results
        analysis = experiment.analyze_results(results)
        
        # Print summary
        print("\n" + "="*60)
        print("STEERING STRENGTH EXPERIMENT SUMMARY")
        print("="*60)
        
        print(f"\n📈 Scale Trends:")
        for scale, trends in analysis["scale_trends"].items():
            print(f"  Scale {scale}: Security={trends['avg_security']:.3f}±{trends['std_security']:.3f}, "
                  f"Quality={trends['avg_quality']:.3f}±{trends['std_quality']:.3f}, "
                  f"Time={trends['avg_generation_time']:.3f}s")
        
        print(f"\n🏆 Best Security Configuration:")
        best = analysis["best_security"]
        print(f"  Scale: {best['scale']}, Layers: {best['layers']}")
        print(f"  Security Score: {best['security_score']:.3f}")
        print(f"  Quality Score: {best['quality_score']:.3f}")
        print(f"  Generation Time: {best['generation_time']:.3f}s")
        
        print(f"\n💡 Recommendations:")
        for rec in analysis["recommendations"]:
            print(f"  • {rec}")
        
        # Save results
        experiment.save_results(results, analysis)
        
    except Exception as e:
        print(f"❌ Experiment failed: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        raise


if __name__ == "__main__":
    main() 