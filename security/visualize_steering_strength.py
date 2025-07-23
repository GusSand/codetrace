#!/usr/bin/env python3
"""
Visualization script for steering strength experiment results.
This version includes comprehensive tracing and debugging capabilities.
"""

import sys
import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import logging
import traceback
import time
from datetime import datetime
import warnings

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import security patterns for reference
try:
    from security.security_patterns import (
        SQL_INJECTION_PATTERNS, XSS_PATTERNS, PATH_TRAVERSAL_PATTERNS,
        COMMAND_INJECTION_PATTERNS
    )
except ImportError:
    print("⚠️ Warning: Could not import security patterns. Using fallback patterns.")
    SQL_INJECTION_PATTERNS = ["parameterized", "execute", "prepare"]
    XSS_PATTERNS = ["escape", "clean", "sanitize"]
    PATH_TRAVERSAL_PATTERNS = ["basename", "abspath", "join"]
    COMMAND_INJECTION_PATTERNS = ["subprocess", "check", "shell=False"]

# Set up matplotlib for better plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class TracingVisualizer:
    """Enhanced visualizer with tracing capabilities."""
    
    def __init__(self, log_file: str = None, debug_mode: bool = True):
        self.debug_mode = debug_mode
        
        # Set up logging
        if log_file is None:
            log_dir = Path("security/logs")
            log_dir.mkdir(exist_ok=True)
            log_file = str(log_dir / f"visualization_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        
        logging.basicConfig(
            level=logging.DEBUG if debug_mode else logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Track visualization metrics
        self.visualization_metrics = {
            'plots_created': 0,
            'data_loaded': 0,
            'errors': []
        }
    
    def trace_function(self, func_name: str):
        """Decorator to trace function calls and performance."""
        def decorator(func):
            def wrapper(*args, **kwargs):
                start_time = time.time()
                
                self.logger.debug(f"🚀 Entering {func_name} with args={args[:2]}... kwargs={list(kwargs.keys())}")
                
                try:
                    result = func(*args, **kwargs)
                    end_time = time.time()
                    execution_time = end_time - start_time
                    
                    self.logger.debug(f"✅ {func_name} completed in {execution_time:.3f}s")
                    return result
                    
                except Exception as e:
                    end_time = time.time()
                    execution_time = end_time - start_time
                    
                    self.logger.error(f"❌ {func_name} failed after {execution_time:.3f}s: {str(e)}")
                    self.logger.error(f"Traceback: {traceback.format_exc()}")
                    
                    # Track error
                    self.visualization_metrics['errors'].append({
                        'function': func_name,
                        'error': str(e),
                        'traceback': traceback.format_exc(),
                        'execution_time': execution_time
                    })
                    
                    raise
            
            return wrapper
        return decorator
    
    def log_data_info(self, data, name: str):
        """Log detailed data information."""
        if self.debug_mode and data is not None:
            if isinstance(data, pd.DataFrame):
                self.logger.debug(f"📊 {name}: shape={data.shape}, columns={list(data.columns)}")
            elif isinstance(data, dict):
                self.logger.debug(f"📊 {name}: keys={list(data.keys())}")
            elif isinstance(data, list):
                self.logger.debug(f"📊 {name}: length={len(data)}")
            else:
                self.logger.debug(f"📊 {name}: type={type(data)}")


class SteeringStrengthVisualizer:
    """
    Comprehensive visualizer for steering strength experiment results.
    """
    
    def __init__(self, debug_mode: bool = True):
        self.debug_mode = debug_mode
        self.tracer = TracingVisualizer(debug_mode=debug_mode)
        self.logger = self.tracer.logger
        
        # Create output directories
        self.output_dir = Path("security/report/visualizations")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"🔧 Initialized visualizer with output directory: {self.output_dir}")
    
    def load_results(self, results_file: str) -> Dict[str, Any]:
        """Load experiment results from file."""
        return self.tracer.trace_function("load_results")(self._load_results)(results_file)
    
    def _load_results(self, results_file: str) -> Dict[str, Any]:
        """Load experiment results from file."""
        self.logger.debug(f"📥 Loading results from: {results_file}")
        
        try:
            with open(results_file, 'r') as f:
                results = json.load(f)
            
            self.tracer.log_data_info(results, "loaded_results")
            self.logger.info(f"✅ Loaded results with {len(results.get('results', []))} experiments")
            return results
            
        except Exception as e:
            self.logger.error(f"❌ Error loading results: {e}")
            raise
    
    def prepare_dataframe(self, results: Dict[str, Any]) -> pd.DataFrame:
        """Convert results to pandas DataFrame for analysis."""
        return self.tracer.trace_function("prepare_dataframe")(self._prepare_dataframe)(results)
    
    def _prepare_dataframe(self, results: Dict[str, Any]) -> pd.DataFrame:
        """Convert results to pandas DataFrame for analysis."""
        self.logger.debug("🔄 Preparing DataFrame from results...")
        
        data = []
        for result in results.get('results', []):
            # Extract basic info
            row = {
                'steering_scale': result.get('steering_scale', 0),
                'layer_config': str(result.get('layer_config', [])),
                'vulnerability_type': result.get('test_case', {}).get('vulnerability_type', 'unknown'),
                'prompt': result.get('test_case', {}).get('prompt', ''),
                'generated_code': result.get('generated_code', ''),
                'generation_time': result.get('generation_time', 0),
            }
            
            # Extract evaluation metrics
            evaluation = result.get('evaluation', {})
            row.update({
                'security_score': evaluation.get('security_score', 0),
                'quality_score': evaluation.get('quality_score', 0),
                'match_score': evaluation.get('match_score', 0),
                'secure_patterns_found': evaluation.get('secure_patterns_found', 0),
                'vulnerable_patterns_found': evaluation.get('vulnerable_patterns_found', 0),
            })
            
            # Extract memory usage
            memory = result.get('memory_usage', {})
            row.update({
                'memory_before': memory.get('before', 0),
                'memory_after': memory.get('after', 0),
                'memory_delta': memory.get('delta', 0),
            })
            
            data.append(row)
        
        df = pd.DataFrame(data)
        self.tracer.log_data_info(df, "prepared_dataframe")
        
        # Convert layer_config back to list for easier analysis
        df['layer_config_list'] = df['layer_config'].apply(eval)
        df['num_layers'] = df['layer_config_list'].apply(len)
        
        self.logger.info(f"✅ Prepared DataFrame with {len(df)} rows and {len(df.columns)} columns")
        return df
    
    def create_comprehensive_plots(self, df: pd.DataFrame, results: Dict[str, Any]) -> List[str]:
        """Create comprehensive visualization plots."""
        return self.tracer.trace_function("create_comprehensive_plots")(self._create_comprehensive_plots)(df, results)
    
    def _create_comprehensive_plots(self, df: pd.DataFrame, results: Dict[str, Any]) -> List[str]:
        """Create comprehensive visualization plots."""
        self.logger.debug("🎨 Creating comprehensive plots...")
        
        plot_files = []
        
        # 1. Steering Scale Analysis
        plot_files.append(self._plot_steering_scale_analysis(df))
        
        # 2. Layer Configuration Analysis
        plot_files.append(self._plot_layer_config_analysis(df))
        
        # 3. Vulnerability Type Analysis
        plot_files.append(self._plot_vulnerability_analysis(df))
        
        # 4. Performance Analysis
        plot_files.append(self._plot_performance_analysis(df))
        
        # 5. Combined Analysis
        plot_files.append(self._plot_combined_analysis(df))
        
        # 6. Heatmap Analysis
        plot_files.append(self._plot_heatmap_analysis(df))
        
        self.logger.info(f"✅ Created {len(plot_files)} comprehensive plots")
        return plot_files
    
    def _plot_steering_scale_analysis(self, df: pd.DataFrame) -> str:
        """Plot analysis of steering scale effects."""
        self.logger.debug("📊 Creating steering scale analysis plot...")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Steering Scale Analysis', fontsize=16, fontweight='bold')
        
        # Plot 1: Security Score vs Scale
        ax1 = axes[0, 0]
        for layer_config in df['layer_config'].unique():
            config_data = df[df['layer_config'] == layer_config]
            ax1.scatter(config_data['steering_scale'], config_data['security_score'], 
                       label=layer_config, alpha=0.7, s=50)
        
        ax1.set_xlabel('Steering Scale')
        ax1.set_ylabel('Security Score')
        ax1.set_title('Security Score vs Steering Scale')
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Quality Score vs Scale
        ax2 = axes[0, 1]
        for layer_config in df['layer_config'].unique():
            config_data = df[df['layer_config'] == layer_config]
            ax2.scatter(config_data['steering_scale'], config_data['quality_score'], 
                       label=layer_config, alpha=0.7, s=50)
        
        ax2.set_xlabel('Steering Scale')
        ax2.set_ylabel('Quality Score')
        ax2.set_title('Quality Score vs Steering Scale')
        ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Average trends
        ax3 = axes[1, 0]
        avg_security = df.groupby('steering_scale')['security_score'].mean()
        avg_quality = df.groupby('steering_scale')['quality_score'].mean()
        
        ax3.plot(avg_security.index, avg_security.values, 'o-', label='Security Score', linewidth=2)
        ax3.plot(avg_quality.index, avg_quality.values, 's-', label='Quality Score', linewidth=2)
        ax3.set_xlabel('Steering Scale')
        ax3.set_ylabel('Average Score')
        ax3.set_title('Average Scores vs Steering Scale')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Scale distribution
        ax4 = axes[1, 1]
        df['steering_scale'].hist(bins=20, alpha=0.7, ax=ax4)
        ax4.set_xlabel('Steering Scale')
        ax4.set_ylabel('Frequency')
        ax4.set_title('Distribution of Steering Scales')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        filename = str(self.output_dir / "steering_scale_analysis.png")
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        self.logger.debug(f"✅ Saved steering scale analysis plot to {filename}")
        return filename
    
    def _plot_layer_config_analysis(self, df: pd.DataFrame) -> str:
        """Plot analysis of layer configuration effects."""
        self.logger.debug("📊 Creating layer configuration analysis plot...")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Layer Configuration Analysis', fontsize=16, fontweight='bold')
        
        # Plot 1: Security Score by Layer Config
        ax1 = axes[0, 0]
        layer_avg = df.groupby('layer_config')['security_score'].mean().sort_values(ascending=False)
        layer_avg.plot(kind='bar', ax=ax1, color='skyblue')
        ax1.set_xlabel('Layer Configuration')
        ax1.set_ylabel('Average Security Score')
        ax1.set_title('Average Security Score by Layer Configuration')
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Number of Layers vs Performance
        ax2 = axes[0, 1]
        num_layers_avg = df.groupby('num_layers')[['security_score', 'quality_score']].mean()
        num_layers_avg.plot(kind='bar', ax=ax2)
        ax2.set_xlabel('Number of Layers')
        ax2.set_ylabel('Average Score')
        ax2.set_title('Performance vs Number of Layers')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Layer Config vs Generation Time
        ax3 = axes[1, 0]
        time_avg = df.groupby('layer_config')['generation_time'].mean().sort_values(ascending=False)
        time_avg.plot(kind='bar', ax=ax3, color='lightcoral')
        ax3.set_xlabel('Layer Configuration')
        ax3.set_ylabel('Average Generation Time (s)')
        ax3.set_title('Generation Time by Layer Configuration')
        ax3.tick_params(axis='x', rotation=45)
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Memory Usage by Layer Config
        ax4 = axes[1, 1]
        memory_avg = df.groupby('layer_config')['memory_delta'].mean().sort_values(ascending=False)
        memory_avg.plot(kind='bar', ax=ax4, color='lightgreen')
        ax4.set_xlabel('Layer Configuration')
        ax4.set_ylabel('Average Memory Delta (MB)')
        ax4.set_title('Memory Usage by Layer Configuration')
        ax4.tick_params(axis='x', rotation=45)
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        filename = str(self.output_dir / "layer_config_analysis.png")
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        self.logger.debug(f"✅ Saved layer configuration analysis plot to {filename}")
        return filename
    
    def _plot_vulnerability_analysis(self, df: pd.DataFrame) -> str:
        """Plot analysis of vulnerability type effects."""
        self.logger.debug("📊 Creating vulnerability analysis plot...")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Vulnerability Type Analysis', fontsize=16, fontweight='bold')
        
        # Plot 1: Security Score by Vulnerability Type
        ax1 = axes[0, 0]
        vuln_avg = df.groupby('vulnerability_type')['security_score'].mean().sort_values(ascending=False)
        vuln_avg.plot(kind='bar', ax=ax1, color='gold')
        ax1.set_xlabel('Vulnerability Type')
        ax1.set_ylabel('Average Security Score')
        ax1.set_title('Security Score by Vulnerability Type')
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Pattern Analysis
        ax2 = axes[0, 1]
        pattern_data = df.groupby('vulnerability_type')[['secure_patterns_found', 'vulnerable_patterns_found']].mean()
        pattern_data.plot(kind='bar', ax=ax2)
        ax2.set_xlabel('Vulnerability Type')
        ax2.set_ylabel('Average Pattern Count')
        ax2.set_title('Pattern Detection by Vulnerability Type')
        ax2.legend()
        ax2.tick_params(axis='x', rotation=45)
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Vulnerability Type vs Steering Scale
        ax3 = axes[1, 0]
        for vuln_type in df['vulnerability_type'].unique():
            vuln_data = df[df['vulnerability_type'] == vuln_type]
            ax3.scatter(vuln_data['steering_scale'], vuln_data['security_score'], 
                       label=vuln_type, alpha=0.7, s=50)
        
        ax3.set_xlabel('Steering Scale')
        ax3.set_ylabel('Security Score')
        ax3.set_title('Security Score vs Steering Scale by Vulnerability Type')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Quality Score by Vulnerability Type
        ax4 = axes[1, 1]
        quality_avg = df.groupby('vulnerability_type')['quality_score'].mean().sort_values(ascending=False)
        quality_avg.plot(kind='bar', ax=ax4, color='lightblue')
        ax4.set_xlabel('Vulnerability Type')
        ax4.set_ylabel('Average Quality Score')
        ax4.set_title('Quality Score by Vulnerability Type')
        ax4.tick_params(axis='x', rotation=45)
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        filename = str(self.output_dir / "vulnerability_analysis.png")
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        self.logger.debug(f"✅ Saved vulnerability analysis plot to {filename}")
        return filename
    
    def _plot_performance_analysis(self, df: pd.DataFrame) -> str:
        """Plot performance analysis."""
        self.logger.debug("📊 Creating performance analysis plot...")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Performance Analysis', fontsize=16, fontweight='bold')
        
        # Plot 1: Generation Time vs Security Score
        ax1 = axes[0, 0]
        ax1.scatter(df['generation_time'], df['security_score'], alpha=0.6, s=30)
        ax1.set_xlabel('Generation Time (s)')
        ax1.set_ylabel('Security Score')
        ax1.set_title('Security Score vs Generation Time')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Memory Usage vs Security Score
        ax2 = axes[0, 1]
        ax2.scatter(df['memory_delta'], df['security_score'], alpha=0.6, s=30)
        ax2.set_xlabel('Memory Delta (MB)')
        ax2.set_ylabel('Security Score')
        ax2.set_title('Security Score vs Memory Usage')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Generation Time Distribution
        ax3 = axes[1, 0]
        df['generation_time'].hist(bins=30, alpha=0.7, ax=ax3)
        ax3.set_xlabel('Generation Time (s)')
        ax3.set_ylabel('Frequency')
        ax3.set_title('Distribution of Generation Times')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Memory Usage Distribution
        ax4 = axes[1, 1]
        df['memory_delta'].hist(bins=30, alpha=0.7, ax=ax4)
        ax4.set_xlabel('Memory Delta (MB)')
        ax4.set_ylabel('Frequency')
        ax4.set_title('Distribution of Memory Usage')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        filename = str(self.output_dir / "performance_analysis.png")
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        self.logger.debug(f"✅ Saved performance analysis plot to {filename}")
        return filename
    
    def _plot_combined_analysis(self, df: pd.DataFrame) -> str:
        """Plot combined analysis showing interactions."""
        self.logger.debug("📊 Creating combined analysis plot...")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Combined Analysis', fontsize=16, fontweight='bold')
        
        # Plot 1: Security vs Quality Score
        ax1 = axes[0, 0]
        scatter = ax1.scatter(df['security_score'], df['quality_score'], 
                             c=df['steering_scale'], cmap='viridis', alpha=0.7, s=50)
        ax1.set_xlabel('Security Score')
        ax1.set_ylabel('Quality Score')
        ax1.set_title('Security vs Quality Score (colored by steering scale)')
        plt.colorbar(scatter, ax=ax1, label='Steering Scale')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Security vs Match Score
        ax2 = axes[0, 1]
        scatter = ax2.scatter(df['security_score'], df['match_score'], 
                             c=df['num_layers'], cmap='plasma', alpha=0.7, s=50)
        ax2.set_xlabel('Security Score')
        ax2.set_ylabel('Match Score')
        ax2.set_title('Security vs Match Score (colored by number of layers)')
        plt.colorbar(scatter, ax=ax2, label='Number of Layers')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: 3D-like plot using size
        ax3 = axes[1, 0]
        sizes = 50 + df['steering_scale'] * 20  # Scale sizes based on steering scale
        ax3.scatter(df['security_score'], df['quality_score'], s=sizes, alpha=0.6)
        ax3.set_xlabel('Security Score')
        ax3.set_ylabel('Quality Score')
        ax3.set_title('Security vs Quality (size = steering scale)')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Box plot of security scores by steering scale
        ax4 = axes[1, 1]
        df.boxplot(column='security_score', by='steering_scale', ax=ax4)
        ax4.set_xlabel('Steering Scale')
        ax4.set_ylabel('Security Score')
        ax4.set_title('Security Score Distribution by Steering Scale')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        filename = str(self.output_dir / "combined_analysis.png")
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        self.logger.debug(f"✅ Saved combined analysis plot to {filename}")
        return filename
    
    def _plot_heatmap_analysis(self, df: pd.DataFrame) -> str:
        """Plot heatmap analysis of key metrics."""
        self.logger.debug("📊 Creating heatmap analysis plot...")
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Heatmap Analysis', fontsize=16, fontweight='bold')
        
        # Plot 1: Security Score Heatmap by Scale and Layers
        ax1 = axes[0, 0]
        pivot_security = df.pivot_table(
            values='security_score', 
            index='steering_scale', 
            columns='num_layers', 
            aggfunc='mean'
        )
        sns.heatmap(pivot_security, annot=True, fmt='.3f', cmap='RdYlGn', ax=ax1)
        ax1.set_title('Security Score Heatmap\n(Scale vs Number of Layers)')
        
        # Plot 2: Quality Score Heatmap
        ax2 = axes[0, 1]
        pivot_quality = df.pivot_table(
            values='quality_score', 
            index='steering_scale', 
            columns='num_layers', 
            aggfunc='mean'
        )
        sns.heatmap(pivot_quality, annot=True, fmt='.3f', cmap='RdYlGn', ax=ax2)
        ax2.set_title('Quality Score Heatmap\n(Scale vs Number of Layers)')
        
        # Plot 3: Generation Time Heatmap
        ax3 = axes[1, 0]
        pivot_time = df.pivot_table(
            values='generation_time', 
            index='steering_scale', 
            columns='num_layers', 
            aggfunc='mean'
        )
        sns.heatmap(pivot_time, annot=True, fmt='.3f', cmap='viridis', ax=ax3)
        ax3.set_title('Generation Time Heatmap\n(Scale vs Number of Layers)')
        
        # Plot 4: Correlation Matrix
        ax4 = axes[1, 1]
        numeric_cols = ['steering_scale', 'security_score', 'quality_score', 'match_score', 
                       'generation_time', 'memory_delta', 'num_layers']
        correlation_matrix = df[numeric_cols].corr()
        sns.heatmap(correlation_matrix, annot=True, fmt='.3f', cmap='coolwarm', ax=ax4)
        ax4.set_title('Correlation Matrix')
        
        plt.tight_layout()
        
        filename = str(self.output_dir / "heatmap_analysis.png")
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        self.logger.debug(f"✅ Saved heatmap analysis plot to {filename}")
        return filename
    
    def generate_summary_report(self, df: pd.DataFrame, results: Dict[str, Any]) -> str:
        """Generate a comprehensive summary report."""
        return self.tracer.trace_function("generate_summary_report")(self._generate_summary_report)(df, results)
    
    def _generate_summary_report(self, df: pd.DataFrame, results: Dict[str, Any]) -> str:
        """Generate a comprehensive summary report."""
        self.logger.debug("📝 Generating summary report...")
        
        report_lines = []
        report_lines.append("# Steering Strength Experiment Results Summary")
        report_lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # Experiment Info
        experiment_info = results.get('experiment_info', {})
        report_lines.append("## Experiment Information")
        report_lines.append(f"- Model: {experiment_info.get('model_name', 'Unknown')}")
        report_lines.append(f"- Timestamp: {experiment_info.get('timestamp', 'Unknown')}")
        report_lines.append(f"- Total Experiments: {len(df)}")
        report_lines.append(f"- Steering Scales: {experiment_info.get('steering_scales', [])}")
        report_lines.append(f"- Layer Configurations: {experiment_info.get('layer_configs', [])}")
        report_lines.append("")
        
        # Key Statistics
        report_lines.append("## Key Statistics")
        report_lines.append(f"- Average Security Score: {df['security_score'].mean():.3f}")
        report_lines.append(f"- Average Quality Score: {df['quality_score'].mean():.3f}")
        report_lines.append(f"- Average Match Score: {df['match_score'].mean():.3f}")
        report_lines.append(f"- Average Generation Time: {df['generation_time'].mean():.3f}s")
        report_lines.append("")
        
        # Best Performing Configurations
        report_lines.append("## Best Performing Configurations")
        
        # Best security score
        best_security = df.loc[df['security_score'].idxmax()]
        report_lines.append(f"### Best Security Score: {best_security['security_score']:.3f}")
        report_lines.append(f"- Steering Scale: {best_security['steering_scale']}")
        report_lines.append(f"- Layer Config: {best_security['layer_config']}")
        report_lines.append(f"- Vulnerability Type: {best_security['vulnerability_type']}")
        report_lines.append("")
        
        # Best quality score
        best_quality = df.loc[df['quality_score'].idxmax()]
        report_lines.append(f"### Best Quality Score: {best_quality['quality_score']:.3f}")
        report_lines.append(f"- Steering Scale: {best_quality['steering_scale']}")
        report_lines.append(f"- Layer Config: {best_quality['layer_config']}")
        report_lines.append(f"- Vulnerability Type: {best_quality['vulnerability_type']}")
        report_lines.append("")
        
        # Scale Analysis
        report_lines.append("## Steering Scale Analysis")
        scale_analysis = df.groupby('steering_scale').agg({
            'security_score': ['mean', 'std'],
            'quality_score': ['mean', 'std'],
            'generation_time': 'mean'
        }).round(3)
        report_lines.append("```")
        report_lines.append(str(scale_analysis))
        report_lines.append("```")
        report_lines.append("")
        
        # Layer Analysis
        report_lines.append("## Layer Configuration Analysis")
        layer_analysis = df.groupby('num_layers').agg({
            'security_score': ['mean', 'std'],
            'quality_score': ['mean', 'std'],
            'generation_time': 'mean'
        }).round(3)
        report_lines.append("```")
        report_lines.append(str(layer_analysis))
        report_lines.append("```")
        report_lines.append("")
        
        # Vulnerability Analysis
        report_lines.append("## Vulnerability Type Analysis")
        vuln_analysis = df.groupby('vulnerability_type').agg({
            'security_score': ['mean', 'std'],
            'quality_score': ['mean', 'std'],
            'secure_patterns_found': 'mean',
            'vulnerable_patterns_found': 'mean'
        }).round(3)
        report_lines.append("```")
        report_lines.append(str(vuln_analysis))
        report_lines.append("```")
        report_lines.append("")
        
        # Recommendations
        report_lines.append("## Recommendations")
        
        # Find optimal scale
        optimal_scale = df.groupby('steering_scale')['security_score'].mean().idxmax()
        report_lines.append(f"1. **Optimal Steering Scale**: {optimal_scale} (highest average security score)")
        
        # Find optimal layer count
        optimal_layers = df.groupby('num_layers')['security_score'].mean().idxmax()
        report_lines.append(f"2. **Optimal Number of Layers**: {optimal_layers} (highest average security score)")
        
        # Find best trade-off
        df['combined_score'] = df['security_score'] * 0.7 + df['quality_score'] * 0.3
        best_tradeoff = df.loc[df['combined_score'].idxmax()]
        report_lines.append(f"3. **Best Security-Quality Trade-off**: Scale {best_tradeoff['steering_scale']}, Layers {best_tradeoff['layer_config']}")
        
        # Performance considerations
        fast_config = df.loc[df['generation_time'].idxmin()]
        report_lines.append(f"4. **Fastest Generation**: Scale {fast_config['steering_scale']}, Layers {fast_config['layer_config']} ({fast_config['generation_time']:.3f}s)")
        
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("*This report was generated automatically by the Steering Strength Visualizer*")
        
        # Save report
        report_filename = str(self.output_dir / "experiment_summary_report.md")
        with open(report_filename, 'w') as f:
            f.write('\n'.join(report_lines))
        
        self.logger.info(f"✅ Generated summary report: {report_filename}")
        return report_filename


def main():
    """Main function to run the visualization."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Visualize steering strength experiment results')
    parser.add_argument('--results-file', type=str, required=True,
                       help='Path to the results JSON file')
    parser.add_argument('--debug', action='store_true', default=True,
                       help='Enable debug mode')
    parser.add_argument('--output-dir', type=str, default='security/report/visualizations',
                       help='Output directory for plots')
    
    args = parser.parse_args()
    
    print("🎨 Starting steering strength visualization...")
    
    try:
        # Initialize visualizer
        visualizer = SteeringStrengthVisualizer(debug_mode=args.debug)
        
        # Load results
        results = visualizer.load_results(args.results_file)
        
        # Prepare DataFrame
        df = visualizer.prepare_dataframe(results)
        
        # Create plots
        plot_files = visualizer.create_comprehensive_plots(df, results)
        
        # Generate summary report
        report_file = visualizer.generate_summary_report(df, results)
        
        print(f"✅ Visualization completed successfully!")
        print(f"📊 Created {len(plot_files)} plots:")
        for plot_file in plot_files:
            print(f"   - {plot_file}")
        print(f"📝 Generated summary report: {report_file}")
        
    except Exception as e:
        print(f"❌ Visualization failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 