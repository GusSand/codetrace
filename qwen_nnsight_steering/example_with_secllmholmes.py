#!/usr/bin/env python3
"""
Example: Creating CWE-specific steering vectors with real SecLLMHolmes data
This follows the proven methodology from the breakthrough research.
"""

import os
import sys
import json
import torch
import logging
from pathlib import Path
from typing import List, Dict

# Add parent directory for imports
sys.path.append(str(Path(__file__).parent.parent))

from qwen_steering_integration import QwenNNSightSteering, QwenSteeringConfig

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SecLLMHolmesDataLoader:
    """Load and process SecLLMHolmes vulnerability dataset."""
    
    def __init__(self, dataset_base_path: str = "../security/SecLLMHolmes/datasets"):
        self.dataset_base_path = Path(dataset_base_path)
        self.cwe_names = {
            "cwe-22": "Path Traversal",
            "cwe-77": "Command Injection",
            "cwe-79": "Cross-site Scripting", 
            "cwe-89": "SQL Injection",
            "cwe-190": "Integer Overflow",
            "cwe-416": "Use After Free",
            "cwe-476": "NULL Pointer Dereference",
            "cwe-787": "Out-of-bounds Write"
        }
    
    def load_cwe_data(self, cwe_id: str) -> Dict[str, List[Dict]]:
        """Load vulnerable and secure examples for a specific CWE."""
        cwe_data = {"vulnerable": [], "secure": []}
        
        # Convert to uppercase format (CWE-77 not cwe-77)
        cwe_upper = cwe_id.upper() if not cwe_id.startswith('CWE-') else cwe_id
        if not cwe_upper.startswith('CWE-'):
            cwe_upper = cwe_upper.replace('cwe-', 'CWE-')
        
        # Look for SecLLMHolmes dataset structure
        cwe_path = self.dataset_base_path / "hand-crafted" / "dataset" / cwe_upper
        
        if not cwe_path.exists():
            logger.warning(f"⚠️ CWE path not found: {cwe_path}")
            return cwe_data
        
        # Load vulnerable examples (numbered files: 1.c, 2.c, 3.c, etc.)
        for file_path in cwe_path.glob("[0-9]*.c"):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    cwe_data["vulnerable"].append({
                        "content": content,
                        "label": "vulnerable",
                        "cwe": cwe_upper,
                        "file": str(file_path.name)
                    })
            except Exception as e:
                logger.warning(f"⚠️ Error reading {file_path}: {e}")
        
        # Also check for Python files
        for file_path in cwe_path.glob("[0-9]*.py"):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    cwe_data["vulnerable"].append({
                        "content": content,
                        "label": "vulnerable",
                        "cwe": cwe_upper,
                        "file": str(file_path.name)
                    })
            except Exception as e:
                logger.warning(f"⚠️ Error reading {file_path}: {e}")
        
        # Load secure examples (patched files: p_1.c, p_2.c, p_3.c, etc.)
        for file_path in cwe_path.glob("p_*.c"):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    cwe_data["secure"].append({
                        "content": content,
                        "label": "secure", 
                        "cwe": cwe_upper,
                        "file": str(file_path.name)
                    })
            except Exception as e:
                logger.warning(f"⚠️ Error reading {file_path}: {e}")
        
        # Also check for Python patched files
        for file_path in cwe_path.glob("p_*.py"):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    cwe_data["secure"].append({
                        "content": content,
                        "label": "secure", 
                        "cwe": cwe_upper,
                        "file": str(file_path.name)
                    })
            except Exception as e:
                logger.warning(f"⚠️ Error reading {file_path}: {e}")
        
        logger.info(f"📊 Loaded {cwe_upper}: {len(cwe_data['vulnerable'])} vulnerable, {len(cwe_data['secure'])} secure")
        return cwe_data
    
    def get_available_cwes(self) -> List[str]:
        """Get list of available CWE directories."""
        dataset_path = self.dataset_base_path / "hand-crafted" / "dataset"
        if not dataset_path.exists():
            logger.warning(f"⚠️ Dataset path not found: {dataset_path}")
            return []
        
        cwes = []
        for cwe_dir in dataset_path.iterdir():
            if cwe_dir.is_dir() and cwe_dir.name.startswith("cwe-"):
                cwes.append(cwe_dir.name)
        
        return sorted(cwes)

def create_cwe_specific_vectors(cwe_id: str, use_small_model: bool = False):
    """Create steering vectors for a specific CWE using real data."""
    logger.info(f"🎯 Creating steering vectors for {cwe_id}")
    
    # Load data
    data_loader = SecLLMHolmesDataLoader()
    cwe_data = data_loader.load_cwe_data(cwe_id)
    
    if not cwe_data["vulnerable"] or not cwe_data["secure"]:
        logger.error(f"❌ Insufficient data for {cwe_id}")
        return None
    
    # Configure model
    config = QwenSteeringConfig()
    if use_small_model:
        config.model_name = "Qwen/Qwen2.5-1.5B-Instruct"
        config.hidden_dim = 1536
        config.target_layers = [4, 8, 12, 23]
    
    # Create steering vectors
    try:
        steerer = QwenNNSightSteering(config)
        steerer.load_model()
        
        steering_vectors = steerer.create_steering_vectors(
            vulnerable_examples=cwe_data["vulnerable"],
            secure_examples=cwe_data["secure"],
            cwe_type=cwe_id
        )
        
        if steering_vectors:
            # Save vectors
            output_path = f"vectors/{cwe_id}_steering_vectors.pt"
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            metadata = {
                "cwe_id": cwe_id,
                "cwe_name": data_loader.cwe_names.get(cwe_id, "Unknown"),
                "vulnerable_count": len(cwe_data["vulnerable"]),
                "secure_count": len(cwe_data["secure"]),
                "model_name": config.model_name,
                "creation_method": "qwen_nnsight_integration"
            }
            
            steerer.save_steering_vectors(steering_vectors, output_path, metadata)
            
            logger.info(f"✅ Successfully created and saved {cwe_id} steering vectors")
            return steering_vectors
        else:
            logger.error(f"❌ Failed to create steering vectors for {cwe_id}")
            return None
            
    except Exception as e:
        logger.error(f"❌ Error creating vectors for {cwe_id}: {e}")
        return None

def create_multiple_cwe_vectors(cwe_list: List[str], use_small_model: bool = False):
    """Create steering vectors for multiple CWEs."""
    logger.info(f"🚀 Creating steering vectors for {len(cwe_list)} CWEs...")
    
    results = {}
    
    for cwe_id in cwe_list:
        logger.info(f"\n{'='*60}")
        logger.info(f"🔄 Processing {cwe_id}")
        logger.info(f"{'='*60}")
        
        vectors = create_cwe_specific_vectors(cwe_id, use_small_model)
        results[cwe_id] = vectors is not None
        
        # Memory cleanup between CWEs
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    
    # Summary
    logger.info(f"\n{'='*60}")
    logger.info("📊 STEERING VECTOR CREATION SUMMARY")
    logger.info(f"{'='*60}")
    
    success_count = sum(results.values())
    for cwe_id, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        logger.info(f"{status} {cwe_id}")
    
    logger.info(f"\n🎯 Overall: {success_count}/{len(cwe_list)} CWEs successful")
    
    return results

def demonstrate_vector_analysis():
    """Demonstrate analysis of created steering vectors."""
    logger.info("🔍 Analyzing created steering vectors...")
    
    config = QwenSteeringConfig()
    steerer = QwenNNSightSteering(config)
    
    vector_files = list(Path("vectors").glob("*_steering_vectors.pt"))
    
    if not vector_files:
        logger.warning("⚠️ No steering vector files found")
        return
    
    for vector_file in vector_files:
        try:
            vectors, metadata = steerer.load_steering_vectors(str(vector_file))
            
            cwe_id = metadata.get("cwe_id", "unknown")
            cwe_name = metadata.get("cwe_name", "Unknown")
            
            logger.info(f"\n📊 Analysis for {cwe_id} ({cwe_name}):")
            logger.info(f"   Model: {metadata.get('model_name', 'unknown')}")
            logger.info(f"   Data: {metadata.get('vulnerable_count', '?')} vulnerable, {metadata.get('secure_count', '?')} secure")
            
            for layer_name, vector in vectors.items():
                norm = torch.norm(vector).item()
                mean_abs = torch.mean(torch.abs(vector)).item()
                logger.info(f"   {layer_name}: norm={norm:.4f}, mean_abs={mean_abs:.6f}")
                
        except Exception as e:
            logger.error(f"❌ Error analyzing {vector_file}: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Create CWE-specific steering vectors with SecLLMHolmes data")
    parser.add_argument("--cwe", type=str, help="Specific CWE to process (e.g., cwe-22)")
    parser.add_argument("--cwe-list", nargs="+", help="List of CWEs to process")
    parser.add_argument("--all-available", action="store_true", help="Process all available CWEs")
    parser.add_argument("--small-model", action="store_true", help="Use smaller Qwen model")
    parser.add_argument("--analyze", action="store_true", help="Analyze existing steering vectors")
    parser.add_argument("--dataset-path", type=str, default="../security/SecLLMHolmes/datasets",
                       help="Path to SecLLMHolmes dataset")
    
    args = parser.parse_args()
    
    if args.analyze:
        demonstrate_vector_analysis()
    elif args.cwe:
        create_cwe_specific_vectors(args.cwe, args.small_model)
    elif args.cwe_list:
        create_multiple_cwe_vectors(args.cwe_list, args.small_model)
    elif args.all_available:
        data_loader = SecLLMHolmesDataLoader(args.dataset_path)
        available_cwes = data_loader.get_available_cwes()
        
        if available_cwes:
            logger.info(f"📋 Found {len(available_cwes)} available CWEs: {available_cwes}")
            # Process a subset to avoid overwhelming the system
            priority_cwes = ["cwe-22", "cwe-77", "cwe-79", "cwe-89"]  # From breakthrough research
            target_cwes = [cwe for cwe in priority_cwes if cwe in available_cwes]
            
            if target_cwes:
                logger.info(f"🎯 Processing priority CWEs: {target_cwes}")
                create_multiple_cwe_vectors(target_cwes, args.small_model) 
            else:
                logger.info(f"🔄 Processing first 4 available CWEs: {available_cwes[:4]}")
                create_multiple_cwe_vectors(available_cwes[:4], args.small_model)
        else:
            logger.error("❌ No CWE directories found in dataset")
    else:
        # Default: create vectors for command injection (proven most effective)
        logger.info("🎯 Running default: Creating vectors for CWE-77 (Command Injection)")
        create_cwe_specific_vectors("cwe-77", args.small_model) 