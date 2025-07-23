#!/usr/bin/env python3
"""
Template script for saving chat conversations to text files.
You can customize the conversation content by editing the conversation variable.
"""

import os
import json
from datetime import datetime
from pathlib import Path

def save_chat_conversation(conversation_title="Chat Conversation", conversation_content=""):
    """
    Save a chat conversation to a text file.
    
    Args:
        conversation_title (str): Title for the conversation
        conversation_content (str): The actual conversation content
    """
    
    # Create the conversation header
    header = f"""# {conversation_title}

**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Topic:** {conversation_title}

---

"""
    
    # Combine header and content
    full_conversation = header + conversation_content
    
    # Create output directory
    output_dir = Path("security/conversations")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    # Create a safe filename from the title
    safe_title = "".join(c for c in conversation_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_title = safe_title.replace(' ', '_').lower()
    filename = output_dir / f"{safe_title}_{timestamp}.md"
    
    # Save the conversation
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(full_conversation)
    
    print(f"✅ Chat conversation saved to: {filename}")
    print(f"📄 File size: {os.path.getsize(filename)} bytes")
    
    return str(filename)

def save_custom_conversation():
    """
    Example function showing how to save a custom conversation.
    Edit this function to save your specific conversation content.
    """
    
    # CUSTOMIZE THIS SECTION WITH YOUR CONVERSATION CONTENT
    conversation_content = """
## Conversation Content

Replace this section with your actual conversation content.

### Example Structure:
- **User Question**: What was asked
- **Assistant Response**: What was answered
- **Key Points**: Important takeaways
- **Code Created**: Any scripts or files generated
- **Results**: Any experimental results or findings

### Technical Details
- Models used
- Experiments run
- Results obtained
- Files created

### Next Steps
- What to do next
- Future experiments
- Paper writing tasks

---
*This conversation was saved on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    # Save with custom title
    return save_chat_conversation(
        conversation_title="Custom Chat Conversation",
        conversation_content=conversation_content
    )

def create_conversation_index():
    """Create an index of all saved conversations."""
    
    conversations_dir = Path("security/conversations")
    if not conversations_dir.exists():
        print("❌ No conversations directory found")
        return
    
    # Find all markdown files
    md_files = list(conversations_dir.glob("*.md"))
    
    if not md_files:
        print("❌ No conversation files found")
        return
    
    # Create index content
    index_content = f"""# Chat Conversations Index

**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total Conversations:** {len(md_files)}

## Conversations List

"""
    
    # Sort files by modification time (newest first)
    md_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    for i, file_path in enumerate(md_files, 1):
        # Get file stats
        stat = file_path.stat()
        mod_time = datetime.fromtimestamp(stat.st_mtime)
        file_size = stat.st_size
        
        # Extract title from filename
        title = file_path.stem.replace('_', ' ').title()
        
        index_content += f"""### {i}. {title}
- **File:** `{file_path.name}`
- **Modified:** {mod_time.strftime('%Y-%m-%d %H:%M:%S')}
- **Size:** {file_size} bytes
- **Path:** `{file_path}`

"""
    
    # Save index
    index_file = conversations_dir / "conversations_index.md"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"✅ Conversations index created: {index_file}")
    print(f"📊 Found {len(md_files)} conversation files")

if __name__ == "__main__":
    print("🔄 Chat Conversation Saver")
    print("1. Save custom conversation")
    print("2. Create conversations index")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == "1":
        print("\n📝 To save a custom conversation:")
        print("1. Edit the save_custom_conversation() function")
        print("2. Replace the conversation_content with your actual conversation")
        print("3. Run this script again")
        
        # Uncomment the line below to actually save a custom conversation
        # save_custom_conversation()
        
    elif choice == "2":
        create_conversation_index()
    else:
        print("❌ Invalid choice") 