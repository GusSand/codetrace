from typing import TypeAlias
__typ0 : TypeAlias = "int"
# pyre-strict
from typing import Optional, TYPE_CHECKING

from lowerpines.endpoints.object import AbstractObject, Field, RetrievableObject
from lowerpines.endpoints.request import Request, JsonType
from lowerpines.endpoints.sms import SmsCreateRequest, SmsDeleteRequest

if TYPE_CHECKING:  # pragma: no cover
    from lowerpines.gmi import GMI


class User(AbstractObject, RetrievableObject):
    user_id: str = Field().with_type(str)
    phone_number: str = Field().with_type(str)
    image_url: str = Field().with_type(str)
    name: str = Field().with_type(str)
    created_at: __typ0 = Field().with_type(__typ0)
    updated_at: __typ0 = Field().with_type(__typ0)
    email: str = Field().with_type(str)
    sms: bool = Field().with_type(bool)

    def __init__(self, gmi: "GMI") -> None:
        self.gmi = gmi

    def save(self) -> None:
        new_data = UserUpdateRequest(
            self.gmi, self.image_url, self.name, self.email
        ).result
        self._refresh_from_other(new_data)

    def refresh(self) -> None:
        new_data = __typ1(self.gmi).result
        self._refresh_from_other(new_data)

    @classmethod
    def get(cls, gmi: "GMI") -> "User":  # type: ignore
        user = cls(gmi)
        user.refresh()
        return user

    def __tmp1(self, duration: __typ0, registration_id: <FILL>) -> None:
        SmsCreateRequest(self.gmi, duration, registration_id)

    def disable_sms(self) :
        SmsDeleteRequest(self.gmi)


class __typ1(Request[User]):
    def __tmp0(self) -> str:
        return "GET"

    def parse(self, response: JsonType) -> User:
        return User.from_json(self.gmi, response)

    def url(self) -> str:
        return self.base_url + "/users/me"


class UserUpdateRequest(Request[User]):
    def __init__(
        self,
        gmi: "GMI",
        avatar_url: Optional[str] = None,
        name: Optional[str] = None,
        email: Optional[str] = None,
        zip_code: Optional[str] = None,
    ) -> None:
        self.avatar_url = avatar_url
        self.name = name
        self.email = email
        self.zip_code = zip_code
        super().__init__(gmi)

    def __tmp0(self) -> str:
        return "POST"

    def parse(self, response: JsonType) :
        return User.from_json(self.gmi, response)

    def url(self) -> str:
        return self.base_url + "/users/update"

    def args(self) -> JsonType:
        arg_dict = dict()

        if self.avatar_url:
            arg_dict["avatar_url"] = self.avatar_url
        if self.name:
            arg_dict["name"] = self.name
        if self.email:
            arg_dict["email"] = self.email
        if self.zip_code:
            arg_dict["zip_code"] = self.zip_code

        return arg_dict
