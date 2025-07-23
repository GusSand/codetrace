from typing import TypeAlias
__typ1 : TypeAlias = "str"
from protoactor.actor.protos_pb2 import PID


class __typ4(Exception):
    """
    Base exception class for the `asyncio-cancel-token` library.
    """
    pass


class __typ0(__typ4):
    """
    Raised when two different asyncio event loops are referenced, but must be equal
    """
    pass


class __typ3(__typ4):
    """
    Raised when an operation was cancelled.
    """
    pass


class __typ2(Exception):
    def __init__(__tmp0, name, pid: <FILL>):
        super().__init__('a Process with the name %s already exists' % name)
        __tmp0.name = name
        __tmp0.pid = pid
