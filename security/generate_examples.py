import json
import os

# Define vulnerability types
VULNERABILITY_TYPES = [
    'sql_injection',
    'xss',
    'path_traversal',
    'command_injection',
    'buffer_overflow',
    'use_after_free',
    'integer_overflow',
    'hardcoded_credentials'
]

# Example pairs of secure and vulnerable code
EXAMPLES = {
    'sql_injection': {
        'secure': [
            """def get_user(username):
    import sqlite3
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    return cursor.fetchone()""",
            """def query_user(user_id):
    import psycopg2
    conn = psycopg2.connect(database='mydb')
    cur = conn.cursor()
    cur.execute('SELECT name FROM users WHERE id = %s', (user_id,))
    return cur.fetchone()"""
        ],
        'vulnerable': [
            """def get_user(username):
    import sqlite3
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM users WHERE username = "{username}"')
    return cursor.fetchone()""",
            """def query_user(user_id):
    import psycopg2
    conn = psycopg2.connect(database='mydb')
    cur = conn.cursor()
    cur.execute('SELECT name FROM users WHERE id = ' + user_id)
    return cur.fetchone()"""
        ]
    },
    'xss': {
        'secure': [
            """def display_comment(comment):
    from html import escape
    return f'<p>{escape(comment)}</p>'""",
            """def show_username(username):
    import bleach
    return f'<div>Welcome, {bleach.clean(username)}</div>'"""
        ],
        'vulnerable': [
            """def display_comment(comment):
    return f'<p>{comment}</p>'""",
            """def show_username(username):
    return f'<div>Welcome, {username}</div>'"""
        ]
    },
    'path_traversal': {
        'secure': [
            """def read_file(filename):
    import os
    base_dir = '/app/files'
    filepath = os.path.normpath(os.path.join(base_dir, filename))
    if not filepath.startswith(base_dir):
        raise ValueError('Invalid path')
    with open(filepath) as f:
        return f.read()""",
            """def get_user_file(username, filename):
    import os
    user_dir = f'/home/users/{username}'
    safe_path = os.path.abspath(os.path.join(user_dir, filename))
    if not safe_path.startswith(user_dir):
        raise ValueError('Access denied')
    return open(safe_path).read()"""
        ],
        'vulnerable': [
            """def read_file(filename):
    with open(filename) as f:
        return f.read()""",
            """def get_user_file(username, filename):
    return open(f'/home/users/{username}/{filename}').read()"""
        ]
    },
    'command_injection': {
        'secure': [
            """def ping_host(hostname):
    import subprocess
    result = subprocess.run(['ping', '-c', '1', hostname],
                          capture_output=True,
                          text=True,
                          shell=False)
    return result.stdout""",
            """def execute_git_command(repo_name):
    import subprocess
    cmd = ['git', 'clone', f'https://github.com/{repo_name}']
    subprocess.run(cmd, check=True, shell=False)"""
        ],
        'vulnerable': [
            """def ping_host(hostname):
    import os
    return os.system(f'ping -c 1 {hostname}')""",
            """def execute_git_command(repo_name):
    import os
    os.system(f'git clone {repo_name}')"""
        ]
    },
    'buffer_overflow': {
        'secure': [
            """def copy_data(source, dest, size):
    if len(source) >= size:
        raise ValueError('Source too large')
    dest[:len(source)] = source""",
            """def write_string(buffer, text, max_size):
    if len(text) >= max_size:
        text = text[:max_size-1]
    buffer.write(text + '\\0')"""
        ],
        'vulnerable': [
            """def copy_data(source, dest, size):
    for i in range(len(source)):
        dest[i] = source[i]""",
            """def write_string(buffer, text, max_size):
    buffer.write(text)"""
        ]
    },
    'use_after_free': {
        'secure': [
            """class SafeResource:
    def __init__(self):
        self.data = None
        self.is_freed = False
    
    def free(self):
        self.data = None
        self.is_freed = True
    
    def use(self):
        if self.is_freed:
            raise ValueError('Resource already freed')
        return self.data""",
            """def process_data(data):
    resource = allocate_resource()
    try:
        return process(resource, data)
    finally:
        free_resource(resource)
        resource = None"""
        ],
        'vulnerable': [
            """class Resource:
    def __init__(self):
        self.data = None
    
    def free(self):
        self.data = None
    
    def use(self):
        return self.data""",
            """def process_data(data):
    resource = allocate_resource()
    result = process(resource, data)
    free_resource(resource)
    return resource.data"""
        ]
    },
    'integer_overflow': {
        'secure': [
            """def multiply(a: int, b: int) -> int:
    import sys
    if a > 0 and b > sys.maxsize // a:
        raise ValueError('Integer overflow')
    if a < 0 and b < sys.maxsize // a:
        raise ValueError('Integer overflow')
    return a * b""",
            """def add_positive(a: int, b: int) -> int:
    import sys
    if a > sys.maxsize - b:
        raise ValueError('Integer overflow')
    return a + b"""
        ],
        'vulnerable': [
            """def multiply(a: int, b: int) -> int:
    return a * b""",
            """def add_positive(a: int, b: int) -> int:
    return a + b"""
        ]
    },
    'hardcoded_credentials': {
        'secure': [
            """def connect_db():
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    username = os.getenv('DB_USER')
    password = os.getenv('DB_PASS')
    return create_connection(username, password)""",
            """def authenticate():
    import configparser
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    api_key = config['auth']['api_key']
    return make_api_call(api_key)"""
        ],
        'vulnerable': [
            """def connect_db():
    username = 'admin'
    password = 'secretpass123'
    return create_connection(username, password)""",
            """def authenticate():
    api_key = 'sk_live_123456789abcdef'
    return make_api_call(api_key)"""
        ]
    }
}

def main():
    # Create examples directory if it doesn't exist
    os.makedirs('security/examples', exist_ok=True)
    
    # Generate files for each vulnerability type
    for vuln_type in VULNERABILITY_TYPES:
        # Save secure examples
        secure_file = f'security/examples/{vuln_type}_secure.json'
        with open(secure_file, 'w') as f:
            json.dump(EXAMPLES[vuln_type]['secure'], f, indent=2)
        
        # Save vulnerable examples
        vulnerable_file = f'security/examples/{vuln_type}_vulnerable.json'
        with open(vulnerable_file, 'w') as f:
            json.dump(EXAMPLES[vuln_type]['vulnerable'], f, indent=2)
        
        print(f'Generated examples for {vuln_type}')

if __name__ == '__main__':
    main() 