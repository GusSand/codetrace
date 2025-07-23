import copy
import sys
from datetime import datetime
from typing import Dict, List, Optional

from aw_core.models import Event

from . import logger
from .abstract import AbstractStorage


class MemoryStorage(AbstractStorage):
    """For storage of data in-memory, useful primarily in testing"""

    sid = "memory"

    def __init__(__tmp1, testing: bool) -> None:
        __tmp1.logger = logger.getChild(__tmp1.sid)
        # self.logger.warning("Using in-memory storage, any events stored will not be persistent and will be lost when server is shut down. Use the --storage parameter to set a different storage method.")
        __tmp1.db: Dict[str, List[Event]] = {}
        __tmp1._metadata: Dict[str, dict] = dict()

    def create_bucket(
        __tmp1,
        __tmp0,
        type_id,
        client,
        hostname,
        created,
        name=None,
        data=None,
    ) -> None:
        if not name:
            name = __tmp0
        __tmp1._metadata[__tmp0] = {
            "id": __tmp0,
            "name": name,
            "type": type_id,
            "client": client,
            "hostname": hostname,
            "created": created,
            "data": data or {},
        }
        __tmp1.db[__tmp0] = []

    def update_bucket(
        __tmp1,
        __tmp0: str,
        type_id: Optional[str] = None,
        client: Optional[str] = None,
        hostname: Optional[str] = None,
        name: Optional[str] = None,
        data: Optional[dict] = None,
    ) -> None:
        if __tmp0 in __tmp1._metadata:
            if type_id:
                __tmp1._metadata[__tmp0]["type"] = type_id
            if client:
                __tmp1._metadata[__tmp0]["client"] = client
            if hostname:
                __tmp1._metadata[__tmp0]["hostname"] = hostname
            if name:
                __tmp1._metadata[__tmp0]["name"] = name
            if data:
                __tmp1._metadata[__tmp0]["data"] = data
        else:
            raise Exception("Bucket did not exist, could not update")

    def delete_bucket(__tmp1, __tmp0: str) -> None:
        if __tmp0 in __tmp1.db:
            del __tmp1.db[__tmp0]
        if __tmp0 in __tmp1._metadata:
            del __tmp1._metadata[__tmp0]
        else:
            raise Exception("Bucket did not exist, could not delete")

    def buckets(__tmp1):
        buckets = dict()
        for __tmp0 in __tmp1.db:
            buckets[__tmp0] = __tmp1.get_metadata(__tmp0)
        return buckets

    def get_event(
        __tmp1,
        __tmp0: <FILL>,
        event_id: int,
    ) -> Optional[Event]:
        event = __tmp1._get_event(__tmp0, event_id)
        return copy.deepcopy(event)

    def get_events(
        __tmp1,
        __tmp2,
        limit: int,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) -> List[Event]:
        events = __tmp1.db[__tmp2]

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

    def get_eventcount(
        __tmp1,
        __tmp2: str,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) -> int:
        return len(
            [
                e
                for e in __tmp1.db[__tmp2]
                if (not starttime or starttime <= e.timestamp)
                and (not endtime or e.timestamp <= endtime)
            ]
        )

    def get_metadata(__tmp1, __tmp0: str):
        if __tmp0 in __tmp1._metadata:
            return __tmp1._metadata[__tmp0]
        else:
            raise Exception("Bucket did not exist, could not get metadata")

    def insert_one(__tmp1, __tmp2: str, event: Event) -> Event:
        if event.id is not None:
            __tmp1.replace(__tmp2, event.id, event)
        else:
            # We need to copy the event to avoid setting the ID on the passed event
            event = copy.copy(event)
            if __tmp1.db[__tmp2]:
                event.id = max(int(e.id or 0) for e in __tmp1.db[__tmp2]) + 1
            else:
                event.id = 0
            __tmp1.db[__tmp2].append(event)
        return event

    def delete(__tmp1, __tmp0, event_id):
        for idx in (
            idx
            for idx, event in reversed(list(enumerate(__tmp1.db[__tmp0])))
            if event.id == event_id
        ):
            __tmp1.db[__tmp0].pop(idx)
            return True
        return False

    def _get_event(__tmp1, __tmp0, event_id) -> Optional[Event]:
        events = [
            event
            for idx, event in reversed(list(enumerate(__tmp1.db[__tmp0])))
            if event.id == event_id
        ]
        if len(events) < 1:
            return None
        else:
            return events[0]

    def replace(__tmp1, __tmp0, event_id, event):
        for idx in (
            idx
            for idx, event in reversed(list(enumerate(__tmp1.db[__tmp0])))
            if event.id == event_id
        ):
            # We need to copy the event to avoid setting the ID on the passed event
            event = copy.copy(event)
            event.id = event_id
            __tmp1.db[__tmp0][idx] = event

    def __tmp3(__tmp1, __tmp0, event):
        # NOTE: This does not actually get the most recent event, only the last inserted
        last = sorted(__tmp1.db[__tmp0], key=lambda e: e.timestamp)[-1]
        __tmp1.replace(__tmp0, last.id, event)
