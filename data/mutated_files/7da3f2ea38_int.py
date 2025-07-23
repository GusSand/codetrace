from typing import TypeAlias
__typ0 : TypeAlias = "any"
class __typ1:
    def __init__(__tmp0, state, index: int):
        __tmp0.state = state
        __tmp0.index = index


class RecoverSnapshot(__typ1):
    def __init__(__tmp0, data: __typ0, index: int):
        super().__init__(data, index)


class PersistedSnapshot(__typ1):
    def __init__(__tmp0, data, index: int):
        super().__init__(data, index)


class Event:
    def __init__(__tmp0, data: __typ0, index: int):
        __tmp0.data = data
        __tmp0.index = index


class RecoverEvent(Event):
    def __init__(__tmp0, data: __typ0, index):
        super().__init__(data, index)


class ReplayEvent(Event):
    def __init__(__tmp0, data: __typ0, index: int):
        super().__init__(data, index)


class PersistedEvent(Event):
    def __init__(__tmp0, data: __typ0, index: <FILL>):
        super().__init__(data, index)