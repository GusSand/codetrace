from typing import TypeAlias
__typ3 : TypeAlias = "JsonType"
__typ2 : TypeAlias = "bytes"
__typ1 : TypeAlias = "str"
# pyre-strict
from requests import Response
from typing import TYPE_CHECKING

from lowerpines.endpoints.request import Request, JsonType

if TYPE_CHECKING:  # pragma: no cover
    from lowerpines.gmi import GMI


class __typ0(Request[__typ1]):
    def __init__(self, gmi, data) :
        self.data = data
        super().__init__(gmi)

    def __tmp1(self) -> __typ1:
        return "https://image.groupme.com/pictures"

    def mode(self) :
        return "POST_RAW"

    def args(self) :
        return self.data

    def parse(self, __tmp2) :
        return __tmp2["payload"]["url"]

    def __tmp0(self, __tmp2: <FILL>) :
        return __tmp2.json()
