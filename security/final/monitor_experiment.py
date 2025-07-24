#!/usr/bin/env python3
"""
Monitor the comprehensive baseline experiment progress.
Checks for intermediate results and provides status updates.
"""

import json
import time
from pathlib import Path
from datetime import datetime
import glob

def monitor_experiment():
    """Monitor the comprehensive experiment progress."""
    print("🔍 Monitoring Comprehensive Baseline Experiment")
    print("=" * 60)
    
    results_dir = Path("comprehensive_results")
    
    while True:
        # Check for intermediate trial results
        trial_files = list(results_dir.glob("*_trial_*.json"))
        complete_files = list(results_dir.glob("*_complete_*.json"))
        comprehensive_files = list(results_dir.glob("comprehensive_results_*.json"))
        
        print(f"⏰ {datetime.now().strftime('%H:%M:%S')} - Status Update:")
        print(f"   📄 Trial files: {len(trial_files)}")
        print(f"   ✅ Complete model files: {len(complete_files)}")
        print(f"   🎯 Comprehensive results: {len(comprehensive_files)}")
        
        if trial_files:
            print("\n📊 Latest Trial Results:")
            for trial_file in sorted(trial_files, key=lambda x: x.stat().st_mtime)[-3:]:
                try:
                    with open(trial_file, 'r') as f:
                        data = json.load(f)
                    
                    model_name = trial_file.name.split('_trial_')[0].replace('_', '/')
                    trial_num = data.get('trial', '?')
                    accuracy = data.get('overall_accuracy', 0)
                    duration = data.get('duration', 0)
                    
                    print(f"   • {model_name} Trial {trial_num}: {accuracy:.4f} accuracy ({duration:.1f}s)")
                    
                except Exception as e:
                    print(f"   • Error reading {trial_file.name}: {e}")
        
        if comprehensive_files:
            print("\n🎉 EXPERIMENT COMPLETED!")
            latest_comprehensive = max(comprehensive_files, key=lambda x: x.stat().st_mtime)
            print(f"   📁 Results: {latest_comprehensive}")
            
            # Show final summary
            try:
                with open(latest_comprehensive, 'r') as f:
                    data = json.load(f)
                
                print("\n📈 Final Results Summary:")
                for model_name, model_results in data.get('results', {}).items():
                    agg_metrics = model_results.get('aggregated_metrics', {})
                    overall_metrics = agg_metrics.get('overall_metrics', {})
                    mean_acc = overall_metrics.get('mean_accuracy', 0)
                    std_acc = overall_metrics.get('std_accuracy', 0)
                    print(f"   • {model_name.split('/')[-1]}: {mean_acc:.4f} ± {std_acc:.4f}")
                
            except Exception as e:
                print(f"   Error reading comprehensive results: {e}")
            
            break
        
        print("\n⏳ Experiment still running... (checking again in 30 seconds)")
        print("-" * 60)
        time.sleep(30)

if __name__ == "__main__":
    monitor_experiment() 