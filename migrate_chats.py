#!/usr/bin/env python3
"""
Migration script to move existing chat conversations to the new chats directory.
"""

import os
import shutil
from pathlib import Path
from chats.chat_manager import ChatManager

def migrate_existing_chats():
    """Migrate existing chat conversations to the new chats directory."""
    
    print("🔄 Migrating existing chat conversations...")
    
    # Initialize chat manager
    manager = ChatManager()
    
    # Check for existing conversations in security/conversations
    old_conversations_dir = Path("security/conversations")
    if old_conversations_dir.exists():
        md_files = list(old_conversations_dir.glob("*.md"))
        
        for md_file in md_files:
            if md_file.name == "conversations_index.md":
                continue  # Skip the old index file
                
            print(f"📄 Processing: {md_file.name}")
            
            # Read the content
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract title from filename
            title = md_file.stem.replace('_', ' ').title()
            
            # Determine category and tags based on content
            category = "research"
            tags = ["neural-steering", "nnsight", "security"]
            
            if "neural" in title.lower() or "steering" in title.lower():
                tags.extend(["code-generation", "experiments"])
            
            # Save with new system
            manager.save_chat(title, content, tags, category)
            
            print(f"✅ Migrated: {md_file.name}")
    
    # Create the new index
    manager.create_index()
    
    print("\n✅ Migration completed!")
    print(f"📁 New chats directory: {manager.chats_dir}")
    print(f"📋 Index file: {manager.index_file}")
    print(f"📊 Metadata file: {manager.metadata_file}")

def create_readme():
    """Create a README file for the chats directory."""
    
    readme_content = """# Chat Conversations

This directory contains organized chat conversations related to the project.

## Structure

- `index.md` - Main index of all conversations
- `metadata.json` - Metadata for all conversations
- `chat_manager.py` - Management system for organizing chats
- Individual `.md` files - Each conversation

## Usage

### Using the Chat Manager

```bash
# Save a new chat
python chats/chat_manager.py --action save --title "My Chat" --content "Chat content..." --category research --tags "tag1,tag2"

# Create/update index
python chats/chat_manager.py --action index

# List all chats
python chats/chat_manager.py --action list

# List chats by category
python chats/chat_manager.py --action list --filter-category research

# List chats by tag
python chats/chat_manager.py --action list --filter-tag neural-steering
```

### Using the Python API

```python
from chats.chat_manager import ChatManager

manager = ChatManager()

# Save a chat
manager.save_chat(
    title="My Chat",
    content="Chat content...",
    tags=["tag1", "tag2"],
    category="research"
)

# Create index
manager.create_index()

# List chats
manager.list_chats(category="research")
```

## Categories

- **research** - Research-related conversations
- **development** - Development and coding discussions
- **experiments** - Experimental results and analysis
- **general** - General discussions

## Tags

Common tags used:
- `neural-steering` - Neural steering experiments
- `nnsight` - NNSight-related discussions
- `security` - Security-focused conversations
- `code-generation` - Code generation topics
- `experiments` - Experimental work

## File Naming

Files are automatically named using the pattern:
`{safe-title}_{timestamp}.md`

Where:
- `safe-title` is the title with special characters removed
- `timestamp` is the creation timestamp (YYYYMMDD_HHMMSS)

## Index Features

The index includes:
- Quick statistics
- Categorized conversations
- Tag index
- Recent conversations list
- File metadata (size, creation date, etc.)
"""
    
    readme_file = Path("chats/README.md")
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✅ Created README: {readme_file}")

if __name__ == "__main__":
    migrate_existing_chats()
    create_readme()
    
    print("\n🎉 Chat migration and setup completed!")
    print("\n📖 Next steps:")
    print("1. Review the new index: cat chats/index.md")
    print("2. Check the README: cat chats/README.md")
    print("3. Use the chat manager for future conversations") 