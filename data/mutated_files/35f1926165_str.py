from typing import TypeAlias
__typ1 : TypeAlias = "JsonType"
__typ4 : TypeAlias = "bool"
# pyre-strict
from typing import TYPE_CHECKING, List

from lowerpines.endpoints.object import AbstractObject, Field
from lowerpines.endpoints.request import Request, JsonType

if TYPE_CHECKING:  # pragma: no cover
    from lowerpines.gmi import GMI


class __typ5(AbstractObject):
    user_id: str = Field().with_type(str)
    blocked_user_id: str = Field().with_type(str)

    def __init__(__tmp1, gmi: "GMI") :
        __tmp1.gmi = gmi

    def __tmp6(__tmp1, user_id: str) :
        return __typ0(__tmp1.gmi, user_id).result

    @staticmethod
    def block_exists(gmi, user_id: str, other_user_id: <FILL>) -> __typ4:
        return __typ6(gmi, user_id, other_user_id).result

    @staticmethod
    def __tmp2(gmi: "GMI", user_id: str, other_user_id: str) -> None:
        __typ3(gmi, user_id, other_user_id)

    @staticmethod
    def unblock(gmi, user_id: str, other_user_id: str) :
        __typ2(gmi, user_id, other_user_id)


class __typ0(Request[List[__typ5]]):
    def __init__(__tmp1, gmi: "GMI", user_id: str) :
        __tmp1.user_id = user_id
        super().__init__(gmi)

    def __tmp3(__tmp1) -> str:
        return "GET"

    def __tmp7(__tmp1, __tmp5: __typ1) -> List[__typ5]:
        blocks = list()
        for block_json in __tmp5["blocks"]:
            blocks.append(__typ5.from_json(__tmp1.gmi, block_json))
        return blocks

    def __tmp0(__tmp1) :
        return {"user": __tmp1.user_id}

    def __tmp4(__tmp1) -> str:
        return __tmp1.base_url + "/blocks"


class __typ6(Request[__typ4]):
    def __init__(__tmp1, gmi: "GMI", user_id: str, other_user_id: str) -> None:
        __tmp1.user_id = user_id
        __tmp1.other_user_id = other_user_id
        super().__init__(gmi)

    def __tmp3(__tmp1) -> str:
        return "GET"

    def __tmp7(__tmp1, __tmp5: __typ1) -> __typ4:
        return __tmp5["between"]

    def __tmp0(__tmp1) -> __typ1:
        return {"user": __tmp1.user_id, "otherUser": __tmp1.other_user_id}

    def __tmp4(__tmp1) -> str:
        return __tmp1.base_url + "/blocks/between"


class __typ3(Request[None]):
    def __init__(__tmp1, gmi, user_id, other_user_id) :
        __tmp1.user_id = user_id
        __tmp1.other_user_id = other_user_id
        super().__init__(gmi)

    def __tmp3(__tmp1) -> str:
        return "POST"

    def __tmp7(__tmp1, __tmp5: __typ1) -> None:
        return None

    def __tmp0(__tmp1) -> __typ1:
        return {}

    def __tmp4(__tmp1) -> str:
        return (
            __tmp1.base_url
            + "/blocks?user="
            + __tmp1.user_id
            + "&otherUser="
            + __tmp1.other_user_id
        )


class __typ2(Request[None]):
    def __init__(__tmp1, gmi, user_id, other_user_id: str) -> None:
        __tmp1.user_id = user_id
        __tmp1.other_user_id = other_user_id
        super().__init__(gmi)

    def __tmp3(__tmp1) -> str:
        return "POST"

    def __tmp7(__tmp1, __tmp5: __typ1) -> None:
        return None

    def __tmp0(__tmp1) -> __typ1:
        return {}

    def __tmp4(__tmp1) :
        return (
            __tmp1.base_url
            + "/blocks/delete"
            + "/blocks?user="
            + __tmp1.user_id
            + "&otherUser="
            + __tmp1.other_user_id
        )
