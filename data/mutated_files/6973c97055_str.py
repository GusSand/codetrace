from typing import TypeAlias
__typ3 : TypeAlias = "int"
__typ1 : TypeAlias = "GMI"
# pyre-strict

from typing import Any, Dict, Optional

from lowerpines.gmi import GMI
from lowerpines.endpoints.request import Request, JsonType


class __typ2(Request[None]):
    def __init__(__tmp1, gmi: __typ1, duration: __typ3, registration_id: <FILL>) -> None:
        if duration > 48:
            raise ValueError(
                "Cannot have a duration of SMS mode for more than 48 hours"
            )
        __tmp1.duration = duration
        __tmp1.registration_id = registration_id
        super().__init__(gmi)

    def __tmp2(__tmp1) -> str:
        return "POST"

    def __tmp5(__tmp1, __tmp4: Optional[JsonType]) :
        return None

    def __tmp0(__tmp1) :
        return {"duration": __tmp1.duration, "registration_id": __tmp1.registration_id}

    def __tmp3(__tmp1) -> str:
        return __tmp1.base_url + "/users/sms_mode"


class __typ0(Request[None]):
    def __tmp2(__tmp1) -> str:
        return "POST"

    def __tmp5(__tmp1, __tmp4: Optional[JsonType]) -> None:
        return None

    def __tmp3(__tmp1) -> str:
        return __tmp1.base_url + "/users/sms_mode/delete"
