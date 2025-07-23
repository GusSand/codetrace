#!/usr/bin/env python3
"""
Helper script to start a new conversation with saved context.
This script provides easy access to saved context and templates.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

def show_context_files():
    """Show available context files."""
    context_dir = Path("chats/context")
    if not context_dir.exists():
        print("❌ No context directory found. Run save_current_context.py first.")
        return
    
    print("📁 Available context files:")
    print()
    
    # Show markdown summaries
    md_files = list(context_dir.glob("*.md"))
    for md_file in sorted(md_files, reverse=True):
        if md_file.name.startswith("neural_steering_context_"):
            print(f"📄 {md_file.name}")
            print(f"   Path: {md_file}")
            print()
    
    # Show index
    index_file = context_dir / "index.md"
    if index_file.exists():
        print(f"📋 Context index: {index_file}")
        print()

def show_latest_context():
    """Show the latest context summary."""
    context_dir = Path("chats/context")
    if not context_dir.exists():
        print("❌ No context directory found.")
        return
    
    # Find latest context file
    context_files = list(context_dir.glob("neural_steering_context_*.md"))
    if not context_files:
        print("❌ No context files found.")
        return
    
    latest_file = max(context_files, key=lambda x: x.stat().st_mtime)
    
    print(f"📖 Latest context summary: {latest_file.name}")
    print("=" * 60)
    
    with open(latest_file, 'r') as f:
        content = f.read()
        print(content)
    
    print("=" * 60)
    print(f"📄 Full file: {latest_file}")

def show_template():
    """Show the latest conversation template."""
    context_dir = Path("chats/context")
    if not context_dir.exists():
        print("❌ No context directory found.")
        return
    
    # Find latest template
    template_files = list(context_dir.glob("new_conversation_template_*.md"))
    if not template_files:
        print("❌ No template files found.")
        return
    
    latest_template = max(template_files, key=lambda x: x.stat().st_mtime)
    
    print(f"📝 Latest conversation template: {latest_template.name}")
    print("=" * 60)
    
    with open(latest_template, 'r') as f:
        content = f.read()
        print(content)
    
    print("=" * 60)
    print(f"📄 Full file: {latest_template}")

def copy_context_to_clipboard():
    """Copy the latest context to clipboard (if available)."""
    try:
        import pyperclip
    except ImportError:
        print("❌ pyperclip not available. Install with: pip install pyperclip")
        return
    
    context_dir = Path("chats/context")
    if not context_dir.exists():
        print("❌ No context directory found.")
        return
    
    # Find latest context file
    context_files = list(context_dir.glob("neural_steering_context_*.md"))
    if not context_files:
        print("❌ No context files found.")
        return
    
    latest_file = max(context_files, key=lambda x: x.stat().st_mtime)
    
    with open(latest_file, 'r') as f:
        content = f.read()
    
    try:
        pyperclip.copy(content)
        print(f"✅ Copied context from {latest_file.name} to clipboard!")
        print("📋 You can now paste it in your new conversation.")
    except Exception as e:
        print(f"❌ Failed to copy to clipboard: {e}")

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Start a new conversation with saved context')
    parser.add_argument('--show-files', action='store_true', help='Show available context files')
    parser.add_argument('--show-context', action='store_true', help='Show latest context summary')
    parser.add_argument('--show-template', action='store_true', help='Show latest conversation template')
    parser.add_argument('--copy', action='store_true', help='Copy latest context to clipboard')
    parser.add_argument('--all', action='store_true', help='Show all information')
    
    args = parser.parse_args()
    
    if not any([args.show_files, args.show_context, args.show_template, args.copy, args.all]):
        print("🎯 Starting new conversation helper...")
        print()
        print("Available options:")
        print("  --show-files     Show available context files")
        print("  --show-context   Show latest context summary")
        print("  --show-template  Show latest conversation template")
        print("  --copy          Copy latest context to clipboard")
        print("  --all           Show all information")
        print()
        print("Example: python start_new_conversation.py --all")
        return
    
    if args.all or args.show_files:
        show_context_files()
        print()
    
    if args.all or args.show_context:
        show_latest_context()
        print()
    
    if args.all or args.show_template:
        show_template()
        print()
    
    if args.all or args.copy:
        copy_context_to_clipboard()
        print()
    
    if args.all:
        print("🎉 Ready to start your new conversation!")
        print("💡 Tip: Use the context summary at the beginning of your new conversation.")

if __name__ == "__main__":
    main() 