from typing import TypeAlias
__typ0 : TypeAlias = "JsonType"
__typ1 : TypeAlias = "str"
# pyre-strict
from typing import Optional, TYPE_CHECKING

from lowerpines.endpoints.object import AbstractObject, Field, RetrievableObject
from lowerpines.endpoints.request import Request, JsonType
from lowerpines.endpoints.sms import SmsCreateRequest, SmsDeleteRequest

if TYPE_CHECKING:  # pragma: no cover
    from lowerpines.gmi import GMI


class __typ2(AbstractObject, RetrievableObject):
    user_id: __typ1 = Field().with_type(__typ1)
    phone_number: __typ1 = Field().with_type(__typ1)
    image_url: __typ1 = Field().with_type(__typ1)
    name: __typ1 = Field().with_type(__typ1)
    created_at: int = Field().with_type(int)
    updated_at: int = Field().with_type(int)
    email: __typ1 = Field().with_type(__typ1)
    sms: bool = Field().with_type(bool)

    def __init__(__tmp0, gmi) -> None:
        __tmp0.gmi = gmi

    def save(__tmp0) :
        new_data = __typ3(
            __tmp0.gmi, __tmp0.image_url, __tmp0.name, __tmp0.email
        ).result
        __tmp0._refresh_from_other(new_data)

    def refresh(__tmp0) :
        new_data = __typ4(__tmp0.gmi).result
        __tmp0._refresh_from_other(new_data)

    @classmethod
    def get(cls, gmi: "GMI") :  # type: ignore
        user = cls(gmi)
        user.refresh()
        return user

    def enable_sms(__tmp0, duration: <FILL>, registration_id: __typ1) -> None:
        SmsCreateRequest(__tmp0.gmi, duration, registration_id)

    def disable_sms(__tmp0) :
        SmsDeleteRequest(__tmp0.gmi)


class __typ4(Request[__typ2]):
    def mode(__tmp0) -> __typ1:
        return "GET"

    def parse(__tmp0, response: __typ0) :
        return __typ2.from_json(__tmp0.gmi, response)

    def __tmp1(__tmp0) :
        return __tmp0.base_url + "/users/me"


class __typ3(Request[__typ2]):
    def __init__(
        __tmp0,
        gmi: "GMI",
        avatar_url: Optional[__typ1] = None,
        name: Optional[__typ1] = None,
        email: Optional[__typ1] = None,
        zip_code: Optional[__typ1] = None,
    ) :
        __tmp0.avatar_url = avatar_url
        __tmp0.name = name
        __tmp0.email = email
        __tmp0.zip_code = zip_code
        super().__init__(gmi)

    def mode(__tmp0) :
        return "POST"

    def parse(__tmp0, response: __typ0) :
        return __typ2.from_json(__tmp0.gmi, response)

    def __tmp1(__tmp0) -> __typ1:
        return __tmp0.base_url + "/users/update"

    def args(__tmp0) -> __typ0:
        arg_dict = dict()

        if __tmp0.avatar_url:
            arg_dict["avatar_url"] = __tmp0.avatar_url
        if __tmp0.name:
            arg_dict["name"] = __tmp0.name
        if __tmp0.email:
            arg_dict["email"] = __tmp0.email
        if __tmp0.zip_code:
            arg_dict["zip_code"] = __tmp0.zip_code

        return arg_dict
