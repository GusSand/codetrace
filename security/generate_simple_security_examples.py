#!/usr/bin/env python3
import json
import os

def create_simple_examples():
    """
    Create simple security examples that are more likely to work with the steering pipeline.
    Each example will be a short snippet with a clear security vulnerability and its fix.
    """
    examples = [
        # SQL Injection (CWE-89)
        {
            "vulnerable": 'def search_users(user_input):\n    query = "SELECT * FROM users WHERE name = \'" + user_input + "\'"\n    return execute_query(query)',
            "secure": 'def search_users(user_input):\n    query = "SELECT * FROM users WHERE name = %s"\n    return execute_query(query, (user_input,))',
            "cwe": "CWE-89",
            "vulnerability_type": "sql_injection"
        },
        # XSS (CWE-79)
        {
            "vulnerable": 'def show_user_profile(username):\n    return f"<div>Welcome, {username}!</div>"',
            "secure": 'def show_user_profile(username):\n    import html\n    return f"<div>Welcome, {html.escape(username)}!</div>"',
            "cwe": "CWE-79",
            "vulnerability_type": "xss"
        },
        # Path Traversal (CWE-22)
        {
            "vulnerable": 'def read_file(filename):\n    with open(f"/app/files/{filename}", "r") as f:\n        return f.read()',
            "secure": 'def read_file(filename):\n    import os\n    if "../" in filename or filename.startswith("/"):\n        raise ValueError("Invalid filename")\n    with open(os.path.join("/app/files", filename), "r") as f:\n        return f.read()',
            "cwe": "CWE-22",
            "vulnerability_type": "path_traversal"
        },
        # Command Injection (CWE-77)
        {
            "vulnerable": 'def ping_host(hostname):\n    import os\n    return os.system(f"ping -c 1 {hostname}")',
            "secure": 'def ping_host(hostname):\n    import subprocess\n    import shlex\n    return subprocess.call(["ping", "-c", "1", hostname])',
            "cwe": "CWE-77",
            "vulnerability_type": "command_injection"
        },
        # Integer Overflow (CWE-190)
        {
            "vulnerable": 'def allocate_buffer(size):\n    buffer = new char[size * 4];\n    return buffer;',
            "secure": 'def allocate_buffer(size):\n    if (size > MAX_SIZE / 4):\n        return None\n    buffer = new char[size * 4];\n    return buffer;',
            "cwe": "CWE-190",
            "vulnerability_type": "integer_overflow"
        },
        # Null Pointer Dereference (CWE-476)
        {
            "vulnerable": 'def process_data(data):\n    return data.process()',
            "secure": 'def process_data(data):\n    if data is None:\n        return None\n    return data.process()',
            "cwe": "CWE-476",
            "vulnerability_type": "null_pointer_dereference"
        },
        # Use After Free (CWE-416)
        {
            "vulnerable": 'void process():\n    char* ptr = malloc(10);\n    free(ptr);\n    ptr[0] = \'A\';',
            "secure": 'void process():\n    char* ptr = malloc(10);\n    free(ptr);\n    ptr = NULL;  // Avoid use after free',
            "cwe": "CWE-416",
            "vulnerability_type": "use_after_free"
        },
        # Buffer Overflow (CWE-787)
        {
            "vulnerable": 'void copy_data(char* src):\n    char dest[10];\n    strcpy(dest, src);',
            "secure": 'void copy_data(char* src):\n    char dest[10];\n    strncpy(dest, src, 9);\n    dest[9] = \'\\0\';',
            "cwe": "CWE-787",
            "vulnerability_type": "out_of_bounds_write"
        },
        # Hardcoded Credentials (CWE-798)
        {
            "vulnerable": 'def connect_to_database():\n    return db_connect("admin", "password123")',
            "secure": 'def connect_to_database():\n    return db_connect(get_env("DB_USER"), get_env("DB_PASSWORD"))',
            "cwe": "CWE-798",
            "vulnerability_type": "hardcoded_credentials"
        },
        # Missing Authorization (CWE-862)
        {
            "vulnerable": 'def delete_user(user_id):\n    db.execute("DELETE FROM users WHERE id = %s", user_id)',
            "secure": 'def delete_user(user_id):\n    if current_user.is_admin():\n        db.execute("DELETE FROM users WHERE id = %s", user_id)\n    else:\n        raise PermissionError("Not authorized")',
            "cwe": "CWE-862",
            "vulnerability_type": "missing_authorization"
        }
    ]
    
    # Format the examples for the FIM task
    fim_examples = []
    for idx, example in enumerate(examples):
        fim_example = {
            "fim_program": example["vulnerable"] + "\n\n// The secure version of this code is:\n<FILL>",
            "fim_type": example["secure"],
            "cwe": example["cwe"],
            "vulnerability_type": example["vulnerability_type"],
            "idx": idx,
            "source": "simple-generated",
            "original_vulnerable_code": example["vulnerable"],
            "original_secure_code": example["secure"],
            "typechecks": True
        }
        fim_examples.append(fim_example)
    
    # Save to file
    output_path = "simple_security_examples_fim.json"
    with open(output_path, 'w') as f:
        json.dump(fim_examples, f, indent=2)
    
    print(f"Created {len(fim_examples)} simple security examples in {output_path}")

if __name__ == "__main__":
    create_simple_examples() 