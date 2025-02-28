import json

def pretty_print_jsonl(file_path):
    with open(file_path, 'r') as f:
        # Just read the first line as an example
        data = json.loads(f.readline())
        
        print("=" * 80)
        print("Example FIM Task")
        print("=" * 80)
        print(f"Name: {data['name']}")
        print(f"Language: {data['language']}")
        print("\nPrompt (broken down):")
        
        # Break down the FIM parts
        prompt = data['prompt']
        parts = prompt.split('<fim_')
        
        print("\nPrefix part:")
        print(parts[0].strip())
        
        for part in parts[1:]:
            if part.startswith('prefix>'):
                print("\nPrefix marker content:")
                print(part[7:].strip())
            elif part.startswith('suffix>'):
                print("\nSuffix marker content:")
                print(part[7:].strip())
            elif part.startswith('middle>'):
                print("\nMiddle marker content:")
                print(part[7:].strip())
                
        print("\nCanonical Solution:")
        print(data['canonical_solution'])
        print("\n" + "=" * 80)

if __name__ == "__main__":
    pretty_print_jsonl("starcoder1_fim_py.jsonl") 