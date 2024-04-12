import datasets
from codetrace.type_inf_exp.build_dataset import *
from codetrace.utils import *
from argparse import ArgumentParser
import multiprocessing
from transformers import AutoTokenizer
from tqdm import tqdm
from functools import partial
from typing import Callable
from codetrace.fast_utils import get_batches_fast, batched_do_func
import shutil

def batch_filter_is_one_token(batch, tokenizer):
    if len(batch) == 0:
        return []
    input_ids = tokenizer.batch_encode_plus([ex["fim_type"] for ex in batch])["input_ids"]
    return [ex for i,ex in enumerate(batch) if len(input_ids[i]) == 1]


def _func_combo(batch, query_str, do_remove_comments):
    """
    func combo for:
    - remove comments (optional)
    - get prompts
    - filter fill in prog
    """
    new_batch = []
    for ex in batch:
        # filter out too large or too small
        if ex["size"] > 10000 or ex["size"] < 1000:
            continue
        
        if do_remove_comments:
            new_ex = {"_content": remove_comments(ex["content"]), **ex}
        else:
            new_ex = {"_content": ex["content"], **ex}
        
        prompts = make_natural_typeinf_prompt(new_ex, query_str, content_key="_content")
        
        for p in prompts:
            if ": <FILL>" in p["fim_program"]:
                new_batch.append(p)
    return new_batch

    
def multi_process(ds, args):
    """
    Method for processing a dataset with multiple processes.
    Does following:
    - removes comments (optional)
    - gets natural typeinf prompts
    - filters out examples that do not have a fill in program
    - pushes to hub
    - pushes a copy to hub where all examples have a one token type
    """
    num_chunks = args.num_chunks
    for i in range(num_chunks):
        print(f"Processing chunk {i} / {num_chunks}")
        ds_chunk=ds.shard(num_chunks, i)
        batches = get_batches_fast(ds_chunk, len(ds_chunk), args.num_proc)
        del ds_chunk
        results = batched_do_func(batches, args.num_proc, _func_combo, 
                                query_str=TS_QUERY_FUNC_TYPES, 
                                do_remove_comments=args.do_remove_comments)
        print(f"Length of ds: {len(results)}")
        def yielder():
            for ex in tqdm(results, desc="Yielding", total=len(results)):
                yield ex
        ds = datasets.Dataset.from_generator(yielder)
        print(ds)
        ds.save_to_disk("dataset_chunks/"+ args.output_ds.split("/")[-1] + f"-chunk_{i}")

        tokenizer = AutoTokenizer.from_pretrained(args.tokenizer)
        batches = get_batches_fast(results, len(results), args.num_proc)
        ds = batched_do_func(batches, args.num_proc, batch_filter_is_one_token, tokenizer=tokenizer)
        print(f"Length of ds: {len(ds)}")
        def yielder():
            for ex in tqdm(ds, desc="Yielding", total=len(ds)):
                yield ex
        ds = datasets.Dataset.from_generator(yielder)
        print(ds)
        ds.save_to_disk("dataset_chunks/"+ args.output_ds.split("/")[-1] + f"-1tok-chunk_{i}")
        
    # load all chunks and push to hub
    ds_1tok = []
    ds_any_tok = []
    for i in range(num_chunks):
        ds = datasets.load_from_disk("dataset_chunks/"+ args.output_ds.split("/")[-1] + f"-chunk_{i}")
        one_tok = datasets.load_from_disk("dataset_chunks/"+ args.output_ds.split("/")[-1] + f"-1tok-chunk_{i}")
        ds_1tok.append(one_tok)
        ds_any_tok.append(ds)
    ds_1tok = datasets.concatenate_datasets(ds_1tok)
    print(ds_1tok)
    ds_1tok.push_to_hub(args.output_ds + "-1tok", private=True)
    
    ds_any_tok = datasets.concatenate_datasets(ds_any_tok)
    print(ds_any_tok)
    ds_any_tok.push_to_hub(args.output_ds + "-ntok", private=True)

    
def process(ds, args):
    """
    Method for processing a dataset with a single process.
    Does following:
    - removes comments (optional)
    - gets natural typeinf prompts
    - filters out examples that do not have a fill in program
    - pushes to hub
    - pushes a copy to hub where all examples have a one token type
    """
    if args.remove_comments:
        ds = ds.map(lambda x: {"content": remove_comments(x["content"])})

    def _generate_prompts(ds):
        for ex in ds:
            prompts = make_natural_typeinf_prompt(ex, TS_QUERY_FUNC_TYPES)
            for prompt in prompts:
                yield prompt
    
    prompts = datasets.Dataset.from_generator(partial(_generate_prompts, ds), features=ds.features)
        
    ds = ds.filter(lambda x: ": <FILL>" in x["fim_program"])
    print(ds)
    ds.push_to_hub(args.output_ds)

    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer)
    ds = ds.filter(lambda x: len(tokenizer(x["fim_type"])["input_ids"]) == 1, desc="Creating one token ds")
    ds.push_to_hub(args.output_ds + "-1tok")
    print(ds)

def _get_subset(iterable_ds, max_size):
    for i, ex in enumerate(iterable_ds):
        if i >= max_size:
            break
        yield ex

def main(args):
    ds = datasets.load_dataset(args.input_ds, split="train")

    if args.max_size > -1:
        ds = ds.select(range(args.max_size))
            
    if not args.do_multiproc:
        print("Using single process")
        process(ds, args)
    else:
        print("Using multiprocessing")
        if os.path.exists(Path("dataset_chunks")):
            raise ValueError("dataset_chunks directory already exists. Please remove.")
        os.mkdir("dataset_chunks")
        args.num_proc = multiprocessing.cpu_count()
        multi_process(ds, args)
        
        
if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--output_ds", type=str, required=True)
    parser.add_argument("--input_ds", type=str, required=True)
    parser.add_argument("--tokenizer", type=str, default="/home/arjun/models/starcoderbase-1b")
    parser.add_argument("--do-remove-comments", action="store_true", default=False)
    parser.add_argument("--max-size", type=int, default=-1)
    parser.add_argument("--do-multiproc", action="store_true", default=False)
    parser.add_argument("--num-chunks", type=int, default=1)
    args = parser.parse_args()
    main(args)