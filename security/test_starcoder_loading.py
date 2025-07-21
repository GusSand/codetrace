#!/usr/bin/env python3
"""
Test loading StarCoder models to see what works on this machine.
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import psutil
import gc

def check_system_resources():
    """Check available system resources."""
    print("🖥️  SYSTEM RESOURCES:")
    print(f"CPU cores: {psutil.cpu_count()}")
    print(f"RAM: {psutil.virtual_memory().total / (1024**3):.1f} GB")
    print(f"Available RAM: {psutil.virtual_memory().available / (1024**3):.1f} GB")
    
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / (1024**3):.1f} GB")
    else:
        print("GPU: Not available")
    print()

def try_load_model(model_name, use_device_map=True, load_in_8bit=False, load_in_4bit=False):
    """Try to load a model with different configurations."""
    print(f"🔄 Attempting to load: {model_name}")
    
    try:
        # Clear memory first
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        # Try loading tokenizer first
        print("  Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        # Try loading model with different strategies
        kwargs = {}
        if use_device_map:
            kwargs["device_map"] = "auto"
        if load_in_8bit:
            kwargs["load_in_8bit"] = True
        if load_in_4bit:
            kwargs["load_in_4bit"] = True
        
        print(f"  Loading model with kwargs: {kwargs}")
        model = AutoModelForCausalLM.from_pretrained(model_name, **kwargs)
        
        print(f"  ✅ Successfully loaded {model_name}")
        
        # Get model info
        num_params = sum(p.numel() for p in model.parameters())
        print(f"  Parameters: {num_params:,}")
        print(f"  Model size estimate: {num_params * 4 / (1024**3):.2f} GB (fp32)")
        
        # Test a simple generation
        print("  Testing generation...")
        prompt = "def hello_world():"
        inputs = tokenizer(prompt, return_tensors="pt")
        
        if torch.cuda.is_available() and not use_device_map:
            model = model.cuda()
            inputs = {k: v.cuda() for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = model.generate(
                inputs.input_ids, 
                max_new_tokens=10, 
                do_sample=True,
                temperature=0.7,
                pad_token_id=tokenizer.eos_token_id
            )
            
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"  Test generation: {generated_text}")
        
        return model, tokenizer, True
        
    except Exception as e:
        print(f"  ❌ Failed to load {model_name}: {str(e)[:200]}...")
        return None, None, False

def main():
    """Test loading various StarCoder models."""
    print("="*70)
    print("STARCODER MODEL LOADING TEST")
    print("="*70)
    
    check_system_resources()
    
    # Models to try, from smallest to largest
    models_to_test = [
        "bigcode/tiny_starcoder",         # ~164M parameters
        "bigcode/starcoderbase-1b",       # ~1B parameters  
        "bigcode/starcoderbase-3b",       # ~3B parameters
        "bigcode/starcoderbase-7b",       # ~7B parameters
    ]
    
    successful_models = []
    
    for model_name in models_to_test:
        print(f"\n{'='*50}")
        print(f"TESTING: {model_name}")
        print('='*50)
        
        # Try different loading strategies
        strategies = [
            ("Standard loading", {"use_device_map": False}),
            ("Device map auto", {"use_device_map": True}),
            ("8-bit quantization", {"use_device_map": True, "load_in_8bit": True}),
            ("4-bit quantization", {"use_device_map": True, "load_in_4bit": True}),
        ]
        
        model_loaded = False
        for strategy_name, kwargs in strategies:
            if model_loaded:
                break
                
            print(f"\n🔧 Strategy: {strategy_name}")
            try:
                model, tokenizer, success = try_load_model(model_name, **kwargs)
                if success:
                    successful_models.append({
                        "model_name": model_name,
                        "strategy": strategy_name,
                        "model": model,
                        "tokenizer": tokenizer
                    })
                    model_loaded = True
                    break
                else:
                    # Clean up failed attempt
                    del model, tokenizer
                    gc.collect()
                    if torch.cuda.is_available():
                        torch.cuda.empty_cache()
            except Exception as e:
                print(f"  ❌ Strategy failed: {e}")
                continue
        
        if not model_loaded:
            print(f"  ❌ All strategies failed for {model_name}")
    
    # Summary
    print(f"\n{'='*70}")
    print("LOADING RESULTS SUMMARY")
    print('='*70)
    
    if successful_models:
        print(f"✅ Successfully loaded {len(successful_models)} models:")
        for result in successful_models:
            print(f"  • {result['model_name']} using {result['strategy']}")
        
        # Recommend best model for testing
        largest_model = successful_models[-1]  # Last one should be largest
        print(f"\n🎯 RECOMMENDATION: Use {largest_model['model_name']} for empirical testing")
        print(f"   Strategy: {largest_model['strategy']}")
        
        return largest_model
    else:
        print("❌ No models loaded successfully")
        print("Possible solutions:")
        print("  • Try running on a machine with more RAM/GPU memory")
        print("  • Install additional quantization libraries (bitsandbytes)")
        print("  • Use smaller models or CPU-only execution")
        
        return None

if __name__ == "__main__":
    try:
        result = main()
        if result:
            print(f"\n✅ Ready to run empirical tests with: {result['model_name']}")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        print("This may be due to missing dependencies or insufficient system resources")