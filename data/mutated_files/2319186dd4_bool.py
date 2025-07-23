from typing import TypeAlias
__typ0 : TypeAlias = "Event"
__typ2 : TypeAlias = "str"
__typ1 : TypeAlias = "int"
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

    def __init__(__tmp2, testing: <FILL>) -> None:
        __tmp2.logger = logger.getChild(__tmp2.sid)
        # self.logger.warning("Using in-memory storage, any events stored will not be persistent and will be lost when server is shut down. Use the --storage parameter to set a different storage method.")
        __tmp2.db: Dict[__typ2, List[__typ0]] = {}
        __tmp2._metadata: Dict[__typ2, dict] = dict()

    def __tmp5(
        __tmp2,
        __tmp0,
        __tmp6,
        __tmp8,
        hostname,
        created,
        name=None,
        data=None,
    ) -> None:
        if not name:
            name = __tmp0
        __tmp2._metadata[__tmp0] = {
            "id": __tmp0,
            "name": name,
            "type": __tmp6,
            "client": __tmp8,
            "hostname": hostname,
            "created": created,
            "data": data or {},
        }
        __tmp2.db[__tmp0] = []

    def update_bucket(
        __tmp2,
        __tmp0: __typ2,
        __tmp6: Optional[__typ2] = None,
        __tmp8: Optional[__typ2] = None,
        hostname: Optional[__typ2] = None,
        name: Optional[__typ2] = None,
        data: Optional[dict] = None,
    ) -> None:
        if __tmp0 in __tmp2._metadata:
            if __tmp6:
                __tmp2._metadata[__tmp0]["type"] = __tmp6
            if __tmp8:
                __tmp2._metadata[__tmp0]["client"] = __tmp8
            if hostname:
                __tmp2._metadata[__tmp0]["hostname"] = hostname
            if name:
                __tmp2._metadata[__tmp0]["name"] = name
            if data:
                __tmp2._metadata[__tmp0]["data"] = data
        else:
            raise Exception("Bucket did not exist, could not update")

    def __tmp9(__tmp2, __tmp0: __typ2) -> None:
        if __tmp0 in __tmp2.db:
            del __tmp2.db[__tmp0]
        if __tmp0 in __tmp2._metadata:
            del __tmp2._metadata[__tmp0]
        else:
            raise Exception("Bucket did not exist, could not delete")

    def __tmp1(__tmp2):
        __tmp1 = dict()
        for __tmp0 in __tmp2.db:
            __tmp1[__tmp0] = __tmp2.get_metadata(__tmp0)
        return __tmp1

    def __tmp11(
        __tmp2,
        __tmp0: __typ2,
        __tmp7,
    ) -> Optional[__typ0]:
        __tmp3 = __tmp2._get_event(__tmp0, __tmp7)
        return copy.deepcopy(__tmp3)

    def get_events(
        __tmp2,
        bucket: __typ2,
        __tmp4,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) :
        events = __tmp2.db[bucket]

        # Sort by timestamp
        events = sorted(events, key=lambda k: k["timestamp"])[::-1]

        # Filter by date
        if starttime:
            events = [e for e in events if starttime <= (e.timestamp + e.duration)]
        if endtime:
            events = [e for e in events if e.timestamp <= endtime]

        # Limit
        if __tmp4 == 0:
            return []
        elif __tmp4 < 0:
            __tmp4 = sys.maxsize
        events = events[:__tmp4]
        # Return
        return copy.deepcopy(events)

    def __tmp10(
        __tmp2,
        bucket: __typ2,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) -> __typ1:
        return len(
            [
                e
                for e in __tmp2.db[bucket]
                if (not starttime or starttime <= e.timestamp)
                and (not endtime or e.timestamp <= endtime)
            ]
        )

    def get_metadata(__tmp2, __tmp0: __typ2):
        if __tmp0 in __tmp2._metadata:
            return __tmp2._metadata[__tmp0]
        else:
            raise Exception("Bucket did not exist, could not get metadata")

    def insert_one(__tmp2, bucket: __typ2, __tmp3: __typ0) -> __typ0:
        if __tmp3.id is not None:
            __tmp2.replace(bucket, __tmp3.id, __tmp3)
        else:
            # We need to copy the event to avoid setting the ID on the passed event
            __tmp3 = copy.copy(__tmp3)
            if __tmp2.db[bucket]:
                __tmp3.id = max(__typ1(e.id or 0) for e in __tmp2.db[bucket]) + 1
            else:
                __tmp3.id = 0
            __tmp2.db[bucket].append(__tmp3)
        return __tmp3

    def delete(__tmp2, __tmp0, __tmp7):
        for idx in (
            idx
            for idx, __tmp3 in reversed(list(enumerate(__tmp2.db[__tmp0])))
            if __tmp3.id == __tmp7
        ):
            __tmp2.db[__tmp0].pop(idx)
            return True
        return False

    def _get_event(__tmp2, __tmp0, __tmp7) -> Optional[__typ0]:
        events = [
            __tmp3
            for idx, __tmp3 in reversed(list(enumerate(__tmp2.db[__tmp0])))
            if __tmp3.id == __tmp7
        ]
        if len(events) < 1:
            return None
        else:
            return events[0]

    def replace(__tmp2, __tmp0, __tmp7, __tmp3):
        for idx in (
            idx
            for idx, __tmp3 in reversed(list(enumerate(__tmp2.db[__tmp0])))
            if __tmp3.id == __tmp7
        ):
            # We need to copy the event to avoid setting the ID on the passed event
            __tmp3 = copy.copy(__tmp3)
            __tmp3.id = __tmp7
            __tmp2.db[__tmp0][idx] = __tmp3

    def replace_last(__tmp2, __tmp0, __tmp3):
        # NOTE: This does not actually get the most recent event, only the last inserted
        last = sorted(__tmp2.db[__tmp0], key=lambda e: e.timestamp)[-1]
        __tmp2.replace(__tmp0, last.id, __tmp3)
