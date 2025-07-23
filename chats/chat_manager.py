#!/usr/bin/env python3
"""
Chat Management System for organizing and indexing chat conversations.
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

class ChatManager:
    """Manages chat conversations with indexing and organization."""
    
    def __init__(self, chats_dir: str = "chats"):
        self.chats_dir = Path(chats_dir)
        self.chats_dir.mkdir(exist_ok=True)
        self.index_file = self.chats_dir / "index.md"
        self.metadata_file = self.chats_dir / "metadata.json"
        
    def save_chat(self, title: str, content: str, tags: List[str] = None, 
                  category: str = "general") -> str:
        """
        Save a new chat conversation.
        
        Args:
            title: Title of the conversation
            content: The conversation content
            tags: List of tags for categorization
            category: Category of the conversation
            
        Returns:
            Path to the saved file
        """
        # Create safe filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_title = re.sub(r'[^\w\s-]', '', title).strip()
        safe_title = re.sub(r'[-\s]+', '-', safe_title).lower()
        
        filename = f"{safe_title}_{timestamp}.md"
        filepath = self.chats_dir / filename
        
        # Create metadata
        metadata = {
            "title": title,
            "filename": filename,
            "created": datetime.now().isoformat(),
            "category": category,
            "tags": tags or [],
            "size": len(content.encode('utf-8'))
        }
        
        # Save content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Update metadata
        self._update_metadata(filename, metadata)
        
        print(f"✅ Chat saved: {filepath}")
        return str(filepath)
    
    def _update_metadata(self, filename: str, metadata: Dict[str, Any]):
        """Update the metadata file with new chat information."""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                all_metadata = json.load(f)
        else:
            all_metadata = {}
        
        all_metadata[filename] = metadata
        
        with open(self.metadata_file, 'w') as f:
            json.dump(all_metadata, f, indent=2)
    
    def create_index(self) -> str:
        """Create a comprehensive index of all chat conversations."""
        
        if not self.metadata_file.exists():
            print("❌ No metadata found. No chats to index.")
            return ""
        
        with open(self.metadata_file, 'r') as f:
            metadata = json.load(f)
        
        # Group by category
        categories = {}
        for filename, meta in metadata.items():
            category = meta.get('category', 'general')
            if category not in categories:
                categories[category] = []
            categories[category].append((filename, meta))
        
        # Create index content
        index_content = f"""# Chat Conversations Index

**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total Conversations:** {len(metadata)}

## Quick Stats
- **Categories:** {len(categories)}
- **Total Size:** {sum(meta.get('size', 0) for meta in metadata.values())} bytes
- **Date Range:** {min(meta.get('created', '') for meta in metadata.values())[:10]} to {max(meta.get('created', '') for meta in metadata.values())[:10]}

## Categories

"""
        
        # Sort categories alphabetically
        for category in sorted(categories.keys()):
            chats = categories[category]
            # Sort chats by creation date (newest first)
            chats.sort(key=lambda x: x[1].get('created', ''), reverse=True)
            
            index_content += f"### {category.title()}\n\n"
            
            for i, (filename, meta) in enumerate(chats, 1):
                created_date = datetime.fromisoformat(meta.get('created', '')).strftime('%Y-%m-%d %H:%M')
                tags_str = ', '.join(meta.get('tags', [])) if meta.get('tags') else 'No tags'
                
                index_content += f"""#### {i}. {meta.get('title', 'Untitled')}
- **File:** `{filename}`
- **Created:** {created_date}
- **Size:** {meta.get('size', 0)} bytes
- **Tags:** {tags_str}
- **Path:** `{self.chats_dir}/{filename}`

"""
        
        # Add tag index
        all_tags = set()
        for meta in metadata.values():
            all_tags.update(meta.get('tags', []))
        
        if all_tags:
            index_content += "## Tag Index\n\n"
            for tag in sorted(all_tags):
                tagged_chats = [meta.get('title') for meta in metadata.values() 
                              if tag in meta.get('tags', [])]
                index_content += f"### {tag}\n"
                for title in tagged_chats:
                    index_content += f"- {title}\n"
                index_content += "\n"
        
        # Add recent conversations
        recent_chats = sorted(metadata.items(), 
                            key=lambda x: x[1].get('created', ''), 
                            reverse=True)[:5]
        
        index_content += "## Recent Conversations\n\n"
        for filename, meta in recent_chats:
            created_date = datetime.fromisoformat(meta.get('created', '')).strftime('%Y-%m-%d %H:%M')
            index_content += f"- **{meta.get('title', 'Untitled')}** ({created_date}) - `{filename}`\n"
        
        # Save index
        with open(self.index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        print(f"✅ Index created: {self.index_file}")
        return str(self.index_file)
    
    def list_chats(self, category: str = None, tag: str = None):
        """List all chats with optional filtering."""
        
        if not self.metadata_file.exists():
            print("❌ No metadata found.")
            return
        
        with open(self.metadata_file, 'r') as f:
            metadata = json.load(f)
        
        # Filter if needed
        if category:
            metadata = {k: v for k, v in metadata.items() 
                       if v.get('category') == category}
        
        if tag:
            metadata = {k: v for k, v in metadata.items() 
                       if tag in v.get('tags', [])}
        
        if not metadata:
            print("❌ No chats found matching criteria.")
            return
        
        print(f"📚 Found {len(metadata)} chat(s):\n")
        
        for filename, meta in sorted(metadata.items(), 
                                   key=lambda x: x[1].get('created', ''), 
                                   reverse=True):
            created_date = datetime.fromisoformat(meta.get('created', '')).strftime('%Y-%m-%d %H:%M')
            print(f"📄 {meta.get('title', 'Untitled')}")
            print(f"   📁 {filename}")
            print(f"   📅 {created_date}")
            print(f"   🏷️  {', '.join(meta.get('tags', []))}")
            print(f"   📊 {meta.get('size', 0)} bytes")
            print()

def main():
    """Main function for chat management."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Chat Management System')
    parser.add_argument('--action', choices=['save', 'index', 'list'], required=True,
                       help='Action to perform')
    parser.add_argument('--title', type=str, help='Chat title (for save action)')
    parser.add_argument('--content', type=str, help='Chat content (for save action)')
    parser.add_argument('--category', type=str, default='general', help='Chat category')
    parser.add_argument('--tags', type=str, help='Comma-separated tags')
    parser.add_argument('--filter-category', type=str, help='Filter by category (for list action)')
    parser.add_argument('--filter-tag', type=str, help='Filter by tag (for list action)')
    
    args = parser.parse_args()
    
    manager = ChatManager()
    
    if args.action == 'save':
        if not args.title or not args.content:
            print("❌ Title and content are required for save action")
            return
        
        tags = [tag.strip() for tag in args.tags.split(',')] if args.tags else []
        manager.save_chat(args.title, args.content, tags, args.category)
        manager.create_index()
        
    elif args.action == 'index':
        manager.create_index()
        
    elif args.action == 'list':
        manager.list_chats(args.filter_category, args.filter_tag)

if __name__ == "__main__":
    main() 