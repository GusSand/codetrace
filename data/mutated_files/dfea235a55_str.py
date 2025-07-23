# pyre-strict

from typing import TYPE_CHECKING

from lowerpines.endpoints.request import Request, JsonType

if TYPE_CHECKING:  # pragma: no cover
    from lowerpines.gmi import GMI


class __typ1(Request[None]):
    def __init__(__tmp0, gmi, conversation_id, message_id) :
        __tmp0.conversation_id = conversation_id
        __tmp0.message_id = message_id
        super().__init__(gmi)

    def __tmp2(__tmp0, __tmp1) :
        return None

    def url(__tmp0) :
        return (
            __tmp0.base_url
            + "/messages/"
            + __tmp0.conversation_id
            + "/"
            + __tmp0.message_id
            + "/like"
        )

    def mode(__tmp0) :
        return "POST"


class __typ0(Request[None]):
    def __init__(__tmp0, gmi, conversation_id, message_id: <FILL>) :
        __tmp0.conversation_id = conversation_id
        __tmp0.message_id = message_id
        super().__init__(gmi)

    def __tmp2(__tmp0, __tmp1) :
        return None

    def url(__tmp0) :
        return (
            __tmp0.base_url
            + "/messages/"
            + __tmp0.conversation_id
            + "/"
            + __tmp0.message_id
            + "/unlike"
        )

    def mode(__tmp0) :
        return "POST"
