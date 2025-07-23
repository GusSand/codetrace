# pyre-strict
from typing import List, TYPE_CHECKING

from lowerpines.endpoints.request import Request, JsonType
from lowerpines.endpoints.message import Message

if TYPE_CHECKING:  # pragma: no cover
    from lowerpines.gmi import GMI


class Leaderboard:
    def __init__(__tmp2, gmi: "GMI", group_id: str) -> None:
        __tmp2.gmi = gmi
        __tmp2.group_id = group_id

    def _for_period(__tmp2, period: str) -> List[Message]:
        return LeaderboardIndexRequest(__tmp2.gmi, __tmp2.group_id, period).result

    def __tmp3(__tmp2) -> List[Message]:
        return __tmp2._for_period("day")

    def __tmp0(__tmp2) -> List[Message]:
        return __tmp2._for_period("week")

    def __tmp7(__tmp2) :
        return __tmp2._for_period("month")

    def __tmp1(__tmp2) :
        return LeaderboardMyLikesRequest(__tmp2.gmi, __tmp2.group_id).result

    def my_hits(__tmp2) :
        return LeaderboardMyHitsRequest(__tmp2.gmi, __tmp2.group_id).result


class LeaderboardIndexRequest(Request[List[Message]]):
    def __init__(__tmp2, gmi: "GMI", group_id: str, period: <FILL>) -> None:
        __tmp2.group_id = group_id
        if period not in ["day", "week", "month"]:
            raise ValueError("Period must be one of: day, week, or month")
        __tmp2.period = period
        super().__init__(gmi)

    def __tmp8(__tmp2, __tmp6) :
        messages = []
        for message_json in __tmp6["messages"]:
            messages.append(Message.from_json(__tmp2.gmi, message_json))
        return messages

    def __tmp5(__tmp2) -> str:
        return __tmp2.base_url + "/groups/" + __tmp2.group_id + "/likes"

    def __tmp4(__tmp2) :
        return "GET"


class LeaderboardMyLikesRequest(Request[List[Message]]):
    def __init__(__tmp2, gmi: "GMI", group_id) -> None:
        __tmp2.group_id = group_id
        super().__init__(gmi)

    def __tmp8(__tmp2, __tmp6) -> List[Message]:
        messages = []
        for message_json in __tmp6["messages"]:
            messages.append(Message.from_json(__tmp2.gmi, message_json))
        return messages

    def __tmp5(__tmp2) :
        return __tmp2.base_url + "/groups/" + __tmp2.group_id + "/likes/mine"

    def __tmp4(__tmp2) :
        return "GET"


class LeaderboardMyHitsRequest(Request[List[Message]]):
    def __init__(__tmp2, gmi, group_id) :
        __tmp2.group_id = group_id
        super().__init__(gmi)

    def __tmp8(__tmp2, __tmp6: JsonType) -> List[Message]:
        messages = []
        for message_json in __tmp6["messages"]:
            messages.append(Message.from_json(__tmp2.gmi, message_json))
        return messages

    def __tmp5(__tmp2) -> str:
        return __tmp2.base_url + "/groups/" + __tmp2.group_id + "/likes/for_me"

    def __tmp4(__tmp2) -> str:
        return "GET"
