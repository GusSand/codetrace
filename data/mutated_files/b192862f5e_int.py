from typing import TypeAlias
__typ0 : TypeAlias = "str"
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

    def __init__(__tmp3, __tmp0: bool) -> None:
        __tmp3.logger = logger.getChild(__tmp3.sid)
        # self.logger.warning("Using in-memory storage, any events stored will not be persistent and will be lost when server is shut down. Use the --storage parameter to set a different storage method.")
        __tmp3.db: Dict[__typ0, List[Event]] = {}
        __tmp3._metadata: Dict[__typ0, dict] = dict()

    def create_bucket(
        __tmp3,
        __tmp1,
        __tmp7,
        __tmp11,
        __tmp12,
        __tmp15,
        name=None,
        data=None,
    ) :
        if not name:
            name = __tmp1
        __tmp3._metadata[__tmp1] = {
            "id": __tmp1,
            "name": name,
            "type": __tmp7,
            "client": __tmp11,
            "hostname": __tmp12,
            "created": __tmp15,
            "data": data or {},
        }
        __tmp3.db[__tmp1] = []

    def update_bucket(
        __tmp3,
        __tmp1,
        __tmp7: Optional[__typ0] = None,
        __tmp11: Optional[__typ0] = None,
        __tmp12: Optional[__typ0] = None,
        name: Optional[__typ0] = None,
        data: Optional[dict] = None,
    ) :
        if __tmp1 in __tmp3._metadata:
            if __tmp7:
                __tmp3._metadata[__tmp1]["type"] = __tmp7
            if __tmp11:
                __tmp3._metadata[__tmp1]["client"] = __tmp11
            if __tmp12:
                __tmp3._metadata[__tmp1]["hostname"] = __tmp12
            if name:
                __tmp3._metadata[__tmp1]["name"] = name
            if data:
                __tmp3._metadata[__tmp1]["data"] = data
        else:
            raise Exception("Bucket did not exist, could not update")

    def __tmp13(__tmp3, __tmp1: __typ0) -> None:
        if __tmp1 in __tmp3.db:
            del __tmp3.db[__tmp1]
        if __tmp1 in __tmp3._metadata:
            del __tmp3._metadata[__tmp1]
        else:
            raise Exception("Bucket did not exist, could not delete")

    def __tmp2(__tmp3):
        __tmp2 = dict()
        for __tmp1 in __tmp3.db:
            __tmp2[__tmp1] = __tmp3.get_metadata(__tmp1)
        return __tmp2

    def __tmp14(
        __tmp3,
        __tmp1: __typ0,
        __tmp8: <FILL>,
    ) -> Optional[Event]:
        __tmp4 = __tmp3._get_event(__tmp1, __tmp8)
        return copy.deepcopy(__tmp4)

    def __tmp5(
        __tmp3,
        __tmp10: __typ0,
        limit: int,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) -> List[Event]:
        events = __tmp3.db[__tmp10]

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
        __tmp3,
        __tmp10: __typ0,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) -> int:
        return len(
            [
                e
                for e in __tmp3.db[__tmp10]
                if (not starttime or starttime <= e.timestamp)
                and (not endtime or e.timestamp <= endtime)
            ]
        )

    def get_metadata(__tmp3, __tmp1: __typ0):
        if __tmp1 in __tmp3._metadata:
            return __tmp3._metadata[__tmp1]
        else:
            raise Exception("Bucket did not exist, could not get metadata")

    def insert_one(__tmp3, __tmp10: __typ0, __tmp4: Event) -> Event:
        if __tmp4.id is not None:
            __tmp3.replace(__tmp10, __tmp4.id, __tmp4)
        else:
            # We need to copy the event to avoid setting the ID on the passed event
            __tmp4 = copy.copy(__tmp4)
            if __tmp3.db[__tmp10]:
                __tmp4.id = max(int(e.id or 0) for e in __tmp3.db[__tmp10]) + 1
            else:
                __tmp4.id = 0
            __tmp3.db[__tmp10].append(__tmp4)
        return __tmp4

    def __tmp6(__tmp3, __tmp1, __tmp8):
        for idx in (
            idx
            for idx, __tmp4 in reversed(list(enumerate(__tmp3.db[__tmp1])))
            if __tmp4.id == __tmp8
        ):
            __tmp3.db[__tmp1].pop(idx)
            return True
        return False

    def _get_event(__tmp3, __tmp1, __tmp8) -> Optional[Event]:
        events = [
            __tmp4
            for idx, __tmp4 in reversed(list(enumerate(__tmp3.db[__tmp1])))
            if __tmp4.id == __tmp8
        ]
        if len(events) < 1:
            return None
        else:
            return events[0]

    def replace(__tmp3, __tmp1, __tmp8, __tmp4):
        for idx in (
            idx
            for idx, __tmp4 in reversed(list(enumerate(__tmp3.db[__tmp1])))
            if __tmp4.id == __tmp8
        ):
            # We need to copy the event to avoid setting the ID on the passed event
            __tmp4 = copy.copy(__tmp4)
            __tmp4.id = __tmp8
            __tmp3.db[__tmp1][idx] = __tmp4

    def __tmp9(__tmp3, __tmp1, __tmp4):
        # NOTE: This does not actually get the most recent event, only the last inserted
        last = sorted(__tmp3.db[__tmp1], key=lambda e: e.timestamp)[-1]
        __tmp3.replace(__tmp1, last.id, __tmp4)
