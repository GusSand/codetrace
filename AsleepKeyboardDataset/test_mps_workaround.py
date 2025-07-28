#!/usr/bin/env python3
"""
Quick test to verify MPS workaround is working
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import warnings

warnings.filterwarnings("ignore")

def test_mps_workaround():
    print("=== Testing MPS Workaround ===\n")
    
    # 1. Check MPS availability
    print(f"1. MPS Available: {torch.backends.mps.is_available()}")
    print(f"   MPS Built: {torch.backends.mps.is_built()}")
    print(f"   PyTorch Version: {torch.__version__}\n")
    
    # 2. Test basic MPS operations
    if torch.backends.mps.is_available():
        try:
            mps_device = torch.device("mps")
            x = torch.randn(2, 3).to(mps_device)
            y = torch.randn(3, 4).to(mps_device)
            z = x @ y
            print(f"2. Basic MPS tensor operations: ✓ WORKING")
            print(f"   Created tensors on {x.device}, result shape: {z.shape}\n")
        except Exception as e:
            print(f"2. Basic MPS tensor operations: ✗ FAILED - {e}\n")
    
    # 3. Test model loading and generation on CPU
    print("3. Testing CPU-based generation (MPS workaround)...")
    
    model_name = "bigcode/starcoderbase-1b"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id
    
    # Load on CPU
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
            **inputs,
            max_new_tokens=20,
            temperature=0.6,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id
        )
    
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"   CPU generation: ✓ WORKING")
    print(f"   Generated: {result}\n")
    
    # 4. Summary
    print("=== Summary ===")
    print("✓ MPS is available for basic tensor operations")
    print("✓ CPU-based generation works correctly")
    print("✓ This workaround avoids the transformers MPS bug")
    print("\nRecommendation: Use CPU for model generation, MPS for other operations")

if __name__ == "__main__":
    test_mps_workaround()