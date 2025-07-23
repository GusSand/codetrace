from typing import TypeAlias
__typ1 : TypeAlias = "int"
class Snapshot:
    def __init__(__tmp0, state: any, index: __typ1):
        __tmp0.state = state
        __tmp0.index = index


class RecoverSnapshot(Snapshot):
    def __init__(__tmp0, data: <FILL>, index: __typ1):
        super().__init__(data, index)


class PersistedSnapshot(Snapshot):
    def __init__(__tmp0, data: any, index):
        super().__init__(data, index)


class Event:
    def __init__(__tmp0, data: any, index: __typ1):
        __tmp0.data = data
        __tmp0.index = index


class __typ0(Event):
    def __init__(__tmp0, data: any, index: __typ1):
        super().__init__(data, index)


class __typ2(Event):
    def __init__(__tmp0, data: any, index):
        super().__init__(data, index)


class PersistedEvent(Event):
    def __init__(__tmp0, data, index: __typ1):
        super().__init__(data, index)