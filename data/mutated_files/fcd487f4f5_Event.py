from typing import TypeAlias
__typ1 : TypeAlias = "str"
__typ0 : TypeAlias = "int"
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

    def __init__(__tmp2, __tmp12) :
        __tmp2.logger = logger.getChild(__tmp2.sid)
        # self.logger.warning("Using in-memory storage, any events stored will not be persistent and will be lost when server is shut down. Use the --storage parameter to set a different storage method.")
        __tmp2.db: Dict[__typ1, List[Event]] = {}
        __tmp2._metadata: Dict[__typ1, dict] = dict()

    def __tmp8(
        __tmp2,
        __tmp0,
        __tmp9,
        client,
        hostname,
        __tmp15,
        name=None,
        data=None,
    ) :
        if not name:
            name = __tmp0
        __tmp2._metadata[__tmp0] = {
            "id": __tmp0,
            "name": name,
            "type": __tmp9,
            "client": client,
            "hostname": hostname,
            "created": __tmp15,
            "data": data or {},
        }
        __tmp2.db[__tmp0] = []

    def update_bucket(
        __tmp2,
        __tmp0,
        __tmp9: Optional[__typ1] = None,
        client: Optional[__typ1] = None,
        hostname: Optional[__typ1] = None,
        name: Optional[__typ1] = None,
        data: Optional[dict] = None,
    ) :
        if __tmp0 in __tmp2._metadata:
            if __tmp9:
                __tmp2._metadata[__tmp0]["type"] = __tmp9
            if client:
                __tmp2._metadata[__tmp0]["client"] = client
            if hostname:
                __tmp2._metadata[__tmp0]["hostname"] = hostname
            if name:
                __tmp2._metadata[__tmp0]["name"] = name
            if data:
                __tmp2._metadata[__tmp0]["data"] = data
        else:
            raise Exception("Bucket did not exist, could not update")

    def delete_bucket(__tmp2, __tmp0) :
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

    def __tmp3(
        __tmp2,
        __tmp0: __typ1,
        __tmp10,
    ) :
        __tmp4 = __tmp2._get_event(__tmp0, __tmp10)
        return copy.deepcopy(__tmp4)

    def __tmp5(
        __tmp2,
        __tmp11,
        __tmp7,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) :
        events = __tmp2.db[__tmp11]

        # Sort by timestamp
        events = sorted(events, key=lambda k: k["timestamp"])[::-1]

        # Filter by date
        if starttime:
            events = [e for e in events if starttime <= (e.timestamp + e.duration)]
        if endtime:
            events = [e for e in events if e.timestamp <= endtime]

        # Limit
        if __tmp7 == 0:
            return []
        elif __tmp7 < 0:
            __tmp7 = sys.maxsize
        events = events[:__tmp7]
        # Return
        return copy.deepcopy(events)

    def __tmp13(
        __tmp2,
        __tmp11,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) :
        return len(
            [
                e
                for e in __tmp2.db[__tmp11]
                if (not starttime or starttime <= e.timestamp)
                and (not endtime or e.timestamp <= endtime)
            ]
        )

    def get_metadata(__tmp2, __tmp0):
        if __tmp0 in __tmp2._metadata:
            return __tmp2._metadata[__tmp0]
        else:
            raise Exception("Bucket did not exist, could not get metadata")

    def __tmp6(__tmp2, __tmp11, __tmp4: <FILL>) :
        if __tmp4.id is not None:
            __tmp2.replace(__tmp11, __tmp4.id, __tmp4)
        else:
            # We need to copy the event to avoid setting the ID on the passed event
            __tmp4 = copy.copy(__tmp4)
            if __tmp2.db[__tmp11]:
                __tmp4.id = max(__typ0(e.id or 0) for e in __tmp2.db[__tmp11]) + 1
            else:
                __tmp4.id = 0
            __tmp2.db[__tmp11].append(__tmp4)
        return __tmp4

    def __tmp14(__tmp2, __tmp0, __tmp10):
        for idx in (
            idx
            for idx, __tmp4 in reversed(list(enumerate(__tmp2.db[__tmp0])))
            if __tmp4.id == __tmp10
        ):
            __tmp2.db[__tmp0].pop(idx)
            return True
        return False

    def _get_event(__tmp2, __tmp0, __tmp10) :
        events = [
            __tmp4
            for idx, __tmp4 in reversed(list(enumerate(__tmp2.db[__tmp0])))
            if __tmp4.id == __tmp10
        ]
        if len(events) < 1:
            return None
        else:
            return events[0]

    def replace(__tmp2, __tmp0, __tmp10, __tmp4):
        for idx in (
            idx
            for idx, __tmp4 in reversed(list(enumerate(__tmp2.db[__tmp0])))
            if __tmp4.id == __tmp10
        ):
            # We need to copy the event to avoid setting the ID on the passed event
            __tmp4 = copy.copy(__tmp4)
            __tmp4.id = __tmp10
            __tmp2.db[__tmp0][idx] = __tmp4

    def replace_last(__tmp2, __tmp0, __tmp4):
        # NOTE: This does not actually get the most recent event, only the last inserted
        last = sorted(__tmp2.db[__tmp0], key=lambda e: e.timestamp)[-1]
        __tmp2.replace(__tmp0, last.id, __tmp4)
