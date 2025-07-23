from typing import Generic
from typing import TypeVar

T = TypeVar('T')


class __typ0(Generic[T]):
    def __init__(__tmp1, __tmp0, __tmp2, __tmp3: <FILL>) :
        __tmp1._image1 = __tmp0
        __tmp1._image2 = __tmp2
        __tmp1._is_match = __tmp3

    @property
    def __tmp0(__tmp1):
        return __tmp1._image1

    @property
    def __tmp2(__tmp1):
        return __tmp1._image2

    @property
    def __tmp3(__tmp1):
        return __tmp1._is_match
