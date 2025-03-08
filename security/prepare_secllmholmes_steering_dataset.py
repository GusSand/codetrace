#!/usr/bin/env python3
import os
import json
import argparse
import random
from typing import List, Dict, Any, Tuple
from pathlib import Path

def load_file_content(file_path: str) -> str:
    """Load the content of a file."""
    with open(file_path, 'r') as f:
        return f.read()

def get_hand_crafted_pairs(base_dir: str, num_pairs: int = 10) -> List[Dict]:
    """
    Get pairs of vulnerable and patched code from hand-crafted examples.
    Returns a list of dictionaries with vulnerable and secure code.
    """
    base_path = Path(base_dir) / "hand-crafted" / "dataset"
    pairs = []
    
    # Find all CWE directories
    cwe_dirs = [d for d in base_path.iterdir() if d.is_dir()]
    
    for cwe_dir in cwe_dirs:
        cwe_id = cwe_dir.name
        
        # Find vulnerable/patched pairs (files with and without p_ prefix)
        vuln_files = [f for f in cwe_dir.iterdir() if not f.name.startswith("p_") and f.is_file()]
        
        for vuln_file in vuln_files:
            patched_file = cwe_dir / f"p_{vuln_file.name}"
            
            if patched_file.exists():
                vuln_code = load_file_content(str(vuln_file))
                secure_code = load_file_content(str(patched_file))
                
                pairs.append({
                    "vulnerable": vuln_code,
                    "secure": secure_code,
                    "cwe": cwe_id,
                    "source": "hand-crafted",
                    "file_name": vuln_file.name
                })
    
    # If we have more pairs than requested, randomly select
    if len(pairs) > num_pairs:
        # First, make sure we have at least one example from each CWE if possible
        cwe_groups = {}
        for pair in pairs:
            cwe = pair["cwe"]
            if cwe not in cwe_groups:
                cwe_groups[cwe] = []
            cwe_groups[cwe].append(pair)
        
        # Select one example from each CWE
        selected_pairs = []
        for cwe, cwe_pairs in cwe_groups.items():
            selected_pairs.append(random.choice(cwe_pairs))
        
        # If we still need more examples, randomly select from remaining pairs
        remaining_count = num_pairs - len(selected_pairs)
        if remaining_count > 0:
            # Remove already selected pairs
            remaining_pairs = [p for p in pairs if p not in selected_pairs]
            # Randomly select from remaining
            selected_pairs.extend(random.sample(remaining_pairs, min(remaining_count, len(remaining_pairs))))
        
        pairs = selected_pairs[:num_pairs]
    
    return pairs

def get_real_world_pairs(base_dir: str, num_pairs: int = 10) -> List[Dict]:
    """
    Get pairs of vulnerable and patched code from real-world CVEs.
    Returns a list of dictionaries with vulnerable and secure code.
    """
    base_path = Path(base_dir) / "real-world"
    cve_details_path = base_path / "cve_details.json"
    
    with open(cve_details_path, 'r') as f:
        cve_details = json.load(f)
    
    pairs = []
    
    # Process each project
    for project, cves in cve_details.items():
        project_path = base_path / project
        
        for cve_id, details in cves.items():
            cve_path = project_path / cve_id
            
            # Get the simplified C files if they exist
            vuln_c_path = cve_path / "vuln.c"
            patch_c_path = cve_path / "patch.c"
            
            if vuln_c_path.exists() and patch_c_path.exists():
                vuln_code = load_file_content(str(vuln_c_path))
                secure_code = load_file_content(str(patch_c_path))
                
                pairs.append({
                    "vulnerable": vuln_code,
                    "secure": secure_code,
                    "cwe": details.get("cwe", "unknown"),
                    "source": "real-world",
                    "cve": cve_id,
                    "project": project
                })
    
    # If we have more pairs than requested, randomly select
    if len(pairs) > num_pairs:
        # First, make sure we have at least one example from each CWE if possible
        cwe_groups = {}
        for pair in pairs:
            cwe = pair["cwe"]
            if cwe not in cwe_groups:
                cwe_groups[cwe] = []
            cwe_groups[cwe].append(pair)
        
        # Select one example from each CWE
        selected_pairs = []
        for cwe, cwe_pairs in cwe_groups.items():
            selected_pairs.append(random.choice(cwe_pairs))
        
        # If we still need more examples, randomly select from remaining pairs
        remaining_count = num_pairs - len(selected_pairs)
        if remaining_count > 0:
            # Remove already selected pairs
            remaining_pairs = [p for p in pairs if p not in selected_pairs]
            # Randomly select from remaining
            selected_pairs.extend(random.sample(remaining_pairs, min(remaining_count, len(remaining_pairs))))
        
        pairs = selected_pairs[:num_pairs]
    
    return pairs

def prepare_steering_data(pairs: List[Dict]) -> List[Dict]:
    """
    Prepare the steering data from pairs of vulnerable and secure code.
    """
    steering_data = []
    
    for idx, pair in enumerate(pairs):
        vuln_code = pair['vulnerable']
        secure_code = pair['secure']
        cwe = pair.get('cwe', 'unknown').upper()  # Ensure consistent upper case format
        source = pair.get('source', 'unknown')
        
        # Determine a more specific vulnerability type if available
        if cwe.upper().startswith("CWE-"):
            cwe_map = {
                "CWE-89": "sql_injection",
                "CWE-79": "xss",
                "CWE-22": "path_traversal",
                "CWE-787": "out_of_bounds_write",
                "CWE-476": "null_pointer_dereference",
                "CWE-190": "integer_overflow",
                "CWE-77": "command_injection",
                "CWE-416": "use_after_free"
            }
            vulnerability_type = cwe_map.get(cwe, cwe.lower())
        else:
            # Handle cases where CWE is not in standard format
            cwe_norm = "CWE-" + cwe.upper().replace("CWE", "").strip("-").strip()
            vulnerability_type = cwe_norm
        
        # Create steering example - for security we want to steer AWAY from vulnerable code
        # and TOWARD secure code
        steering_example = {
            "prompt": f"Security review of this code:\n\n{vuln_code}",
            "completion": "This code contains security vulnerabilities.",
            "mutated_program": secure_code,
            "source": source,
            "cwe": cwe,
            "vulnerability_type": vulnerability_type,
            "idx": idx,
            "typechecks": True  # Assuming all examples typecheck
        }
        
        # Add additional fields from the original pair
        for key, value in pair.items():
            if key not in steering_example and key not in ['vulnerable', 'secure', 'similarity']:
                steering_example[key] = value
        
        steering_data.append(steering_example)
    
    return steering_data

def main():
    parser = argparse.ArgumentParser(description='Prepare security steering dataset from SecLLMHolmes')
    parser.add_argument('--base_dir', type=str, 
                      default='./SecLLMHolmes/datasets',
                      help='Path to the SecLLMHolmes datasets directory')
    parser.add_argument('--output_file', type=str, default='./security_steering_data.json',
                      help='Output file for the steering dataset')
    parser.add_argument('--hand_crafted_pairs', type=int, default=25,
                      help='Number of hand-crafted pairs to include')
    parser.add_argument('--real_world_pairs', type=int, default=25,
                      help='Number of real-world pairs to include')
    args = parser.parse_args()
    
    # Get pairs from hand-crafted examples
    hand_crafted_pairs = get_hand_crafted_pairs(args.base_dir, args.hand_crafted_pairs)
    print(f"Selected {len(hand_crafted_pairs)} hand-crafted pairs")
    
    # Get pairs from real-world CVEs
    real_world_pairs = get_real_world_pairs(args.base_dir, args.real_world_pairs)
    print(f"Selected {len(real_world_pairs)} real-world pairs")
    
    # Combine pairs
    all_pairs = hand_crafted_pairs + real_world_pairs
    
    # Prepare steering data
    steering_data = prepare_steering_data(all_pairs)
    
    # Print statistics
    cwe_counts = {}
    source_counts = {}
    for example in steering_data:
        cwe = example['cwe']
        source = example['source']
        
        if cwe not in cwe_counts:
            cwe_counts[cwe] = 0
        cwe_counts[cwe] += 1
        
        if source not in source_counts:
            source_counts[source] = 0
        source_counts[source] += 1
    
    print("\nSteering data statistics:")
    print(f"Total examples: {len(steering_data)}")
    
    print("\nExamples by source:")
    for source, count in source_counts.items():
        print(f"- {source}: {count}")
    
    print("\nExamples by CWE:")
    for cwe, count in cwe_counts.items():
        print(f"- {cwe}: {count}")
    
    # Save the steering data
    with open(args.output_file, 'w') as f:
        json.dump(steering_data, f, indent=2)
    
    print(f"\nSaved steering data to {args.output_file}")
    print("\nTo run the steering process, use:")
    print(f"python3 -m steering.run_steering --model bigcode/starcoderbase-1b \\\n"
          f"--output_dir security_steering_results \\\n"
          f"--test_split datasets/codexglue/CodeXGLUE/Code-Code/Defect-detection/dataset/test.jsonl \\\n"
          f"--test_steer_batch_size 32 \\\n"
          f"--test_batch_size 32 \\\n"
          f"--steering_file {args.output_file}")

if __name__ == "__main__":
    main() 