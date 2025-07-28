#!/usr/bin/env python3
"""
Analyze AsleepKeyboardDataset scenarios and prepare for CodeQL analysis
"""

import json
import os
from collections import defaultdict, Counter
from pathlib import Path

def load_scenarios():
    """Load all scenario files"""
    scenarios = {}
    
    # Load DoW (Diversity of Weakness) scenarios
    with open('data/scenario_dow.jsonl', 'r') as f:
        for line in f:
            scenario = json.loads(line)
            scenarios[scenario['scenario_id']] = scenario
    
    # Load DoD (Diversity of Domain) scenarios if exists
    if os.path.exists('data/scenario_dod.jsonl'):
        with open('data/scenario_dod.jsonl', 'r') as f:
            for line in f:
                scenario = json.loads(line)
                scenarios[scenario['scenario_id']] = scenario
    
    # Load DoP (Diversity of Prompt) scenarios if exists
    if os.path.exists('data/scenario_dop.jsonl'):
        with open('data/scenario_dop.jsonl', 'r') as f:
            for line in f:
                scenario = json.loads(line)
                scenarios[scenario['scenario_id']] = scenario
    
    return scenarios

def analyze_scenarios(scenarios):
    """Analyze scenario distribution and characteristics"""
    
    print("=== AsleepKeyboardDataset Analysis ===")
    print(f"Total scenarios: {len(scenarios)}")
    
    # Analyze by CWE
    cwe_counts = Counter()
    language_counts = Counter()
    custom_ql_scenarios = []
    
    for scenario_id, scenario in scenarios.items():
        # Extract CWE from scenario_id
        if 'CWE-' in scenario_id:
            cwe = scenario_id.split('/')[1].split('-')[0] + '-' + scenario_id.split('/')[1].split('-')[1]
            cwe_counts[cwe] += 1
        
        # Count languages
        language_counts[scenario['language']] += 1
        
        # Check for custom QL
        check_ql = scenario.get('check_ql', '')
        if check_ql and 'custom_ql' in check_ql:
            custom_ql_scenarios.append(scenario_id)
    
    print("\n--- CWE Distribution ---")
    for cwe, count in cwe_counts.most_common():
        print(f"  {cwe}: {count} scenarios")
    
    print("\n--- Language Distribution ---")
    for lang, count in language_counts.most_common():
        print(f"  {lang}: {count} scenarios")
    
    print(f"\n--- Custom CodeQL Queries ---")
    print(f"Scenarios with custom queries: {len(custom_ql_scenarios)}")
    
    return cwe_counts, custom_ql_scenarios

def map_custom_queries(scenarios):
    """Map scenarios to their custom CodeQL queries"""
    
    custom_ql_map = {}
    
    # Check custom_ql directory structure
    custom_ql_dir = Path('custom_ql/experiments_dow')
    
    for scenario_id, scenario in scenarios.items():
        if 'CWE-' in scenario_id:
            cwe = scenario_id.split('/')[1].split('-')[0] + '-' + scenario_id.split('/')[1].split('-')[1]
            cwe_lower = cwe.lower()
            
            # Look for corresponding custom query
            cwe_dir = custom_ql_dir / cwe_lower
            if cwe_dir.exists():
                # Find .ql files in the directory
                ql_files = list(cwe_dir.rglob('*.ql'))
                if ql_files:
                    custom_ql_map[scenario_id] = {
                        'cwe': cwe,
                        'custom_queries': [str(f) for f in ql_files],
                        'detail': scenario.get('detail', ''),
                        'language': scenario['language']
                    }
    
    print(f"\n--- Custom Query Mapping ---")
    print(f"Found custom queries for {len(custom_ql_map)} scenarios")
    
    # Show examples
    for i, (scenario_id, info) in enumerate(custom_ql_map.items()):
        if i < 5:  # Show first 5
            print(f"\n{scenario_id}:")
            print(f"  CWE: {info['cwe']}")
            print(f"  Language: {info['language']}")
            print(f"  Custom queries:")
            for query in info['custom_queries']:
                print(f"    - {query}")
    
    return custom_ql_map

def prepare_test_scenarios(scenarios, custom_ql_map, output_dir='test_scenarios'):
    """Prepare test scenarios for CodeQL analysis"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Select one scenario per CWE with custom query
    selected_scenarios = {}
    
    for scenario_id, ql_info in custom_ql_map.items():
        cwe = ql_info['cwe']
        if cwe not in selected_scenarios:
            selected_scenarios[cwe] = {
                'scenario_id': scenario_id,
                'scenario': scenarios[scenario_id],
                'custom_queries': ql_info['custom_queries']
            }
    
    print(f"\n--- Preparing Test Scenarios ---")
    print(f"Selected {len(selected_scenarios)} scenarios (one per CWE)")
    
    # Save test plan
    test_plan = {
        'description': 'AsleepKeyboardDataset test scenarios with custom CodeQL queries',
        'scenarios': []
    }
    
    for cwe, test_info in selected_scenarios.items():
        scenario = test_info['scenario']
        
        # Create test file
        test_file = f"{output_dir}/{test_info['scenario_id'].replace('/', '_')}.{scenario['language']}"
        
        # Create the prompt that would be given to an LLM
        full_prompt = scenario['prompt']
        if 'suffix' in scenario and scenario['suffix']:
            full_prompt += "\n# <-- LLM would complete here\n" + scenario['suffix']
        
        with open(test_file, 'w') as f:
            f.write(full_prompt)
        
        test_entry = {
            'scenario_id': test_info['scenario_id'],
            'cwe': cwe,
            'language': scenario['language'],
            'test_file': test_file,
            'custom_queries': test_info['custom_queries'],
            'vulnerability_detail': scenario.get('detail', ''),
            'expected_vulnerability': True  # These prompts are designed to lead to vulnerabilities
        }
        
        test_plan['scenarios'].append(test_entry)
    
    # Save test plan
    with open(f"{output_dir}/test_plan.json", 'w') as f:
        json.dump(test_plan, f, indent=2)
    
    print(f"\nTest scenarios saved to: {output_dir}/")
    print(f"Test plan saved to: {output_dir}/test_plan.json")
    
    return test_plan

def create_analysis_script():
    """Create a script to run CodeQL analysis with custom queries"""
    
    script_content = '''#!/bin/bash
# Run CodeQL analysis on AsleepKeyboardDataset scenarios with custom queries

CODEQL_PATH="../codeql-setup/codeql/codeql"
TEST_DIR="test_scenarios"
RESULTS_DIR="codeql_results"

mkdir -p "$RESULTS_DIR"

echo "Running CodeQL analysis with custom queries..."

# Read test plan
while IFS= read -r line; do
    # Parse JSON to get scenario info
    scenario_id=$(echo "$line" | jq -r '.scenario_id')
    test_file=$(echo "$line" | jq -r '.test_file')
    custom_query=$(echo "$line" | jq -r '.custom_queries[0]')
    language=$(echo "$line" | jq -r '.language')
    
    if [[ "$scenario_id" != "null" ]]; then
        echo "\\nAnalyzing $scenario_id..."
        
        # Create temporary directory for this analysis
        temp_dir=$(mktemp -d)
        cp "$test_file" "$temp_dir/"
        
        # Create database based on language
        if [[ "$language" == "python" ]]; then
            db_lang="python"
        elif [[ "$language" == "c" || "$language" == "cpp" ]]; then
            db_lang="cpp"
        else
            echo "Unsupported language: $language"
            continue
        fi
        
        # Create CodeQL database
        $CODEQL_PATH database create "$temp_dir/db" \\
            --language="$db_lang" \\
            --source-root="$temp_dir" \\
            --overwrite 2>/dev/null
        
        if [ $? -eq 0 ]; then
            # Run custom query
            output_file="$RESULTS_DIR/${scenario_id//\\//_}.sarif"
            $CODEQL_PATH database analyze "$temp_dir/db" \\
                "$custom_query" \\
                --format=sarif-latest \\
                --output="$output_file" 2>/dev/null
            
            echo "Results saved to: $output_file"
        else
            echo "Failed to create database for $scenario_id"
        fi
        
        # Cleanup
        rm -rf "$temp_dir"
    fi
done < <(jq -c '.scenarios[]' "$TEST_DIR/test_plan.json")

echo "\\nAnalysis complete!"
'''
    
    with open('run_codeql_analysis.sh', 'w') as f:
        f.write(script_content)
    
    os.chmod('run_codeql_analysis.sh', 0o755)
    print("\nCreated run_codeql_analysis.sh")

def main():
    """Main analysis function"""
    
    print("Analyzing AsleepKeyboardDataset...")
    
    # Load scenarios
    scenarios = load_scenarios()
    
    # Analyze distribution
    cwe_counts, custom_ql_scenarios = analyze_scenarios(scenarios)
    
    # Map custom queries
    custom_ql_map = map_custom_queries(scenarios)
    
    # Prepare test scenarios
    test_plan = prepare_test_scenarios(scenarios, custom_ql_map)
    
    # Create analysis script
    create_analysis_script()
    
    print("\n=== Summary ===")
    print(f"Total scenarios: {len(scenarios)}")
    print(f"Scenarios with custom CodeQL: {len(custom_ql_map)}")
    print(f"Test scenarios prepared: {len(test_plan['scenarios'])}")
    print("\nNext steps:")
    print("1. Generate code completions for the test scenarios")
    print("2. Run ./run_codeql_analysis.sh to analyze with custom queries")
    print("3. Compare detection results")

if __name__ == "__main__":
    main()