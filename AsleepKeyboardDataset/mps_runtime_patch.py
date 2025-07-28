#!/usr/bin/env python3
"""
Runtime patch for MPS - directly modifies the transformers module
"""

import torch
import os
import sys

# Enable MPS fallback
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

def patch_transformers_before_import():
    """Patch transformers before it's fully imported"""
    
    # Define the fixed function
    def fixed_isin_mps_friendly(elements, test_elements):
        """Fixed version that handles all MPS edge cases"""
        
        # Convert non-tensor to tensor
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
        
        # MPS workaround for older PyTorch
        # Handle scalar tensors
        if test_elements.dim() == 0:
            test_elements = test_elements.unsqueeze(0)
        
        # Flatten for comparison
        elements_flat = elements.flatten()
        test_elements_flat = test_elements.flatten()
        
        # Handle empty cases
        if elements_flat.numel() == 0 or test_elements_flat.numel() == 0:
            return torch.zeros_like(elements, dtype=torch.bool)
        
        # Use broadcasting for comparison
        # This avoids the problematic tile operation
        result = torch.zeros_like(elements_flat, dtype=torch.bool)
        
        # For small test_elements, use a loop (more stable on MPS)
        if test_elements_flat.numel() <= 10:
            for test_val in test_elements_flat:
                result = result | (elements_flat == test_val)
        else:
            # For larger arrays, use broadcasting
            elements_expanded = elements_flat.unsqueeze(1)  # Shape: [n, 1]
            test_expanded = test_elements_flat.unsqueeze(0)  # Shape: [1, m]
            matches = elements_expanded == test_expanded  # Shape: [n, m]
            result = matches.any(dim=1)
        
        # Restore original shape
        return result.reshape(elements.shape)
    
    # Import transformers modules
    import transformers.pytorch_utils
    
    # Replace the function
    transformers.pytorch_utils.isin_mps_friendly = fixed_isin_mps_friendly
    
    print("✅ Successfully patched transformers.pytorch_utils.isin_mps_friendly")
    
    # Verify the patch
    test_elem = torch.tensor([1, 2, 3], device="mps" if torch.backends.mps.is_available() else "cpu")
    test_val = torch.tensor(2, device=test_elem.device)
    try:
        result = transformers.pytorch_utils.isin_mps_friendly(test_elem, test_val)
        print(f"✅ Patch verification successful: {result}")
    except Exception as e:
        print(f"❌ Patch verification failed: {e}")

# Apply the patch FIRST
patch_transformers_before_import()

# Now we can safely import and use transformers
from transformers import AutoTokenizer, AutoModelForCausalLM
import warnings
warnings.filterwarnings("ignore")

def test_mps_generation():
    """Test MPS generation with patched transformers"""
    print("\n=== Testing MPS Generation ===\n")
    
    if not torch.backends.mps.is_available():
        print("MPS not available on this system")
        return False
    
    device = torch.device("mps")
    model_name = "bigcode/starcoderbase-1b"
    
    # Load tokenizer and model
    print("Loading model...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id
    
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float32,
        low_cpu_mem_usage=True
    ).to(device)
    model.eval()
    print(f"Model loaded on {device}\n")
    
    # Test cases
    test_prompts = [
        "def factorial(n):",
        "class Person:\n    def __init__(self, name):",
        "# Calculate the sum of two numbers\ndef add(x, y):",
        "import sqlite3\n\ndef get_user_by_id(user_id):\n    conn = sqlite3.connect('users.db')\n    query = \""
    ]
    
    success_count = 0
    for i, prompt in enumerate(test_prompts, 1):
        print(f"Test {i}: {prompt[:50]}...")
        
        try:
            inputs = tokenizer(prompt, return_tensors="pt", padding=True)
            input_ids = inputs["input_ids"].to(device)
            attention_mask = inputs.get("attention_mask")
            if attention_mask is not None:
                attention_mask = attention_mask.to(device)
            
            with torch.no_grad():
                outputs = model.generate(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    max_new_tokens=40,
                    temperature=0.6,
                    do_sample=True,
                    pad_token_id=tokenizer.pad_token_id,
                    eos_token_id=tokenizer.eos_token_id,
                    use_cache=True
                )
            
            generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
            completion = generated[len(prompt):]
            
            print(f"✅ Success! Generated: ...{completion[:60]}...")
            success_count += 1
            
        except Exception as e:
            print(f"❌ Failed: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\nResults: {success_count}/{len(test_prompts)} generations succeeded")
    return success_count == len(test_prompts)

def create_production_ready_script():
    """Create a production-ready evaluation script"""
    
    script_content = '''#!/usr/bin/env python3
"""
Production-ready MPS evaluation script
Auto-patches transformers for MPS compatibility
"""

import torch
import os
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

# Apply MPS patch
def patch_mps():
    def fixed_isin_mps_friendly(elements, test_elements):
        if not isinstance(test_elements, torch.Tensor):
            test_elements = torch.tensor(test_elements, device=elements.device, dtype=elements.dtype)
        
        if elements.device.type != "mps":
            return torch.isin(elements, test_elements)
        
        # MPS workaround
        if test_elements.dim() == 0:
            test_elements = test_elements.unsqueeze(0)
        
        elements_flat = elements.flatten()
        result = torch.zeros_like(elements_flat, dtype=torch.bool)
        
        for test_val in test_elements.flatten():
            result = result | (elements_flat == test_val)
        
        return result.reshape(elements.shape)
    
    import transformers.pytorch_utils
    transformers.pytorch_utils.isin_mps_friendly = fixed_isin_mps_friendly

patch_mps()

# Now import and use transformers normally
from transformers import AutoTokenizer, AutoModelForCausalLM

# Your evaluation code here...
'''
    
    with open("mps_production_template.py", "w") as f:
        f.write(script_content)
    
    print("\n✅ Created mps_production_template.py for production use")

if __name__ == "__main__":
    # Test the patched generation
    success = test_mps_generation()
    
    if success:
        print("\n🎉 MPS generation is fully working!")
        create_production_ready_script()
        print("\nYou can now use MPS for transformer generation by:")
        print("1. Applying the patch at the start of your script")
        print("2. Using the mps_production_template.py as a base")
    else:
        print("\n⚠️  MPS still has issues. Investigating further...")