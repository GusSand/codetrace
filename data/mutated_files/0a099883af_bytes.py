class __typ0():
    def __init__(__tmp0):
        __tmp0._fnv_prime = 0x01000193
        __tmp0._fnv_offset_basis = 0x811C9DC5
        __tmp0._hash = __tmp0._fnv_offset_basis
        __tmp0._uint32_max = 0x100000000

    def __tmp1(__tmp0, buffer: <FILL>) :
        __tmp0._hash = __tmp0._fnv_offset_basis

        if buffer is None:
            raise ValueError('buffer is empty')

        for b in buffer:
            __tmp0._hash = __tmp0._hash ^ b
            __tmp0._hash = (__tmp0._hash * __tmp0._fnv_prime) % __tmp0._uint32_max

        return __tmp0._hash
