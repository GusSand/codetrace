from typing import TypeAlias
__typ0 : TypeAlias = "any"
__typ2 : TypeAlias = "str"
from abc import abstractmethod, ABCMeta
from typing import Callable, Tuple


class __typ4(metaclass=ABCMeta):
    @abstractmethod
    async def __tmp2(__tmp1, __tmp7) -> Tuple[__typ0, int]:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def persist_snapshot(__tmp1, __tmp7: __typ2, index: <FILL>, __tmp8: __typ0) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp5(__tmp1, __tmp7: __typ2, __tmp0: int) :
        raise NotImplementedError("Should Implement this method")


class __typ3(metaclass=ABCMeta):
    @abstractmethod
    async def get_events(__tmp1, __tmp7: __typ2, index_start: int, __tmp3: int,
                         callback: Callable[[__typ0], None]) -> int:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp6(__tmp1, __tmp7, index, __tmp4: __typ0) -> int:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def delete_events(__tmp1, __tmp7: __typ2, __tmp0: int) -> None:
        raise NotImplementedError("Should Implement this method")


class __typ1(__typ3, __typ4, metaclass=ABCMeta):
    pass
