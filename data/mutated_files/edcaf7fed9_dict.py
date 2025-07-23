from typing import TypeAlias
__typ4 : TypeAlias = "bool"
__typ1 : TypeAlias = "str"
__typ2 : TypeAlias = "timedelta"
__typ7 : TypeAlias = "datetime"
__typ5 : TypeAlias = "object"
import json
import logging
import numbers
import typing
from datetime import datetime, timedelta, timezone
from typing import (
    Any,
    Dict,
    Optional,
    Union,
)

import iso8601

logger = logging.getLogger(__name__)


Number = Union[int, float]
__typ8 = Optional[Union[int, __typ1]]
__typ0 = Union[__typ7, __typ1]
__typ3 = Union[__typ2, Number]
Data = Dict[__typ1, Any]


def __tmp8(__tmp3: __typ0) -> __typ7:
    """
    Takes something representing a timestamp and
    returns a timestamp in the representation we want.
    """
    ts = iso8601.parse_date(__tmp3) if isinstance(__tmp3, __typ1) else __tmp3
    # Set resolution to milliseconds instead of microseconds
    # (Fixes incompability with software based on unix time, for example mongodb)
    ts = ts.replace(microsecond=int(ts.microsecond / 1000) * 1000)
    # Add timezone if not set
    if not ts.tzinfo:
        # Needed? All timestamps should be iso8601 so ought to always contain timezone.
        # Yes, because it is optional in iso8601
        logger.warning(f"timestamp without timezone found, using UTC: {ts}")
        ts = ts.replace(tzinfo=timezone.utc)
    return ts


class __typ6(dict):
    """
    Used to represents an event.
    """

    def __tmp6(
        __tmp1,
        id: Optional[__typ8] = None,
        timestamp: Optional[__typ0] = None,
        duration: __typ3 = 0,
        data: Data = dict(),
    ) -> None:
        __tmp1.id = id
        if timestamp is None:
            logger.warning(
                "Event initializer did not receive a timestamp argument, "
                "using now as timestamp"
            )
            # FIXME: The typing.cast here was required for mypy to shut up, weird...
            __tmp1.timestamp = __typ7.now(typing.cast(timezone, timezone.utc))
        else:
            # The conversion needs to be explicit here for mypy to pick it up
            # (lacks support for properties)
            __tmp1.timestamp = __tmp8(timestamp)
        __tmp1.duration = duration  # type: ignore
        __tmp1.data = data

    def __tmp2(__tmp1, __tmp5: __typ5) -> __typ4:
        if isinstance(__tmp5, __typ6):
            return (
                __tmp1.timestamp == __tmp5.timestamp
                and __tmp1.duration == __tmp5.duration
                and __tmp1.data == __tmp5.data
            )
        else:
            raise TypeError(
                "operator not supported between instances of '{}' and '{}'".format(
                    type(__tmp1), type(__tmp5)
                )
            )

    def __tmp0(__tmp1, __tmp5: __typ5) -> __typ4:
        if isinstance(__tmp5, __typ6):
            return __tmp1.timestamp < __tmp5.timestamp
        else:
            raise TypeError(
                "operator not supported between instances of '{}' and '{}'".format(
                    type(__tmp1), type(__tmp5)
                )
            )

    def to_json_dict(__tmp1) -> dict:
        """Useful when sending data over the wire.
        Any mongodb interop should not use do this as it accepts datetimes."""
        json_data = __tmp1.copy()
        json_data["timestamp"] = __tmp1.timestamp.astimezone(timezone.utc).isoformat()
        json_data["duration"] = __tmp1.duration.total_seconds()
        return json_data

    def __tmp4(__tmp1) -> __typ1:
        data = __tmp1.to_json_dict()
        return json.dumps(data)

    def _hasprop(__tmp1, __tmp7: __typ1) :
        """Badly named, but basically checks if the underlying
        dict has a prop, and if it is a non-empty list"""
        return __tmp7 in __tmp1 and __tmp1[__tmp7] is not None

    @property
    def id(__tmp1) :
        return __tmp1["id"] if __tmp1._hasprop("id") else None

    @id.setter
    def id(__tmp1, id: __typ8) -> None:
        __tmp1["id"] = id

    @property
    def data(__tmp1) -> dict:
        return __tmp1["data"] if __tmp1._hasprop("data") else {}

    @data.setter
    def data(__tmp1, data: <FILL>) -> None:
        __tmp1["data"] = data

    @property
    def timestamp(__tmp1) -> __typ7:
        return __tmp1["timestamp"]

    @timestamp.setter
    def timestamp(__tmp1, timestamp: __typ0) -> None:
        __tmp1["timestamp"] = __tmp8(timestamp).astimezone(timezone.utc)

    @property
    def duration(__tmp1) :
        return __tmp1["duration"] if __tmp1._hasprop("duration") else __typ2(0)

    @duration.setter
    def duration(__tmp1, duration: __typ3) -> None:
        if isinstance(duration, __typ2):
            __tmp1["duration"] = duration
        elif isinstance(duration, numbers.Real):
            __tmp1["duration"] = __typ2(seconds=duration)  # type: ignore
        else:
            raise TypeError(f"Couldn't parse duration of invalid type {type(duration)}")
