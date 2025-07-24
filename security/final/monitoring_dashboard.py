#!/usr/bin/env python3
"""
Real-time monitoring dashboard for extended baseline experiments.
Provides live progress tracking, GPU monitoring, and result visualization.
"""

import json
import time
import os
import sys
import subprocess
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
import numpy as np

class ExtendedExperimentDashboard:
    """Comprehensive monitoring dashboard for the extended experiment."""
    
    def __init__(self):
        self.results_dir = Path("extended_results")
        self.log_file = Path("extended_experiment_log.txt")
        self.start_time = datetime.now()
        
        # Model configuration
        self.models = [
            {"name": "Qwen/Qwen2.5-Coder-14B-Instruct", "display": "Qwen2.5-14B", "size": "14B"},
            {"name": "microsoft/Phi-3-medium-14b-instruct", "display": "Phi3-Medium-14B", "size": "14B"},
            {"name": "deepseek-ai/deepseek-coder-33b-base", "display": "DeepSeek-33B", "size": "33B"},
            {"name": "google/gemma-2-27b", "display": "Gemma2-27B", "size": "27B"},
            {"name": "bigcode/starcoder2-15b", "display": "StarCoder2-15B", "size": "15B"}
        ]
        
        # Progress tracking
        self.model_progress = {model["display"]: {"status": "⏳ Waiting", "trials": 0, "accuracy": None, "duration": None} for model in self.models}
        self.overall_progress = {"completed_models": 0, "total_models": 5, "current_model": None}
        
        # Results storage for visualization
        self.results_history = []
        self.gpu_usage_history = []
        
        # Console formatting
        self.colors = {
            "GREEN": "\033[92m",
            "YELLOW": "\033[93m", 
            "RED": "\033[91m",
            "BLUE": "\033[94m",
            "CYAN": "\033[96m",
            "MAGENTA": "\033[95m",
            "WHITE": "\033[97m",
            "BOLD": "\033[1m",
            "UNDERLINE": "\033[4m",
            "END": "\033[0m"
        }

    def get_gpu_info(self) -> Dict[str, Any]:
        """Get current GPU usage information."""
        try:
            result = subprocess.run(['nvidia-smi', '--query-gpu=memory.used,memory.total,utilization.gpu,temperature.gpu', 
                                   '--format=csv,noheader,nounits'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                gpu_data = []
                for line in lines:
                    if line:
                        values = [float(x.strip()) for x in line.split(',')]
                        gpu_data.append({
                            'memory_used': values[0],
                            'memory_total': values[1], 
                            'utilization': values[2],
                            'temperature': values[3]
                        })
                return {"available": True, "gpus": gpu_data}
        except:
            pass
        return {"available": False, "gpus": []}

    def parse_log_file(self) -> Dict[str, Any]:
        """Parse the experiment log file for current status."""
        status = {
            "current_phase": "Starting",
            "current_model": None,
            "current_trial": None,
            "last_update": None,
            "errors": []
        }
        
        if not self.log_file.exists():
            return status
            
        try:
            with open(self.log_file, 'r') as f:
                lines = f.readlines()
                
            # Parse recent lines for status
            for line in reversed(lines[-50:]):  # Check last 50 lines
                line = line.strip()
                if "Loading model:" in line:
                    model_name = line.split("Loading model: ")[-1]
                    for model in self.models:
                        if model["name"] in model_name:
                            status["current_model"] = model["display"]
                            status["current_phase"] = "Loading Model"
                            break
                            
                elif "Running trial" in line:
                    if "for" in line:
                        parts = line.split()
                        trial_info = [p for p in parts if "trial" in p.lower()]
                        if trial_info:
                            status["current_trial"] = trial_info[0].split("/")[0].replace("trial", "").strip()
                            status["current_phase"] = "Running Trial"
                            
                elif "Processing" in line and "CWE" in line:
                    cwe = line.split("Processing ")[-1].split(" ")[0]
                    status["current_phase"] = f"Processing {cwe}"
                    
                elif "ERROR" in line or "Error" in line:
                    status["errors"].append(line)
                    
                elif "INFO:" in line:
                    status["last_update"] = datetime.now()
                    
        except Exception as e:
            status["errors"].append(f"Log parsing error: {e}")
            
        return status

    def scan_results(self) -> Dict[str, Any]:
        """Scan for completed results and update progress."""
        if not self.results_dir.exists():
            return {"trial_files": 0, "complete_files": 0, "comprehensive_files": 0}
            
        # Scan result files
        trial_files = list(self.results_dir.glob("*_trial_*.json"))
        complete_files = list(self.results_dir.glob("*_complete_*.json"))
        comprehensive_files = list(self.results_dir.glob("comprehensive_results_*.json"))
        
        # Update model progress
        for model in self.models:
            model_key = model["display"]
            
            # Count trials for this model
            model_trials = [f for f in trial_files if self.normalize_model_name(model["name"]) in f.name]
            self.model_progress[model_key]["trials"] = len(model_trials)
            
            # Check if model is complete
            model_complete = [f for f in complete_files if self.normalize_model_name(model["name"]) in f.name]
            if model_complete:
                self.model_progress[model_key]["status"] = "✅ Complete"
                
                # Try to get accuracy from complete file
                try:
                    with open(model_complete[0], 'r') as f:
                        data = json.load(f)
                    agg_metrics = data.get("aggregated_metrics", {})
                    overall_metrics = agg_metrics.get("overall_metrics", {})
                    accuracy = overall_metrics.get("mean_accuracy", 0)
                    self.model_progress[model_key]["accuracy"] = accuracy
                except:
                    pass
                    
            elif model_trials:
                trial_count = len(model_trials)
                self.model_progress[model_key]["status"] = f"🔄 Running ({trial_count}/3 trials)"
                
                # Get latest trial accuracy
                if model_trials:
                    latest_trial = max(model_trials, key=lambda x: x.stat().st_mtime)
                    try:
                        with open(latest_trial, 'r') as f:
                            data = json.load(f)
                        accuracy = data.get("overall_accuracy", 0)
                        duration = data.get("duration", 0)
                        self.model_progress[model_key]["accuracy"] = accuracy
                        self.model_progress[model_key]["duration"] = duration
                    except:
                        pass
        
        # Update overall progress
        self.overall_progress["completed_models"] = len([m for m in self.model_progress.values() if "Complete" in m["status"]])
        
        return {
            "trial_files": len(trial_files),
            "complete_files": len(complete_files), 
            "comprehensive_files": len(comprehensive_files)
        }

    def normalize_model_name(self, model_name: str) -> str:
        """Normalize model name for file matching."""
        return model_name.replace("/", "_").replace("-", "_")

    def print_header(self):
        """Print dashboard header."""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}")
        print("=" * 80)
        print("🚀 EXTENDED BASELINE EXPERIMENT MONITORING DASHBOARD")
        print("=" * 80)
        print(f"{self.colors['END']}")
        
        elapsed = datetime.now() - self.start_time
        print(f"{self.colors['WHITE']}Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Elapsed: {str(elapsed).split('.')[0]}")
        print(f"Dashboard Updated: {datetime.now().strftime('%H:%M:%S')}{self.colors['END']}")
        print()

    def print_overall_progress(self):
        """Print overall experiment progress."""
        completed = self.overall_progress["completed_models"]
        total = self.overall_progress["total_models"]
        progress_pct = (completed / total) * 100
        
        print(f"{self.colors['BOLD']}{self.colors['YELLOW']}📊 OVERALL PROGRESS{self.colors['END']}")
        print(f"Models Completed: {completed}/{total} ({progress_pct:.1f}%)")
        
        # Progress bar
        bar_length = 50
        filled_length = int(bar_length * completed // total)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        print(f"[{bar}] {progress_pct:.1f}%")
        print()

    def print_model_status(self):
        """Print detailed model status."""
        print(f"{self.colors['BOLD']}{self.colors['BLUE']}🤖 MODEL STATUS{self.colors['END']}")
        print()
        
        headers = ["Model", "Size", "Status", "Trials", "Latest Accuracy", "Duration"]
        col_widths = [20, 6, 25, 8, 15, 10]
        
        # Print headers
        header_line = ""
        for i, header in enumerate(headers):
            header_line += f"{header:<{col_widths[i]}}"
        print(f"{self.colors['UNDERLINE']}{header_line}{self.colors['END']}")
        
        # Print model data
        for model in self.models:
            model_key = model["display"]
            progress = self.model_progress[model_key]
            
            accuracy_str = f"{progress['accuracy']:.4f}" if progress['accuracy'] is not None else "N/A"
            duration_str = f"{progress['duration']:.1f}s" if progress['duration'] is not None else "N/A"
            
            # Color coding based on status
            if "Complete" in progress["status"]:
                color = self.colors['GREEN']
            elif "Running" in progress["status"]:
                color = self.colors['YELLOW']
            else:
                color = self.colors['WHITE']
                
            row = f"{color}{model_key:<{col_widths[0]}}{model['size']:<{col_widths[1]}}{progress['status']:<{col_widths[2]}}{progress['trials']:<{col_widths[3]}}{accuracy_str:<{col_widths[4]}}{duration_str:<{col_widths[5]}}{self.colors['END']}"
            print(row)
        print()

    def print_current_activity(self, log_status: Dict[str, Any]):
        """Print current activity and status."""
        print(f"{self.colors['BOLD']}{self.colors['MAGENTA']}⚡ CURRENT ACTIVITY{self.colors['END']}")
        
        if log_status["current_model"]:
            print(f"Model: {self.colors['CYAN']}{log_status['current_model']}{self.colors['END']}")
        
        if log_status["current_trial"]:
            print(f"Trial: {self.colors['YELLOW']}{log_status['current_trial']}{self.colors['END']}")
            
        print(f"Phase: {self.colors['WHITE']}{log_status['current_phase']}{self.colors['END']}")
        
        if log_status["last_update"]:
            time_since = datetime.now() - log_status["last_update"]
            if time_since.total_seconds() > 300:  # 5 minutes
                print(f"{self.colors['RED']}⚠️  No updates for {time_since}{self.colors['END']}")
        print()

    def print_gpu_status(self):
        """Print GPU usage information."""
        gpu_info = self.get_gpu_info()
        
        print(f"{self.colors['BOLD']}{self.colors['GREEN']}🖥️  GPU STATUS{self.colors['END']}")
        
        if gpu_info["available"]:
            for i, gpu in enumerate(gpu_info["gpus"]):
                memory_pct = (gpu['memory_used'] / gpu['memory_total']) * 100
                
                # Color coding for memory usage
                if memory_pct > 90:
                    mem_color = self.colors['RED']
                elif memory_pct > 70:
                    mem_color = self.colors['YELLOW']
                else:
                    mem_color = self.colors['GREEN']
                    
                print(f"GPU {i}: {mem_color}Memory: {gpu['memory_used']:.0f}/{gpu['memory_total']:.0f}MB ({memory_pct:.1f}%){self.colors['END']}")
                print(f"      Utilization: {gpu['utilization']:.0f}% | Temperature: {gpu['temperature']:.0f}°C")
                
                # Store for history
                self.gpu_usage_history.append({
                    'timestamp': datetime.now(),
                    'memory_pct': memory_pct,
                    'utilization': gpu['utilization'],
                    'temperature': gpu['temperature']
                })
                
                # Keep only recent history
                if len(self.gpu_usage_history) > 100:
                    self.gpu_usage_history = self.gpu_usage_history[-50:]
        else:
            print(f"{self.colors['RED']}No GPU information available{self.colors['END']}")
        print()

    def print_results_summary(self, results_info: Dict[str, Any]):
        """Print results file summary."""
        print(f"{self.colors['BOLD']}{self.colors['CYAN']}📁 RESULTS SUMMARY{self.colors['END']}")
        print(f"Trial files: {results_info['trial_files']}")
        print(f"Complete model files: {results_info['complete_files']}")
        print(f"Comprehensive results: {results_info['comprehensive_files']}")
        
        if results_info['comprehensive_files'] > 0:
            print(f"{self.colors['GREEN']}✅ Experiment completed! Results ready for analysis.{self.colors['END']}")
        print()

    def print_errors(self, log_status: Dict[str, Any]):
        """Print any errors from the log."""
        if log_status["errors"]:
            print(f"{self.colors['BOLD']}{self.colors['RED']}❌ RECENT ERRORS{self.colors['END']}")
            for error in log_status["errors"][-3:]:  # Show last 3 errors
                print(f"{self.colors['RED']}{error[:100]}{'...' if len(error) > 100 else ''}{self.colors['END']}")
            print()

    def print_next_steps(self, results_info: Dict[str, Any]):
        """Print suggested next steps."""
        print(f"{self.colors['BOLD']}{self.colors['WHITE']}🎯 NEXT STEPS{self.colors['END']}")
        
        if results_info['comprehensive_files'] > 0:
            print(f"{self.colors['GREEN']}1. Run combined analysis: python combined_analysis_for_paper.py{self.colors['END']}")
            print(f"{self.colors['GREEN']}2. Generate paper charts and tables{self.colors['END']}")
            print(f"{self.colors['GREEN']}3. Commit final results to git{self.colors['END']}")
        else:
            completed = self.overall_progress["completed_models"]
            remaining = self.overall_progress["total_models"] - completed
            print(f"{self.colors['YELLOW']}⏳ Waiting for {remaining} more models to complete{self.colors['END']}")
            print(f"{self.colors['CYAN']}💡 Estimated time remaining: {remaining * 45} - {remaining * 90} minutes{self.colors['END']}")
        print()

    def run_dashboard(self, refresh_interval: int = 30):
        """Run the monitoring dashboard with periodic updates."""
        print(f"{self.colors['BOLD']}🚀 Starting Extended Experiment Monitoring Dashboard{self.colors['END']}")
        print(f"Refresh interval: {refresh_interval} seconds")
        print(f"Press Ctrl+C to exit\n")
        
        try:
            while True:
                # Gather current status
                log_status = self.parse_log_file()
                results_info = self.scan_results()
                
                # Print dashboard
                self.print_header()
                self.print_overall_progress()
                self.print_model_status()
                self.print_current_activity(log_status)
                self.print_gpu_status()
                self.print_results_summary(results_info)
                self.print_errors(log_status)
                self.print_next_steps(results_info)
                
                # Check if experiment completed
                if results_info['comprehensive_files'] > 0:
                    print(f"{self.colors['BOLD']}{self.colors['GREEN']}🎉 EXTENDED EXPERIMENT COMPLETED!{self.colors['END']}")
                    print(f"{self.colors['CYAN']}Ready to generate paper charts and analysis.{self.colors['END']}")
                    break
                
                # Wait for next update
                print(f"{self.colors['WHITE']}Next update in {refresh_interval} seconds...{self.colors['END']}")
                time.sleep(refresh_interval)
                
        except KeyboardInterrupt:
            print(f"\n{self.colors['YELLOW']}Dashboard stopped by user.{self.colors['END']}")
        except Exception as e:
            print(f"\n{self.colors['RED']}Dashboard error: {e}{self.colors['END']}")

def main():
    """Run the monitoring dashboard."""
    dashboard = ExtendedExperimentDashboard()
    
    # Check if experiment is running
    result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
    if 'extended_baseline_experiment' not in result.stdout:
        print(f"{dashboard.colors['YELLOW']}⚠️  Extended experiment process not detected.{dashboard.colors['END']}")
        print(f"Make sure the experiment is running: python extended_baseline_experiment.py")
        print()
    
    # Start dashboard
    dashboard.run_dashboard(refresh_interval=30)

if __name__ == "__main__":
    main() 