from typing import TypeAlias
__typ0 : TypeAlias = "int"
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

    def __init__(__tmp0, __tmp1: bool) :
        __tmp0.logger = logger.getChild(__tmp0.sid)
        # self.logger.warning("Using in-memory storage, any events stored will not be persistent and will be lost when server is shut down. Use the --storage parameter to set a different storage method.")
        __tmp0.db: Dict[str, List[Event]] = {}
        __tmp0._metadata: Dict[str, dict] = dict()

    def __tmp4(
        __tmp0,
        __tmp2,
        __tmp17,
        __tmp13,
        __tmp14,
        __tmp10,
        name=None,
        data=None,
    ) -> None:
        if not name:
            name = __tmp2
        __tmp0._metadata[__tmp2] = {
            "id": __tmp2,
            "name": name,
            "type": __tmp17,
            "client": __tmp13,
            "hostname": __tmp14,
            "created": __tmp10,
            "data": data or {},
        }
        __tmp0.db[__tmp2] = []

    def __tmp7(
        __tmp0,
        __tmp2,
        __tmp17: Optional[str] = None,
        __tmp13: Optional[str] = None,
        __tmp14: Optional[str] = None,
        name: Optional[str] = None,
        data: Optional[dict] = None,
    ) :
        if __tmp2 in __tmp0._metadata:
            if __tmp17:
                __tmp0._metadata[__tmp2]["type"] = __tmp17
            if __tmp13:
                __tmp0._metadata[__tmp2]["client"] = __tmp13
            if __tmp14:
                __tmp0._metadata[__tmp2]["hostname"] = __tmp14
            if name:
                __tmp0._metadata[__tmp2]["name"] = name
            if data:
                __tmp0._metadata[__tmp2]["data"] = data
        else:
            raise Exception("Bucket did not exist, could not update")

    def __tmp15(__tmp0, __tmp2: str) -> None:
        if __tmp2 in __tmp0.db:
            del __tmp0.db[__tmp2]
        if __tmp2 in __tmp0._metadata:
            del __tmp0._metadata[__tmp2]
        else:
            raise Exception("Bucket did not exist, could not delete")

    def __tmp16(__tmp0):
        __tmp16 = dict()
        for __tmp2 in __tmp0.db:
            __tmp16[__tmp2] = __tmp0.get_metadata(__tmp2)
        return __tmp16

    def __tmp18(
        __tmp0,
        __tmp2: str,
        __tmp5,
    ) -> Optional[Event]:
        __tmp3 = __tmp0._get_event(__tmp2, __tmp5)
        return copy.deepcopy(__tmp3)

    def get_events(
        __tmp0,
        __tmp6: str,
        __tmp11,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) -> List[Event]:
        events = __tmp0.db[__tmp6]

        # Sort by timestamp
        events = sorted(events, key=lambda k: k["timestamp"])[::-1]

        # Filter by date
        if starttime:
            events = [e for e in events if starttime <= (e.timestamp + e.duration)]
        if endtime:
            events = [e for e in events if e.timestamp <= endtime]

        # Limit
        if __tmp11 == 0:
            return []
        elif __tmp11 < 0:
            __tmp11 = sys.maxsize
        events = events[:__tmp11]
        # Return
        return copy.deepcopy(events)

    def __tmp8(
        __tmp0,
        __tmp6: str,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) -> __typ0:
        return len(
            [
                e
                for e in __tmp0.db[__tmp6]
                if (not starttime or starttime <= e.timestamp)
                and (not endtime or e.timestamp <= endtime)
            ]
        )

    def get_metadata(__tmp0, __tmp2: <FILL>):
        if __tmp2 in __tmp0._metadata:
            return __tmp0._metadata[__tmp2]
        else:
            raise Exception("Bucket did not exist, could not get metadata")

    def insert_one(__tmp0, __tmp6: str, __tmp3: Event) -> Event:
        if __tmp3.id is not None:
            __tmp0.replace(__tmp6, __tmp3.id, __tmp3)
        else:
            # We need to copy the event to avoid setting the ID on the passed event
            __tmp3 = copy.copy(__tmp3)
            if __tmp0.db[__tmp6]:
                __tmp3.id = max(__typ0(e.id or 0) for e in __tmp0.db[__tmp6]) + 1
            else:
                __tmp3.id = 0
            __tmp0.db[__tmp6].append(__tmp3)
        return __tmp3

    def __tmp9(__tmp0, __tmp2, __tmp5):
        for idx in (
            idx
            for idx, __tmp3 in reversed(list(enumerate(__tmp0.db[__tmp2])))
            if __tmp3.id == __tmp5
        ):
            __tmp0.db[__tmp2].pop(idx)
            return True
        return False

    def _get_event(__tmp0, __tmp2, __tmp5) -> Optional[Event]:
        events = [
            __tmp3
            for idx, __tmp3 in reversed(list(enumerate(__tmp0.db[__tmp2])))
            if __tmp3.id == __tmp5
        ]
        if len(events) < 1:
            return None
        else:
            return events[0]

    def replace(__tmp0, __tmp2, __tmp5, __tmp3):
        for idx in (
            idx
            for idx, __tmp3 in reversed(list(enumerate(__tmp0.db[__tmp2])))
            if __tmp3.id == __tmp5
        ):
            # We need to copy the event to avoid setting the ID on the passed event
            __tmp3 = copy.copy(__tmp3)
            __tmp3.id = __tmp5
            __tmp0.db[__tmp2][idx] = __tmp3

    def __tmp12(__tmp0, __tmp2, __tmp3):
        # NOTE: This does not actually get the most recent event, only the last inserted
        last = sorted(__tmp0.db[__tmp2], key=lambda e: e.timestamp)[-1]
        __tmp0.replace(__tmp2, last.id, __tmp3)
