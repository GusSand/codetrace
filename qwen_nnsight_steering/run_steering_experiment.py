#!/usr/bin/env python3
"""
Streamlined Steering Experiment Runner
Runs comprehensive steering experiments using existing or newly created vectors

Usage:
    python run_steering_experiment.py --quick  # Quick test with existing vectors
    python run_steering_experiment.py --full   # Full experiment with all CWEs
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# Add parent directory for imports
sys.path.append(str(Path(__file__).parent.parent))

from comprehensive_steering_experiment import ComprehensiveSteeringExperiment, ExperimentConfig
from example_with_secllmholmes import create_cwe_specific_vectors, SecLLMHolmesDataLoader

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_existing_vectors():
    """Check which steering vectors already exist."""
    vectors_dir = Path("vectors")
    if not vectors_dir.exists():
        return []
    
    existing_vectors = []
    for vector_file in vectors_dir.glob("*_steering_vectors.pt"):
        cwe_id = vector_file.stem.replace("_steering_vectors", "")
        existing_vectors.append(cwe_id)
    
    return existing_vectors

def create_missing_vectors(target_cwes, use_small_model=False):
    """Create steering vectors for missing CWEs."""
    logger.info("🔧 Creating missing steering vectors...")
    
    existing_vectors = check_existing_vectors()
    missing_cwes = [cwe for cwe in target_cwes if cwe not in existing_vectors]
    
    if not missing_cwes:
        logger.info("✅ All required steering vectors already exist")
        return True
    
    logger.info(f"📋 Creating vectors for: {missing_cwes}")
    
    success_count = 0
    for cwe_id in missing_cwes:
        try:
            logger.info(f"🔄 Creating vectors for {cwe_id}")
            vectors = create_cwe_specific_vectors(cwe_id, use_small_model)
            if vectors:
                success_count += 1
                logger.info(f"✅ Successfully created vectors for {cwe_id}")
            else:
                logger.warning(f"⚠️ Failed to create vectors for {cwe_id}")
        except Exception as e:
            logger.error(f"❌ Error creating vectors for {cwe_id}: {e}")
    
    logger.info(f"📊 Created {success_count}/{len(missing_cwes)} missing vectors")
    return success_count == len(missing_cwes)

def run_quick_experiment():
    """Run a quick experiment using existing vectors."""
    logger.info("🚀 Running Quick Steering Experiment")
    
    # Use existing vectors for priority CWEs
    existing_vectors = check_existing_vectors()
    if not existing_vectors:
        logger.error("❌ No existing steering vectors found. Run with --create-vectors first.")
        return
    
    logger.info(f"📋 Using existing vectors: {existing_vectors}")
    
    # Configure for quick experiment
    config = ExperimentConfig(
        model_name="Qwen/Qwen2.5-14B-Instruct",
        steering_strength=20.0,
        target_layers=[12, 24, 36, 47],
        max_examples_per_cwe=5,  # Reduced for quick test
        results_dir="results_quick"
    )
    
    experiment = ComprehensiveSteeringExperiment(config)
    experiment.run_comprehensive_experiment()

def run_full_experiment():
    """Run full experiment with all CWEs."""
    logger.info("🚀 Running Full Steering Experiment")
    
    # Target all available CWEs
    target_cwes = ["cwe-22", "cwe-77", "cwe-79", "cwe-89", "cwe-190", "cwe-416", "cwe-476", "cwe-787"]
    
    # Create missing vectors
    if not create_missing_vectors(target_cwes):
        logger.warning("⚠️ Some vectors could not be created, continuing with available ones")
    
    # Configure for full experiment
    config = ExperimentConfig(
        model_name="Qwen/Qwen2.5-14B-Instruct",
        steering_strength=20.0,
        target_layers=[12, 24, 36, 47],
        max_examples_per_cwe=10,
        results_dir="results_full"
    )
    
    experiment = ComprehensiveSteeringExperiment(config)
    experiment.run_comprehensive_experiment()

def run_focused_experiment():
    """Run focused experiment on challenging CWEs."""
    logger.info("🎯 Running Focused Experiment on Challenging CWEs")
    
    # Focus on CWEs that showed lower performance in baseline
    challenging_cwes = ["cwe-476", "cwe-77", "cwe-79"]  # NULL pointer, command injection, XSS
    
    # Create vectors for challenging CWEs
    if not create_missing_vectors(challenging_cwes):
        logger.warning("⚠️ Some challenging CWE vectors could not be created")
    
    # Configure for focused experiment
    config = ExperimentConfig(
        model_name="Qwen/Qwen2.5-14B-Instruct",
        steering_strength=20.0,
        target_layers=[12, 24, 36, 47],
        max_examples_per_cwe=8,
        results_dir="results_focused"
    )
    
    experiment = ComprehensiveSteeringExperiment(config)
    experiment.run_comprehensive_experiment()

def create_all_vectors():
    """Create steering vectors for all CWEs."""
    logger.info("🔧 Creating Steering Vectors for All CWEs")
    
    target_cwes = ["cwe-22", "cwe-77", "cwe-79", "cwe-89", "cwe-190", "cwe-416", "cwe-476", "cwe-787"]
    
    # Check what already exists
    existing_vectors = check_existing_vectors()
    logger.info(f"📋 Existing vectors: {existing_vectors}")
    
    # Create all vectors
    success = create_missing_vectors(target_cwes)
    
    if success:
        logger.info("✅ All steering vectors created successfully")
    else:
        logger.warning("⚠️ Some vectors could not be created")
    
    # List final status
    final_vectors = check_existing_vectors()
    logger.info(f"📊 Final vector count: {len(final_vectors)}")
    for cwe in final_vectors:
        logger.info(f"   ✅ {cwe}")

def main():
    parser = argparse.ArgumentParser(description="Run comprehensive steering experiments")
    parser.add_argument("--quick", action="store_true", 
                       help="Run quick experiment with existing vectors")
    parser.add_argument("--full", action="store_true",
                       help="Run full experiment with all CWEs")
    parser.add_argument("--focused", action="store_true",
                       help="Run focused experiment on challenging CWEs")
    parser.add_argument("--create-vectors", action="store_true",
                       help="Create steering vectors for all CWEs")
    parser.add_argument("--small-model", action="store_true",
                       help="Use smaller Qwen model for vector creation")
    parser.add_argument("--check-vectors", action="store_true",
                       help="Check which steering vectors exist")
    
    args = parser.parse_args()
    
    if args.check_vectors:
        existing = check_existing_vectors()
        logger.info(f"📋 Existing steering vectors: {existing}")
        return
    
    if args.create_vectors:
        create_all_vectors()
        return
    
    if args.quick:
        run_quick_experiment()
    elif args.focused:
        run_focused_experiment()
    elif args.full:
        run_full_experiment()
    else:
        # Default: run quick experiment
        logger.info("🎯 Running default quick experiment")
        run_quick_experiment()

if __name__ == "__main__":
    main() 