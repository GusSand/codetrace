from typing import TypeAlias
__typ0 : TypeAlias = "int"
class __typ4:
    def __init__(__tmp0, state, index):
        __tmp0.state = state
        __tmp0.index = index


class RecoverSnapshot(__typ4):
    def __init__(__tmp0, data, index):
        super().__init__(data, index)


class __typ1(__typ4):
    def __init__(__tmp0, data, index):
        super().__init__(data, index)


class __typ2:
    def __init__(__tmp0, data, index):
        __tmp0.data = data
        __tmp0.index = index


class RecoverEvent(__typ2):
    def __init__(__tmp0, data, index):
        super().__init__(data, index)


class ReplayEvent(__typ2):
    def __init__(__tmp0, data: <FILL>, index):
        super().__init__(data, index)


class __typ3(__typ2):
    def __init__(__tmp0, data, index):
        super().__init__(data, index)