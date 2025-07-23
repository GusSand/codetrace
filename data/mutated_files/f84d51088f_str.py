from typing import List

from .mnemonic import get_seed
from .tree import (
    derive_master_SK,
    derive_child_SK,
)


def __tmp2(__tmp0: str) :
    __tmp0 = __tmp0.replace(' ', '')
    assert set(__tmp0).issubset(set('m1234567890/'))
    indices = __tmp0.split('/')
    assert indices.pop(0) == 'm'
    return [int(index) for index in indices]


def mnemonic_and_path_to_key(mnemonic: str, __tmp1, __tmp0: <FILL>) -> int:
    seed = get_seed(mnemonic=mnemonic, __tmp1='')
    sk = derive_master_SK(seed)
    for node in __tmp2(__tmp0):
        sk = derive_child_SK(parent_SK=sk, index=node)
    return sk
