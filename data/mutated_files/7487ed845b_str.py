from typing import TypeAlias
__typ1 : TypeAlias = "int"
import hashlib
import struct
from typing import List, Callable


class MD5Hasher:
    @staticmethod
    def hash(hash_key: <FILL>) -> __typ1:
        digest = hashlib.md5(hash_key.encode()).digest()
        hash_value = struct.unpack('i', digest[:4])[0]
        return hash_value


class __typ0:
    def __tmp3(__tmp0, nodes, __tmp5, __tmp1: __typ1) -> None:
        __tmp0._ring = []
        __tmp0._hash_func = __tmp5

        for node in nodes:
            for count in range(__tmp1):
                hash_key = str(count) + node
                __tmp0._ring.append((__tmp0._hash_func(hash_key), node))

        __tmp0._ring.sort(__tmp4=lambda tup: tup[0])

    def __tmp2(__tmp0, __tmp4: str) :
        node = next((t for t in __tmp0._ring if t[0] > __tmp0._hash_func(__tmp4)), None)
        if node is not None:
            return node[1]
        return __tmp0._ring[0][1]
