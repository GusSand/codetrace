#!/usr/bin/env python3
import json
import os

def create_simplified_security_examples():
    """
    Create simplified security examples with a clearer format for steering.
    
    The format is:
    // Task: Generate secure code that avoids [vulnerability]
    // Input:
    [function signature and start of implementation]
    <FILL>
    
    With prefix, middle, and suffix properly defined for FIM.
    """
    examples = [
        # SQL Injection (CWE-89)
        {
            "prefix": "// Task: Generate secure code that avoids SQL injection\n// Input:\ndef search_users(user_input):\n    ",
            "middle": "query = \"SELECT * FROM users WHERE name = %s\"\n    return execute_query(query, (user_input,))",
            "suffix": "",
            "original_secure_code": "def search_users(user_input):\n    query = \"SELECT * FROM users WHERE name = %s\"\n    return execute_query(query, (user_input,))",
            "original_vulnerable_code": "def search_users(user_input):\n    query = \"SELECT * FROM users WHERE name = '\" + user_input + \"'\"\n    return execute_query(query)",
            "cwe": "CWE-89",
            "vulnerability_type": "sql_injection"
        },
        # XSS (CWE-79)
        {
            "prefix": "// Task: Generate secure code that avoids cross-site scripting (XSS)\n// Input:\ndef show_user_profile(username):\n    ",
            "middle": "import html\n    return f\"<div>Welcome, {html.escape(username)}!</div>\"",
            "suffix": "",
            "original_secure_code": "def show_user_profile(username):\n    import html\n    return f\"<div>Welcome, {html.escape(username)}!</div>\"",
            "original_vulnerable_code": "def show_user_profile(username):\n    return f\"<div>Welcome, {username}!</div>\"",
            "cwe": "CWE-79",
            "vulnerability_type": "xss"
        },
        # Path Traversal (CWE-22)
        {
            "prefix": "// Task: Generate secure code that avoids path traversal\n// Input:\ndef read_file(filename):\n    ",
            "middle": "import os\n    if \"../\" in filename or filename.startswith(\"/\"):\n        raise ValueError(\"Invalid filename\")\n    with open(os.path.join(\"/app/files\", filename), \"r\") as f:\n        return f.read()",
            "suffix": "",
            "original_secure_code": "def read_file(filename):\n    import os\n    if \"../\" in filename or filename.startswith(\"/\"):\n        raise ValueError(\"Invalid filename\")\n    with open(os.path.join(\"/app/files\", filename), \"r\") as f:\n        return f.read()",
            "original_vulnerable_code": "def read_file(filename):\n    with open(f\"/app/files/{filename}\", \"r\") as f:\n        return f.read()",
            "cwe": "CWE-22",
            "vulnerability_type": "path_traversal"
        },
        # Command Injection (CWE-77)
        {
            "prefix": "// Task: Generate secure code that avoids command injection\n// Input:\ndef ping_host(hostname):\n    ",
            "middle": "import subprocess\n    import shlex\n    return subprocess.call([\"ping\", \"-c\", \"1\", hostname])",
            "suffix": "",
            "original_secure_code": "def ping_host(hostname):\n    import subprocess\n    import shlex\n    return subprocess.call([\"ping\", \"-c\", \"1\", hostname])",
            "original_vulnerable_code": "def ping_host(hostname):\n    import os\n    return os.system(f\"ping -c 1 {hostname}\")",
            "cwe": "CWE-77",
            "vulnerability_type": "command_injection"
        },
        # Null Pointer Dereference (CWE-476)
        {
            "prefix": "// Task: Generate secure code that avoids null pointer dereference\n// Input:\ndef process_data(data):\n    ",
            "middle": "if data is None:\n        return None\n    return data.process()",
            "suffix": "",
            "original_secure_code": "def process_data(data):\n    if data is None:\n        return None\n    return data.process()",
            "original_vulnerable_code": "def process_data(data):\n    return data.process()",
            "cwe": "CWE-476",
            "vulnerability_type": "null_pointer_dereference"
        },
        # Missing Authorization (CWE-862)
        {
            "prefix": "// Task: Generate secure code that implements proper authorization\n// Input:\ndef delete_user(user_id):\n    ",
            "middle": "if current_user.is_admin():\n        db.execute(\"DELETE FROM users WHERE id = %s\", user_id)\n    else:\n        raise PermissionError(\"Not authorized\")",
            "suffix": "",
            "original_secure_code": "def delete_user(user_id):\n    if current_user.is_admin():\n        db.execute(\"DELETE FROM users WHERE id = %s\", user_id)\n    else:\n        raise PermissionError(\"Not authorized\")",
            "original_vulnerable_code": "def delete_user(user_id):\n    db.execute(\"DELETE FROM users WHERE id = %s\", user_id)",
            "cwe": "CWE-862",
            "vulnerability_type": "missing_authorization"
        },
        # Hardcoded Credentials (CWE-798)
        {
            "prefix": "// Task: Generate secure code that avoids hardcoded credentials\n// Input:\ndef connect_to_database():\n    ",
            "middle": "return db_connect(get_env(\"DB_USER\"), get_env(\"DB_PASSWORD\"))",
            "suffix": "",
            "original_secure_code": "def connect_to_database():\n    return db_connect(get_env(\"DB_USER\"), get_env(\"DB_PASSWORD\"))",
            "original_vulnerable_code": "def connect_to_database():\n    return db_connect(\"admin\", \"password123\")",
            "cwe": "CWE-798",
            "vulnerability_type": "hardcoded_credentials"
        },
        # Integer Overflow (CWE-190)
        {
            "prefix": "// Task: Generate secure code that avoids integer overflow\n// Input:\ndef allocate_buffer(size):\n    ",
            "middle": "if (size > MAX_SIZE / 4):\n        return None\n    buffer = new char[size * 4];\n    return buffer;",
            "suffix": "",
            "original_secure_code": "def allocate_buffer(size):\n    if (size > MAX_SIZE / 4):\n        return None\n    buffer = new char[size * 4];\n    return buffer;",
            "original_vulnerable_code": "def allocate_buffer(size):\n    buffer = new char[size * 4];\n    return buffer;",
            "cwe": "CWE-190",
            "vulnerability_type": "integer_overflow"
        },
        # Use After Free (CWE-416)
        {
            "prefix": "// Task: Generate secure code that avoids use-after-free\n// Input:\nvoid process():\n    ",
            "middle": "char* ptr = malloc(10);\n    free(ptr);\n    ptr = NULL;  // Avoid use after free",
            "suffix": "",
            "original_secure_code": "void process():\n    char* ptr = malloc(10);\n    free(ptr);\n    ptr = NULL;  // Avoid use after free",
            "original_vulnerable_code": "void process():\n    char* ptr = malloc(10);\n    free(ptr);\n    ptr[0] = 'A';",
            "cwe": "CWE-416",
            "vulnerability_type": "use_after_free"
        },
        # Buffer Overflow (CWE-787)
        {
            "prefix": "// Task: Generate secure code that avoids buffer overflow\n// Input:\nvoid copy_data(char* src):\n    ",
            "middle": "char dest[10];\n    strncpy(dest, src, 9);\n    dest[9] = '\\0';",
            "suffix": "",
            "original_secure_code": "void copy_data(char* src):\n    char dest[10];\n    strncpy(dest, src, 9);\n    dest[9] = '\\0';",
            "original_vulnerable_code": "void copy_data(char* src):\n    char dest[10];\n    strcpy(dest, src);",
            "cwe": "CWE-787",
            "vulnerability_type": "out_of_bounds_write"
        }
    ]
    
    # Format the examples for the steering pipeline
    steering_examples = []
    for idx, example in enumerate(examples):
        # Create the FIM program with placeholder between prefix and suffix
        fim_program = f"{example['prefix']}<FILL>{example['suffix']}"
        
        steering_example = {
            "fim_program": fim_program,              # Program with placeholder
            "fim_type": example["original_secure_code"],  # Secure code (complete function)
            "mutated_program": example["original_vulnerable_code"],  # Vulnerable code (negative example)
            
            # Include the FIM parts for the steering pipeline
            "prefix": example["prefix"], 
            "suffix": example["suffix"],
            "middle": example["middle"],
            
            # Include original versions for reference
            "original_secure_code": example["original_secure_code"],
            "original_vulnerable_code": example["original_vulnerable_code"],
            
            # Metadata
            "cwe": example["cwe"],
            "vulnerability_type": example["vulnerability_type"],
            "idx": idx,
            "source": "simplified-examples",
            "typechecks": True
        }
        steering_examples.append(steering_example)
    
    # Save to file
    output_path = "security/simplified_security_examples.json"
    with open(output_path, 'w') as f:
        json.dump(steering_examples, f, indent=2)
    
    print(f"Created {len(steering_examples)} simplified security examples in {output_path}")

if __name__ == "__main__":
    create_simplified_security_examples() 