#!/usr/bin/env python3
"""
Example webhook server for Claude Code approvals
Can be deployed on any server/cloud platform
"""

from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import uuid
import os

app = Flask(__name__)

# In-memory storage (use Redis/DB in production)
pending_approvals = {}
approval_history = []

# Configuration
API_KEY = os.environ.get('WEBHOOK_API_KEY', 'your-secret-key')
AUTO_APPROVE_PATTERNS = [
    {'tool': 'Read', 'auto': True},
    {'tool': 'LS', 'auto': True},
    {'tool': 'Grep', 'auto': True},
]

@app.route('/claude/approve', methods=['POST'])
def create_approval_request():
    """Receive approval request from Claude Code"""
    
    # Verify API key
    if request.headers.get('X-API-Key') != API_KEY:
        return jsonify({'error': 'Invalid API key'}), 401
    
    data = request.json
    request_id = data['id']
    tool_info = data['tool_info']
    
    # Check auto-approval rules
    for pattern in AUTO_APPROVE_PATTERNS:
        if tool_info['tool_name'] == pattern['tool'] and pattern['auto']:
            approval_history.append({
                'id': request_id,
                'tool_info': tool_info,
                'status': 'auto-approved',
                'timestamp': datetime.now().isoformat()
            })
            return jsonify({
                'status': 'approved',
                'auto': True,
                'reason': 'Matched auto-approval pattern'
            })
    
    # Store pending approval
    pending_approvals[request_id] = {
        'id': request_id,
        'tool_info': tool_info,
        'status': 'pending',
        'created_at': datetime.now(),
        'expires_at': datetime.now() + timedelta(minutes=5)
    }
    
    # Send notification (implement your preferred method)
    send_notification(request_id, tool_info)
    
    return jsonify({
        'status': 'pending',
        'id': request_id,
        'approve_url': f"/approve/{request_id}",
        'deny_url': f"/deny/{request_id}"
    })

@app.route('/claude/approve/<request_id>', methods=['GET'])
def check_approval_status(request_id):
    """Check status of approval request"""
    
    if request.headers.get('X-API-Key') != API_KEY:
        return jsonify({'error': 'Invalid API key'}), 401
    
    if request_id in pending_approvals:
        approval = pending_approvals[request_id]
        
        # Check if expired
        if datetime.now() > approval['expires_at']:
            approval['status'] = 'timeout'
            del pending_approvals[request_id]
        
        return jsonify({
            'status': approval['status'],
            'tool_info': approval['tool_info']
        })
    
    # Check history
    for item in approval_history:
        if item['id'] == request_id:
            return jsonify({
                'status': item['status'],
                'reason': item.get('reason', '')
            })
    
    return jsonify({'status': 'not_found'}), 404

@app.route('/approve/<request_id>', methods=['GET', 'POST'])
def approve_request(request_id):
    """Approve a pending request (via web interface or API)"""
    
    if request_id not in pending_approvals:
        return "Request not found or already processed", 404
    
    approval = pending_approvals[request_id]
    approval['status'] = 'approved'
    approval['approved_at'] = datetime.now().isoformat()
    
    # Move to history
    approval_history.append(approval)
    del pending_approvals[request_id]
    
    if request.method == 'GET':
        # Web interface
        return f"""
        <html>
        <body style="font-family: Arial; padding: 20px;">
            <h2>✅ Approved!</h2>
            <p>Tool: {approval['tool_info']['tool_name']}</p>
            <p>Time: {approval['approved_at']}</p>
            <script>setTimeout(() => window.close(), 3000);</script>
        </body>
        </html>
        """
    else:
        return jsonify({'status': 'approved'})

@app.route('/deny/<request_id>', methods=['GET', 'POST'])
def deny_request(request_id):
    """Deny a pending request"""
    
    if request_id not in pending_approvals:
        return "Request not found or already processed", 404
    
    approval = pending_approvals[request_id]
    approval['status'] = 'denied'
    approval['reason'] = request.args.get('reason', 'User denied')
    
    # Move to history
    approval_history.append(approval)
    del pending_approvals[request_id]
    
    if request.method == 'GET':
        return f"""
        <html>
        <body style="font-family: Arial; padding: 20px;">
            <h2>❌ Denied</h2>
            <p>Tool: {approval['tool_info']['tool_name']}</p>
            <script>setTimeout(() => window.close(), 3000);</script>
        </body>
        </html>
        """
    else:
        return jsonify({'status': 'denied', 'reason': approval['reason']})

@app.route('/dashboard')
def dashboard():
    """Simple web dashboard to view and manage approvals"""
    
    pending_html = ""
    for req_id, approval in pending_approvals.items():
        tool_info = approval['tool_info']
        pending_html += f"""
        <div style="border: 1px solid #ccc; padding: 10px; margin: 10px;">
            <h3>{tool_info['tool_name']}</h3>
            <pre>{tool_info.get('tool_input', '')[:200]}...</pre>
            <p>From: {tool_info['hostname']} | User: {tool_info['user']}</p>
            <a href="/approve/{req_id}" target="_blank" style="background: green; color: white; padding: 5px 10px; text-decoration: none;">Approve</a>
            <a href="/deny/{req_id}" target="_blank" style="background: red; color: white; padding: 5px 10px; text-decoration: none;">Deny</a>
        </div>
        """
    
    return f"""
    <html>
    <head>
        <title>Claude Approvals</title>
        <meta http-equiv="refresh" content="5">
    </head>
    <body style="font-family: Arial; padding: 20px;">
        <h1>Claude Code Approval Dashboard</h1>
        <h2>Pending Approvals ({len(pending_approvals)})</h2>
        {pending_html or '<p>No pending approvals</p>'}
        <h2>Recent History</h2>
        <pre>{str(approval_history[-10:])}</pre>
    </body>
    </html>
    """

def send_notification(request_id, tool_info):
    """Send notification about pending approval"""
    # Implement your preferred notification method:
    # - Slack webhook
    # - Email
    # - SMS (Twilio)
    # - Push notification
    # - macOS notification
    
    print(f"🔔 New approval request: {tool_info['tool_name']} (ID: {request_id})")
    
    # Example: Send to Slack
    # slack_webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
    # if slack_webhook_url:
    #     requests.post(slack_webhook_url, json={
    #         'text': f"Claude needs approval for: {tool_info['tool_name']}",
    #         'attachments': [{
    #             'fallback': 'Approve or Deny',
    #             'actions': [
    #                 {'type': 'button', 'text': 'Approve', 'url': f"{BASE_URL}/approve/{request_id}"},
    #                 {'type': 'button', 'text': 'Deny', 'url': f"{BASE_URL}/deny/{request_id}"}
    #             ]
    #         }]
    #     })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)