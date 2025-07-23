from typing import TypeAlias
__typ0 : TypeAlias = "any"
__typ2 : TypeAlias = "str"
from abc import abstractmethod, ABCMeta
from typing import Callable, Tuple


class __typ3(metaclass=ABCMeta):
    @abstractmethod
    async def get_snapshot(__tmp1, __tmp7: __typ2) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp5(__tmp1, __tmp7: __typ2, __tmp8: int, snapshot: __typ0) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp2(__tmp1, __tmp7, inclusive_to_index: int) -> None:
        raise NotImplementedError("Should Implement this method")


class __typ1(metaclass=ABCMeta):
    @abstractmethod
    async def __tmp3(__tmp1, __tmp7, __tmp4: int, __tmp0: int,
                         __tmp6: Callable[[__typ0], None]) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def persist_event(__tmp1, __tmp7: __typ2, __tmp8: <FILL>, event: __typ0) -> int:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def delete_events(__tmp1, __tmp7: __typ2, inclusive_to_index: int) :
        raise NotImplementedError("Should Implement this method")


class AbstractProvider(__typ1, __typ3, metaclass=ABCMeta):
    pass
