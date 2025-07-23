from abc import abstractmethod, ABCMeta
from typing import Callable, Tuple


class AbstractSnapshotStore(metaclass=ABCMeta):
    @abstractmethod
    async def get_snapshot(__tmp0, actor_name: str) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def persist_snapshot(__tmp0, actor_name, __tmp4: int, __tmp3) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def delete_snapshots(__tmp0, actor_name: <FILL>, inclusive_to_index) :
        raise NotImplementedError("Should Implement this method")


class AbstractEventStore(metaclass=ABCMeta):
    @abstractmethod
    async def get_events(__tmp0, actor_name, __tmp1, index_end,
                         __tmp2: Callable[[any], None]) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def persist_event(__tmp0, actor_name, __tmp4: int, event) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def delete_events(__tmp0, actor_name, inclusive_to_index) :
        raise NotImplementedError("Should Implement this method")


class __typ0(AbstractEventStore, AbstractSnapshotStore, metaclass=ABCMeta):
    pass
