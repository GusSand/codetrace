# pyre-strict
from requests import Response
from typing import TYPE_CHECKING

from lowerpines.endpoints.request import Request, JsonType

if TYPE_CHECKING:  # pragma: no cover
    from lowerpines.gmi import GMI


class ImageConvertRequest(Request[str]):
    def __init__(__tmp2, gmi, data: <FILL>) -> None:
        __tmp2.data = data
        super().__init__(gmi)

    def __tmp4(__tmp2) -> str:
        return "https://image.groupme.com/pictures"

    def __tmp3(__tmp2) :
        return "POST_RAW"

    def __tmp1(__tmp2) :
        return __tmp2.data

    def __tmp6(__tmp2, __tmp5) :
        return __tmp5["payload"]["url"]

    def __tmp0(__tmp2, __tmp5) :
        return __tmp5.json()
