from typing import TypeAlias
__typ1 : TypeAlias = "str"
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
__typ2 = Optional[Union[int, __typ1]]
__typ3 = Union[datetime, __typ1]
Duration = Union[timedelta, Number]
Data = Dict[__typ1, Any]


def __tmp6(__tmp2) :
    """
    Takes something representing a timestamp and
    returns a timestamp in the representation we want.
    """
    ts = iso8601.parse_date(__tmp2) if isinstance(__tmp2, __typ1) else __tmp2
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


class __typ0(dict):
    """
    Used to represents an event.
    """

    def __init__(
        __tmp0,
        id: Optional[__typ2] = None,
        timestamp: Optional[__typ3] = None,
        duration: Duration = 0,
        data: Data = dict(),
    ) :
        __tmp0.id = id
        if timestamp is None:
            logger.warning(
                "Event initializer did not receive a timestamp argument, "
                "using now as timestamp"
            )
            # FIXME: The typing.cast here was required for mypy to shut up, weird...
            __tmp0.timestamp = datetime.now(typing.cast(timezone, timezone.utc))
        else:
            # The conversion needs to be explicit here for mypy to pick it up
            # (lacks support for properties)
            __tmp0.timestamp = __tmp6(timestamp)
        __tmp0.duration = duration  # type: ignore
        __tmp0.data = data

    def __tmp1(__tmp0, __tmp4: <FILL>) -> bool:
        if isinstance(__tmp4, __typ0):
            return (
                __tmp0.timestamp == __tmp4.timestamp
                and __tmp0.duration == __tmp4.duration
                and __tmp0.data == __tmp4.data
            )
        else:
            raise TypeError(
                "operator not supported between instances of '{}' and '{}'".format(
                    type(__tmp0), type(__tmp4)
                )
            )

    def __lt__(__tmp0, __tmp4) -> bool:
        if isinstance(__tmp4, __typ0):
            return __tmp0.timestamp < __tmp4.timestamp
        else:
            raise TypeError(
                "operator not supported between instances of '{}' and '{}'".format(
                    type(__tmp0), type(__tmp4)
                )
            )

    def to_json_dict(__tmp0) -> dict:
        """Useful when sending data over the wire.
        Any mongodb interop should not use do this as it accepts datetimes."""
        json_data = __tmp0.copy()
        json_data["timestamp"] = __tmp0.timestamp.astimezone(timezone.utc).isoformat()
        json_data["duration"] = __tmp0.duration.total_seconds()
        return json_data

    def __tmp3(__tmp0) -> __typ1:
        data = __tmp0.to_json_dict()
        return json.dumps(data)

    def _hasprop(__tmp0, __tmp5) -> bool:
        """Badly named, but basically checks if the underlying
        dict has a prop, and if it is a non-empty list"""
        return __tmp5 in __tmp0 and __tmp0[__tmp5] is not None

    @property
    def id(__tmp0) -> __typ2:
        return __tmp0["id"] if __tmp0._hasprop("id") else None

    @id.setter
    def id(__tmp0, id: __typ2) :
        __tmp0["id"] = id

    @property
    def data(__tmp0) :
        return __tmp0["data"] if __tmp0._hasprop("data") else {}

    @data.setter
    def data(__tmp0, data: dict) :
        __tmp0["data"] = data

    @property
    def timestamp(__tmp0) :
        return __tmp0["timestamp"]

    @timestamp.setter
    def timestamp(__tmp0, timestamp) :
        __tmp0["timestamp"] = __tmp6(timestamp).astimezone(timezone.utc)

    @property
    def duration(__tmp0) :
        return __tmp0["duration"] if __tmp0._hasprop("duration") else timedelta(0)

    @duration.setter
    def duration(__tmp0, duration: Duration) -> None:
        if isinstance(duration, timedelta):
            __tmp0["duration"] = duration
        elif isinstance(duration, numbers.Real):
            __tmp0["duration"] = timedelta(seconds=duration)  # type: ignore
        else:
            raise TypeError(f"Couldn't parse duration of invalid type {type(duration)}")
