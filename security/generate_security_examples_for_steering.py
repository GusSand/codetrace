#!/usr/bin/env python3
import json
import os

def create_security_examples_for_steering():
    """
    Create security examples properly formatted for Fill-In-Middle (FIM) steering.
    
    Each example contains:
    - fim_program: Code with a placeholder (<FILL>) where secure code should go
    - mutated_program: Vulnerable code (negative example, what we want to steer away from)
    - fim_type: Secure code (positive example, what should fill the placeholder)
    - prefix: Text before the placeholder (NOT including FIM tags)
    - suffix: Text after the placeholder (NOT including FIM tags)
    - middle: The expected content for the placeholder (same as fim_type)
    
    The steering pipeline will convert the placeholder format to FIM format with tokens:
    <fim_prefix>prefix<fim_suffix>suffix<fim_middle>middle
    """
    examples = [
        # SQL Injection (CWE-89)
        {
            "secure": 'def search_users(user_input):\n    query = "SELECT * FROM users WHERE name = %s"\n    return execute_query(query, (user_input,))',
            "vulnerable": 'def search_users(user_input):\n    query = "SELECT * FROM users WHERE name = \'" + user_input + "\'"\n    return execute_query(query)',
            "cwe": "CWE-89",
            "vulnerability_type": "sql_injection"
        },
        # XSS (CWE-79)
        {
            "secure": 'def show_user_profile(username):\n    import html\n    return f"<div>Welcome, {html.escape(username)}!</div>"',
            "vulnerable": 'def show_user_profile(username):\n    return f"<div>Welcome, {username}!</div>"',
            "cwe": "CWE-79",
            "vulnerability_type": "xss"
        },
        # Path Traversal (CWE-22)
        {
            "secure": 'def read_file(filename):\n    import os\n    if "../" in filename or filename.startswith("/"):\n        raise ValueError("Invalid filename")\n    with open(os.path.join("/app/files", filename), "r") as f:\n        return f.read()',
            "vulnerable": 'def read_file(filename):\n    with open(f"/app/files/{filename}", "r") as f:\n        return f.read()',
            "cwe": "CWE-22",
            "vulnerability_type": "path_traversal"
        },
        # Command Injection (CWE-77)
        {
            "secure": 'def ping_host(hostname):\n    import subprocess\n    import shlex\n    return subprocess.call(["ping", "-c", "1", hostname])',
            "vulnerable": 'def ping_host(hostname):\n    import os\n    return os.system(f"ping -c 1 {hostname}")',
            "cwe": "CWE-77",
            "vulnerability_type": "command_injection"
        },
        # Integer Overflow (CWE-190)
        {
            "secure": 'def allocate_buffer(size):\n    if (size > MAX_SIZE / 4):\n        return None\n    buffer = new char[size * 4];\n    return buffer;',
            "vulnerable": 'def allocate_buffer(size):\n    buffer = new char[size * 4];\n    return buffer;',
            "cwe": "CWE-190",
            "vulnerability_type": "integer_overflow"
        },
        # Null Pointer Dereference (CWE-476)
        {
            "secure": 'def process_data(data):\n    if data is None:\n        return None\n    return data.process()',
            "vulnerable": 'def process_data(data):\n    return data.process()',
            "cwe": "CWE-476",
            "vulnerability_type": "null_pointer_dereference"
        },
        # Use After Free (CWE-416)
        {
            "secure": 'void process():\n    char* ptr = malloc(10);\n    free(ptr);\n    ptr = NULL;  // Avoid use after free',
            "vulnerable": 'void process():\n    char* ptr = malloc(10);\n    free(ptr);\n    ptr[0] = \'A\';',
            "cwe": "CWE-416",
            "vulnerability_type": "use_after_free"
        },
        # Buffer Overflow (CWE-787)
        {
            "secure": 'void copy_data(char* src):\n    char dest[10];\n    strncpy(dest, src, 9);\n    dest[9] = \'\\0\';',
            "vulnerable": 'void copy_data(char* src):\n    char dest[10];\n    strcpy(dest, src);',
            "cwe": "CWE-787",
            "vulnerability_type": "out_of_bounds_write"
        },
        # Hardcoded Credentials (CWE-798)
        {
            "secure": 'def connect_to_database():\n    return db_connect(get_env("DB_USER"), get_env("DB_PASSWORD"))',
            "vulnerable": 'def connect_to_database():\n    return db_connect("admin", "password123")',
            "cwe": "CWE-798",
            "vulnerability_type": "hardcoded_credentials"
        },
        # Missing Authorization (CWE-862)
        {
            "secure": 'def delete_user(user_id):\n    if current_user.is_admin():\n        db.execute("DELETE FROM users WHERE id = %s", user_id)\n    else:\n        raise PermissionError("Not authorized")',
            "vulnerable": 'def delete_user(user_id):\n    db.execute("DELETE FROM users WHERE id = %s", user_id)',
            "cwe": "CWE-862",
            "vulnerability_type": "missing_authorization"
        }
    ]
    
    # Format the examples for the steering pipeline
    steering_examples = []
    for idx, example in enumerate(examples):
        # For the FIM placeholder format, we need text before and after the placeholder
        # The placeholder must be surrounded by text on both sides
        
        # Create a comment header
        header = f"// Security task: Replace vulnerable code with secure implementation\n// Vulnerability: {example['vulnerability_type']} ({example['cwe']})\n\n"
        
        # Get the function signature (first line) from the vulnerable code
        vulnerable_lines = example["vulnerable"].split('\n')
        function_signature = vulnerable_lines[0]
        
        # Create prefix - everything before the placeholder
        prefix = header + function_signature + " "
        
        # Create suffix - everything after the placeholder
        # We need to ensure there's text after the placeholder
        suffix = " " + "\n".join(vulnerable_lines[1:])
        
        # The middle is the secure implementation excluding the first line
        secure_lines = example["secure"].split('\n')
        middle = "\n".join(secure_lines[1:])
        
        # Create the FIM program with placeholder between prefix and suffix
        fim_program = f"{prefix}<FILL>{suffix}"
        
        steering_example = {
            "fim_program": fim_program,              # Program with placeholder
            "fim_type": example["secure"],          # Secure code (complete function)
            "mutated_program": example["vulnerable"],  # Vulnerable code (negative example)
            
            # Include the FIM parts for the steering pipeline
            "prefix": prefix,
            "suffix": suffix, 
            "middle": middle,
            
            # Include original versions for reference
            "original_secure_code": example["secure"],
            "original_vulnerable_code": example["vulnerable"],
            
            # Metadata
            "cwe": example["cwe"],
            "vulnerability_type": example["vulnerability_type"],
            "idx": idx,
            "source": "simple-generated",
            "typechecks": True
        }
        steering_examples.append(steering_example)
    
    # Save to file
    output_path = "security_steering_examples.json"
    with open(output_path, 'w') as f:
        json.dump(steering_examples, f, indent=2)
    
    print(f"Created {len(steering_examples)} security examples in {output_path}")

if __name__ == "__main__":
    create_security_examples_for_steering()