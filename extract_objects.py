import json

def extract_first_n_objects(input_file, output_file, n):
    with open(input_file, 'r') as fin:
        # Skip first line (opening bracket)
        fin.readline()
        
        objects = []
        current_object = []
        brace_count = 0
        
        for line in fin:
            brace_count += line.count('{') - line.count('}')
            current_object.append(line)
            
            if brace_count == 0 and line.strip():
                # We found a complete object
                obj_str = ''.join(current_object).strip()
                if obj_str.endswith(','):
                    obj_str = obj_str[:-1]
                
                # Validate that this is valid JSON
                try:
                    obj = json.loads(obj_str)
                    objects.append(obj)
                    if len(objects) >= n:
                        break
                except json.JSONDecodeError:
                    print(f"Warning: Found invalid JSON object, skipping")
                
                current_object = []
    
    # Write the objects to output file
    with open(output_file, 'w') as fout:
        json.dump(objects, fout, indent=2)

if __name__ == '__main__':
    extract_first_n_objects(
        'data/steering_results/steering_results.json',
        'data/steering_results/test_small.json',
        2
    ) 