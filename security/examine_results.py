#!/usr/bin/env python3
import sys
import os
import json
from pathlib import Path

# Add the parent directory to the path so we can import from codetrace
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    """Analyze the steering results and suggest improvements."""
    
    # Load the generation results
    results_path = Path("security/generation_results.json")
    if not results_path.exists():
        print(f"Results file not found: {results_path}")
        return
    
    with open(results_path, "r") as f:
        results = json.load(f)
    
    examples = results["examples"]
    completions_without_steering = results["completions_without_steering"]
    completions_with_steering = results["completions_with_steering"]
    
    # Analyze the results
    print("\n=== ANALYSIS OF RESULTS ===\n")
    
    # Check if steering is making any difference
    identical_completions = 0
    for comp_without, comp_with in zip(completions_without_steering, completions_with_steering):
        if comp_without == comp_with:
            identical_completions += 1
    
    print(f"Identical completions: {identical_completions}/{len(completions_without_steering)} ({identical_completions/len(completions_without_steering)*100:.1f}%)")
    
    # Identify patterns in the completions
    patterns = {}
    for completion in completions_without_steering + completions_with_steering:
        for line in completion.split("\n"):
            if line.strip().startswith("Update") or line.strip().startswith("Fix"):
                patterns[line.strip()] = patterns.get(line.strip(), 0) + 1
    
    print("\nCommon patterns in completions:")
    for pattern, count in sorted(patterns.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f" - {pattern} ({count} occurrences)")
    
    # Check for format issues
    print("\nFormat analysis:")
    
    fim_format_issues = 0
    for example in examples:
        if "<fim_prefix>" in example["fim_program"] or "<fim_suffix>" in example["fim_program"] or "<fim_middle>" in example["fim_program"]:
            fim_format_issues += 1
    
    print(f" - FIM format issues: {fim_format_issues}/{len(examples)}")
    
    # Check prompt formatting
    prompt_format_issues = 0
    for example in examples:
        if "\n\n" not in example["fim_program"]:
            prompt_format_issues += 1
    
    print(f" - Prompt format issues: {prompt_format_issues}/{len(examples)}")
    
    # Suggestions for improvement
    print("\n=== SUGGESTIONS FOR IMPROVEMENT ===\n")
    
    print("1. FIM Format:")
    print("   - Ensure the FIM placeholder (<FILL>) is properly positioned in the prompt")
    print("   - Verify that the FIM format conversion is working correctly")
    
    print("\n2. Prompt Structure:")
    print("   - Simplify the prompt structure to be more consistent")
    print("   - Ensure clear separation between instructions and code")
    
    print("\n3. Steering Implementation:")
    print("   - Our current steering approach isn't effectively applying the steering tensor")
    print("   - Need to implement proper hidden state manipulation during generation")
    
    print("\n4. Example Complexity:")
    print("   - The security examples might be too complex for the model")
    print("   - Consider simplifying the examples or using a larger model")
    
    print("\n5. Training Approach:")
    print("   - We might need to fine-tune the model on security examples instead of using steering")
    print("   - Steering might not be effective for this specific task")
    
    # Generate improved examples
    print("\n=== SUGGESTED IMPROVED EXAMPLES ===\n")
    
    print("Here's an improved example format:")
    
    improved_example = """
// Task: Generate secure code that avoids SQL injection
// Input:
def search_users(user_input):
    <FILL>

// Expected output:
def search_users(user_input):
    query = "SELECT * FROM users WHERE name = %s"
    return execute_query(query, (user_input,))
"""
    print(improved_example)
    
    # Explain next steps
    print("\n=== NEXT STEPS ===\n")
    
    print("1. Revise the example format to be clearer and more concise")
    print("2. Try steering with different layers (e.g., 6, 7, 8 instead of 10)")
    print("3. Experiment with a stronger steering vector (amplify the tensor)")
    print("4. Consider using a larger model like StarCoder-7B or CodeLlama")
    print("5. If steering continues to be ineffective, consider fine-tuning or other approaches")

if __name__ == "__main__":
    main() 