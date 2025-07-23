from typing import TypeAlias
__typ0 : TypeAlias = "Event"
__typ3 : TypeAlias = "bool"
__typ1 : TypeAlias = "int"
import copy
import sys
from datetime import datetime
from typing import Dict, List, Optional

from aw_core.models import Event

from . import logger
from .abstract import AbstractStorage


class __typ2(AbstractStorage):
    """For storage of data in-memory, useful primarily in testing"""

    sid = "memory"

    def __init__(self, testing) -> None:
        self.logger = logger.getChild(self.sid)
        # self.logger.warning("Using in-memory storage, any events stored will not be persistent and will be lost when server is shut down. Use the --storage parameter to set a different storage method.")
        self.db: Dict[str, List[__typ0]] = {}
        self._metadata: Dict[str, dict] = dict()

    def create_bucket(
        self,
        __tmp0,
        type_id,
        client,
        hostname,
        created,
        name=None,
        data=None,
    ) :
        if not name:
            name = __tmp0
        self._metadata[__tmp0] = {
            "id": __tmp0,
            "name": name,
            "type": type_id,
            "client": client,
            "hostname": hostname,
            "created": created,
            "data": data or {},
        }
        self.db[__tmp0] = []

    def update_bucket(
        self,
        __tmp0: <FILL>,
        type_id: Optional[str] = None,
        client: Optional[str] = None,
        hostname: Optional[str] = None,
        name: Optional[str] = None,
        data: Optional[dict] = None,
    ) :
        if __tmp0 in self._metadata:
            if type_id:
                self._metadata[__tmp0]["type"] = type_id
            if client:
                self._metadata[__tmp0]["client"] = client
            if hostname:
                self._metadata[__tmp0]["hostname"] = hostname
            if name:
                self._metadata[__tmp0]["name"] = name
            if data:
                self._metadata[__tmp0]["data"] = data
        else:
            raise Exception("Bucket did not exist, could not update")

    def delete_bucket(self, __tmp0) -> None:
        if __tmp0 in self.db:
            del self.db[__tmp0]
        if __tmp0 in self._metadata:
            del self._metadata[__tmp0]
        else:
            raise Exception("Bucket did not exist, could not delete")

    def buckets(self):
        buckets = dict()
        for __tmp0 in self.db:
            buckets[__tmp0] = self.get_metadata(__tmp0)
        return buckets

    def __tmp5(
        self,
        __tmp0: str,
        __tmp2,
    ) :
        __tmp1 = self._get_event(__tmp0, __tmp2)
        return copy.deepcopy(__tmp1)

    def get_events(
        self,
        __tmp3,
        limit,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) :
        events = self.db[__tmp3]

        # Sort by timestamp
        events = sorted(events, key=lambda k: k["timestamp"])[::-1]

        # Filter by date
        if starttime:
            events = [e for e in events if starttime <= (e.timestamp + e.duration)]
        if endtime:
            events = [e for e in events if e.timestamp <= endtime]

        # Limit
        if limit == 0:
            return []
        elif limit < 0:
            limit = sys.maxsize
        events = events[:limit]
        # Return
        return copy.deepcopy(events)

    def __tmp4(
        self,
        __tmp3,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) -> __typ1:
        return len(
            [
                e
                for e in self.db[__tmp3]
                if (not starttime or starttime <= e.timestamp)
                and (not endtime or e.timestamp <= endtime)
            ]
        )

    def get_metadata(self, __tmp0: str):
        if __tmp0 in self._metadata:
            return self._metadata[__tmp0]
        else:
            raise Exception("Bucket did not exist, could not get metadata")

    def insert_one(self, __tmp3: str, __tmp1) :
        if __tmp1.id is not None:
            self.replace(__tmp3, __tmp1.id, __tmp1)
        else:
            # We need to copy the event to avoid setting the ID on the passed event
            __tmp1 = copy.copy(__tmp1)
            if self.db[__tmp3]:
                __tmp1.id = max(__typ1(e.id or 0) for e in self.db[__tmp3]) + 1
            else:
                __tmp1.id = 0
            self.db[__tmp3].append(__tmp1)
        return __tmp1

    def delete(self, __tmp0, __tmp2):
        for idx in (
            idx
            for idx, __tmp1 in reversed(list(enumerate(self.db[__tmp0])))
            if __tmp1.id == __tmp2
        ):
            self.db[__tmp0].pop(idx)
            return True
        return False

    def _get_event(self, __tmp0, __tmp2) :
        events = [
            __tmp1
            for idx, __tmp1 in reversed(list(enumerate(self.db[__tmp0])))
            if __tmp1.id == __tmp2
        ]
        if len(events) < 1:
            return None
        else:
            return events[0]

    def replace(self, __tmp0, __tmp2, __tmp1):
        for idx in (
            idx
            for idx, __tmp1 in reversed(list(enumerate(self.db[__tmp0])))
            if __tmp1.id == __tmp2
        ):
            # We need to copy the event to avoid setting the ID on the passed event
            __tmp1 = copy.copy(__tmp1)
            __tmp1.id = __tmp2
            self.db[__tmp0][idx] = __tmp1

    def replace_last(self, __tmp0, __tmp1):
        # NOTE: This does not actually get the most recent event, only the last inserted
        last = sorted(self.db[__tmp0], key=lambda e: e.timestamp)[-1]
        self.replace(__tmp0, last.id, __tmp1)
