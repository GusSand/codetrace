from typing import TypeAlias
__typ0 : TypeAlias = "any"
__typ1 : TypeAlias = "int"
from abc import abstractmethod, ABCMeta
from typing import Callable, Tuple


class __typ2(metaclass=ABCMeta):
    @abstractmethod
    async def get_snapshot(__tmp1, __tmp5) -> Tuple[__typ0, __typ1]:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def persist_snapshot(__tmp1, __tmp5, __tmp6: __typ1, snapshot: __typ0) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def delete_snapshots(__tmp1, __tmp5, __tmp0) :
        raise NotImplementedError("Should Implement this method")


class AbstractEventStore(metaclass=ABCMeta):
    @abstractmethod
    async def get_events(__tmp1, __tmp5: str, index_start, __tmp2,
                         __tmp4: Callable[[__typ0], None]) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp3(__tmp1, __tmp5, __tmp6, event: __typ0) -> __typ1:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def delete_events(__tmp1, __tmp5: <FILL>, __tmp0: __typ1) -> None:
        raise NotImplementedError("Should Implement this method")


class AbstractProvider(AbstractEventStore, __typ2, metaclass=ABCMeta):
    pass
