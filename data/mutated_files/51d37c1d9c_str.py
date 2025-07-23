# pyre-strict
from typing import TYPE_CHECKING, List, Optional

from lowerpines.endpoints.object import AbstractObject, Field, RetrievableObject
from lowerpines.endpoints.request import Request, JsonType
from lowerpines.exceptions import InvalidOperationException

if TYPE_CHECKING:  # pragma: no cover
    from lowerpines.gmi import GMI


class Member(AbstractObject, RetrievableObject):
    member_id: str = Field().with_api_name("id").with_type(str)
    user_id: str = Field().with_type(str)
    nickname: str = Field().with_type(str)
    muted: bool = Field().with_type(bool)
    image_url: Optional[str] = Field().with_type(str)
    autokicked: bool = Field().with_type(bool)
    app_installed: bool = Field().with_type(bool)
    guid: str = Field().with_type(str)
    phone_number: str = Field().with_type(str)
    email: str = Field().with_type(str)

    def __init__(
        __tmp1,
        gmi: "GMI",
        group_id: <FILL>,
        nickname: Optional[str] = None,
        user_id: Optional[str] = None,
        phone_number: Optional[str] = None,
        email: Optional[str] = None,
    ) :
        __tmp1.gmi = gmi
        __tmp1.group_id = group_id  # type: ignore
        __tmp1.nickname = nickname  # type: ignore
        __tmp1.user_id = user_id  # type: ignore
        __tmp1.phone_number = phone_number  # type: ignore
        __tmp1.email = email  # type: ignore

    def save(__tmp1) :
        if __tmp1.member_id is None:
            if __tmp1.user_id is not None:
                __typ0(
                    __tmp1.gmi, __tmp1.group_id, __tmp1.nickname, user_id=__tmp1.user_id
                )
            elif __tmp1.phone_number is not None:
                __typ0(
                    __tmp1.gmi,
                    __tmp1.group_id,
                    __tmp1.nickname,
                    phone_number=__tmp1.phone_number,
                )
            elif __tmp1.email is not None:
                __typ0(
                    __tmp1.gmi, __tmp1.group_id, __tmp1.nickname, email=__tmp1.email
                )
            else:
                raise ValueError(
                    "Please define one of user_id, phone_number, email before saving"
                )
        else:  # Only works for current user
            new_data = __typ1(
                __tmp1.gmi, __tmp1.group_id, __tmp1.nickname
            ).result
            __tmp1._refresh_from_other(new_data)

    def __tmp0(__tmp1) :
        raise InvalidOperationException("Nontrivial to implement")

    @staticmethod
    def get(gmi: "GMI", member_id) :  # type: ignore
        raise InvalidOperationException("Nontrivial to implement")

    def __str__(__tmp1) :
        return __tmp1.nickname

    def __repr__(__tmp1) :
        return str(__tmp1)


class __typ0(Request[str]):
    def __init__(
        __tmp1,
        gmi: "GMI",
        group_id: str,
        nickname,
        user_id: Optional[str] = None,
        phone_number: Optional[str] = None,
        email: Optional[str] = None,
        guid: Optional[str] = None,
    ) :
        __tmp1.group_id = group_id
        __tmp1.nickname = nickname
        __tmp1.guid = guid

        __tmp1.user_id = user_id
        __tmp1.email = email
        __tmp1.phone_number = phone_number

        if user_id is None and email is not None and phone_number is not None:
            raise ValueError("Must provide user_id, email, or phone_number")
        super().__init__(gmi)

    def __tmp3(__tmp1) :
        return __tmp1.base_url + "/groups/" + str(__tmp1.group_id) + "/members/add"

    def args(__tmp1) -> JsonType:
        add_dict = {"members": [{"nickname": __tmp1.nickname, "user_id": __tmp1.user_id}]}
        return add_dict

    def __tmp2(__tmp1) :
        return "POST"

    def parse(__tmp1, __tmp4) :
        return __tmp4["results_id"]


# Not used
class MembersResultsRequest(Request[List[Member]]):
    def __init__(__tmp1, gmi, group_id, results_id: str) -> None:
        __tmp1.group_id = group_id
        __tmp1.results_id = results_id
        super().__init__(gmi)

    def __tmp2(__tmp1) :
        return "GET"

    def __tmp3(__tmp1) :
        return (
            __tmp1.base_url
            + "/groups/"
            + str(__tmp1.group_id)
            + "/members/results/"
            + str(__tmp1.results_id)
        )

    def parse(__tmp1, __tmp4: JsonType) :
        members = []
        for member_json in __tmp4["members"]:
            members.append(Member.from_json(__tmp1.gmi, member_json, __tmp1.group_id))
        return members


class MembersRemoveRequest(Request[None]):
    def __init__(__tmp1, gmi, group_id, member_id: str) :
        __tmp1.group_id = group_id
        __tmp1.member_id = member_id
        super().__init__(gmi)

    def __tmp2(__tmp1) :
        return "POST"

    def __tmp3(__tmp1) -> str:
        return (
            __tmp1.base_url
            + "/groups/"
            + str(__tmp1.group_id)
            + "/members/"
            + str(__tmp1.member_id)
            + "/remove"
        )

    def parse(__tmp1, __tmp4) -> None:
        return None


class __typ1(Request[Member]):
    def __init__(__tmp1, gmi, group_id, nickname) :
        __tmp1.group_id = group_id
        __tmp1.nickname = nickname
        super().__init__(gmi)

    def __tmp2(__tmp1) :
        return "POST"

    def __tmp3(__tmp1) :
        return __tmp1.base_url + "/groups/" + str(__tmp1.group_id) + "/memberships/update"

    def args(__tmp1) -> JsonType:
        return {"membership": {"nickname": __tmp1.nickname}}

    def parse(__tmp1, __tmp4: JsonType) :
        return Member.from_json(__tmp1.gmi, __tmp4, __tmp1.group_id)
