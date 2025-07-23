from typing import TypeAlias
__typ0 : TypeAlias = "int"
class __typ5:
    def __init__(__tmp0, state: any, index: __typ0):
        __tmp0.state = state
        __tmp0.index = index


class RecoverSnapshot(__typ5):
    def __init__(__tmp0, data, index: __typ0):
        super().__init__(data, index)


class __typ1(__typ5):
    def __init__(__tmp0, data: <FILL>, index: __typ0):
        super().__init__(data, index)


class Event:
    def __init__(__tmp0, data: any, index: __typ0):
        __tmp0.data = data
        __tmp0.index = index


class __typ2(Event):
    def __init__(__tmp0, data: any, index: __typ0):
        super().__init__(data, index)


class __typ3(Event):
    def __init__(__tmp0, data, index):
        super().__init__(data, index)


class __typ4(Event):
    def __init__(__tmp0, data: any, index):
        super().__init__(data, index)