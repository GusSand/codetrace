from typing import TypeAlias
__typ1 : TypeAlias = "any"
class Snapshot:
    def __init__(self, state: __typ1, index: int):
        self.state = state
        self.index = index


class __typ3(Snapshot):
    def __init__(self, data, index):
        super().__init__(data, index)


class PersistedSnapshot(Snapshot):
    def __init__(self, data, index):
        super().__init__(data, index)


class __typ0:
    def __init__(self, data, index: <FILL>):
        self.data = data
        self.index = index


class RecoverEvent(__typ0):
    def __init__(self, data: __typ1, index: int):
        super().__init__(data, index)


class ReplayEvent(__typ0):
    def __init__(self, data, index: int):
        super().__init__(data, index)


class __typ2(__typ0):
    def __init__(self, data: __typ1, index):
        super().__init__(data, index)