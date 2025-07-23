from typing import TypeAlias
__typ0 : TypeAlias = "Event"
__typ2 : TypeAlias = "str"
__typ3 : TypeAlias = "bool"
import copy
import sys
from datetime import datetime
from typing import Dict, List, Optional

from aw_core.models import Event

from . import logger
from .abstract import AbstractStorage


class __typ1(AbstractStorage):
    """For storage of data in-memory, useful primarily in testing"""

    sid = "memory"

    def __init__(__tmp1, testing) -> None:
        __tmp1.logger = logger.getChild(__tmp1.sid)
        # self.logger.warning("Using in-memory storage, any events stored will not be persistent and will be lost when server is shut down. Use the --storage parameter to set a different storage method.")
        __tmp1.db: Dict[__typ2, List[__typ0]] = {}
        __tmp1._metadata: Dict[__typ2, dict] = dict()

    def create_bucket(
        __tmp1,
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

    def __tmp2(
        __tmp1,
        __tmp0,
        type_id: Optional[__typ2] = None,
        client: Optional[__typ2] = None,
        hostname: Optional[__typ2] = None,
        name: Optional[__typ2] = None,
        data: Optional[dict] = None,
    ) :
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

    def delete_bucket(__tmp1, __tmp0) :
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
        __tmp0,
        event_id,
    ) :
        __tmp3 = __tmp1._get_event(__tmp0, event_id)
        return copy.deepcopy(__tmp3)

    def get_events(
        __tmp1,
        bucket,
        limit: <FILL>,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) -> List[__typ0]:
        events = __tmp1.db[bucket]

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
        bucket,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) :
        return len(
            [
                e
                for e in __tmp1.db[bucket]
                if (not starttime or starttime <= e.timestamp)
                and (not endtime or e.timestamp <= endtime)
            ]
        )

    def get_metadata(__tmp1, __tmp0):
        if __tmp0 in __tmp1._metadata:
            return __tmp1._metadata[__tmp0]
        else:
            raise Exception("Bucket did not exist, could not get metadata")

    def insert_one(__tmp1, bucket, __tmp3) :
        if __tmp3.id is not None:
            __tmp1.replace(bucket, __tmp3.id, __tmp3)
        else:
            # We need to copy the event to avoid setting the ID on the passed event
            __tmp3 = copy.copy(__tmp3)
            if __tmp1.db[bucket]:
                __tmp3.id = max(int(e.id or 0) for e in __tmp1.db[bucket]) + 1
            else:
                __tmp3.id = 0
            __tmp1.db[bucket].append(__tmp3)
        return __tmp3

    def delete(__tmp1, __tmp0, event_id):
        for idx in (
            idx
            for idx, __tmp3 in reversed(list(enumerate(__tmp1.db[__tmp0])))
            if __tmp3.id == event_id
        ):
            __tmp1.db[__tmp0].pop(idx)
            return True
        return False

    def _get_event(__tmp1, __tmp0, event_id) :
        events = [
            __tmp3
            for idx, __tmp3 in reversed(list(enumerate(__tmp1.db[__tmp0])))
            if __tmp3.id == event_id
        ]
        if len(events) < 1:
            return None
        else:
            return events[0]

    def replace(__tmp1, __tmp0, event_id, __tmp3):
        for idx in (
            idx
            for idx, __tmp3 in reversed(list(enumerate(__tmp1.db[__tmp0])))
            if __tmp3.id == event_id
        ):
            # We need to copy the event to avoid setting the ID on the passed event
            __tmp3 = copy.copy(__tmp3)
            __tmp3.id = event_id
            __tmp1.db[__tmp0][idx] = __tmp3

    def replace_last(__tmp1, __tmp0, __tmp3):
        # NOTE: This does not actually get the most recent event, only the last inserted
        last = sorted(__tmp1.db[__tmp0], key=lambda e: e.timestamp)[-1]
        __tmp1.replace(__tmp0, last.id, __tmp3)
