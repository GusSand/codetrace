from typing import TypeAlias
__typ0 : TypeAlias = "JsonType"
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
        __tmp3,
        gmi,
        group_id,
        nickname: Optional[str] = None,
        user_id: Optional[str] = None,
        phone_number: Optional[str] = None,
        email: Optional[str] = None,
    ) :
        __tmp3.gmi = gmi
        __tmp3.group_id = group_id  # type: ignore
        __tmp3.nickname = nickname  # type: ignore
        __tmp3.user_id = user_id  # type: ignore
        __tmp3.phone_number = phone_number  # type: ignore
        __tmp3.email = email  # type: ignore

    def __tmp1(__tmp3) :
        if __tmp3.member_id is None:
            if __tmp3.user_id is not None:
                MembersAddRequest(
                    __tmp3.gmi, __tmp3.group_id, __tmp3.nickname, user_id=__tmp3.user_id
                )
            elif __tmp3.phone_number is not None:
                MembersAddRequest(
                    __tmp3.gmi,
                    __tmp3.group_id,
                    __tmp3.nickname,
                    phone_number=__tmp3.phone_number,
                )
            elif __tmp3.email is not None:
                MembersAddRequest(
                    __tmp3.gmi, __tmp3.group_id, __tmp3.nickname, email=__tmp3.email
                )
            else:
                raise ValueError(
                    "Please define one of user_id, phone_number, email before saving"
                )
        else:  # Only works for current user
            new_data = MembersUpdateRequest(
                __tmp3.gmi, __tmp3.group_id, __tmp3.nickname
            ).result
            __tmp3._refresh_from_other(new_data)

    def __tmp0(__tmp3) :
        raise InvalidOperationException("Nontrivial to implement")

    @staticmethod
    def __tmp4(gmi, member_id) :  # type: ignore
        raise InvalidOperationException("Nontrivial to implement")

    def __tmp9(__tmp3) :
        return __tmp3.nickname

    def __tmp8(__tmp3) :
        return str(__tmp3)


class MembersAddRequest(Request[str]):
    def __init__(
        __tmp3,
        gmi: "GMI",
        group_id,
        nickname: str,
        user_id: Optional[str] = None,
        phone_number: Optional[str] = None,
        email: Optional[str] = None,
        guid: Optional[str] = None,
    ) :
        __tmp3.group_id = group_id
        __tmp3.nickname = nickname
        __tmp3.guid = guid

        __tmp3.user_id = user_id
        __tmp3.email = email
        __tmp3.phone_number = phone_number

        if user_id is None and email is not None and phone_number is not None:
            raise ValueError("Must provide user_id, email, or phone_number")
        super().__init__(gmi)

    def __tmp6(__tmp3) :
        return __tmp3.base_url + "/groups/" + str(__tmp3.group_id) + "/members/add"

    def __tmp2(__tmp3) :
        add_dict = {"members": [{"nickname": __tmp3.nickname, "user_id": __tmp3.user_id}]}
        return add_dict

    def __tmp5(__tmp3) :
        return "POST"

    def __tmp10(__tmp3, __tmp7) :
        return __tmp7["results_id"]


# Not used
class __typ1(Request[List[Member]]):
    def __init__(__tmp3, gmi, group_id, results_id) :
        __tmp3.group_id = group_id
        __tmp3.results_id = results_id
        super().__init__(gmi)

    def __tmp5(__tmp3) :
        return "GET"

    def __tmp6(__tmp3) :
        return (
            __tmp3.base_url
            + "/groups/"
            + str(__tmp3.group_id)
            + "/members/results/"
            + str(__tmp3.results_id)
        )

    def __tmp10(__tmp3, __tmp7) :
        members = []
        for member_json in __tmp7["members"]:
            members.append(Member.from_json(__tmp3.gmi, member_json, __tmp3.group_id))
        return members


class MembersRemoveRequest(Request[None]):
    def __init__(__tmp3, gmi, group_id: <FILL>, member_id) :
        __tmp3.group_id = group_id
        __tmp3.member_id = member_id
        super().__init__(gmi)

    def __tmp5(__tmp3) -> str:
        return "POST"

    def __tmp6(__tmp3) :
        return (
            __tmp3.base_url
            + "/groups/"
            + str(__tmp3.group_id)
            + "/members/"
            + str(__tmp3.member_id)
            + "/remove"
        )

    def __tmp10(__tmp3, __tmp7) :
        return None


class MembersUpdateRequest(Request[Member]):
    def __init__(__tmp3, gmi, group_id: str, nickname) :
        __tmp3.group_id = group_id
        __tmp3.nickname = nickname
        super().__init__(gmi)

    def __tmp5(__tmp3) :
        return "POST"

    def __tmp6(__tmp3) :
        return __tmp3.base_url + "/groups/" + str(__tmp3.group_id) + "/memberships/update"

    def __tmp2(__tmp3) :
        return {"membership": {"nickname": __tmp3.nickname}}

    def __tmp10(__tmp3, __tmp7) :
        return Member.from_json(__tmp3.gmi, __tmp7, __tmp3.group_id)
