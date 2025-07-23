from typing import TypeAlias
__typ1 : TypeAlias = "object"
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
__typ2 = Optional[Union[int, str]]
__typ0 = Union[datetime, str]
Duration = Union[timedelta, Number]
Data = Dict[str, Any]


def _timestamp_parse(ts_in: __typ0) -> datetime:
    """
    Takes something representing a timestamp and
    returns a timestamp in the representation we want.
    """
    ts = iso8601.parse_date(ts_in) if isinstance(ts_in, str) else ts_in
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


class Event(dict):
    """
    Used to represents an event.
    """

    def __init__(
        __tmp1,
        id: Optional[__typ2] = None,
        timestamp: Optional[__typ0] = None,
        duration: Duration = 0,
        data: Data = dict(),
    ) :
        __tmp1.id = id
        if timestamp is None:
            logger.warning(
                "Event initializer did not receive a timestamp argument, "
                "using now as timestamp"
            )
            # FIXME: The typing.cast here was required for mypy to shut up, weird...
            __tmp1.timestamp = datetime.now(typing.cast(timezone, timezone.utc))
        else:
            # The conversion needs to be explicit here for mypy to pick it up
            # (lacks support for properties)
            __tmp1.timestamp = _timestamp_parse(timestamp)
        __tmp1.duration = duration  # type: ignore
        __tmp1.data = data

    def __eq__(__tmp1, other) :
        if isinstance(other, Event):
            return (
                __tmp1.timestamp == other.timestamp
                and __tmp1.duration == other.duration
                and __tmp1.data == other.data
            )
        else:
            raise TypeError(
                "operator not supported between instances of '{}' and '{}'".format(
                    type(__tmp1), type(other)
                )
            )

    def __tmp0(__tmp1, other) :
        if isinstance(other, Event):
            return __tmp1.timestamp < other.timestamp
        else:
            raise TypeError(
                "operator not supported between instances of '{}' and '{}'".format(
                    type(__tmp1), type(other)
                )
            )

    def to_json_dict(__tmp1) :
        """Useful when sending data over the wire.
        Any mongodb interop should not use do this as it accepts datetimes."""
        json_data = __tmp1.copy()
        json_data["timestamp"] = __tmp1.timestamp.astimezone(timezone.utc).isoformat()
        json_data["duration"] = __tmp1.duration.total_seconds()
        return json_data

    def __tmp2(__tmp1) -> str:
        data = __tmp1.to_json_dict()
        return json.dumps(data)

    def _hasprop(__tmp1, propname: <FILL>) -> bool:
        """Badly named, but basically checks if the underlying
        dict has a prop, and if it is a non-empty list"""
        return propname in __tmp1 and __tmp1[propname] is not None

    @property
    def id(__tmp1) -> __typ2:
        return __tmp1["id"] if __tmp1._hasprop("id") else None

    @id.setter
    def id(__tmp1, id) -> None:
        __tmp1["id"] = id

    @property
    def data(__tmp1) :
        return __tmp1["data"] if __tmp1._hasprop("data") else {}

    @data.setter
    def data(__tmp1, data) -> None:
        __tmp1["data"] = data

    @property
    def timestamp(__tmp1) :
        return __tmp1["timestamp"]

    @timestamp.setter
    def timestamp(__tmp1, timestamp) -> None:
        __tmp1["timestamp"] = _timestamp_parse(timestamp).astimezone(timezone.utc)

    @property
    def duration(__tmp1) -> timedelta:
        return __tmp1["duration"] if __tmp1._hasprop("duration") else timedelta(0)

    @duration.setter
    def duration(__tmp1, duration: Duration) :
        if isinstance(duration, timedelta):
            __tmp1["duration"] = duration
        elif isinstance(duration, numbers.Real):
            __tmp1["duration"] = timedelta(seconds=duration)  # type: ignore
        else:
            raise TypeError(f"Couldn't parse duration of invalid type {type(duration)}")
