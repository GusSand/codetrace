#!/usr/bin/env python3
"""
Monitor the extended baseline experiment progress for large models.
Tracks progress across Qwen14B, Phi3-14B, DeepSeek-33B, Gemma2-27B, StarCoder2-15B.
"""

import json
import time
from pathlib import Path
from datetime import datetime
import glob

def monitor_extended_experiment():
    """Monitor the extended experiment progress."""
    print("🔍 Monitoring Extended Baseline Experiment (Large Models)")
    print("=" * 70)
    print("Models: Qwen2.5-14B, Phi3-Medium-14B, DeepSeek-33B, Gemma2-27B, StarCoder2-15B")
    print("⚠️  Large models - expect long runtime and high memory usage")
    print("")
    
    results_dir = Path("extended_results")
    
    # Expected models
    expected_models = [
        "Qwen_Qwen2.5_Coder_14B_Instruct",
        "microsoft_Phi_3_medium_14b_instruct", 
        "deepseek_ai_deepseek_coder_33b_base",
        "google_gemma_2_27b",
        "bigcode_starcoder2_15b"
    ]
    
    while True:
        # Check for intermediate trial results
        trial_files = list(results_dir.glob("*_trial_*.json")) if results_dir.exists() else []
        complete_files = list(results_dir.glob("*_complete_*.json")) if results_dir.exists() else []
        comprehensive_files = list(results_dir.glob("comprehensive_results_*.json")) if results_dir.exists() else []
        
        print(f"⏰ {datetime.now().strftime('%H:%M:%S')} - Extended Experiment Status:")
        print(f"   📁 Results directory: {'✅ Exists' if results_dir.exists() else '❌ Not found'}")
        print(f"   📄 Trial files: {len(trial_files)}")
        print(f"   ✅ Complete model files: {len(complete_files)}")
        print(f"   🎯 Comprehensive results: {len(comprehensive_files)}")
        
        # Show progress by model
        print("\n📊 Progress by Model:")
        for model in expected_models:
            model_trials = [f for f in trial_files if model in f.name]
            model_complete = [f for f in complete_files if model in f.name]
            
            if model_complete:
                status = "✅ COMPLETE"
            elif model_trials:
                status = f"🔄 In Progress ({len(model_trials)}/3 trials)"
            else:
                status = "⏳ Waiting"
                
            # Clean up model name for display
            display_name = model.replace("_", "/").replace("Qwen/Qwen2.5/Coder/14B/Instruct", "Qwen2.5-14B").replace("microsoft/Phi/3/medium/14b/instruct", "Phi3-14B").replace("deepseek/ai/deepseek/coder/33b/base", "DeepSeek-33B").replace("google/gemma/2/27b", "Gemma2-27B").replace("bigcode/starcoder2/15b", "StarCoder2-15B")
            
            print(f"   • {display_name:<20}: {status}")
        
        if trial_files:
            print(f"\n📈 Latest Trial Results:")
            for trial_file in sorted(trial_files, key=lambda x: x.stat().st_mtime)[-3:]:
                try:
                    with open(trial_file, 'r') as f:
                        data = json.load(f)
                    
                    model_name = trial_file.name.split('_trial_')[0]
                    trial_num = data.get('trial', '?')
                    accuracy = data.get('overall_accuracy', 0)
                    duration = data.get('duration', 0)
                    
                    print(f"   • {model_name} Trial {trial_num}: {accuracy:.4f} accuracy ({duration:.1f}s)")
                    
                except Exception as e:
                    print(f"   • Error reading {trial_file.name}: {e}")
        
        # Check if all experiments completed
        if comprehensive_files:
            print(f"\n🎉 EXTENDED EXPERIMENT COMPLETED!")
            latest_comprehensive = max(comprehensive_files, key=lambda x: x.stat().st_mtime)
            print(f"   📁 Results: {latest_comprehensive}")
            
            # Show final summary
            try:
                with open(latest_comprehensive, 'r') as f:
                    data = json.load(f)
                
                print(f"\n📈 Final Extended Results Summary:")
                results = data.get('results', {})
                if results:
                    # Sort by performance
                    model_performance = []
                    for model_name, model_results in results.items():
                        agg_metrics = model_results.get('aggregated_metrics', {})
                        overall_metrics = agg_metrics.get('overall_metrics', {})
                        mean_acc = overall_metrics.get('mean_accuracy', 0)
                        model_performance.append((model_name, mean_acc))
                    
                    model_performance.sort(key=lambda x: x[1], reverse=True)
                    
                    for model_name, accuracy in model_performance:
                        display_name = model_name.split('/')[-1] if '/' in model_name else model_name
                        print(f"   • {display_name}: {accuracy:.4f}")
                else:
                    print("   ⚠️  No results found in comprehensive file")
                
            except Exception as e:
                print(f"   Error reading comprehensive results: {e}")
            
            break
        
        print(f"\n⏳ Extended experiment still running... (checking again in 60 seconds)")
        print("-" * 70)
        time.sleep(60)  # Check every minute for large models

if __name__ == "__main__":
    monitor_extended_experiment() 