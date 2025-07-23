from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ1 : TypeAlias = "dict"
__typ0 : TypeAlias = "str"
__typ4 : TypeAlias = "datetime"
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
__typ5 = Optional[Union[int, __typ0]]
ConvertibleTimestamp = Union[__typ4, __typ0]
Duration = Union[timedelta, Number]
Data = Dict[__typ0, Any]


def __tmp8(__tmp3: ConvertibleTimestamp) -> __typ4:
    """
    Takes something representing a timestamp and
    returns a timestamp in the representation we want.
    """
    ts = iso8601.parse_date(__tmp3) if isinstance(__tmp3, __typ0) else __tmp3
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


class __typ3(__typ1):
    """
    Used to represents an event.
    """

    def __tmp6(
        __tmp1,
        id: Optional[__typ5] = None,
        timestamp: Optional[ConvertibleTimestamp] = None,
        duration: Duration = 0,
        data: Data = __typ1(),
    ) :
        __tmp1.id = id
        if timestamp is None:
            logger.warning(
                "Event initializer did not receive a timestamp argument, "
                "using now as timestamp"
            )
            # FIXME: The typing.cast here was required for mypy to shut up, weird...
            __tmp1.timestamp = __typ4.now(typing.cast(timezone, timezone.utc))
        else:
            # The conversion needs to be explicit here for mypy to pick it up
            # (lacks support for properties)
            __tmp1.timestamp = __tmp8(timestamp)
        __tmp1.duration = duration  # type: ignore
        __tmp1.data = data

    def __tmp2(__tmp1, __tmp5: object) -> __typ2:
        if isinstance(__tmp5, __typ3):
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

    def __tmp0(__tmp1, __tmp5: <FILL>) -> __typ2:
        if isinstance(__tmp5, __typ3):
            return __tmp1.timestamp < __tmp5.timestamp
        else:
            raise TypeError(
                "operator not supported between instances of '{}' and '{}'".format(
                    type(__tmp1), type(__tmp5)
                )
            )

    def to_json_dict(__tmp1) -> __typ1:
        """Useful when sending data over the wire.
        Any mongodb interop should not use do this as it accepts datetimes."""
        json_data = __tmp1.copy()
        json_data["timestamp"] = __tmp1.timestamp.astimezone(timezone.utc).isoformat()
        json_data["duration"] = __tmp1.duration.total_seconds()
        return json_data

    def __tmp4(__tmp1) -> __typ0:
        data = __tmp1.to_json_dict()
        return json.dumps(data)

    def _hasprop(__tmp1, __tmp7: __typ0) -> __typ2:
        """Badly named, but basically checks if the underlying
        dict has a prop, and if it is a non-empty list"""
        return __tmp7 in __tmp1 and __tmp1[__tmp7] is not None

    @property
    def id(__tmp1) -> __typ5:
        return __tmp1["id"] if __tmp1._hasprop("id") else None

    @id.setter
    def id(__tmp1, id: __typ5) :
        __tmp1["id"] = id

    @property
    def data(__tmp1) -> __typ1:
        return __tmp1["data"] if __tmp1._hasprop("data") else {}

    @data.setter
    def data(__tmp1, data: __typ1) -> None:
        __tmp1["data"] = data

    @property
    def timestamp(__tmp1) -> __typ4:
        return __tmp1["timestamp"]

    @timestamp.setter
    def timestamp(__tmp1, timestamp) -> None:
        __tmp1["timestamp"] = __tmp8(timestamp).astimezone(timezone.utc)

    @property
    def duration(__tmp1) -> timedelta:
        return __tmp1["duration"] if __tmp1._hasprop("duration") else timedelta(0)

    @duration.setter
    def duration(__tmp1, duration) -> None:
        if isinstance(duration, timedelta):
            __tmp1["duration"] = duration
        elif isinstance(duration, numbers.Real):
            __tmp1["duration"] = timedelta(seconds=duration)  # type: ignore
        else:
            raise TypeError(f"Couldn't parse duration of invalid type {type(duration)}")
