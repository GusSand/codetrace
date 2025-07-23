from typing import Generic
from typing import TypeVar

T = TypeVar('T')


class __typ0(Generic[T]):
    def __init__(self, __tmp0: T, __tmp1: <FILL>, __tmp2) -> None:
        self._image1 = __tmp0
        self._image2 = __tmp1
        self._is_match = __tmp2

    @property
    def __tmp0(self):
        return self._image1

    @property
    def __tmp1(self):
        return self._image2

    @property
    def __tmp2(self):
        return self._is_match
