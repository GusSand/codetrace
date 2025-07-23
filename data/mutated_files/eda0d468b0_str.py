from typing import TypeAlias
__typ3 : TypeAlias = "JsonType"
# pyre-strict
from typing import TYPE_CHECKING, List

from lowerpines.endpoints.object import AbstractObject, Field
from lowerpines.endpoints.request import Request, JsonType

if TYPE_CHECKING:  # pragma: no cover
    from lowerpines.gmi import GMI


class __typ0(AbstractObject):
    user_id: str = Field().with_type(str)
    blocked_user_id: str = Field().with_type(str)

    def __init__(__tmp1, gmi: "GMI") -> None:
        __tmp1.gmi = gmi

    def __tmp5(__tmp1, user_id) :
        return BlockIndexRequest(__tmp1.gmi, user_id).result

    @staticmethod
    def block_exists(gmi: "GMI", user_id: str, other_user_id) -> bool:
        return __typ1(gmi, user_id, other_user_id).result

    @staticmethod
    def __tmp2(gmi: "GMI", user_id: str, other_user_id: str) :
        BlockCreateRequest(gmi, user_id, other_user_id)

    @staticmethod
    def unblock(gmi: "GMI", user_id: str, other_user_id: str) -> None:
        __typ2(gmi, user_id, other_user_id)


class BlockIndexRequest(Request[List[__typ0]]):
    def __init__(__tmp1, gmi: "GMI", user_id: <FILL>) -> None:
        __tmp1.user_id = user_id
        super().__init__(gmi)

    def mode(__tmp1) -> str:
        return "GET"

    def __tmp6(__tmp1, __tmp4) :
        blocks = list()
        for block_json in __tmp4["blocks"]:
            blocks.append(__typ0.from_json(__tmp1.gmi, block_json))
        return blocks

    def __tmp0(__tmp1) -> __typ3:
        return {"user": __tmp1.user_id}

    def __tmp3(__tmp1) -> str:
        return __tmp1.base_url + "/blocks"


class __typ1(Request[bool]):
    def __init__(__tmp1, gmi: "GMI", user_id, other_user_id: str) -> None:
        __tmp1.user_id = user_id
        __tmp1.other_user_id = other_user_id
        super().__init__(gmi)

    def mode(__tmp1) -> str:
        return "GET"

    def __tmp6(__tmp1, __tmp4: __typ3) -> bool:
        return __tmp4["between"]

    def __tmp0(__tmp1) -> __typ3:
        return {"user": __tmp1.user_id, "otherUser": __tmp1.other_user_id}

    def __tmp3(__tmp1) -> str:
        return __tmp1.base_url + "/blocks/between"


class BlockCreateRequest(Request[None]):
    def __init__(__tmp1, gmi: "GMI", user_id: str, other_user_id) -> None:
        __tmp1.user_id = user_id
        __tmp1.other_user_id = other_user_id
        super().__init__(gmi)

    def mode(__tmp1) -> str:
        return "POST"

    def __tmp6(__tmp1, __tmp4: __typ3) -> None:
        return None

    def __tmp0(__tmp1) -> __typ3:
        return {}

    def __tmp3(__tmp1) -> str:
        return (
            __tmp1.base_url
            + "/blocks?user="
            + __tmp1.user_id
            + "&otherUser="
            + __tmp1.other_user_id
        )


class __typ2(Request[None]):
    def __init__(__tmp1, gmi: "GMI", user_id: str, other_user_id: str) -> None:
        __tmp1.user_id = user_id
        __tmp1.other_user_id = other_user_id
        super().__init__(gmi)

    def mode(__tmp1) -> str:
        return "POST"

    def __tmp6(__tmp1, __tmp4: __typ3) -> None:
        return None

    def __tmp0(__tmp1) -> __typ3:
        return {}

    def __tmp3(__tmp1) -> str:
        return (
            __tmp1.base_url
            + "/blocks/delete"
            + "/blocks?user="
            + __tmp1.user_id
            + "&otherUser="
            + __tmp1.other_user_id
        )
