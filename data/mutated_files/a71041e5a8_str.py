from typing import TypeAlias
__typ0 : TypeAlias = "any"
__typ1 : TypeAlias = "int"
from abc import abstractmethod, ABCMeta
from typing import Callable, Tuple


class __typ3(metaclass=ABCMeta):
    @abstractmethod
    async def __tmp1(__tmp2, __tmp6) -> Tuple[__typ0, __typ1]:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def persist_snapshot(__tmp2, __tmp6: str, __tmp8: __typ1, __tmp7: __typ0) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def delete_snapshots(__tmp2, __tmp6: str, __tmp0) -> None:
        raise NotImplementedError("Should Implement this method")


class AbstractEventStore(metaclass=ABCMeta):
    @abstractmethod
    async def get_events(__tmp2, __tmp6: str, index_start: __typ1, index_end: __typ1,
                         __tmp5: Callable[[__typ0], None]) -> __typ1:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def __tmp4(__tmp2, __tmp6: <FILL>, __tmp8: __typ1, __tmp3: __typ0) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def delete_events(__tmp2, __tmp6: str, __tmp0) -> None:
        raise NotImplementedError("Should Implement this method")


class __typ2(AbstractEventStore, __typ3, metaclass=ABCMeta):
    pass
