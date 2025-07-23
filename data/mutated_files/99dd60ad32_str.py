from typing import TypeAlias
__typ1 : TypeAlias = "JsonType"
# pyre-strict
from typing import TYPE_CHECKING, List

from lowerpines.endpoints.object import AbstractObject, Field
from lowerpines.endpoints.request import Request, JsonType

if TYPE_CHECKING:  # pragma: no cover
    from lowerpines.gmi import GMI


class Block(AbstractObject):
    user_id: str = Field().with_type(str)
    blocked_user_id: str = Field().with_type(str)

    def __init__(__tmp2, gmi) -> None:
        __tmp2.gmi = gmi

    def __tmp7(__tmp2, user_id: str) -> List["Block"]:
        return BlockIndexRequest(__tmp2.gmi, user_id).result

    @staticmethod
    def __tmp8(gmi: "GMI", user_id, other_user_id: str) :
        return BlockBetweenRequest(gmi, user_id, other_user_id).result

    @staticmethod
    def __tmp3(gmi: "GMI", user_id, other_user_id) -> None:
        __typ0(gmi, user_id, other_user_id)

    @staticmethod
    def __tmp0(gmi, user_id, other_user_id) -> None:
        BlockUnblockRequest(gmi, user_id, other_user_id)


class BlockIndexRequest(Request[List[Block]]):
    def __init__(__tmp2, gmi: "GMI", user_id: str) :
        __tmp2.user_id = user_id
        super().__init__(gmi)

    def __tmp4(__tmp2) :
        return "GET"

    def __tmp9(__tmp2, __tmp6: __typ1) -> List[Block]:
        blocks = list()
        for block_json in __tmp6["blocks"]:
            blocks.append(Block.from_json(__tmp2.gmi, block_json))
        return blocks

    def __tmp1(__tmp2) :
        return {"user": __tmp2.user_id}

    def __tmp5(__tmp2) -> str:
        return __tmp2.base_url + "/blocks"


class BlockBetweenRequest(Request[bool]):
    def __init__(__tmp2, gmi: "GMI", user_id: str, other_user_id) -> None:
        __tmp2.user_id = user_id
        __tmp2.other_user_id = other_user_id
        super().__init__(gmi)

    def __tmp4(__tmp2) :
        return "GET"

    def __tmp9(__tmp2, __tmp6: __typ1) :
        return __tmp6["between"]

    def __tmp1(__tmp2) :
        return {"user": __tmp2.user_id, "otherUser": __tmp2.other_user_id}

    def __tmp5(__tmp2) -> str:
        return __tmp2.base_url + "/blocks/between"


class __typ0(Request[None]):
    def __init__(__tmp2, gmi: "GMI", user_id, other_user_id: str) :
        __tmp2.user_id = user_id
        __tmp2.other_user_id = other_user_id
        super().__init__(gmi)

    def __tmp4(__tmp2) :
        return "POST"

    def __tmp9(__tmp2, __tmp6) :
        return None

    def __tmp1(__tmp2) -> __typ1:
        return {}

    def __tmp5(__tmp2) -> str:
        return (
            __tmp2.base_url
            + "/blocks?user="
            + __tmp2.user_id
            + "&otherUser="
            + __tmp2.other_user_id
        )


class BlockUnblockRequest(Request[None]):
    def __init__(__tmp2, gmi, user_id: <FILL>, other_user_id) -> None:
        __tmp2.user_id = user_id
        __tmp2.other_user_id = other_user_id
        super().__init__(gmi)

    def __tmp4(__tmp2) -> str:
        return "POST"

    def __tmp9(__tmp2, __tmp6) :
        return None

    def __tmp1(__tmp2) -> __typ1:
        return {}

    def __tmp5(__tmp2) :
        return (
            __tmp2.base_url
            + "/blocks/delete"
            + "/blocks?user="
            + __tmp2.user_id
            + "&otherUser="
            + __tmp2.other_user_id
        )
