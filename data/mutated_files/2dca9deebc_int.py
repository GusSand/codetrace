class Snapshot:
    def __init__(__tmp0, state, index: int):
        __tmp0.state = state
        __tmp0.index = index


class RecoverSnapshot(Snapshot):
    def __init__(__tmp0, data, index: <FILL>):
        super().__init__(data, index)


class __typ0(Snapshot):
    def __init__(__tmp0, data, index: int):
        super().__init__(data, index)


class Event:
    def __init__(__tmp0, data: any, index):
        __tmp0.data = data
        __tmp0.index = index


class RecoverEvent(Event):
    def __init__(__tmp0, data, index):
        super().__init__(data, index)


class ReplayEvent(Event):
    def __init__(__tmp0, data: any, index):
        super().__init__(data, index)


class PersistedEvent(Event):
    def __init__(__tmp0, data: any, index):
        super().__init__(data, index)