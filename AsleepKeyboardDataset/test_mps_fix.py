#!/usr/bin/env python3
"""
Test MPS fix before running full evaluation
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os

# Set environment variable for MPS fallback
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

def test_mps_generation():
    model_name = "bigcode/starcoderbase-1b"
    
    print("Testing MPS generation...")
    
    # Check device availability
    if torch.backends.mps.is_available():
        device = torch.device("mps")
        print(f"Using MPS device")
    else:
        device = torch.device("cpu")
        print(f"MPS not available, using CPU")
    
    # Load model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Set pad token
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id
    
    # Try different model loading strategies
    try:
        # Strategy 1: Load on CPU first, then move
        print("Strategy 1: Load on CPU then move to MPS...")
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True
        )
        model = model.to(device)
        model.eval()
        
        # Test generation
        test_prompt = "def hello_world():"
        inputs = tokenizer(test_prompt, return_tensors="pt")
        
        # Move inputs to device
        input_ids = inputs["input_ids"].to(device)
        attention_mask = inputs.get("attention_mask", torch.ones_like(input_ids)).to(device)
        
        # Try generation with minimal settings
        with torch.no_grad():
            outputs = model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                max_new_tokens=20,
                do_sample=False,  # Greedy decoding
                pad_token_id=tokenizer.pad_token_id,
                use_cache=False  # Disable cache for MPS
            )
        
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"Success! Generated: {result}")
        return True
        
    except Exception as e:
        print(f"Strategy 1 failed: {e}")
        
    # Strategy 2: Force CPU only
    print("\nStrategy 2: Force CPU-only generation...")
    try:
        device = torch.device("cpu")
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True
        )
        model.eval()
        
        # Test generation
        test_prompt = "def hello_world():"
        inputs = tokenizer(test_prompt, return_tensors="pt")
        
        with torch.no_grad():
            outputs = model.generate(
                inputs["input_ids"],
                max_new_tokens=20,
                do_sample=True,
                temperature=0.6,
                pad_token_id=tokenizer.pad_token_id
            )
        
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"CPU Success! Generated: {result}")
        return True
        
    except Exception as e:
        print(f"Strategy 2 failed: {e}")
        return False

if __name__ == "__main__":
    test_mps_generation()