from typing import TypeAlias
__typ1 : TypeAlias = "int"
class __typ0():
    def __init__(__tmp0):
        __tmp0._fnv_prime = 0x01000193
        __tmp0._fnv_offset_basis = 0x811C9DC5
        __tmp0._hash = __tmp0._fnv_offset_basis
        __tmp0._uint32_max = 0x100000000

    def compute_hash(__tmp0, __tmp1: <FILL>) -> __typ1:
        __tmp0._hash = __tmp0._fnv_offset_basis

        if __tmp1 is None:
            raise ValueError('buffer is empty')

        for b in __tmp1:
            __tmp0._hash = __tmp0._hash ^ b
            __tmp0._hash = (__tmp0._hash * __tmp0._fnv_prime) % __tmp0._uint32_max

        return __tmp0._hash
