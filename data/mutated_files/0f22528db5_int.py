from typing import TypeAlias
__typ0 : TypeAlias = "any"
class Snapshot:
    def __init__(__tmp0, state, index: <FILL>):
        __tmp0.state = state
        __tmp0.index = index


class __typ1(Snapshot):
    def __init__(__tmp0, data: __typ0, index: int):
        super().__init__(data, index)


class PersistedSnapshot(Snapshot):
    def __init__(__tmp0, data: __typ0, index):
        super().__init__(data, index)


class __typ4:
    def __init__(__tmp0, data, index: int):
        __tmp0.data = data
        __tmp0.index = index


class __typ2(__typ4):
    def __init__(__tmp0, data, index):
        super().__init__(data, index)


class __typ3(__typ4):
    def __init__(__tmp0, data: __typ0, index: int):
        super().__init__(data, index)


class __typ5(__typ4):
    def __init__(__tmp0, data, index: int):
        super().__init__(data, index)