from typing import TypeAlias
__typ2 : TypeAlias = "str"
__typ3 : TypeAlias = "any"
from abc import abstractmethod, ABCMeta
from typing import Callable, Tuple


class AbstractSnapshotStore(metaclass=ABCMeta):
    @abstractmethod
    async def get_snapshot(__tmp0, actor_name: __typ2) :
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def persist_snapshot(__tmp0, actor_name: __typ2, index: int, snapshot) -> None:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def delete_snapshots(__tmp0, actor_name: __typ2, inclusive_to_index: <FILL>) -> None:
        raise NotImplementedError("Should Implement this method")


class __typ1(metaclass=ABCMeta):
    @abstractmethod
    async def get_events(__tmp0, actor_name: __typ2, index_start: int, index_end: int,
                         callback) -> int:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def persist_event(__tmp0, actor_name, index: int, event) -> int:
        raise NotImplementedError("Should Implement this method")

    @abstractmethod
    async def delete_events(__tmp0, actor_name, inclusive_to_index: int) -> None:
        raise NotImplementedError("Should Implement this method")


class __typ0(__typ1, AbstractSnapshotStore, metaclass=ABCMeta):
    pass
