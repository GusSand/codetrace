from typing import TypeAlias
__typ0 : TypeAlias = "Event"
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

    def __tmp9(__tmp2, __tmp0: bool) :
        __tmp2.logger = logger.getChild(__tmp2.sid)
        # self.logger.warning("Using in-memory storage, any events stored will not be persistent and will be lost when server is shut down. Use the --storage parameter to set a different storage method.")
        __tmp2.db: Dict[str, List[__typ0]] = {}
        __tmp2._metadata: Dict[str, dict] = dict()

    def create_bucket(
        __tmp2,
        __tmp1,
        __tmp6,
        client,
        hostname,
        created,
        name=None,
        data=None,
    ) :
        if not name:
            name = __tmp1
        __tmp2._metadata[__tmp1] = {
            "id": __tmp1,
            "name": name,
            "type": __tmp6,
            "client": client,
            "hostname": hostname,
            "created": created,
            "data": data or {},
        }
        __tmp2.db[__tmp1] = []

    def update_bucket(
        __tmp2,
        __tmp1,
        __tmp6: Optional[str] = None,
        client: Optional[str] = None,
        hostname: Optional[str] = None,
        name: Optional[str] = None,
        data: Optional[dict] = None,
    ) -> None:
        if __tmp1 in __tmp2._metadata:
            if __tmp6:
                __tmp2._metadata[__tmp1]["type"] = __tmp6
            if client:
                __tmp2._metadata[__tmp1]["client"] = client
            if hostname:
                __tmp2._metadata[__tmp1]["hostname"] = hostname
            if name:
                __tmp2._metadata[__tmp1]["name"] = name
            if data:
                __tmp2._metadata[__tmp1]["data"] = data
        else:
            raise Exception("Bucket did not exist, could not update")

    def __tmp10(__tmp2, __tmp1: <FILL>) :
        if __tmp1 in __tmp2.db:
            del __tmp2.db[__tmp1]
        if __tmp1 in __tmp2._metadata:
            del __tmp2._metadata[__tmp1]
        else:
            raise Exception("Bucket did not exist, could not delete")

    def buckets(__tmp2):
        buckets = dict()
        for __tmp1 in __tmp2.db:
            buckets[__tmp1] = __tmp2.get_metadata(__tmp1)
        return buckets

    def __tmp11(
        __tmp2,
        __tmp1,
        __tmp7,
    ) :
        __tmp3 = __tmp2._get_event(__tmp1, __tmp7)
        return copy.deepcopy(__tmp3)

    def __tmp4(
        __tmp2,
        __tmp8,
        __tmp5: int,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) :
        events = __tmp2.db[__tmp8]

        # Sort by timestamp
        events = sorted(events, key=lambda k: k["timestamp"])[::-1]

        # Filter by date
        if starttime:
            events = [e for e in events if starttime <= (e.timestamp + e.duration)]
        if endtime:
            events = [e for e in events if e.timestamp <= endtime]

        # Limit
        if __tmp5 == 0:
            return []
        elif __tmp5 < 0:
            __tmp5 = sys.maxsize
        events = events[:__tmp5]
        # Return
        return copy.deepcopy(events)

    def get_eventcount(
        __tmp2,
        __tmp8,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) -> int:
        return len(
            [
                e
                for e in __tmp2.db[__tmp8]
                if (not starttime or starttime <= e.timestamp)
                and (not endtime or e.timestamp <= endtime)
            ]
        )

    def get_metadata(__tmp2, __tmp1):
        if __tmp1 in __tmp2._metadata:
            return __tmp2._metadata[__tmp1]
        else:
            raise Exception("Bucket did not exist, could not get metadata")

    def insert_one(__tmp2, __tmp8, __tmp3: __typ0) -> __typ0:
        if __tmp3.id is not None:
            __tmp2.replace(__tmp8, __tmp3.id, __tmp3)
        else:
            # We need to copy the event to avoid setting the ID on the passed event
            __tmp3 = copy.copy(__tmp3)
            if __tmp2.db[__tmp8]:
                __tmp3.id = max(int(e.id or 0) for e in __tmp2.db[__tmp8]) + 1
            else:
                __tmp3.id = 0
            __tmp2.db[__tmp8].append(__tmp3)
        return __tmp3

    def delete(__tmp2, __tmp1, __tmp7):
        for idx in (
            idx
            for idx, __tmp3 in reversed(list(enumerate(__tmp2.db[__tmp1])))
            if __tmp3.id == __tmp7
        ):
            __tmp2.db[__tmp1].pop(idx)
            return True
        return False

    def _get_event(__tmp2, __tmp1, __tmp7) -> Optional[__typ0]:
        events = [
            __tmp3
            for idx, __tmp3 in reversed(list(enumerate(__tmp2.db[__tmp1])))
            if __tmp3.id == __tmp7
        ]
        if len(events) < 1:
            return None
        else:
            return events[0]

    def replace(__tmp2, __tmp1, __tmp7, __tmp3):
        for idx in (
            idx
            for idx, __tmp3 in reversed(list(enumerate(__tmp2.db[__tmp1])))
            if __tmp3.id == __tmp7
        ):
            # We need to copy the event to avoid setting the ID on the passed event
            __tmp3 = copy.copy(__tmp3)
            __tmp3.id = __tmp7
            __tmp2.db[__tmp1][idx] = __tmp3

    def replace_last(__tmp2, __tmp1, __tmp3):
        # NOTE: This does not actually get the most recent event, only the last inserted
        last = sorted(__tmp2.db[__tmp1], key=lambda e: e.timestamp)[-1]
        __tmp2.replace(__tmp1, last.id, __tmp3)
