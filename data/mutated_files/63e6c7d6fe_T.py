from typing import TypeAlias
__typ1 : TypeAlias = "bool"
from typing import Generic
from typing import TypeVar

T = TypeVar('T')


class __typ0(Generic[T]):
    def __tmp3(__tmp1, __tmp0: <FILL>, __tmp2, __tmp4) :
        __tmp1._image1 = __tmp0
        __tmp1._image2 = __tmp2
        __tmp1._is_match = __tmp4

    @property
    def __tmp0(__tmp1):
        return __tmp1._image1

    @property
    def __tmp2(__tmp1):
        return __tmp1._image2

    @property
    def __tmp4(__tmp1):
        return __tmp1._is_match
