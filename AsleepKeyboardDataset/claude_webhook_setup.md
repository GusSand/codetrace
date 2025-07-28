# Claude Code Webhook Approval System

## Overview

This system allows you to approve Claude Code operations remotely via:
- Web browser on any device
- Mobile notifications (Slack, SMS, email)
- API calls from custom apps
- Auto-approval rules for safe operations

## Setup Instructions

### 1. Deploy the Webhook Server

Deploy `webhook_server_example.py` to any platform:

**Option A: Local testing**
```bash
pip install flask
export WEBHOOK_API_KEY="your-secret-key"
python webhook_server_example.py
```

**Option B: Deploy to cloud (Heroku example)**
```bash
# Create requirements.txt
echo "flask" > requirements.txt

# Create Procfile
echo "web: python webhook_server_example.py" > Procfile

# Deploy
heroku create claude-approvals
heroku config:set WEBHOOK_API_KEY="your-secret-key"
git push heroku main
```

**Option C: Serverless (Vercel/Netlify Functions)**
- Convert Flask routes to serverless functions
- Use managed database for persistence

### 2. Configure Claude Code

Add to `~/.claude/settings.json`:
```json
{
  "hooks": {
    "PreToolUse": {
      "*": "python3 /path/to/claude_webhook_approval.py"
    }
  }
}
```

### 3. Set Environment Variables

Add to your shell profile (`~/.zshrc` or `~/.bashrc`):
```bash
export CLAUDE_WEBHOOK_URL="https://your-server.com/claude/approve"
export CLAUDE_WEBHOOK_KEY="your-secret-key"
export CLAUDE_APPROVAL_TIMEOUT="300"  # 5 minutes
```

## How It Works

1. **Claude tries to use a tool** → Hook script runs
2. **Hook sends request to webhook** → Server stores pending approval
3. **You get notification** → Slack/SMS/Email with approve/deny links
4. **You click approve** → Server updates status
5. **Hook polls for result** → Gets approval and continues

## Features

### Auto-Approval Rules
- Read-only operations auto-approved by default
- Configure patterns in the server
- Time-based rules (business hours)
- User/project specific rules

### Notification Methods

**Slack Integration**
```python
def send_slack_notification(request_id, tool_info):
    slack_webhook = os.environ.get('SLACK_WEBHOOK_URL')
    requests.post(slack_webhook, json={
        'text': f'Claude needs approval: {tool_info["tool_name"]}',
        'attachments': [{
            'fallback': 'Approval needed',
            'actions': [
                {
                    'type': 'button',
                    'text': 'Approve ✅',
                    'url': f'{BASE_URL}/approve/{request_id}',
                    'style': 'primary'
                },
                {
                    'type': 'button', 
                    'text': 'Deny ❌',
                    'url': f'{BASE_URL}/deny/{request_id}',
                    'style': 'danger'
                }
            ]
        }]
    })
```

**SMS via Twilio**
```python
from twilio.rest import Client

def send_sms_notification(request_id, tool_info):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to="+1234567890",
        from_="+0987654321",
        body=f"Claude approval needed: {tool_info['tool_name']}\n"
             f"Approve: {BASE_URL}/approve/{request_id}"
    )
```

**Email**
```python
import smtplib
from email.mime.text import MIMEText

def send_email_notification(request_id, tool_info):
    msg = MIMEText(f"""
    Claude needs approval for: {tool_info['tool_name']}
    
    Approve: {BASE_URL}/approve/{request_id}
    Deny: {BASE_URL}/deny/{request_id}
    
    Details: {json.dumps(tool_info, indent=2)}
    """)
    msg['Subject'] = f'Claude Approval: {tool_info["tool_name"]}'
    msg['From'] = 'claude@your-domain.com'
    msg['To'] = 'you@email.com'
    
    # Send via SMTP
```

### Mobile App Integration

Create a simple mobile web app or native app that:
1. Receives push notifications
2. Shows pending approvals
3. Allows quick approve/deny actions

### Security Features

1. **API Key validation** - All requests verified
2. **Request expiration** - Auto-deny after timeout
3. **Audit trail** - All approvals logged
4. **IP filtering** - Restrict access by IP
5. **2FA option** - Additional security for sensitive operations

## Advanced Configuration

### Conditional Auto-Approval
```python
def should_auto_approve(tool_info):
    # Auto-approve reads during business hours
    if tool_info['tool_name'] in ['Read', 'LS']:
        hour = datetime.now().hour
        if 9 <= hour <= 17:  # 9 AM - 5 PM
            return True
    
    # Auto-approve specific paths
    if tool_info['tool_name'] == 'Write':
        path = json.loads(tool_info['tool_input']).get('file_path', '')
        if path.startswith('/tmp/'):
            return True
    
    return False
```

### Batch Approvals
Add endpoint to approve multiple pending requests at once:
```python
@app.route('/approve-all', methods=['POST'])
def approve_all():
    approved = []
    for req_id in list(pending_approvals.keys()):
        approval = pending_approvals[req_id]
        if should_batch_approve(approval):
            approve_request(req_id)
            approved.append(req_id)
    return jsonify({'approved': approved})
```

### Integration with Corporate Systems
- Connect to corporate SSO for authentication
- Log to SIEM systems
- Integrate with existing approval workflows
- Compliance reporting

## Troubleshooting

**Webhook not receiving requests**
- Check firewall/network settings
- Verify API key matches
- Test with curl: `curl -X POST https://your-server.com/claude/approve -H "X-API-Key: your-key"`

**Approvals timing out**
- Increase `CLAUDE_APPROVAL_TIMEOUT`
- Check notification delivery
- Verify server is reachable

**Auto-approval not working**
- Check patterns match exactly
- Verify environment variables set
- Check server logs

This webhook system provides flexible, secure remote approval for Claude Code operations while maintaining productivity through smart auto-approval rules.