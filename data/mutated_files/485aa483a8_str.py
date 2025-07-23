from typing import TypeAlias
__typ0 : TypeAlias = "JsonType"
# pyre-strict
from typing import TYPE_CHECKING, List

from lowerpines.endpoints.object import AbstractObject, Field
from lowerpines.endpoints.request import Request, JsonType

if TYPE_CHECKING:  # pragma: no cover
    from lowerpines.gmi import GMI


class Block(AbstractObject):
    user_id: str = Field().with_type(str)
    blocked_user_id: str = Field().with_type(str)

    def __init__(__tmp1, gmi) :
        __tmp1.gmi = gmi

    def get_all(__tmp1, user_id) :
        return BlockIndexRequest(__tmp1.gmi, user_id).result

    @staticmethod
    def block_exists(gmi, user_id, other_user_id: str) -> bool:
        return BlockBetweenRequest(gmi, user_id, other_user_id).result

    @staticmethod
    def block(gmi, user_id: str, other_user_id) :
        BlockCreateRequest(gmi, user_id, other_user_id)

    @staticmethod
    def __tmp0(gmi, user_id, other_user_id) :
        BlockUnblockRequest(gmi, user_id, other_user_id)


class BlockIndexRequest(Request[List[Block]]):
    def __init__(__tmp1, gmi, user_id) :
        __tmp1.user_id = user_id
        super().__init__(gmi)

    def __tmp2(__tmp1) :
        return "GET"

    def __tmp5(__tmp1, __tmp4) :
        blocks = list()
        for block_json in __tmp4["blocks"]:
            blocks.append(Block.from_json(__tmp1.gmi, block_json))
        return blocks

    def args(__tmp1) :
        return {"user": __tmp1.user_id}

    def __tmp3(__tmp1) :
        return __tmp1.base_url + "/blocks"


class BlockBetweenRequest(Request[bool]):
    def __init__(__tmp1, gmi, user_id, other_user_id: <FILL>) :
        __tmp1.user_id = user_id
        __tmp1.other_user_id = other_user_id
        super().__init__(gmi)

    def __tmp2(__tmp1) :
        return "GET"

    def __tmp5(__tmp1, __tmp4) :
        return __tmp4["between"]

    def args(__tmp1) :
        return {"user": __tmp1.user_id, "otherUser": __tmp1.other_user_id}

    def __tmp3(__tmp1) -> str:
        return __tmp1.base_url + "/blocks/between"


class BlockCreateRequest(Request[None]):
    def __init__(__tmp1, gmi, user_id, other_user_id) :
        __tmp1.user_id = user_id
        __tmp1.other_user_id = other_user_id
        super().__init__(gmi)

    def __tmp2(__tmp1) -> str:
        return "POST"

    def __tmp5(__tmp1, __tmp4) -> None:
        return None

    def args(__tmp1) :
        return {}

    def __tmp3(__tmp1) :
        return (
            __tmp1.base_url
            + "/blocks?user="
            + __tmp1.user_id
            + "&otherUser="
            + __tmp1.other_user_id
        )


class BlockUnblockRequest(Request[None]):
    def __init__(__tmp1, gmi: "GMI", user_id, other_user_id) :
        __tmp1.user_id = user_id
        __tmp1.other_user_id = other_user_id
        super().__init__(gmi)

    def __tmp2(__tmp1) -> str:
        return "POST"

    def __tmp5(__tmp1, __tmp4) :
        return None

    def args(__tmp1) -> __typ0:
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
