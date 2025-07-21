#!/usr/bin/env python3
"""
Quick test to see if we can load the smallest StarCoder model for empirical testing.
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import psutil
import time

def check_system():
    """Quick system check."""
    print(f"RAM: {psutil.virtual_memory().available / (1024**3):.1f} GB available")
    print(f"GPU: {'Available' if torch.cuda.is_available() else 'Not available'}")
    if torch.cuda.is_available():
        print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / (1024**3):.1f} GB")

def quick_test():
    """Quick test with the smallest available code model."""
    print("QUICK STARCODER TEST")
    print("="*50)
    
    check_system()
    
    # Try the smallest available models first
    models_to_try = [
        "microsoft/DialoGPT-small",  # Fallback - small general model
        "distilgpt2",                # Even smaller fallback
    ]
    
    # Try StarCoder models if we have enough resources
    if psutil.virtual_memory().available > 4 * (1024**3):  # > 4GB available
        models_to_try.insert(0, "bigcode/tiny_starcoder")  # ~164M params
        
    if psutil.virtual_memory().available > 8 * (1024**3):  # > 8GB available
        models_to_try.insert(0, "bigcode/starcoderbase-1b")  # ~1B params
    
    for model_name in models_to_try:
        print(f"\n🔄 Trying: {model_name}")
        start_time = time.time()
        
        try:
            print("  Loading tokenizer...")
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            if tokenizer.pad_token is None:
                tokenizer.pad_token = tokenizer.eos_token
                
            print("  Loading model...")
            
            # Use CPU-only for faster testing
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float32,
                device_map="cpu"  # Force CPU to avoid GPU memory issues
            )
            
            load_time = time.time() - start_time
            print(f"  ✅ Loaded in {load_time:.1f}s")
            
            # Quick generation test
            prompt = "def secure_query(user_id):"
            print(f"  Testing with: '{prompt}'")
            
            inputs = tokenizer(prompt, return_tensors="pt")
            
            with torch.no_grad():
                outputs = model.generate(
                    inputs.input_ids,
                    max_new_tokens=20,
                    do_sample=True,
                    temperature=0.7,
                    pad_token_id=tokenizer.eos_token_id
                )
            
            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            print(f"  Generated: {generated_text}")
            
            print(f"  🎯 SUCCESS! {model_name} is ready for empirical testing")
            return model_name, model, tokenizer
            
        except Exception as e:
            print(f"  ❌ Failed: {str(e)[:100]}...")
            continue
    
    print("\n❌ No models could be loaded")
    return None, None, None

def run_quick_empirical_test(model_name, model, tokenizer):
    """Run a very quick empirical test if model loads."""
    print(f"\n{'='*50}")
    print(f"QUICK EMPIRICAL TEST WITH {model_name}")
    print('='*50)
    
    # Simple test case
    prompt = "cursor.execute('SELECT * FROM users WHERE id = ' + "
    print(f"Prompt: {prompt}")
    
    # Token biasing test
    print("\n🔧 Token Biasing:")
    try:
        inputs = tokenizer(prompt, return_tensors="pt")
        
        with torch.no_grad():
            outputs = model(inputs.input_ids)
            logits = outputs.logits[:, -1, :]
            
            # Simple bias toward common security tokens
            security_tokens = ["%s", "?"]
            for token in security_tokens:
                try:
                    token_ids = tokenizer.encode(token, add_special_tokens=False)
                    for token_id in token_ids:
                        if token_id < logits.shape[1]:
                            logits[:, token_id] += 5.0  # Add bias
                except:
                    continue
            
            # Generate with bias
            probs = torch.softmax(logits, dim=-1)
            next_token = torch.multinomial(probs, 1)
            
            # Generate a few more tokens
            current_input = inputs.input_ids
            generated_text = ""
            
            for _ in range(10):
                current_input = torch.cat([current_input, next_token], dim=-1)
                outputs = model(current_input)
                logits = outputs.logits[:, -1, :]
                
                # Apply same bias
                for token in security_tokens:
                    try:
                        token_ids = tokenizer.encode(token, add_special_tokens=False)
                        for token_id in token_ids:
                            if token_id < logits.shape[1]:
                                logits[:, token_id] += 5.0
                    except:
                        continue
                
                probs = torch.softmax(logits, dim=-1)
                next_token = torch.multinomial(probs, 1)
                
                new_text = tokenizer.decode(next_token[0], skip_special_tokens=True)
                generated_text += new_text
                
                if len(generated_text) > 50:
                    break
            
            print(f"Result: {prompt}{generated_text}")
            
    except Exception as e:
        print(f"Failed: {e}")
    
    # Standard generation test
    print("\n🧠 Standard Generation:")
    try:
        inputs = tokenizer(prompt, return_tensors="pt")
        
        with torch.no_grad():
            outputs = model.generate(
                inputs.input_ids,
                max_new_tokens=15,
                do_sample=True,
                temperature=0.7,
                pad_token_id=tokenizer.eos_token_id
            )
        
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"Result: {generated_text}")
        
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    model_name, model, tokenizer = quick_test()
    
    if model_name:
        run_quick_empirical_test(model_name, model, tokenizer)
        print(f"\n✅ Model {model_name} is available for more sophisticated testing!")
    else:
        print("\n❌ No suitable models available on this system")
        print("Consider running on a system with more resources or using cloud computing")