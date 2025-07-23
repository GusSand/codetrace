
from abc import ABCMeta, abstractmethod
from typing import Callable, Tuple, Any

from protoactor.actor.actor import Actor


class Persistent():
    def __init__(self):
        self._state = None
        self._index = None
        self._context = None
        self._recovering = None

    @property
    def __tmp6(self):
        return self._context.my_self.id

    @property
    def actor_id(self):
        return self._context.self.id

    async def __tmp2(self, __tmp8, context, actor):
        self._state = __tmp8.get_state()
        self._context = context
        self._actor = actor

        __tmp12, __tmp15 = await self._state.get_snapshot()
        if __tmp12 is not None:
            self._index = __tmp15
            actor.update_state(RecoverSnapshot(__tmp12, self._index))

        def __tmp14(e):
            self._index += 1
            actor.update_state(RecoverEvent(e, self._index))

        await self._state.get_events(self.actor_id, __tmp15, __tmp14)

    async def persist_event_async(self, __tmp5):
        self._index += 1
        await self._state.persist_event(self.actor_id, self._index, __tmp5)
        self._actor.update_state(PersistedEvent(__tmp5, self._index))

    async def persist_snapshot(self, __tmp12):
        await self._state.persist_snapshot(self.actor_id, self._index, __tmp12)

    async def delete_snapshot(self, __tmp1):
        await self._state.delete_snapshot(__tmp1)

    async def delete_events(self, __tmp1):
        await self._state.delete_event(__tmp1)


class Snapshot():
    def __init__(self, __tmp7, __tmp15):
        self._state = __tmp7
        self._index = __tmp15

    @property
    def __tmp7(self):
        return self._state

    @property
    def __tmp15(self):
        return self._index


class RecoverSnapshot(Snapshot):
    def __init__(self, __tmp7, __tmp15):
        super(RecoverSnapshot, self).__init__(__tmp7, __tmp15)


class PersistedSnapshot(Snapshot):
    def __init__(self, __tmp7, __tmp15):
        super(PersistedSnapshot, self).__init__(__tmp7, __tmp15)


class __typ0():
    def __init__(self, __tmp4, __tmp15):
        self._data = __tmp4
        self._index = __tmp15

    @property
    def __tmp4(self):
        return self._data

    @property
    def __tmp15(self):
        return self._index


class RecoverEvent(__typ0):
    def __init__(self, __tmp4, __tmp15):
        super(RecoverEvent, self).__init__(__tmp4, __tmp15)


class PersistedEvent(__typ0):
    def __init__(self, __tmp4, __tmp15):
        super(PersistedEvent, self).__init__(__tmp4, __tmp15)


class Persistance():
    pass


class PersistentActor(Actor):
    @abstractmethod
    def __tmp0(self) :
        raise NotImplementedError('Should implement this method')


class Provider(metaclass=ABCMeta):
    @abstractmethod
    def get_state(self) -> 'ProviderState':
        raise NotImplementedError('Should implement this method')


class __typ1(metaclass=ABCMeta):
    @abstractmethod
    async def get_events(self, __tmp13, index_start: int, __tmp9: Callable[..., None]) :
        raise NotImplementedError('Should implement this method')

    @abstractmethod
    async def get_snapshot(self, __tmp13: str) -> Tuple[Any, int]:
        raise NotImplementedError('Should implement this method')

    @abstractmethod
    async def persist_event(self, __tmp13, __tmp15: int, __tmp5: Any) :
        raise NotImplementedError('Should implement this method')

    @abstractmethod
    async def persist_snapshot(self, __tmp13, __tmp15, __tmp12: Any) -> None:
        raise NotImplementedError('Should implement this method')

    @abstractmethod
    async def delete_events(self, __tmp13, __tmp1, __tmp5: Any) -> None:
        raise NotImplementedError('Should implement this method')

    @abstractmethod
    async def __tmp3(self, __tmp13: str, __tmp1: int, __tmp12: Any) -> None:
        raise NotImplementedError('Should implement this method')


class InMemoryProvider(Provider):
    def get_state(self) :
        return InMemoryProviderState()


class InMemoryProviderState(__typ1):
    def __init__(self) -> None:
        self._events = {}
        self._snapshots = {}

    def __tmp10(self) -> int:
        return 0

    async def get_snapshot(self, __tmp13: str) :
        __tmp12 = self._snapshots.get(__tmp13, None)
        return __tmp12

    async def get_events(self, __tmp13: str, __tmp11, __tmp9: Callable[..., None]) -> None:
        events = self._events.get(__tmp13, None)
        if events is not None:
            for e in events:
                __tmp9(e)

    async def persist_event(self, __tmp13, event_index: int, __tmp5) -> None:
        events = self._events.setdefault(__tmp13, [])
        events.append(__tmp5)

    async def persist_snapshot(self, __tmp13: str, event_index, __tmp12: Any) -> None:
        self._snapshots[__tmp13] = __tmp12, event_index

    async def delete_events(self, __tmp13: <FILL>, __tmp1, __tmp5) -> None:
        self._events.pop(__tmp13)

    async def __tmp3(self, __tmp13: str, __tmp1: int, __tmp12: Any) -> None:
        self._snapshots.pop(__tmp13)
