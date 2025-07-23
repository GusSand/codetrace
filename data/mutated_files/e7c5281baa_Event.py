from typing import TypeAlias
__typ0 : TypeAlias = "BucketType"
__typ1 : TypeAlias = "bool"
import datetime
from typing import Dict
from .event import Event
from .bucket_type import BucketType


class __typ2:
    def __init__(self,
                 bucket_type: __typ0,
                 timestamp: datetime.datetime,
                 event: <FILL>,
                 __tmp0: __typ1
                 ) -> None:
        self._bucket_type = bucket_type
        self._is_end = __tmp0
        self.event = event
        self.timestamp = timestamp

    @property
    def event_data(self) -> Dict[str, str]:
        return self.event.data  # type: ignore

    @property
    def event_type(self) -> __typ0:
        return self._bucket_type

    def __tmp0(self) -> __typ1:
        return self._is_end

    def __lt__(self, other) -> __typ1:
        if self.timestamp == other.timestamp:
            return self.event_type == __typ0.AFK \
                   and other.event_type != __typ0.AFK
        return self.timestamp < other.timestamp
