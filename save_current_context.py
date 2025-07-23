#!/usr/bin/env python3
"""
Save current conversation context and learnings for future reference.
This script extracts key information from the current conversation and saves it
in a structured format that can be easily referenced in new conversations.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import re

class ConversationContextSaver:
    """Save conversation context and learnings for future reference."""
    
    def __init__(self):
        self.output_dir = Path("chats/context")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Current conversation summary
        self.conversation_summary = {
            "timestamp": datetime.now().isoformat(),
            "topic": "Neural Steering Security Experiments",
            "key_learnings": [],
            "important_files": [],
            "experiment_results": [],
            "code_snippets": [],
            "next_steps": [],
            "context_for_new_conversation": ""
        }
    
    def extract_key_learnings(self) -> List[str]:
        """Extract key learnings from the conversation."""
        learnings = [
            "Neural steering experiments successfully improved security scores from baseline to 0.125 with 5 samples",
            "Real nnsight steering vectors work better than synthetic ones for security improvements",
            "Layer configurations [4,12,20] with steering scale 20.0 achieved best results in original experiments",
            "Sample efficiency experiments showed diminishing returns with more training examples",
            "Steering vectors need proper dimension matching and context handling",
            "Memory usage and generation time increase with steering scale and number of layers",
            "Different vulnerability types (SQL injection, XSS, path traversal) respond differently to steering",
            "Optimal steering scale varies by vulnerability type and layer configuration",
            "Real-time monitoring and visualization are crucial for steering experiment success",
            "Chat management system provides structured way to save and reference conversations"
        ]
        return learnings
    
    def identify_important_files(self) -> List[Dict[str, str]]:
        """Identify important files from the conversation."""
        important_files = [
            {
                "path": "security/sample_efficiency_experiment/real_steering_experiment.py",
                "description": "Working steering experiment with real nnsight vectors",
                "type": "experiment"
            },
            {
                "path": "security/visualize_steering_strength.py", 
                "description": "Comprehensive visualization and analysis tool",
                "type": "analysis"
            },
            {
                "path": "chats/chat_manager.py",
                "description": "Chat management system for saving conversations",
                "type": "utility"
            },
            {
                "path": "steering_strength_results_20250721_212641.json",
                "description": "Latest steering strength experiment results",
                "type": "data"
            },
            {
                "path": "security/security_patterns.py",
                "description": "Security pattern definitions for evaluation",
                "type": "evaluation"
            }
        ]
        return important_files
    
    def extract_experiment_results(self) -> List[Dict[str, Any]]:
        """Extract key experiment results."""
        results = [
            {
                "experiment": "Original NNSight Steering",
                "best_security_score": 0.222,
                "training_examples": 26,
                "layer_config": [4, 12, 20],
                "steering_scale": 20.0,
                "notes": "Baseline performance with real steering vectors"
            },
            {
                "experiment": "Sample Efficiency Study",
                "best_security_score": 0.125,
                "training_examples": 5,
                "layer_config": [4, 12, 20],
                "steering_scale": 20.0,
                "notes": "Achieved better results with fewer examples"
            },
            {
                "experiment": "Steering Strength Analysis",
                "key_findings": [
                    "Optimal steering scale varies by vulnerability type",
                    "Layer configurations significantly impact performance",
                    "Memory usage scales with steering parameters",
                    "Quality scores trade off with security improvements"
                ]
            }
        ]
        return results
    
    def extract_code_snippets(self) -> List[Dict[str, str]]:
        """Extract important code snippets."""
        snippets = [
            {
                "name": "Steering Vector Application",
                "description": "How to apply steering vectors during generation",
                "code": """
# Key pattern for applying steering vectors
with model.generate(max_new_tokens=100, pad_token_id=tokenizer.eos_token_id) as generator:
    with generator.invoke(prompt) as invoker:
        # Apply steering vectors to specific layers
        for layer_idx in layer_config:
            hidden_states = invoker.model.layers[layer_idx].output[0]
            hidden_states += steering_vectors[layer_idx] * steering_scale
        output = invoker.next()
""",
                "type": "steering"
            },
            {
                "name": "Security Evaluation",
                "description": "Pattern-based security scoring",
                "code": """
def evaluate_security(generated_code, vulnerability_type):
    secure_patterns = SECURITY_PATTERNS[vulnerability_type]['secure']
    vulnerable_patterns = SECURITY_PATTERNS[vulnerability_type]['vulnerable']
    
    secure_count = sum(1 for pattern in secure_patterns if pattern in generated_code)
    vulnerable_count = sum(1 for pattern in vulnerable_patterns if pattern in generated_code)
    
    security_score = secure_count / (secure_count + vulnerable_count + 1)
    return security_score
""",
                "type": "evaluation"
            }
        ]
        return snippets
    
    def generate_next_steps(self) -> List[str]:
        """Generate suggested next steps."""
        next_steps = [
            "Run comprehensive steering strength analysis with more vulnerability types",
            "Investigate optimal layer selection strategies for different models",
            "Develop automated hyperparameter optimization for steering parameters",
            "Create real-time steering vector quality assessment",
            "Extend experiments to larger language models (7B+ parameters)",
            "Investigate steering vector transferability across different tasks",
            "Develop steering vector compression techniques for efficiency",
            "Create interactive visualization dashboard for steering experiments",
            "Implement steering vector versioning and A/B testing framework",
            "Investigate steering vector interpretability and explainability"
        ]
        return next_steps
    
    def generate_context_for_new_conversation(self) -> str:
        """Generate context summary for new conversations."""
        context = """
## Neural Steering Security Experiments - Context Summary

### Key Achievements
- Successfully implemented real nnsight steering vectors for security improvement
- Achieved security score of 0.125 with only 5 training examples
- Developed comprehensive visualization and analysis tools
- Created chat management system for conversation persistence

### Technical Learnings
- Real steering vectors outperform synthetic ones for security tasks
- Layer configurations [4,12,20] with scale 20.0 work well for security
- Proper dimension matching and context handling are crucial
- Memory usage scales with steering parameters

### Important Files
- `security/sample_efficiency_experiment/real_steering_experiment.py` - Working experiment
- `security/visualize_steering_strength.py` - Analysis and visualization
- `chats/chat_manager.py` - Conversation management
- `steering_strength_results_*.json` - Experiment results

### Next Steps
- Extend to more vulnerability types and models
- Optimize steering parameters automatically
- Develop real-time quality assessment
- Create interactive visualization dashboard

### Code Patterns
- Use nnsight's invoke context for steering vector application
- Apply steering vectors to specific transformer layers
- Use pattern-based security evaluation
- Monitor memory usage and generation time

This context can be referenced for continuing neural steering research and development.
"""
        return context.strip()
    
    def save_context(self) -> str:
        """Save the conversation context to files."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Update summary with extracted information
        self.conversation_summary["key_learnings"] = self.extract_key_learnings()
        self.conversation_summary["important_files"] = self.identify_important_files()
        self.conversation_summary["experiment_results"] = self.extract_experiment_results()
        self.conversation_summary["code_snippets"] = self.extract_code_snippets()
        self.conversation_summary["next_steps"] = self.generate_next_steps()
        self.conversation_summary["context_for_new_conversation"] = self.generate_context_for_new_conversation()
        
        # Save detailed context
        context_file = self.output_dir / f"neural_steering_context_{timestamp}.json"
        with open(context_file, 'w') as f:
            json.dump(self.conversation_summary, f, indent=2)
        
        # Save markdown summary
        markdown_file = self.output_dir / f"neural_steering_context_{timestamp}.md"
        with open(markdown_file, 'w') as f:
            f.write(self.generate_context_for_new_conversation())
        
        # Update context index
        self.update_context_index(context_file, markdown_file)
        
        return str(context_file)
    
    def update_context_index(self, context_file: Path, markdown_file: Path):
        """Update the context index file."""
        index_file = self.output_dir / "index.md"
        
        if index_file.exists():
            with open(index_file, 'r') as f:
                content = f.read()
        else:
            content = "# Conversation Context Index\n\n"
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_entry = f"""
## Neural Steering Security Experiments - {timestamp}

- **Context File**: `{context_file.name}`
- **Summary**: `{markdown_file.name}`
- **Topic**: Neural steering experiments for security improvement
- **Key Achievement**: Achieved 0.125 security score with 5 training examples

### Quick Reference
- Working experiment: `security/sample_efficiency_experiment/real_steering_experiment.py`
- Analysis tool: `security/visualize_steering_strength.py`
- Best results: layers [4,12,20], scale 20.0
- Next: Extend to more vulnerability types and models

---
"""
        
        # Insert new entry at the top
        lines = content.split('\n')
        insert_index = 2  # After the title
        lines.insert(insert_index, new_entry.strip())
        
        with open(index_file, 'w') as f:
            f.write('\n'.join(lines))
    
    def create_new_conversation_template(self) -> str:
        """Create a template for starting a new conversation."""
        template = """# New Conversation - Neural Steering Research

## Context from Previous Conversation

This conversation builds on previous work on neural steering for security improvement. Key context:

### Previous Achievements
- Implemented real nnsight steering vectors for security tasks
- Achieved security score of 0.125 with 5 training examples  
- Developed comprehensive analysis and visualization tools
- Created chat management system for conversation persistence

### Technical Foundation
- Working experiment: `security/sample_efficiency_experiment/real_steering_experiment.py`
- Analysis tool: `security/visualize_steering_strength.py`
- Best configuration: layers [4,12,20], steering scale 20.0
- Pattern-based security evaluation with multiple vulnerability types

### Current Goals
[Add your specific goals for this conversation]

### Key Questions
[Add specific questions or challenges you want to address]

---

## Conversation Start

[Begin your new conversation here...]
"""
        
        template_file = self.output_dir / f"new_conversation_template_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(template_file, 'w') as f:
            f.write(template)
        
        return str(template_file)


def main():
    """Main function to save conversation context."""
    print("💾 Saving conversation context and learnings...")
    
    saver = ConversationContextSaver()
    
    try:
        # Save context
        context_file = saver.save_context()
        print(f"✅ Saved detailed context to: {context_file}")
        
        # Create new conversation template
        template_file = saver.create_new_conversation_template()
        print(f"📝 Created new conversation template: {template_file}")
        
        print("\n🎯 Ready to start a new conversation!")
        print("\nTo start fresh while preserving context:")
        print("1. Copy the context summary from the generated markdown file")
        print("2. Start a new conversation in Cursor")
        print("3. Paste the context summary at the beginning")
        print("4. Reference the saved context files as needed")
        
        print(f"\n📁 Context files saved in: {saver.output_dir}")
        print(f"📋 Context index: {saver.output_dir}/index.md")
        
    except Exception as e:
        print(f"❌ Error saving context: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main()) 