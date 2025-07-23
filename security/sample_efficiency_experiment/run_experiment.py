#!/usr/bin/env python3
"""
Quick runner script for the sample efficiency experiment.
"""

import sys
import os
from pathlib import Path

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sample_efficiency_experiment import main

if __name__ == "__main__":
    print("🚀 Running Sample Efficiency Experiment...")
    print("=" * 50)
    
    # Run with default settings
    exit_code = main()
    
    if exit_code == 0:
        print("\n✅ Experiment completed successfully!")
        print("📁 Check the output directory for results:")
        print("   - security/sample_efficiency_experiment/")
    else:
        print("\n❌ Experiment failed!")
    
    sys.exit(exit_code) 