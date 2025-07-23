from typing import TypeAlias
__typ0 : TypeAlias = "Event"
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

    def __init__(__tmp1, __tmp10: bool) -> None:
        __tmp1.logger = logger.getChild(__tmp1.sid)
        # self.logger.warning("Using in-memory storage, any events stored will not be persistent and will be lost when server is shut down. Use the --storage parameter to set a different storage method.")
        __tmp1.db: Dict[str, List[__typ0]] = {}
        __tmp1._metadata: Dict[str, dict] = dict()

    def __tmp5(
        __tmp1,
        __tmp0,
        __tmp6,
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
            "type": __tmp6,
            "client": client,
            "hostname": hostname,
            "created": created,
            "data": data or {},
        }
        __tmp1.db[__tmp0] = []

    def __tmp9(
        __tmp1,
        __tmp0: str,
        __tmp6: Optional[str] = None,
        client: Optional[str] = None,
        hostname: Optional[str] = None,
        name: Optional[str] = None,
        data: Optional[dict] = None,
    ) -> None:
        if __tmp0 in __tmp1._metadata:
            if __tmp6:
                __tmp1._metadata[__tmp0]["type"] = __tmp6
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

    def __tmp4(__tmp1, __tmp0: str) :
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
        __tmp0: str,
        __tmp7,
    ) -> Optional[__typ0]:
        event = __tmp1._get_event(__tmp0, __tmp7)
        return copy.deepcopy(event)

    def __tmp3(
        __tmp1,
        __tmp8: str,
        limit: __typ1,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) -> List[__typ0]:
        events = __tmp1.db[__tmp8]

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

    def __tmp11(
        __tmp1,
        __tmp8: <FILL>,
        starttime: Optional[datetime] = None,
        endtime: Optional[datetime] = None,
    ) -> __typ1:
        return len(
            [
                e
                for e in __tmp1.db[__tmp8]
                if (not starttime or starttime <= e.timestamp)
                and (not endtime or e.timestamp <= endtime)
            ]
        )

    def get_metadata(__tmp1, __tmp0: str):
        if __tmp0 in __tmp1._metadata:
            return __tmp1._metadata[__tmp0]
        else:
            raise Exception("Bucket did not exist, could not get metadata")

    def __tmp2(__tmp1, __tmp8: str, event: __typ0) -> __typ0:
        if event.id is not None:
            __tmp1.replace(__tmp8, event.id, event)
        else:
            # We need to copy the event to avoid setting the ID on the passed event
            event = copy.copy(event)
            if __tmp1.db[__tmp8]:
                event.id = max(__typ1(e.id or 0) for e in __tmp1.db[__tmp8]) + 1
            else:
                event.id = 0
            __tmp1.db[__tmp8].append(event)
        return event

    def delete(__tmp1, __tmp0, __tmp7):
        for idx in (
            idx
            for idx, event in reversed(list(enumerate(__tmp1.db[__tmp0])))
            if event.id == __tmp7
        ):
            __tmp1.db[__tmp0].pop(idx)
            return True
        return False

    def _get_event(__tmp1, __tmp0, __tmp7) -> Optional[__typ0]:
        events = [
            event
            for idx, event in reversed(list(enumerate(__tmp1.db[__tmp0])))
            if event.id == __tmp7
        ]
        if len(events) < 1:
            return None
        else:
            return events[0]

    def replace(__tmp1, __tmp0, __tmp7, event):
        for idx in (
            idx
            for idx, event in reversed(list(enumerate(__tmp1.db[__tmp0])))
            if event.id == __tmp7
        ):
            # We need to copy the event to avoid setting the ID on the passed event
            event = copy.copy(event)
            event.id = __tmp7
            __tmp1.db[__tmp0][idx] = event

    def replace_last(__tmp1, __tmp0, event):
        # NOTE: This does not actually get the most recent event, only the last inserted
        last = sorted(__tmp1.db[__tmp0], key=lambda e: e.timestamp)[-1]
        __tmp1.replace(__tmp0, last.id, event)
