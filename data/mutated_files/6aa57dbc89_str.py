from typing import TypeAlias
__typ0 : TypeAlias = "any"
__typ1 : TypeAlias = "int"
from abc import abstractmethod, ABCMeta
from typing import Callable, Tuple


class AbstractSnapshotStore(metaclass=ABCMeta):
    @abstractmethod
    async def __tmp7(__tmp1, __tmp10: <FILL>) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def persist_snapshot(__tmp1, __tmp10: str, __tmp12, __tmp11) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp3(__tmp1, __tmp10, __tmp0: __typ1) :
        raise NotImplementedError("Should Implement this method")


class AbstractEventStore(metaclass=ABCMeta):
    @abstractmethod
    async def __tmp5(__tmp1, __tmp10, __tmp8, __tmp2,
                         __tmp9) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def persist_event(__tmp1, __tmp10, __tmp12, __tmp4) -> __typ1:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp6(__tmp1, __tmp10, __tmp0) -> None:
        raise NotImplementedError("Should Implement this method")


class AbstractProvider(AbstractEventStore, AbstractSnapshotStore, metaclass=ABCMeta):
    pass
