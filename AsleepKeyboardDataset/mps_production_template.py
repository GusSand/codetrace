#!/usr/bin/env python3
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
