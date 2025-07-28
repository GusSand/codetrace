#!/usr/bin/env python3
"""
Aggressive fix for MPS generation - patches at module load time
"""

import sys
import types
import torch
import os

# Enable MPS fallback
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

# Define the fixed function BEFORE importing transformers
def fixed_isin_mps_friendly(elements: torch.Tensor, test_elements: torch.Tensor) -> torch.Tensor:
    """Fixed version that handles all edge cases"""
    
    # Check PyTorch version
    try:
        is_torch_2_4_plus = tuple(int(x) for x in torch.__version__.split('.')[:2]) >= (2, 4)
    except:
        is_torch_2_4_plus = False
    
    if elements.device.type == "mps" and not is_torch_2_4_plus:
        # Convert int to tensor if needed
        if isinstance(test_elements, int):
            test_elements = torch.tensor([test_elements], device=elements.device)
        
        # Ensure tensors have dimensions
        if test_elements.dim() == 0:
            test_elements = test_elements.unsqueeze(0)
        if elements.dim() == 0:
            elements = elements.unsqueeze(0)
            
        # Handle empty tensors
        if test_elements.numel() == 0:
            return torch.zeros_like(elements, dtype=torch.bool)
        
        # MPS-friendly implementation
        # Expand elements to match test_elements
        expanded = elements.unsqueeze(0).expand(test_elements.shape[0], -1)
        test_expanded = test_elements.unsqueeze(1).expand(-1, elements.shape[0])
        
        # Compare and reduce
        result = (expanded == test_expanded).any(dim=0)
        
        return result
    else:
        # Use native torch.isin for newer versions or non-MPS
        return torch.isin(elements, test_elements)

# Create a custom module loader
class TransformersPatcher:
    @staticmethod
    def patch_pytorch_utils():
        """Patch the pytorch_utils module after it's imported"""
        import transformers.pytorch_utils
        transformers.pytorch_utils.isin_mps_friendly = fixed_isin_mps_friendly
        print("✓ Patched transformers.pytorch_utils.isin_mps_friendly")
    
    @staticmethod
    def patch_on_import():
        """Set up import hooks to patch transformers when loaded"""
        original_import = __builtins__.__import__
        
        def patched_import(name, *args, **kwargs):
            module = original_import(name, *args, **kwargs)
            
            # Patch after transformers.pytorch_utils is imported
            if name == "transformers.pytorch_utils" or (hasattr(module, '__name__') and module.__name__ == "transformers.pytorch_utils"):
                module.isin_mps_friendly = fixed_isin_mps_friendly
                print(f"✓ Patched {name}.isin_mps_friendly on import")
            
            return module
        
        __builtins__.__import__ = patched_import

# Apply the import hook
TransformersPatcher.patch_on_import()

# Now import transformers - it will be patched automatically
from transformers import AutoTokenizer, AutoModelForCausalLM

# Also patch directly in case it's already loaded
TransformersPatcher.patch_pytorch_utils()

def test_mps_generation_with_fix():
    """Test MPS generation with aggressive patching"""
    print("\n=== Testing MPS Generation with Aggressive Fix ===\n")
    
    if not torch.backends.mps.is_available():
        print("MPS not available")
        return False
    
    device = torch.device("mps")
    
    # Test the patch directly
    print("1. Testing patched function:")
    try:
        import transformers.pytorch_utils
        
        # Test scalar
        elements = torch.tensor([1, 2, 3], device=device)
        test_scalar = torch.tensor(2, device=device)
        result = transformers.pytorch_utils.isin_mps_friendly(elements, test_scalar)
        print(f"   Scalar test: {result}")
        
        # Test with int
        result = transformers.pytorch_utils.isin_mps_friendly(elements, 2)
        print(f"   Int test: {result}")
        
        print("   ✓ Patched function works\n")
    except Exception as e:
        print(f"   ✗ Patch test failed: {e}\n")
        return False
    
    # Load model
    print("2. Loading model...")
    model_name = "bigcode/starcoderbase-1b"
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        if tokenizer.pad_token_id is None:
            tokenizer.pad_token_id = tokenizer.eos_token_id
        
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True
        ).to(device)
        model.eval()
        
        print(f"   ✓ Model loaded on {device}\n")
    except Exception as e:
        print(f"   ✗ Model loading failed: {e}")
        return False
    
    # Test generation
    print("3. Testing generation:")
    success_count = 0
    test_prompts = [
        "def hello_world():",
        "def calculate_sum(a, b):",
        "# SQL query function\ndef execute_query(query):"
    ]
    
    for prompt in test_prompts:
        try:
            inputs = tokenizer(prompt, return_tensors="pt")
            input_ids = inputs["input_ids"].to(device)
            
            with torch.no_grad():
                outputs = model.generate(
                    input_ids=input_ids,
                    max_new_tokens=30,
                    temperature=0.6,
                    do_sample=True,
                    pad_token_id=tokenizer.pad_token_id
                )
            
            result = tokenizer.decode(outputs[0], skip_special_tokens=True)
            print(f"   ✓ Generated: {result[:80]}...")
            success_count += 1
            
        except Exception as e:
            print(f"   ✗ Failed: {e}")
    
    print(f"\n{'✅' if success_count == len(test_prompts) else '⚠️ '} {success_count}/{len(test_prompts)} generations succeeded")
    return success_count == len(test_prompts)

def create_mps_enabled_evaluator():
    """Create an evaluator that works with MPS"""
    
    class MPSEnabledEvaluator:
        def __init__(self):
            self.device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
            self.model = None
            self.tokenizer = None
            
        def setup(self, model_name="bigcode/starcoderbase-1b"):
            """Setup model with MPS support"""
            print(f"Setting up model on {self.device}...")
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            if self.tokenizer.pad_token_id is None:
                self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
            
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float32,
                low_cpu_mem_usage=True
            ).to(self.device)
            self.model.eval()
            
            return self
            
        def generate(self, prompt, **kwargs):
            """Generate with MPS support"""
            inputs = self.tokenizer(prompt, return_tensors="pt")
            input_ids = inputs["input_ids"].to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    input_ids=input_ids,
                    pad_token_id=self.tokenizer.pad_token_id,
                    **kwargs
                )
            
            result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return result[len(prompt):]
    
    return MPSEnabledEvaluator()

if __name__ == "__main__":
    # Run comprehensive test
    success = test_mps_generation_with_fix()
    
    if success:
        print("\n🎉 MPS is now fully working! Creating evaluator...")
        evaluator = create_mps_enabled_evaluator()
        evaluator.setup()
        
        # Test the evaluator
        test_result = evaluator.generate("def fibonacci(n):", max_new_tokens=50)
        print(f"\nEvaluator test: {test_result[:100]}...")
        
        print("\n✅ MPS generation is fully functional!")
    else:
        print("\n❌ MPS fix did not work completely. Falling back to CPU is recommended.")