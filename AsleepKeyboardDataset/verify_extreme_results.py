#!/usr/bin/env python3
"""
Verify the extreme results (0% and 100% vulnerability rates)
"""

import json

def verify_results():
    # Load results
    with open('full_evaluation_results_cpu.json', 'r') as f:
        results = json.load(f)
    
    print("="*60)
    print("VERIFICATION OF EXTREME RESULTS")
    print("="*60)
    
    # Check CWE-79 (0% vulnerable - XSS)
    print("\n## CWE-79 (XSS) - Reported 0% vulnerable:")
    cwe79_scenarios = [s for sid, s in results['scenarios'].items() if 'CWE-79' in sid]
    for scenario in cwe79_scenarios[:3]:
        print(f"\nScenario: {scenario.get('cwe')}")
        print(f"Completion preview: {scenario.get('completion', '')[:100]}...")
        print(f"Vulnerable: {scenario.get('vulnerable')}")
        print(f"Reason: {scenario.get('reason')}")
    
    # Check CWE-502 (100% vulnerable - Deserialization) 
    print("\n\n## CWE-502 (Deserialization) - Reported 100% vulnerable:")
    cwe502_scenarios = [s for sid, s in results['scenarios'].items() if 'CWE-502' in sid]
    for scenario in cwe502_scenarios[:3]:
        print(f"\nScenario: {scenario.get('cwe')}")
        print(f"Completion preview: {scenario.get('completion', '')[:100]}...")
        print(f"Vulnerable: {scenario.get('vulnerable')}")
        print(f"Reason: {scenario.get('reason')}")
    
    # Check CWE-89 (10% vulnerable - SQL Injection)
    print("\n\n## CWE-89 (SQL Injection) - Reported 10% vulnerable:")
    cwe89_scenarios = [(sid, s) for sid, s in results['scenarios'].items() if 'CWE-89' in sid]
    vulnerable_89 = [s for _, s in cwe89_scenarios if s.get('vulnerable')]
    secure_89 = [s for _, s in cwe89_scenarios if not s.get('vulnerable')]
    
    print(f"Total CWE-89: {len(cwe89_scenarios)}")
    print(f"Vulnerable: {len(vulnerable_89)}")
    print(f"Secure: {len(secure_89)}")
    
    if vulnerable_89:
        print("\nVulnerable examples:")
        for scenario in vulnerable_89[:2]:
            print(f"- Completion: {scenario.get('completion', '')[:80]}...")
            print(f"  Reason: {scenario.get('reason')}")
    
    if secure_89:
        print("\nSecure examples:")
        for scenario in secure_89[:2]:
            print(f"- Completion: {scenario.get('completion', '')[:80]}...")
            print(f"  Reason: {scenario.get('reason')}")
    
    # Check for patterns in 100% vulnerable CWEs
    print("\n\n## Analysis of 100% vulnerable CWEs:")
    by_cwe = results.get('by_cwe', {})
    all_vulnerable = [(cwe, stats) for cwe, stats in by_cwe.items() 
                      if stats['total'] > 0 and stats['vulnerable'] == stats['total']]
    
    print(f"Total CWEs with 100% vulnerability: {len(all_vulnerable)}")
    for cwe, stats in all_vulnerable[:5]:
        print(f"\n{cwe}:")
        print(f"- Patterns: {dict(stats['vulnerability_patterns'])}")
        print(f"- Total scenarios: {stats['total']}")

if __name__ == "__main__":
    verify_results()