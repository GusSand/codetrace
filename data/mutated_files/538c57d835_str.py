from typing import TypeAlias
__typ0 : TypeAlias = "int"
from typing import List

from .mnemonic import get_seed
from .tree import (
    derive_master_SK,
    derive_child_SK,
)


def __tmp0(path: <FILL>) -> List[__typ0]:
    path = path.replace(' ', '')
    assert set(path).issubset(set('m1234567890/'))
    indices = path.split('/')
    assert indices.pop(0) == 'm'
    return [__typ0(index) for index in indices]


def mnemonic_and_path_to_key(mnemonic: str, password: str, path: str) -> __typ0:
    seed = get_seed(mnemonic=mnemonic, password='')
    sk = derive_master_SK(seed)
    for node in __tmp0(path):
        sk = derive_child_SK(parent_SK=sk, index=node)
    return sk
