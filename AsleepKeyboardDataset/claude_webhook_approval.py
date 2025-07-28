#!/usr/bin/env python3
"""
Webhook-based approval system for Claude Code
Sends tool requests to a remote server for approval
"""

import os
import sys
import json
import time
import requests
import hashlib
from datetime import datetime

# Configuration
WEBHOOK_URL = os.environ.get('CLAUDE_WEBHOOK_URL', 'https://your-server.com/claude/approve')
API_KEY = os.environ.get('CLAUDE_WEBHOOK_KEY', 'your-secret-key')
TIMEOUT = int(os.environ.get('CLAUDE_APPROVAL_TIMEOUT', '300'))  # 5 minutes default
AUTO_APPROVE_READONLY = True

def get_tool_info():
    """Extract tool information from environment"""
    return {
        'tool_name': os.environ.get('TOOL_NAME', 'unknown'),
        'tool_input': os.environ.get('TOOL_INPUT', '{}'),
        'timestamp': datetime.now().isoformat(),
        'hostname': os.uname().nodename,
        'user': os.environ.get('USER', 'unknown'),
        'cwd': os.getcwd()
    }

def is_safe_readonly(tool_info):
    """Check if this is a safe read-only operation"""
    safe_tools = ['Read', 'LS', 'Grep', 'Glob']
    return tool_info['tool_name'] in safe_tools

def create_approval_request(tool_info):
    """Create approval request with security token"""
    request_id = hashlib.sha256(
        f"{tool_info['timestamp']}{tool_info['tool_name']}{API_KEY}".encode()
    ).hexdigest()[:16]
    
    return {
        'id': request_id,
        'tool_info': tool_info,
        'auto_approve_hint': is_safe_readonly(tool_info),
        'api_key_hash': hashlib.sha256(API_KEY.encode()).hexdigest()[:8]
    }

def send_webhook_request(approval_request):
    """Send approval request to webhook and wait for response"""
    try:
        # Send the request
        response = requests.post(
            WEBHOOK_URL,
            json=approval_request,
            headers={'X-API-Key': API_KEY},
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Webhook error: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None

def poll_for_approval(request_id):
    """Poll the webhook for approval status"""
    start_time = time.time()
    poll_url = f"{WEBHOOK_URL}/{request_id}"
    
    while time.time() - start_time < TIMEOUT:
        try:
            response = requests.get(
                poll_url,
                headers={'X-API-Key': API_KEY},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') in ['approved', 'denied']:
                    return data
                    
        except:
            pass
        
        time.sleep(2)  # Poll every 2 seconds
    
    return {'status': 'timeout'}

def main():
    """Main approval flow"""
    tool_info = get_tool_info()
    
    # Auto-approve safe operations if configured
    if AUTO_APPROVE_READONLY and is_safe_readonly(tool_info):
        print(f"Auto-approved read-only operation: {tool_info['tool_name']}")
        sys.exit(0)
    
    # Create and send approval request
    approval_request = create_approval_request(tool_info)
    
    print(f"🔔 Sending approval request for: {tool_info['tool_name']}")
    print(f"   Request ID: {approval_request['id']}")
    
    # Send initial request
    initial_response = send_webhook_request(approval_request)
    
    if initial_response and initial_response.get('status') == 'pending':
        print(f"⏳ Waiting for approval (timeout: {TIMEOUT}s)...")
        print(f"   Approve at: {WEBHOOK_URL}/approve/{approval_request['id']}")
        
        # Poll for result
        result = poll_for_approval(approval_request['id'])
        
        if result['status'] == 'approved':
            print("✅ Approved!")
            sys.exit(0)
        elif result['status'] == 'denied':
            print(f"❌ Denied: {result.get('reason', 'No reason provided')}")
            sys.exit(2)
        else:
            print("⏱️  Timeout - auto-denying")
            sys.exit(2)
    else:
        # Fallback to local approval
        print("⚠️  Webhook unavailable, falling back to local approval")
        response = input(f"Approve {tool_info['tool_name']}? (y/n): ")
        sys.exit(0 if response.lower() == 'y' else 2)

if __name__ == '__main__':
    main()