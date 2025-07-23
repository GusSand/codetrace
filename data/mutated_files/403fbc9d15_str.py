from typing import TypeAlias
__typ3 : TypeAlias = "JsonType"
# pyre-strict
from typing import List, TYPE_CHECKING

from lowerpines.endpoints.request import Request, JsonType
from lowerpines.endpoints.message import Message

if TYPE_CHECKING:  # pragma: no cover
    from lowerpines.gmi import GMI


class __typ1:
    def __init__(__tmp1, gmi: "GMI", group_id: <FILL>) -> None:
        __tmp1.gmi = gmi
        __tmp1.group_id = group_id

    def _for_period(__tmp1, period: str) -> List[Message]:
        return __typ0(__tmp1.gmi, __tmp1.group_id, period).result

    def for_today(__tmp1) -> List[Message]:
        return __tmp1._for_period("day")

    def __tmp0(__tmp1) :
        return __tmp1._for_period("week")

    def for_month(__tmp1) :
        return __tmp1._for_period("month")

    def my_likes(__tmp1) -> List[Message]:
        return __typ2(__tmp1.gmi, __tmp1.group_id).result

    def my_hits(__tmp1) -> List[Message]:
        return LeaderboardMyHitsRequest(__tmp1.gmi, __tmp1.group_id).result


class __typ0(Request[List[Message]]):
    def __init__(__tmp1, gmi: "GMI", group_id: str, period: str) -> None:
        __tmp1.group_id = group_id
        if period not in ["day", "week", "month"]:
            raise ValueError("Period must be one of: day, week, or month")
        __tmp1.period = period
        super().__init__(gmi)

    def __tmp5(__tmp1, __tmp4: __typ3) -> List[Message]:
        messages = []
        for message_json in __tmp4["messages"]:
            messages.append(Message.from_json(__tmp1.gmi, message_json))
        return messages

    def __tmp3(__tmp1) -> str:
        return __tmp1.base_url + "/groups/" + __tmp1.group_id + "/likes"

    def __tmp2(__tmp1) -> str:
        return "GET"


class __typ2(Request[List[Message]]):
    def __init__(__tmp1, gmi: "GMI", group_id: str) -> None:
        __tmp1.group_id = group_id
        super().__init__(gmi)

    def __tmp5(__tmp1, __tmp4) -> List[Message]:
        messages = []
        for message_json in __tmp4["messages"]:
            messages.append(Message.from_json(__tmp1.gmi, message_json))
        return messages

    def __tmp3(__tmp1) -> str:
        return __tmp1.base_url + "/groups/" + __tmp1.group_id + "/likes/mine"

    def __tmp2(__tmp1) -> str:
        return "GET"


class LeaderboardMyHitsRequest(Request[List[Message]]):
    def __init__(__tmp1, gmi: "GMI", group_id: str) -> None:
        __tmp1.group_id = group_id
        super().__init__(gmi)

    def __tmp5(__tmp1, __tmp4: __typ3) -> List[Message]:
        messages = []
        for message_json in __tmp4["messages"]:
            messages.append(Message.from_json(__tmp1.gmi, message_json))
        return messages

    def __tmp3(__tmp1) -> str:
        return __tmp1.base_url + "/groups/" + __tmp1.group_id + "/likes/for_me"

    def __tmp2(__tmp1) -> str:
        return "GET"
