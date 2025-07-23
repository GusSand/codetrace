from typing import TypeAlias
__typ2 : TypeAlias = "JsonType"
__typ1 : TypeAlias = "bool"
# pyre-strict
from typing import TYPE_CHECKING, List

from lowerpines.endpoints.object import AbstractObject, Field
from lowerpines.endpoints.request import Request, JsonType

if TYPE_CHECKING:  # pragma: no cover
    from lowerpines.gmi import GMI


class Block(AbstractObject):
    user_id: str = Field().with_type(str)
    blocked_user_id: str = Field().with_type(str)

    def __init__(__tmp2, gmi: "GMI") :
        __tmp2.gmi = gmi

    def get_all(__tmp2, user_id) -> List["Block"]:
        return __typ0(__tmp2.gmi, user_id).result

    @staticmethod
    def __tmp6(gmi, user_id, other_user_id) -> __typ1:
        return BlockBetweenRequest(gmi, user_id, other_user_id).result

    @staticmethod
    def block(gmi, user_id: str, other_user_id: <FILL>) :
        BlockCreateRequest(gmi, user_id, other_user_id)

    @staticmethod
    def __tmp0(gmi, user_id, other_user_id) :
        BlockUnblockRequest(gmi, user_id, other_user_id)


class __typ0(Request[List[Block]]):
    def __init__(__tmp2, gmi: "GMI", user_id: str) :
        __tmp2.user_id = user_id
        super().__init__(gmi)

    def __tmp3(__tmp2) :
        return "GET"

    def __tmp7(__tmp2, __tmp5: __typ2) -> List[Block]:
        blocks = list()
        for block_json in __tmp5["blocks"]:
            blocks.append(Block.from_json(__tmp2.gmi, block_json))
        return blocks

    def __tmp1(__tmp2) -> __typ2:
        return {"user": __tmp2.user_id}

    def __tmp4(__tmp2) :
        return __tmp2.base_url + "/blocks"


class BlockBetweenRequest(Request[__typ1]):
    def __init__(__tmp2, gmi: "GMI", user_id: str, other_user_id) :
        __tmp2.user_id = user_id
        __tmp2.other_user_id = other_user_id
        super().__init__(gmi)

    def __tmp3(__tmp2) -> str:
        return "GET"

    def __tmp7(__tmp2, __tmp5: __typ2) -> __typ1:
        return __tmp5["between"]

    def __tmp1(__tmp2) :
        return {"user": __tmp2.user_id, "otherUser": __tmp2.other_user_id}

    def __tmp4(__tmp2) -> str:
        return __tmp2.base_url + "/blocks/between"


class BlockCreateRequest(Request[None]):
    def __init__(__tmp2, gmi: "GMI", user_id, other_user_id) -> None:
        __tmp2.user_id = user_id
        __tmp2.other_user_id = other_user_id
        super().__init__(gmi)

    def __tmp3(__tmp2) -> str:
        return "POST"

    def __tmp7(__tmp2, __tmp5) -> None:
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
    def __init__(__tmp2, gmi, user_id, other_user_id) :
        __tmp2.user_id = user_id
        __tmp2.other_user_id = other_user_id
        super().__init__(gmi)

    def __tmp3(__tmp2) :
        return "POST"

    def __tmp7(__tmp2, __tmp5) -> None:
        return None

    def __tmp1(__tmp2) -> __typ2:
        return {}

    def __tmp4(__tmp2) :
        return (
            __tmp2.base_url
            + "/blocks/delete"
            + "/blocks?user="
            + __tmp2.user_id
            + "&otherUser="
            + __tmp2.other_user_id
        )
