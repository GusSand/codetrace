#!/usr/bin/env python3
import json
from collections import Counter

def main():
    # Load the security steering dataset
    with open('security_steering_data.json', 'r') as f:
        data = json.load(f)
    
    # Count CWEs
    cwes = [example['cwe'] for example in data]
    cwe_count = Counter(cwes)
    
    # Print distribution
    print('CWE distribution:')
    for cwe, count in sorted(cwe_count.items()):
        print(f'- {cwe}: {count}')
    
    # Print by source
    print('\nCWE distribution by source:')
    hand_crafted = [example['cwe'] for example in data if example['source'] == 'hand-crafted']
    real_world = [example['cwe'] for example in data if example['source'] == 'real-world']
    
    print('\nHand-crafted examples:')
    hc_count = Counter(hand_crafted)
    for cwe, count in sorted(hc_count.items()):
        print(f'- {cwe}: {count}')
    
    print('\nReal-world examples:')
    rw_count = Counter(real_world)
    for cwe, count in sorted(rw_count.items()):
        print(f'- {cwe}: {count}')

if __name__ == "__main__":
    main() 