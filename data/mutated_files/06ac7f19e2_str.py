from typing import TypeAlias
__typ1 : TypeAlias = "int"
import hashlib
import struct
from typing import List, Callable


class MD5Hasher:
    @staticmethod
    def hash(__tmp0) :
        digest = hashlib.md5(__tmp0.encode()).digest()
        hash_value = struct.unpack('i', digest[:4])[0]
        return hash_value


class __typ0:
    def __tmp4(__tmp1, __tmp3, __tmp6, replica_count) :
        __tmp1._ring = []
        __tmp1._hash_func = __tmp6

        for node in __tmp3:
            for count in range(replica_count):
                __tmp0 = str(count) + node
                __tmp1._ring.append((__tmp1._hash_func(__tmp0), node))

        __tmp1._ring.sort(__tmp5=lambda tup: tup[0])

    def __tmp2(__tmp1, __tmp5: <FILL>) :
        node = next((t for t in __tmp1._ring if t[0] > __tmp1._hash_func(__tmp5)), None)
        if node is not None:
            return node[1]
        return __tmp1._ring[0][1]
