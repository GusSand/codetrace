from typing import TypeAlias
__typ0 : TypeAlias = "any"
class __typ4:
    def __init__(__tmp0, state: __typ0, index: int):
        __tmp0.state = state
        __tmp0.index = index


class __typ1(__typ4):
    def __init__(__tmp0, data: __typ0, index: int):
        super().__init__(data, index)


class PersistedSnapshot(__typ4):
    def __init__(__tmp0, data: __typ0, index: <FILL>):
        super().__init__(data, index)


class __typ3:
    def __init__(__tmp0, data, index: int):
        __tmp0.data = data
        __tmp0.index = index


class RecoverEvent(__typ3):
    def __init__(__tmp0, data: __typ0, index: int):
        super().__init__(data, index)


class __typ2(__typ3):
    def __init__(__tmp0, data: __typ0, index: int):
        super().__init__(data, index)


class PersistedEvent(__typ3):
    def __init__(__tmp0, data: __typ0, index: int):
        super().__init__(data, index)