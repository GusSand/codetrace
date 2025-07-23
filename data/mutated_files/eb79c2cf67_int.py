from typing import TypeAlias
__typ2 : TypeAlias = "str"
__typ1 : TypeAlias = "GMI"
# pyre-strict

from typing import Any, Dict, Optional

from lowerpines.gmi import GMI
from lowerpines.endpoints.request import Request, JsonType


class SmsCreateRequest(Request[None]):
    def __init__(__tmp0, gmi, duration: <FILL>, registration_id) :
        if duration > 48:
            raise ValueError(
                "Cannot have a duration of SMS mode for more than 48 hours"
            )
        __tmp0.duration = duration
        __tmp0.registration_id = registration_id
        super().__init__(gmi)

    def __tmp1(__tmp0) -> __typ2:
        return "POST"

    def __tmp3(__tmp0, __tmp2) :
        return None

    def args(__tmp0) :
        return {"duration": __tmp0.duration, "registration_id": __tmp0.registration_id}

    def url(__tmp0) :
        return __tmp0.base_url + "/users/sms_mode"


class __typ0(Request[None]):
    def __tmp1(__tmp0) :
        return "POST"

    def __tmp3(__tmp0, __tmp2) :
        return None

    def url(__tmp0) :
        return __tmp0.base_url + "/users/sms_mode/delete"
