from typing import TypeAlias
__typ0 : TypeAlias = "JsonType"
__typ3 : TypeAlias = "bool"
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

    def get_all(__tmp2, user_id) -> List["Block"]:
        return BlockIndexRequest(__tmp2.gmi, user_id).result

    @staticmethod
    def block_exists(gmi, user_id, other_user_id) :
        return __typ4(gmi, user_id, other_user_id).result

    @staticmethod
    def __tmp3(gmi: "GMI", user_id, other_user_id: str) :
        __typ2(gmi, user_id, other_user_id)

    @staticmethod
    def __tmp0(gmi, user_id, other_user_id) :
        __typ1(gmi, user_id, other_user_id)


class BlockIndexRequest(Request[List[Block]]):
    def __init__(__tmp2, gmi, user_id: str) :
        __tmp2.user_id = user_id
        super().__init__(gmi)

    def __tmp4(__tmp2) :
        return "GET"

    def parse(__tmp2, __tmp5: __typ0) :
        blocks = list()
        for block_json in __tmp5["blocks"]:
            blocks.append(Block.from_json(__tmp2.gmi, block_json))
        return blocks

    def __tmp1(__tmp2) :
        return {"user": __tmp2.user_id}

    def url(__tmp2) :
        return __tmp2.base_url + "/blocks"


class __typ4(Request[__typ3]):
    def __init__(__tmp2, gmi: "GMI", user_id, other_user_id) :
        __tmp2.user_id = user_id
        __tmp2.other_user_id = other_user_id
        super().__init__(gmi)

    def __tmp4(__tmp2) :
        return "GET"

    def parse(__tmp2, __tmp5) :
        return __tmp5["between"]

    def __tmp1(__tmp2) :
        return {"user": __tmp2.user_id, "otherUser": __tmp2.other_user_id}

    def url(__tmp2) -> str:
        return __tmp2.base_url + "/blocks/between"


class __typ2(Request[None]):
    def __init__(__tmp2, gmi, user_id: <FILL>, other_user_id) -> None:
        __tmp2.user_id = user_id
        __tmp2.other_user_id = other_user_id
        super().__init__(gmi)

    def __tmp4(__tmp2) :
        return "POST"

    def parse(__tmp2, __tmp5) :
        return None

    def __tmp1(__tmp2) :
        return {}

    def url(__tmp2) :
        return (
            __tmp2.base_url
            + "/blocks?user="
            + __tmp2.user_id
            + "&otherUser="
            + __tmp2.other_user_id
        )


class __typ1(Request[None]):
    def __init__(__tmp2, gmi, user_id: str, other_user_id: str) :
        __tmp2.user_id = user_id
        __tmp2.other_user_id = other_user_id
        super().__init__(gmi)

    def __tmp4(__tmp2) -> str:
        return "POST"

    def parse(__tmp2, __tmp5) :
        return None

    def __tmp1(__tmp2) :
        return {}

    def url(__tmp2) -> str:
        return (
            __tmp2.base_url
            + "/blocks/delete"
            + "/blocks?user="
            + __tmp2.user_id
            + "&otherUser="
            + __tmp2.other_user_id
        )
