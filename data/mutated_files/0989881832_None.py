from typing import TypeAlias
__typ0 : TypeAlias = "Path"
from ...types import Path
from .base_handler import BaseHandler


class NoneHandler(BaseHandler[None, None, None]):

    def simplify(__tmp1, __tmp0, value: None) :
        return None

    def realify(__tmp1, __tmp0, value: <FILL>) -> None:
        return None
