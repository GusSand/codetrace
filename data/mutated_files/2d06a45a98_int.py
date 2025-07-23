from typing import TypeAlias
__typ1 : TypeAlias = "str"
import hashlib
import struct
from typing import List, Callable


class __typ2:
    @staticmethod
    def hash(__tmp0: __typ1) :
        digest = hashlib.md5(__tmp0.encode()).digest()
        hash_value = struct.unpack('i', digest[:4])[0]
        return hash_value


class __typ0:
    def __tmp5(__tmp1, __tmp4, __tmp7, __tmp2: <FILL>) :
        __tmp1._ring = []
        __tmp1._hash_func = __tmp7

        for node in __tmp4:
            for count in range(__tmp2):
                __tmp0 = __typ1(count) + node
                __tmp1._ring.append((__tmp1._hash_func(__tmp0), node))

        __tmp1._ring.sort(__tmp6=lambda tup: tup[0])

    def __tmp3(__tmp1, __tmp6) :
        node = next((t for t in __tmp1._ring if t[0] > __tmp1._hash_func(__tmp6)), None)
        if node is not None:
            return node[1]
        return __tmp1._ring[0][1]
