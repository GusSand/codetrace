from typing import Dict,Any,List
import shutil
from collections import namedtuple
from codetrace.steering import (
    subtract_avg,
    get_model_fim,
    prepare_prompt_pairs,
    _steer_test_split,
    balance_prompts,
    SteeringManager
)
import datasets
from codetrace.parsing_utils import LLAMA_CHAT_TEMPLATE
import torch

def test_subtract_avg():
    x = torch.Tensor(
        [
            # layer0
            [
                # prompt 0
                [[1,2],[3,4],[5,6]],
                # prompt 1
                [[1,2],[3,4],[5,6]],
            ],

            # layer1
            [
                # prompt 0
                [[1,2],[3,4],[5,6]],
                # prompt 1
                [[-1,-2],[-3,-4],[-5,-6]],
            ],
            # layer2
            [
                # prompt 0
                [[1,2],[3,4],[5,6]],
                # prompt 1
                [[1,-2],[3,-4],[-5,6]],
            ],
        ]
    )
    output = subtract_avg(x)
    expected = torch.Tensor(
        [
            # layer0
            [
                [[0,0],[0,0],[0,0]],
            ],

            # layer1
            [
                # prompt 0
                [[2,4],[6,8],[10,12]],
            ],
            # layer2
            [
                [[0,4],[0,8],[10,0]],
            ],
        ]).to(dtype=torch.float)
    print(x.shape, expected.shape, output.shape)
    assert torch.equal(output, expected), f"{output} != {expected}"

def test_prepare_prompts():
    prompts = [
        {"fim_program":"my name is <FILL> !","mutated_program":"my name is NOT <FILL> !"},
        {"fim_program":"my job is <FILL> !","mutated_program":"my job is NOT <FILL> !"},
        {"fim_program":"my house is <FILL> !","mutated_program":"my house is NOT <FILL> !"},
        {"fim_program":"my car is <FILL> !","mutated_program":"my car is NOT <FILL> !"},
    ]
    fim_obj = get_model_fim("starcoder")
    output = prepare_prompt_pairs(prompts, (lambda x: fim_obj.placeholder_to_fim(x)))
    expected = []
    for i in prompts:
        expected.append(fim_obj.placeholder_to_fim(i["fim_program"]))
        expected.append(fim_obj.placeholder_to_fim(i["mutated_program"]))
    assert output == expected, f"{output}!={expected}"

def test_split():
    data = [{"hexsha":0, "typechecks": True},
            {"hexsha":1, "typechecks": True},
            {"hexsha":2, "typechecks": True},
            {"hexsha":3, "typechecks": True},
            {"hexsha":4, "typechecks": True},
            {"hexsha":5, "typechecks": True},
            {"hexsha":5, "typechecks": True},
            {"hexsha":5, "typechecks": True},
            {"hexsha":6, "typechecks": True},
            {"hexsha":6, "typechecks": True},
            {"hexsha":7, "typechecks": True},
            ]
    ds = datasets.Dataset.from_list(data)
    steer_split,test_split = _steer_test_split(
        ds,
        4,
        False,
        None,
        "hexsha"
    )
    steer_split = [x["hexsha"] for x in steer_split]
    test_split = [x["hexsha"] for x in test_split]
    print(steer_split, test_split)
    assert set(steer_split).intersection(set(test_split)) == set(), f"{steer_split} - {test_split}"

def test_prepare_chat_prompt():
    from transformers import AutoTokenizer
    fim_obj = get_model_fim("codellama_instruct")

    program = f"""
def is_palindrome(s: {fim_obj.placeholder}):
    return s[::-1]==s
""".strip()
    
    tokenizer = AutoTokenizer.from_pretrained("/mnt/ssd/arjun/models/codellama_7b_instruct")
    output = tokenizer.apply_chat_template(fim_obj.placeholder_to_fim(program), tokenize=False, 
                                           add_generation_prompt=False, continue_final_message=True)
    expected = '''<s>[INST] Continue this program with the correct substitution for <FILL>:

def is_palindrome(s: <FILL>):
    return s[::-1]==s [/INST] def is_palindrome(s:'''
    print(expected)
    print(output)
    assert output == expected, f"{output}!={expected}"

    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")
    output = tokenizer.apply_chat_template(fim_obj.placeholder_to_fim(program), tokenize=False, 
                                           add_generation_prompt=False, continue_final_message=True,
                                           chat_template=LLAMA_CHAT_TEMPLATE)
    expected = '''<|begin_of_text|><|start_header_id|>user<|end_header_id|>

Continue this program with the correct substitution for <FILL>:

def is_palindrome(s: <FILL>):
    return s[::-1]==s<|eot_id|><|start_header_id|>assistant<|end_header_id|>

def is_palindrome(s:'''
    print(expected)
    print(output)
    assert output == expected, f"{output}!={expected}"

import pytest
from unittest.mock import MagicMock
from datasets import Dataset

# Test for the balance_prompts function
@pytest.fixture
def mock_dataset():
    # Create a mock dataset with hexsha (program ids) and fim_type (label types)
    data = [
        {"_original_program": "prog1", "fim_type": "typeA"},
        {"_original_program": "prog1", "fim_type": "typeA"},
        {"_original_program": "prog2", "fim_type": "typeB"},
        {"_original_program": "prog2", "fim_type": "typeA"},
        {"_original_program": "prog3", "fim_type": "typeB"},
        {"_original_program": "prog3", "fim_type": "typeB"},
        {"_original_program": "prog1", "fim_type": "typeB"},
        {"_original_program": "prog3", "fim_type": "typeA"},
    ]
    return Dataset.from_list(data)

def test_balance_prompts(mock_dataset):
    # Case 1: dedup_prog_threshold and dedup_type_threshold are greater than dataset size
    dedup_prog_threshold = 5
    dedup_type_threshold = 5
    result = balance_prompts(mock_dataset, dedup_prog_threshold, dedup_type_threshold)
    assert len(result) == 8, "The dataset should remain unchanged as the thresholds are higher than the data."

def test_balance_prompts_dedup_prog_threshold(mock_dataset):
    # Case 2: Deduplication on program ID (hexsha) with a lower threshold
    dedup_prog_threshold = 2
    dedup_type_threshold = 5
    result = balance_prompts(mock_dataset, dedup_prog_threshold, dedup_type_threshold)
    
    # Verify that no program appears more than 2 times
    prog_count = {}
    for ex in result:
        prog_count[ex["_original_program"]] = prog_count.get(ex["_original_program"], 0) + 1
    
    for count in prog_count.values():
        assert count <= dedup_prog_threshold, f"Program exceeded the deduplication threshold: {prog_count}"

def test_balance_prompts_dedup_type_threshold(mock_dataset):
    # Case 3: Deduplication on label type (fim_type) with a lower threshold
    dedup_prog_threshold = 5
    dedup_type_threshold = 2
    result = balance_prompts(mock_dataset, dedup_prog_threshold, dedup_type_threshold)
    
    # Verify that no type appears more than 2 times
    type_count = {}
    for ex in result:
        type_count[ex["fim_type"]] = type_count.get(ex["fim_type"], 0) + 1
    
    for count in type_count.values():
        assert count <= dedup_type_threshold, f"Label type exceeded the deduplication threshold: {type_count}"

def test_balance_prompts_dedup_both(mock_dataset):
    # Case 4: Deduplication on both program ID and label type with lower thresholds
    dedup_prog_threshold = 2
    dedup_type_threshold = 2
    result = balance_prompts(mock_dataset, dedup_prog_threshold, dedup_type_threshold)
    
    # Verify that no program or label type exceeds the deduplication threshold
    prog_count = {}
    type_count = {}
    
    for ex in result:
        prog_count[ex["_original_program"]] = prog_count.get(ex["_original_program"], 0) + 1
        type_count[ex["fim_type"]] = type_count.get(ex["fim_type"], 0) + 1
    
    for count in prog_count.values():
        assert count <= dedup_prog_threshold, f"Program exceeded the deduplication threshold: {prog_count}"
    
    for count in type_count.values():
        assert count <= dedup_type_threshold, f"Label type exceeded the deduplication threshold: {type_count}"

def test_balance_prompts_dedup_no_limit(mock_dataset):
    # Case 5: No deduplication limit (dedup_prog_threshold = -1, dedup_type_threshold = -1)
    dedup_prog_threshold = -1
    dedup_type_threshold = -1
    result = balance_prompts(mock_dataset, dedup_prog_threshold, dedup_type_threshold)
    
    # Verify that the dataset size remains the same as no limit is applied
    assert len(result) == len(mock_dataset), "The dataset should not be filtered when no deduplication limits are applied."


def _check_dedup(split:List[Dict[str,Any]], dedup_prog_threshold:int, dedup_type_threshold:int):
    prog_count = {}
    type_count = {}
    for ex in split:
        prog_count[ex["_original_program"]] = prog_count.get(ex["_original_program"], 0) + 1
        type_count[ex["fim_type"]] = type_count.get(ex["fim_type"], 0) + 1

    for count in prog_count.values():
        assert count <= dedup_prog_threshold, f"Program exceeded the deduplication threshold: {prog_count}"
    
    for count in type_count.values():
        assert count <= dedup_type_threshold, f"Label type exceeded the deduplication threshold: {type_count}"

@pytest.mark.parametrize("dedup_prog_threshold, dedup_type_threshold", [
    (1, 1),
    (2, 3),
    (3, 1),
    (5, 5)
])
def test_balance_prompts_varying_thresholds(mock_dataset, dedup_prog_threshold, dedup_type_threshold):
    # Case 8: Varying thresholds to test different configurations
    result = balance_prompts(mock_dataset, dedup_prog_threshold, dedup_type_threshold)
    
    # Verify no program or label type exceeds the respective thresholds
    prog_count = {}
    type_count = {}
    
    _check_dedup(result, dedup_prog_threshold, dedup_type_threshold)


def test_steering_test_split():
    """
    Test that for a given candidate ts, test split is always the same
    AND test split fully typechecks
    """
    TEST_SIZE = 100
    MAXN=500
    DEBUG_CYCLE=40
    dedup_type_threshold = 25
    dedup_prog_threshold = 3
    shutil.rmtree("/tmp/testing_steering_manager", ignore_errors=True)
    shutil.rmtree("/tmp/testing_steering_manager2", ignore_errors=True)

    FakeModel = namedtuple("FakeModel", ["tokenizer", "config"])
    FakeConfig = namedtuple("FakeConfig", "name_or_path")
    model = FakeModel(tokenizer=None, config = FakeConfig(name_or_path="starcoder"))
    ds = datasets.load_dataset("nuprl-staging/type-steering", name="mutations-py-types_vars-qwen2p5_coder_7b_base", 
                               split="train")
    smanager = SteeringManager(model, ds, "/tmp/testing_steering_manager", "steer","test","stensor",
                               max_num_candidates=MAXN)
    assert len(smanager.candidates_ds) == MAXN
    steer_split, test_split = smanager.steer_test_splits(TEST_SIZE, dedup_prog_threshold, dedup_type_threshold,
                                                         debug_max_cycle=DEBUG_CYCLE)
    assert set(test_split["typechecks"]) == set([True])
    assert len(test_split) == TEST_SIZE

    _check_dedup(test_split, dedup_prog_threshold, dedup_type_threshold)
    _check_dedup(steer_split, dedup_prog_threshold, dedup_type_threshold)

    smanager2 = SteeringManager(model, ds, "/tmp/testing_steering_manager2", "steer","test","stensor",
                               max_num_candidates=MAXN)
    steer_split2, test_split2 = smanager2.steer_test_splits(TEST_SIZE, dedup_prog_threshold, dedup_type_threshold,
                                                             debug_max_cycle=DEBUG_CYCLE)

    _check_dedup(steer_split2, dedup_prog_threshold, dedup_type_threshold)
    _check_dedup(test_split2, dedup_prog_threshold, dedup_type_threshold)

    assert set(test_split2["mutated_program"]) == set(test_split["mutated_program"])
    assert set(steer_split2["_original_program"]).intersection(test_split2["_original_program"]) == set()
    assert set(steer_split["_original_program"]).intersection(test_split["_original_program"]) == set()

if __name__ == "__main__":
    import pytest
    import os
    pytest.main([os.path.abspath(__file__), "-vv"])