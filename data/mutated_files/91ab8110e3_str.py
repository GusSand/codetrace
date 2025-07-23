from typing import TypeAlias
__typ0 : TypeAlias = "any"
__typ2 : TypeAlias = "int"
from abc import abstractmethod, ABCMeta
from typing import Callable, Tuple


class AbstractSnapshotStore(metaclass=ABCMeta):
    @abstractmethod
    async def __tmp6(__tmp2, __tmp12: str) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp10(__tmp2, __tmp12, __tmp14: __typ2, __tmp13: __typ0) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp0(__tmp2, __tmp12: str, __tmp3) -> None:
        raise NotImplementedError("Should Implement this method")


class __typ1(metaclass=ABCMeta):
    @abstractmethod
    async def __tmp5(__tmp2, __tmp12: <FILL>, __tmp8, __tmp1: __typ2,
                         __tmp11: Callable[[__typ0], None]) -> __typ2:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp9(__tmp2, __tmp12: str, __tmp14: __typ2, __tmp4: __typ0) -> __typ2:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp7(__tmp2, __tmp12: str, __tmp3: __typ2) -> None:
        raise NotImplementedError("Should Implement this method")


class AbstractProvider(__typ1, AbstractSnapshotStore, metaclass=ABCMeta):
    pass
