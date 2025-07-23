from typing import TypeAlias
__typ2 : TypeAlias = "int"
class Snapshot:
    def __init__(__tmp0, state: any, index: __typ2):
        __tmp0.state = state
        __tmp0.index = index


class __typ3(Snapshot):
    def __init__(__tmp0, data, index):
        super().__init__(data, index)


class __typ1(Snapshot):
    def __init__(__tmp0, data, index):
        super().__init__(data, index)


class __typ0:
    def __init__(__tmp0, data: <FILL>, index):
        __tmp0.data = data
        __tmp0.index = index


class RecoverEvent(__typ0):
    def __init__(__tmp0, data: any, index):
        super().__init__(data, index)


class ReplayEvent(__typ0):
    def __init__(__tmp0, data, index):
        super().__init__(data, index)


class PersistedEvent(__typ0):
    def __init__(__tmp0, data, index):
        super().__init__(data, index)