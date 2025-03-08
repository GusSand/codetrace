#!/usr/bin/env python3
import json
import sys
import os
import numpy as np
from collections import defaultdict
from typing import Dict, List, Any

def load_results(results_file: str) -> Dict:
    """Load optimization results from JSON file."""
    with open(results_file, 'r') as f:
        return json.load(f)

def analyze_vulnerability(vuln_data: Dict) -> Dict:
    """Analyze results for a specific vulnerability type."""
    configs = {}
    baselines = {}
    
    # Process each configuration
    for config_name, trials in vuln_data.items():
        # Extract metrics
        security_scores = [trial["security_score"] for trial in trials]
        quality_scores = [trial["quality_score"] for trial in trials]
        repetition_scores = [trial.get("repetition", 0) for trial in trials]
        match_scores = [trial["match_score"] for trial in trials]
        
        # Calculate statistics
        avg_security = np.mean(security_scores)
        avg_quality = np.mean(quality_scores)
        avg_repetition = np.mean(repetition_scores)
        avg_match = np.mean(match_scores)
        
        # Store summary
        if config_name == "no_bias":
            baselines = {
                "security": avg_security,
                "quality": avg_quality,
                "repetition": avg_repetition,
                "match": avg_match
            }
        else:
            # Calculate weighted score (prioritize security)
            weighted_score = (
                0.6 * avg_security +
                0.3 * avg_quality -
                0.2 * avg_repetition +
                0.1 * avg_match
            )
            
            configs[config_name] = {
                "security": avg_security,
                "quality": avg_quality,
                "repetition": avg_repetition,
                "match": avg_match,
                "weighted_score": weighted_score
            }
    
    # Find best configuration
    if configs:
        best_config = max(configs.items(), key=lambda x: x[1]["weighted_score"])
        return {
            "baselines": baselines,
            "configs": configs,
            "best_config": best_config[0],
            "best_config_scores": best_config[1]
        }
    else:
        return {
            "baselines": baselines,
            "configs": {},
            "best_config": None,
            "best_config_scores": None
        }

def analyze_examples(results: Dict) -> Dict:
    """Analyze all vulnerability types."""
    analysis = {}
    
    for vuln_type, vuln_data in results.items():
        analysis[vuln_type] = analyze_vulnerability(vuln_data)
    
    return analysis

def find_best_overall_config(analysis: Dict) -> str:
    """Find the best overall configuration across vulnerability types."""
    config_scores = defaultdict(float)
    
    for vuln_type, vuln_analysis in analysis.items():
        best_config = vuln_analysis["best_config"]
        if best_config:
            config_scores[best_config] += vuln_analysis["best_config_scores"]["weighted_score"]
    
    if config_scores:
        return max(config_scores.items(), key=lambda x: x[1])[0]
    else:
        return None

def analyze_patterns(results: Dict) -> Dict:
    """Analyze which specific patterns were most effective."""
    pattern_effectiveness = defaultdict(lambda: defaultdict(list))
    
    for vuln_type, vuln_data in results.items():
        for config_name, trials in vuln_data.items():
            for trial in trials:
                if "analysis" in trial:
                    for pattern, found in trial["analysis"].items():
                        pattern_effectiveness[vuln_type][pattern].append({
                            "config": config_name,
                            "found": found,
                            "security_score": trial["security_score"],
                            "quality_score": trial["quality_score"]
                        })
    
    # Analyze pattern effectiveness
    pattern_summary = {}
    for vuln_type, patterns in pattern_effectiveness.items():
        pattern_summary[vuln_type] = {}
        for pattern, occurrences in patterns.items():
            found_count = sum(1 for o in occurrences if o["found"])
            total_count = len(occurrences)
            pattern_summary[vuln_type][pattern] = {
                "success_rate": found_count / total_count if total_count > 0 else 0,
                "found_count": found_count,
                "total_count": total_count,
                "configs": {
                    config: sum(1 for o in occurrences if o["config"] == config and o["found"]) / 
                           sum(1 for o in occurrences if o["config"] == config)
                    for config in set(o["config"] for o in occurrences)
                }
            }
    
    return pattern_summary

def format_table(data: List[List[str]], headers: List[str]) -> str:
    """Format data as an ASCII table."""
    # Determine column widths
    col_widths = [max(len(str(x)) for x in col) for col in zip(headers, *data)]
    
    # Create header
    header = "| " + " | ".join(f"{h:{w}}" for h, w in zip(headers, col_widths)) + " |"
    separator = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"
    
    # Create rows
    rows = [
        "| " + " | ".join(f"{str(cell):{w}}" for cell, w in zip(row, col_widths)) + " |"
        for row in data
    ]
    
    # Combine everything
    return "\n".join([separator, header, separator, *rows, separator])

def main():
    # Find most recent results file
    results_dir = "security"
    results_files = [
        os.path.join(results_dir, f) for f in os.listdir(results_dir)
        if f.startswith("bias_optimization_results_") and f.endswith(".json")
    ]
    
    if not results_files:
        print("No results files found!")
        sys.exit(1)
    
    # Get the most recent file
    results_file = max(results_files, key=os.path.getmtime)
    print(f"Analyzing results from: {results_file}")
    
    # Load and analyze results
    results = load_results(results_file)
    analysis = analyze_examples(results)
    best_overall_config = find_best_overall_config(analysis)
    pattern_analysis = analyze_patterns(results)
    
    # Generate report
    report = []
    report.append("=" * 80)
    report.append("SECURITY BIAS OPTIMIZATION RESULTS")
    report.append("=" * 80)
    
    # Overall recommendation
    report.append("\nBEST OVERALL CONFIGURATION:")
    report.append(f"  {best_overall_config}")
    
    # Detailed results per vulnerability type
    report.append("\nRESULTS BY VULNERABILITY TYPE:")
    
    for vuln_type, vuln_analysis in analysis.items():
        report.append(f"\n{vuln_type.upper()}:")
        
        # Baseline scores
        baselines = vuln_analysis["baselines"]
        report.append("  Baseline (no bias):")
        report.append(f"    Security Score: {baselines['security']:.2f}")
        report.append(f"    Quality Score: {baselines['quality']:.2f}")
        report.append(f"    Repetition Score: {baselines['repetition']:.2f}")
        report.append(f"    Match Score: {baselines['match']:.2f}")
        
        # Best configuration
        best_config = vuln_analysis["best_config"]
        if best_config:
            best_scores = vuln_analysis["best_config_scores"]
            report.append(f"  Best Configuration: {best_config}")
            report.append(f"    Security Score: {best_scores['security']:.2f} ({best_scores['security'] - baselines['security']:+.2f})")
            report.append(f"    Quality Score: {best_scores['quality']:.2f} ({best_scores['quality'] - baselines['quality']:+.2f})")
            report.append(f"    Repetition Score: {best_scores['repetition']:.2f} ({best_scores['repetition'] - baselines['repetition']:+.2f})")
            report.append(f"    Match Score: {best_scores['match']:.2f} ({best_scores['match'] - baselines['match']:+.2f})")
            report.append(f"    Weighted Score: {best_scores['weighted_score']:.2f}")
        
        # All configurations table
        configs = vuln_analysis["configs"]
        if configs:
            report.append("\n  All Configurations:")
            
            # Prepare table data
            headers = ["Config", "Security", "Quality", "Repetition", "Match", "Weighted"]
            rows = []
            for config_name, scores in configs.items():
                rows.append([
                    config_name,
                    f"{scores['security']:.2f}",
                    f"{scores['quality']:.2f}",
                    f"{scores['repetition']:.2f}",
                    f"{scores['match']:.2f}",
                    f"{scores['weighted_score']:.2f}"
                ])
            
            # Sort rows by weighted score
            rows.sort(key=lambda x: float(x[5]), reverse=True)
            
            # Add table to report
            table = format_table(rows, headers)
            report.extend(["  " + line for line in table.split("\n")])
    
    # Pattern effectiveness analysis
    report.append("\nPATTERN EFFECTIVENESS ANALYSIS:")
    
    for vuln_type, patterns in pattern_analysis.items():
        report.append(f"\n{vuln_type.upper()} PATTERNS:")
        
        # Prepare table data
        headers = ["Pattern", "Success Rate", "Found", "Total"]
        rows = []
        for pattern_name, stats in patterns.items():
            rows.append([
                pattern_name,
                f"{stats['success_rate']:.2f}",
                f"{stats['found_count']}",
                f"{stats['total_count']}"
            ])
        
        # Sort rows by success rate
        rows.sort(key=lambda x: float(x[1]), reverse=True)
        
        # Add table to report
        table = format_table(rows, headers)
        report.extend(["  " + line for line in table.split("\n")])
    
    # Print report
    print("\n".join(report))
    
    # Save report to file
    report_file = results_file.replace(".json", "_analysis.txt")
    with open(report_file, "w") as f:
        f.write("\n".join(report))
    
    print(f"\nAnalysis saved to: {report_file}")

if __name__ == "__main__":
    main() 