from typing import TypeAlias
__typ0 : TypeAlias = "any"
class Snapshot:
    def __init__(__tmp0, state, index):
        __tmp0.state = state
        __tmp0.index = index


class RecoverSnapshot(Snapshot):
    def __init__(__tmp0, data: __typ0, index):
        super().__init__(data, index)


class PersistedSnapshot(Snapshot):
    def __init__(__tmp0, data, index):
        super().__init__(data, index)


class Event:
    def __init__(__tmp0, data, index):
        __tmp0.data = data
        __tmp0.index = index


class RecoverEvent(Event):
    def __init__(__tmp0, data: __typ0, index: <FILL>):
        super().__init__(data, index)


class ReplayEvent(Event):
    def __init__(__tmp0, data: __typ0, index: int):
        super().__init__(data, index)


class PersistedEvent(Event):
    def __init__(__tmp0, data, index):
        super().__init__(data, index)