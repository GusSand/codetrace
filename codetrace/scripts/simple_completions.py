#!/usr/bin/env python3
import shutil
from argparse import ArgumentParser
from pathlib import Path
import os
import torch
import datasets
from typing import Union
from transformers import AutoTokenizer, AutoModelForCausalLM, PreTrainedTokenizer
from tqdm import tqdm
from codetrace.parsing_utils import get_model_fim, FimObj, FimChat, prepare_fim_prompt
from codetrace.utils import predict, hex_encode

def success_rate(ds: datasets.Dataset) -> str:
    df = ds.to_pandas()
    num_succ = df["correct"].sum()
    num_tot = df["correct"].count()
    mean = df["correct"].mean()*100
    return f"Success rate: {num_succ}/{num_tot} = {mean:.2f} %"

def is_1tok(fim_type: str, tokenizer: PreTrainedTokenizer) -> bool:
    return len(tokenizer(fim_type, add_special_tokens=False)["input_ids"]) == 1

def _save(batch_completions: list, new_ds_path: Path, msg: str):
    if not os.path.exists(new_ds_path):
        ds = datasets.Dataset.from_list(batch_completions)
        ds.save_to_disk(new_ds_path)
    else:
        ds = datasets.load_from_disk(new_ds_path, keep_in_memory=False)
        ds = datasets.concatenate_datasets([ds, datasets.Dataset.from_list(batch_completions)])
        ds.save_to_disk(new_ds_path)
    print(msg)

def main(
    model: AutoModelForCausalLM,
    tokenizer: PreTrainedTokenizer,
    ds: datasets.IterableDataset,
    new_ds_path: Path,
    model_fim: Union[FimObj,FimChat],
    batch_size: int,
    model_name: str,
    max_n: int
):
    # resume from completions if they exist
    completions, blacklist = [], set()
    if os.path.exists(new_ds_path):
        completions = datasets.load_from_disk(new_ds_path, keep_in_memory=False)
        print(f"Resuming from {len(completions)} completions.")
        for row in completions:
            blacklist.add(hex_encode(row["fim_program"]))

    # preprocess dataset
    ds = ds.filter(lambda x: is_1tok(x["fim_type"], tokenizer))
    if len(blacklist) > 0:
        ds = ds.filter(lambda x: hex_encode(x["fim_program"]) not in blacklist)
    
    ds = ds.map(lambda x: {**x, "_prompt": prepare_fim_prompt(tokenizer, model_fim, x["fim_program"])})

    # generate                  
    num_completed = 0
    for i,batch in tqdm(enumerate(ds.iter(batch_size)), desc="Batch generations"):
        prompts = batch["_prompt"]
        generated_texts = predict(model, tokenizer, prompts)
        batch_completions = [{**{k:batch[k][b] for k in batch.keys()}, 
                            "generated_text": generated_texts[b],
                            "correct": generated_texts[b] == batch["fim_type"][b], 
                            "model_name": model_name} for b in range(len(prompts))]
        num_completed += len(batch_completions)
        # save every batch
        _save(batch_completions, new_ds_path, f"Saving {i} batch")
        if max_n > 0 and num_completed >= max_n:
            break
    # save final success rate
    final_succ = success_rate(datasets.Dataset.from_list(batch_completions))
    with open(new_ds_path / "success.md","w") as fp:
        fp.write(final_succ)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--model", type=str, required=True)
    parser.add_argument("--prompt-ds", type=str, required=True)
    parser.add_argument("--new-ds-name", type=str, required=True)
    
    parser.add_argument("--max-size", type=int, default=-1)
    parser.add_argument("--split",type=str,default="train")
    parser.add_argument("--batch-size", type=int, default=32)

    parser.add_argument("--dtype", choices=["bfloat16", "float32", "float16"], default="float16")
    parser.add_argument("--model-name", default=None)
    parser.add_argument("--tokenizer", default=None)

    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--overwrite", action="store_true")

    args = parser.parse_args()

    if args.overwrite:
        shutil.rmtree(Path(args.new_ds_name))

    args.tokenizer=args.tokenizer if args.tokenizer else args.model
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer)

    datasets.disable_caching()
    ds = datasets.load_dataset(args.prompt_ds, split=args.split, streaming=True).shuffle(
                                                                args.seed, buffer_size=2000)
    
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Using device: {device}")
    
    dtype = getattr(torch, args.dtype)
    model = AutoModelForCausalLM.from_pretrained(args.model, torch_dtype=dtype).to(device)
    model_fim = get_model_fim(args.model)
    
    main(model, tokenizer, ds, Path(args.new_ds_name), model_fim, args.batch_size,
         args.model, args.max_size) 