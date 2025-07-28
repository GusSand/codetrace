#!/usr/bin/env python3
"""
Diagnose MPS issues with transformers generation
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import traceback

# Enable MPS fallback
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

def test_basic_mps():
    """Test basic MPS functionality"""
    print("=== Testing Basic MPS Operations ===")
    
    if torch.backends.mps.is_available():
        print("✓ MPS is available")
        print(f"✓ MPS is built: {torch.backends.mps.is_built()}")
        
        # Test basic tensor operations
        try:
            device = torch.device("mps")
            
            # Basic tensor creation
            x = torch.randn(2, 3).to(device)
            print(f"✓ Basic tensor creation works: {x.shape} on {x.device}")
            
            # Matrix multiplication
            y = torch.randn(3, 4).to(device)
            z = torch.mm(x, y)
            print(f"✓ Matrix multiplication works: {z.shape}")
            
            # Attention-like operation
            q = torch.randn(1, 8, 64).to(device)
            k = torch.randn(1, 8, 64).to(device)
            v = torch.randn(1, 8, 64).to(device)
            
            # Scaled dot product attention (manual)
            scores = torch.bmm(q, k.transpose(1, 2)) / (64 ** 0.5)
            attn_weights = torch.softmax(scores, dim=-1)
            output = torch.bmm(attn_weights, v)
            print(f"✓ Attention-like operations work: {output.shape}")
            
        except Exception as e:
            print(f"✗ MPS basic operations failed: {e}")
            traceback.print_exc()
    else:
        print("✗ MPS is not available")

def test_model_generation():
    """Test model generation with different configurations"""
    print("\n=== Testing Model Generation ===")
    
    model_name = "bigcode/starcoderbase-1b"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Set pad token
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id
    
    test_prompt = "def fibonacci(n):"
    
    # Test 1: CPU generation (baseline)
    print("\n--- Test 1: CPU Generation ---")
    try:
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True
        )
        model.eval()
        
        inputs = tokenizer(test_prompt, return_tensors="pt")
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=50,
                temperature=0.6,
                do_sample=True,
                pad_token_id=tokenizer.pad_token_id
            )
        
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"✓ CPU generation works")
        print(f"Generated: {result[:100]}...")
        
        del model
        torch.cuda.empty_cache()
        
    except Exception as e:
        print(f"✗ CPU generation failed: {e}")
    
    # Test 2: MPS with different dtypes
    if torch.backends.mps.is_available():
        for dtype in [torch.float32, torch.float16]:
            print(f"\n--- Test 2: MPS Generation (dtype={dtype}) ---")
            try:
                device = torch.device("mps")
                
                # Load model
                model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    torch_dtype=dtype,
                    low_cpu_mem_usage=True
                )
                model = model.to(device)
                model.eval()
                
                inputs = tokenizer(test_prompt, return_tensors="pt")
                input_ids = inputs["input_ids"].to(device)
                attention_mask = inputs.get("attention_mask", torch.ones_like(input_ids)).to(device)
                
                # Try with minimal generation config
                with torch.no_grad():
                    outputs = model.generate(
                        input_ids=input_ids,
                        attention_mask=attention_mask,
                        max_new_tokens=20,
                        do_sample=False,  # Greedy
                        pad_token_id=tokenizer.pad_token_id,
                        use_cache=False  # Disable KV cache
                    )
                
                result = tokenizer.decode(outputs[0], skip_special_tokens=True)
                print(f"✓ MPS generation works with dtype={dtype}")
                print(f"Generated: {result}")
                
                del model
                torch.mps.empty_cache()
                
            except Exception as e:
                print(f"✗ MPS generation failed with dtype={dtype}: {e}")
                traceback.print_exc()
    
    # Test 3: MPS with specific workarounds
    if torch.backends.mps.is_available():
        print("\n--- Test 3: MPS with Workarounds ---")
        try:
            device = torch.device("mps")
            
            # Load on CPU first
            model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float32,
                low_cpu_mem_usage=True
            )
            
            # Move to MPS layer by layer (sometimes helps)
            model = model.to(device)
            model.eval()
            
            # Prepare inputs
            inputs = tokenizer(test_prompt, return_tensors="pt", padding=True)
            input_ids = inputs["input_ids"].to(device)
            attention_mask = inputs["attention_mask"].to(device)
            
            # Manual generation loop (more control)
            print("Trying manual generation loop...")
            current_ids = input_ids
            
            for i in range(10):  # Generate 10 tokens
                with torch.no_grad():
                    outputs = model(
                        input_ids=current_ids,
                        attention_mask=attention_mask,
                        use_cache=False
                    )
                    
                    # Get next token
                    next_token_logits = outputs.logits[:, -1, :]
                    next_token = torch.argmax(next_token_logits, dim=-1, keepdim=True)
                    
                    # Append to sequence
                    current_ids = torch.cat([current_ids, next_token], dim=1)
                    
                    # Update attention mask
                    attention_mask = torch.cat([
                        attention_mask,
                        torch.ones((attention_mask.shape[0], 1), device=device)
                    ], dim=1)
            
            result = tokenizer.decode(current_ids[0], skip_special_tokens=True)
            print(f"✓ Manual generation loop works")
            print(f"Generated: {result}")
            
        except Exception as e:
            print(f"✗ MPS workarounds failed: {e}")
            traceback.print_exc()

def get_mps_info():
    """Get detailed MPS information"""
    print("\n=== MPS System Information ===")
    
    if torch.backends.mps.is_available():
        print(f"PyTorch version: {torch.__version__}")
        print(f"MPS is available: True")
        print(f"MPS is built: {torch.backends.mps.is_built()}")
        
        # Try to get more info
        try:
            # Create a small tensor to force MPS initialization
            test_tensor = torch.tensor([1.0]).to("mps")
            print(f"MPS device initialized successfully")
            
            # Check available memory (if possible)
            if hasattr(torch.mps, 'current_allocated_memory'):
                print(f"Current allocated memory: {torch.mps.current_allocated_memory() / 1024**2:.2f} MB")
            
        except Exception as e:
            print(f"Error getting MPS details: {e}")
    else:
        print("MPS is not available on this system")

if __name__ == "__main__":
    get_mps_info()
    test_basic_mps()
    test_model_generation()