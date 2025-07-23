from functools import total_ordering
from typing import Tuple

@total_ordering
class __typ0:
    def __init__(__tmp1, positions):
        __tmp1.positions = positions

    def __tmp6(__tmp1):
        return ".".join(str(position) for position in __tmp1.positions)

    def __tmp0(__tmp1, __tmp5):
        return __tmp1.positions < __tmp5.positions

    def __tmp2(__tmp1, __tmp5):
        return __tmp1.positions == __tmp5.positions

    def __tmp4(__tmp1):
        return hash(__tmp1.positions)

    @classmethod
    def __tmp7(cls, __tmp3: <FILL>):
        return cls(tuple(map(int, __tmp3.split("."))))
