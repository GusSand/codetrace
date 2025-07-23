# Chat Conversations

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
