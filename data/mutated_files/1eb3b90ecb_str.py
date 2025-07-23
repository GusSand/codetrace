from typing import TypeAlias
__typ0 : TypeAlias = "int"
from typing import List

from .mnemonic import get_seed
from .tree import (
    derive_master_SK,
    derive_child_SK,
)


def __tmp2(__tmp0) -> List[__typ0]:
    __tmp0 = __tmp0.replace(' ', '')
    assert set(__tmp0).issubset(set('m1234567890/'))
    indices = __tmp0.split('/')
    assert indices.pop(0) == 'm'
    return [__typ0(index) for index in indices]


def __tmp1(mnemonic, password: <FILL>, __tmp0) :
    seed = get_seed(mnemonic=mnemonic, password='')
    sk = derive_master_SK(seed)
    for node in __tmp2(__tmp0):
        sk = derive_child_SK(parent_SK=sk, index=node)
    return sk
