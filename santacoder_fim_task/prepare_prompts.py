"""
The FIM prompts are not identical for every model. This script prepares a
JSON file that uses the right tokens for each model type.

The command-line argument takes a model name (one of a fixed set of models)
and an output filename, and transforms the benchmark
(https://huggingface.co/datasets/bigcode/santacoder-fim-task) to have the
columns:

- name: from the original benchmark
- language: from the original benchmark
- fim_prompt: a combination of the prompt and suffix columns from the original
    benchmark, with the right tokens for the model.
- canonical_solution: from the original benchmark
- fim_style: the style of the FIM prompt (e.g., "santacoder", "codellama")

We drop the tests column.

We save the result in JSONL format.
"""

# cspell:ignore starcoder codellama
import argparse
import json
import datasets
from transformers import AutoTokenizer

STYLE_TO_TOKENIZER_PATH = {
    "codellama": "codellama/CodeLlama-7b-hf",
    "starcoder1": "bigcode/starcoderbase",
    "qwencoder": "Qwen/Qwen2.5-Coder-7B"
}


def formatter_for_style(style: str):
    if style == "codellama":
        return codellama_style()
    elif style == "starcoder1":
        return starcoder1_style()
    elif style == "qwencoder":
        return qwencoder_style()
    else:
        raise ValueError(f"Unknown style: {style}")

def starcoder1_style():
    def formatter(item):
        prompt, suffix = item["prompt"], item["suffix"]
        return {"prompt": f"<fim_prefix>{prompt}<fim_suffix>{suffix}<fim_middle>"}

    return formatter

def qwencoder_style():
    """
    These were determined by looking at the tokenizer here:
    
    https://huggingface.co/Qwen/Qwen2.5-Coder-7B/blob/main/tokenizer_config.json
    """
    def formatter(item):
        prompt, suffix = item["prompt"], item["suffix"]
        return {"prompt": f"<|fim_prefix|>{prompt}<|fim_suffix|>{suffix}<|fim_middle|>"}

    return formatter

def codellama_style():
    """
    Formats using Code Llama's FIM style. The special tokens are here:

    https://github.com/meta-llama/codellama/blob/e81b597e44dbecc2a0dedb9949fdf84adfc22395/llama/tokenizer.py#L28

    The format is here:

    https://github.com/meta-llama/codellama/blob/main/llama/generation.py#L496

    The comment in the code says format as "<PRE> {pre} <SUF>{suf} <MID>"

    However, the code does not insert spaces. Also see

    https://github.com/meta-llama/codellama/blob/e81b597e44dbecc2a0dedb9949fdf84adfc22395/llama/tokenizer.py#L57


    """
    tokenizer = AutoTokenizer.from_pretrained(STYLE_TO_TOKENIZER_PATH["codellama"])
    prefix_token, middle_token, suffix_token, _ = tokenizer.additional_special_tokens

    # Additional sanity checks.
    assert prefix_token == "▁<PRE>"
    assert middle_token == "▁<MID>"
    assert suffix_token == "▁<SUF>"

    def formatter(item):
        prompt, suffix = item["prompt"], item["suffix"]
        return {"prompt": f"{prefix_token}{prompt}{suffix_token}{suffix}{middle_token}"}

    return formatter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fim-style", choices=STYLE_TO_TOKENIZER_PATH.keys(), required=True)
    parser.add_argument("--output-file", type=str)
    args = parser.parse_args()

    if args.output_file is None:
        args.output_file = f"{args.fim_style}_fim_task.jsonl"
        print(f"No output file provided; using default: {args.output_file}")

    original_dataset = datasets.load_dataset(
        "bigcode/santacoder-fim-task", split="train"
    )

    formatter = formatter_for_style(args.fim_style)
    formatted_dataset = original_dataset.map(formatter).remove_columns(
        ["tests", "suffix"]
    )

    # Save to JSONL format
    with open(args.output_file, 'w') as f:
        for item in formatted_dataset:
            f.write(json.dumps(item) + '\n')


if __name__ == "__main__":
    main()
