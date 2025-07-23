from typing import TypeAlias
__typ0 : TypeAlias = "datetime"
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
Id = Optional[Union[int, str]]
ConvertibleTimestamp = Union[__typ0, str]
Duration = Union[timedelta, Number]
Data = Dict[str, Any]


def __tmp6(__tmp2) -> __typ0:
    """
    Takes something representing a timestamp and
    returns a timestamp in the representation we want.
    """
    ts = iso8601.parse_date(__tmp2) if isinstance(__tmp2, str) else __tmp2
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

    def __tmp5(
        __tmp0,
        id: Optional[Id] = None,
        timestamp: Optional[ConvertibleTimestamp] = None,
        duration: Duration = 0,
        data: Data = dict(),
    ) -> None:
        __tmp0.id = id
        if timestamp is None:
            logger.warning(
                "Event initializer did not receive a timestamp argument, "
                "using now as timestamp"
            )
            # FIXME: The typing.cast here was required for mypy to shut up, weird...
            __tmp0.timestamp = __typ0.now(typing.cast(timezone, timezone.utc))
        else:
            # The conversion needs to be explicit here for mypy to pick it up
            # (lacks support for properties)
            __tmp0.timestamp = __tmp6(timestamp)
        __tmp0.duration = duration  # type: ignore
        __tmp0.data = data

    def __tmp1(__tmp0, __tmp3: object) -> bool:
        if isinstance(__tmp3, Event):
            return (
                __tmp0.timestamp == __tmp3.timestamp
                and __tmp0.duration == __tmp3.duration
                and __tmp0.data == __tmp3.data
            )
        else:
            raise TypeError(
                "operator not supported between instances of '{}' and '{}'".format(
                    type(__tmp0), type(__tmp3)
                )
            )

    def __lt__(__tmp0, __tmp3: object) -> bool:
        if isinstance(__tmp3, Event):
            return __tmp0.timestamp < __tmp3.timestamp
        else:
            raise TypeError(
                "operator not supported between instances of '{}' and '{}'".format(
                    type(__tmp0), type(__tmp3)
                )
            )

    def to_json_dict(__tmp0) -> dict:
        """Useful when sending data over the wire.
        Any mongodb interop should not use do this as it accepts datetimes."""
        json_data = __tmp0.copy()
        json_data["timestamp"] = __tmp0.timestamp.astimezone(timezone.utc).isoformat()
        json_data["duration"] = __tmp0.duration.total_seconds()
        return json_data

    def to_json_str(__tmp0) -> str:
        data = __tmp0.to_json_dict()
        return json.dumps(data)

    def _hasprop(__tmp0, __tmp4: str) -> bool:
        """Badly named, but basically checks if the underlying
        dict has a prop, and if it is a non-empty list"""
        return __tmp4 in __tmp0 and __tmp0[__tmp4] is not None

    @property
    def id(__tmp0) -> Id:
        return __tmp0["id"] if __tmp0._hasprop("id") else None

    @id.setter
    def id(__tmp0, id: Id) :
        __tmp0["id"] = id

    @property
    def data(__tmp0) -> dict:
        return __tmp0["data"] if __tmp0._hasprop("data") else {}

    @data.setter
    def data(__tmp0, data: dict) -> None:
        __tmp0["data"] = data

    @property
    def timestamp(__tmp0) :
        return __tmp0["timestamp"]

    @timestamp.setter
    def timestamp(__tmp0, timestamp: ConvertibleTimestamp) :
        __tmp0["timestamp"] = __tmp6(timestamp).astimezone(timezone.utc)

    @property
    def duration(__tmp0) -> timedelta:
        return __tmp0["duration"] if __tmp0._hasprop("duration") else timedelta(0)

    @duration.setter
    def duration(__tmp0, duration: <FILL>) -> None:
        if isinstance(duration, timedelta):
            __tmp0["duration"] = duration
        elif isinstance(duration, numbers.Real):
            __tmp0["duration"] = timedelta(seconds=duration)  # type: ignore
        else:
            raise TypeError(f"Couldn't parse duration of invalid type {type(duration)}")
