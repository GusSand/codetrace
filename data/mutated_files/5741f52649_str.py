from typing import TypeAlias
__typ3 : TypeAlias = "JsonType"
__typ2 : TypeAlias = "bool"
# pyre-strict
from typing import TYPE_CHECKING, List

from lowerpines.endpoints.object import AbstractObject, Field
from lowerpines.endpoints.request import Request, JsonType

if TYPE_CHECKING:  # pragma: no cover
    from lowerpines.gmi import GMI


class __typ0(AbstractObject):
    user_id: str = Field().with_type(str)
    blocked_user_id: str = Field().with_type(str)

    def __init__(__tmp2, gmi: "GMI") -> None:
        __tmp2.gmi = gmi

    def __tmp6(__tmp2, user_id: str) -> List["Block"]:
        return __typ1(__tmp2.gmi, user_id).result

    @staticmethod
    def block_exists(gmi, user_id, other_user_id: str) -> __typ2:
        return BlockBetweenRequest(gmi, user_id, other_user_id).result

    @staticmethod
    def block(gmi: "GMI", user_id, other_user_id) -> None:
        BlockCreateRequest(gmi, user_id, other_user_id)

    @staticmethod
    def __tmp0(gmi: "GMI", user_id, other_user_id) :
        BlockUnblockRequest(gmi, user_id, other_user_id)


class __typ1(Request[List[__typ0]]):
    def __init__(__tmp2, gmi, user_id) -> None:
        __tmp2.user_id = user_id
        super().__init__(gmi)

    def __tmp3(__tmp2) -> str:
        return "GET"

    def __tmp7(__tmp2, __tmp5: __typ3) -> List[__typ0]:
        blocks = list()
        for block_json in __tmp5["blocks"]:
            blocks.append(__typ0.from_json(__tmp2.gmi, block_json))
        return blocks

    def __tmp1(__tmp2) -> __typ3:
        return {"user": __tmp2.user_id}

    def __tmp4(__tmp2) :
        return __tmp2.base_url + "/blocks"


class BlockBetweenRequest(Request[__typ2]):
    def __init__(__tmp2, gmi, user_id: str, other_user_id: str) :
        __tmp2.user_id = user_id
        __tmp2.other_user_id = other_user_id
        super().__init__(gmi)

    def __tmp3(__tmp2) -> str:
        return "GET"

    def __tmp7(__tmp2, __tmp5: __typ3) :
        return __tmp5["between"]

    def __tmp1(__tmp2) -> __typ3:
        return {"user": __tmp2.user_id, "otherUser": __tmp2.other_user_id}

    def __tmp4(__tmp2) :
        return __tmp2.base_url + "/blocks/between"


class BlockCreateRequest(Request[None]):
    def __init__(__tmp2, gmi, user_id: str, other_user_id: <FILL>) :
        __tmp2.user_id = user_id
        __tmp2.other_user_id = other_user_id
        super().__init__(gmi)

    def __tmp3(__tmp2) -> str:
        return "POST"

    def __tmp7(__tmp2, __tmp5: __typ3) -> None:
        return None

    def __tmp1(__tmp2) :
        return {}

    def __tmp4(__tmp2) -> str:
        return (
            __tmp2.base_url
            + "/blocks?user="
            + __tmp2.user_id
            + "&otherUser="
            + __tmp2.other_user_id
        )


class BlockUnblockRequest(Request[None]):
    def __init__(__tmp2, gmi: "GMI", user_id: str, other_user_id: str) :
        __tmp2.user_id = user_id
        __tmp2.other_user_id = other_user_id
        super().__init__(gmi)

    def __tmp3(__tmp2) :
        return "POST"

    def __tmp7(__tmp2, __tmp5) :
        return None

    def __tmp1(__tmp2) :
        return {}

    def __tmp4(__tmp2) -> str:
        return (
            __tmp2.base_url
            + "/blocks/delete"
            + "/blocks?user="
            + __tmp2.user_id
            + "&otherUser="
            + __tmp2.other_user_id
        )
