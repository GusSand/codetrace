#!/usr/bin/env python3
"""
Debug and fix MPS issues with detailed tensor inspection
"""

import torch
import os
import sys

# Enable MPS fallback
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

def debug_isin_mps_friendly():
    """Debug the actual tensor shapes causing issues"""
    print("=== Debugging isin_mps_friendly ===\n")
    
    # Import and inspect current implementation
    import transformers.pytorch_utils
    original_fn = transformers.pytorch_utils.isin_mps_friendly
    
    # Create a debugging wrapper
    def debug_wrapper(elements, test_elements):
        print(f"[DEBUG] isin_mps_friendly called:")
        print(f"  elements: shape={elements.shape}, dtype={elements.dtype}, device={elements.device}")
        print(f"  test_elements: type={type(test_elements)}", end="")
        if isinstance(test_elements, torch.Tensor):
            print(f", shape={test_elements.shape}, dtype={test_elements.dtype}, device={test_elements.device}")
        else:
            print(f", value={test_elements}")
        
        try:
            result = original_fn(elements, test_elements)
            print(f"  result: shape={result.shape}")
            return result
        except Exception as e:
            print(f"  ERROR: {e}")
            raise
    
    # Apply debug wrapper
    transformers.pytorch_utils.isin_mps_friendly = debug_wrapper
    
    # Now test generation to see what's happening
    from transformers import AutoTokenizer, AutoModelForCausalLM
    
    model_name = "bigcode/starcoderbase-1b"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id
    
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    print(f"Using device: {device}\n")
    
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float32,
        low_cpu_mem_usage=True
    ).to(device)
    
    # Try generation
    prompt = "def test():"
    inputs = tokenizer(prompt, return_tensors="pt")
    input_ids = inputs["input_ids"].to(device)
    
    print("Attempting generation...\n")
    try:
        with torch.no_grad():
            outputs = model.generate(
                input_ids=input_ids,
                max_new_tokens=10,
                pad_token_id=tokenizer.pad_token_id
            )
        print("Generation succeeded!")
    except Exception as e:
        print(f"Generation failed: {e}")

def create_comprehensive_fix():
    """Create a comprehensive fix based on debugging"""
    
    def fixed_isin_mps_friendly(elements, test_elements):
        """Comprehensive fix for all edge cases"""
        
        # Handle non-tensor test_elements
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
        
        # MPS-specific implementation
        # Ensure proper dimensions
        elements_1d = elements.flatten()
        test_elements_1d = test_elements.flatten()
        
        # Handle empty cases
        if elements_1d.numel() == 0:
            return torch.zeros_like(elements, dtype=torch.bool)
        if test_elements_1d.numel() == 0:
            return torch.zeros_like(elements, dtype=torch.bool)
        
        # Simple but reliable MPS implementation
        # Create a mask for each test element
        result = torch.zeros_like(elements_1d, dtype=torch.bool)
        for test_val in test_elements_1d:
            result |= (elements_1d == test_val)
        
        # Reshape back to original shape
        return result.reshape(elements.shape)
    
    return fixed_isin_mps_friendly

def apply_comprehensive_fix():
    """Apply the comprehensive fix"""
    import transformers.pytorch_utils
    
    # Store original for fallback
    original_fn = transformers.pytorch_utils.isin_mps_friendly
    
    # Create fixed version
    fixed_fn = create_comprehensive_fix()
    
    # Apply patch
    transformers.pytorch_utils.isin_mps_friendly = fixed_fn
    print("✓ Applied comprehensive MPS fix\n")
    
    return original_fn

def test_fixed_generation():
    """Test generation with the fix"""
    from transformers import AutoTokenizer, AutoModelForCausalLM
    
    print("=== Testing Fixed MPS Generation ===\n")
    
    model_name = "bigcode/starcoderbase-1b"
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    
    # Load model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id
    
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float32,
        low_cpu_mem_usage=True
    ).to(device)
    model.eval()
    
    # Test prompts
    test_cases = [
        ("Simple function", "def hello():"),
        ("With parameters", "def add(a, b):"),
        ("Class definition", "class Calculator:"),
        ("SQL scenario", "import sqlite3\n\ndef query_db(user_input):"),
    ]
    
    success_count = 0
    for name, prompt in test_cases:
        print(f"\nTest: {name}")
        print(f"Prompt: {prompt}")
        
        try:
            inputs = tokenizer(prompt, return_tensors="pt")
            input_ids = inputs["input_ids"].to(device)
            
            with torch.no_grad():
                outputs = model.generate(
                    input_ids=input_ids,
                    max_new_tokens=50,
                    temperature=0.6,
                    do_sample=True,
                    pad_token_id=tokenizer.pad_token_id,
                    eos_token_id=tokenizer.eos_token_id
                )
            
            generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
            completion = generated[len(prompt):]
            
            print(f"✓ Success! Generated: {completion[:80]}...")
            success_count += 1
            
        except Exception as e:
            print(f"✗ Failed: {e}")
    
    print(f"\n{'✅' if success_count == len(test_cases) else '⚠️'} {success_count}/{len(test_cases)} tests passed")
    
    return success_count == len(test_cases)

if __name__ == "__main__":
    # First debug to understand the issue
    print("Step 1: Debugging the issue...\n")
    try:
        debug_isin_mps_friendly()
    except:
        pass
    
    print("\n" + "="*50 + "\n")
    
    # Apply comprehensive fix
    print("Step 2: Applying comprehensive fix...\n")
    original_fn = apply_comprehensive_fix()
    
    # Test the fix
    print("Step 3: Testing the fix...\n")
    success = test_fixed_generation()
    
    if success:
        print("\n🎉 MPS generation is now fully working!")
        print("\nThe fix uses a simple but reliable loop-based approach for MPS devices.")
        print("While slightly slower than the tensor operations, it's completely stable.")
    else:
        print("\n⚠️  Some issues remain. CPU fallback is still recommended for production.")