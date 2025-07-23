# pyre-strict
from typing import List, TYPE_CHECKING

from lowerpines.endpoints.request import Request, JsonType
from lowerpines.endpoints.message import Message

if TYPE_CHECKING:  # pragma: no cover
    from lowerpines.gmi import GMI


class Leaderboard:
    def __init__(self, gmi, group_id) :
        self.gmi = gmi
        self.group_id = group_id

    def _for_period(self, period) :
        return LeaderboardIndexRequest(self.gmi, self.group_id, period).result

    def for_today(self) :
        return self._for_period("day")

    def for_week(self) :
        return self._for_period("week")

    def for_month(self) :
        return self._for_period("month")

    def my_likes(self) :
        return LeaderboardMyLikesRequest(self.gmi, self.group_id).result

    def my_hits(self) :
        return LeaderboardMyHitsRequest(self.gmi, self.group_id).result


class LeaderboardIndexRequest(Request[List[Message]]):
    def __init__(self, gmi, group_id: <FILL>, period) :
        self.group_id = group_id
        if period not in ["day", "week", "month"]:
            raise ValueError("Period must be one of: day, week, or month")
        self.period = period
        super().__init__(gmi)

    def parse(self, response) -> List[Message]:
        messages = []
        for message_json in response["messages"]:
            messages.append(Message.from_json(self.gmi, message_json))
        return messages

    def __tmp0(self) :
        return self.base_url + "/groups/" + self.group_id + "/likes"

    def mode(self) :
        return "GET"


class LeaderboardMyLikesRequest(Request[List[Message]]):
    def __init__(self, gmi, group_id) :
        self.group_id = group_id
        super().__init__(gmi)

    def parse(self, response: JsonType) :
        messages = []
        for message_json in response["messages"]:
            messages.append(Message.from_json(self.gmi, message_json))
        return messages

    def __tmp0(self) :
        return self.base_url + "/groups/" + self.group_id + "/likes/mine"

    def mode(self) :
        return "GET"


class LeaderboardMyHitsRequest(Request[List[Message]]):
    def __init__(self, gmi, group_id) :
        self.group_id = group_id
        super().__init__(gmi)

    def parse(self, response: JsonType) :
        messages = []
        for message_json in response["messages"]:
            messages.append(Message.from_json(self.gmi, message_json))
        return messages

    def __tmp0(self) :
        return self.base_url + "/groups/" + self.group_id + "/likes/for_me"

    def mode(self) :
        return "GET"
