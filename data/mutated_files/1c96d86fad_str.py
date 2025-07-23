from typing import TypeAlias
__typ0 : TypeAlias = "Any"
from typing import Any

class BaseParser:
    def __tmp2(__tmp1, __tmp0: <FILL>) -> None:
        # We import BeautifulSoup here, because it's not used by most
        # processes in production, and bs4 is big enough that
        # importing it adds 10s of milliseconds to manage.py startup.
        from bs4 import BeautifulSoup
        __tmp1._soup = BeautifulSoup(__tmp0, "lxml")

    def __tmp3(__tmp1) :
        raise NotImplementedError()
