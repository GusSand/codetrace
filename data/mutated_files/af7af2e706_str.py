from typing import TypeAlias
__typ0 : TypeAlias = "JsonType"
__typ2 : TypeAlias = "bool"
# pyre-strict
from typing import TYPE_CHECKING, List

from lowerpines.endpoints.object import AbstractObject, Field
from lowerpines.endpoints.request import Request, JsonType

if TYPE_CHECKING:  # pragma: no cover
    from lowerpines.gmi import GMI


class __typ3(AbstractObject):
    user_id: str = Field().with_type(str)
    blocked_user_id: str = Field().with_type(str)

    def __init__(__tmp0, gmi: "GMI") :
        __tmp0.gmi = gmi

    def get_all(__tmp0, user_id: str) :
        return BlockIndexRequest(__tmp0.gmi, user_id).result

    @staticmethod
    def block_exists(gmi, user_id: <FILL>, other_user_id: str) -> __typ2:
        return __typ4(gmi, user_id, other_user_id).result

    @staticmethod
    def block(gmi, user_id: str, other_user_id) -> None:
        __typ1(gmi, user_id, other_user_id)

    @staticmethod
    def unblock(gmi: "GMI", user_id: str, other_user_id) -> None:
        BlockUnblockRequest(gmi, user_id, other_user_id)


class BlockIndexRequest(Request[List[__typ3]]):
    def __init__(__tmp0, gmi, user_id: str) -> None:
        __tmp0.user_id = user_id
        super().__init__(gmi)

    def mode(__tmp0) :
        return "GET"

    def parse(__tmp0, response: __typ0) :
        blocks = list()
        for block_json in response["blocks"]:
            blocks.append(__typ3.from_json(__tmp0.gmi, block_json))
        return blocks

    def args(__tmp0) -> __typ0:
        return {"user": __tmp0.user_id}

    def url(__tmp0) -> str:
        return __tmp0.base_url + "/blocks"


class __typ4(Request[__typ2]):
    def __init__(__tmp0, gmi, user_id: str, other_user_id) :
        __tmp0.user_id = user_id
        __tmp0.other_user_id = other_user_id
        super().__init__(gmi)

    def mode(__tmp0) -> str:
        return "GET"

    def parse(__tmp0, response: __typ0) :
        return response["between"]

    def args(__tmp0) :
        return {"user": __tmp0.user_id, "otherUser": __tmp0.other_user_id}

    def url(__tmp0) :
        return __tmp0.base_url + "/blocks/between"


class __typ1(Request[None]):
    def __init__(__tmp0, gmi, user_id: str, other_user_id) -> None:
        __tmp0.user_id = user_id
        __tmp0.other_user_id = other_user_id
        super().__init__(gmi)

    def mode(__tmp0) -> str:
        return "POST"

    def parse(__tmp0, response) :
        return None

    def args(__tmp0) :
        return {}

    def url(__tmp0) -> str:
        return (
            __tmp0.base_url
            + "/blocks?user="
            + __tmp0.user_id
            + "&otherUser="
            + __tmp0.other_user_id
        )


class BlockUnblockRequest(Request[None]):
    def __init__(__tmp0, gmi, user_id, other_user_id: str) -> None:
        __tmp0.user_id = user_id
        __tmp0.other_user_id = other_user_id
        super().__init__(gmi)

    def mode(__tmp0) :
        return "POST"

    def parse(__tmp0, response) -> None:
        return None

    def args(__tmp0) -> __typ0:
        return {}

    def url(__tmp0) -> str:
        return (
            __tmp0.base_url
            + "/blocks/delete"
            + "/blocks?user="
            + __tmp0.user_id
            + "&otherUser="
            + __tmp0.other_user_id
        )
