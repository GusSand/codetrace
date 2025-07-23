"""Distance util functions."""

import logging
from numbers import Number

from homeassistant.const import (
    LENGTH_KILOMETERS,
    LENGTH_MILES,
    LENGTH_FEET,
    LENGTH_METERS,
    UNIT_NOT_RECOGNIZED_TEMPLATE,
    LENGTH,
)

_LOGGER = logging.getLogger(__name__)

VALID_UNITS = [
    LENGTH_KILOMETERS,
    LENGTH_MILES,
    LENGTH_FEET,
    LENGTH_METERS,
]


def __tmp0(__tmp5, __tmp8: str, __tmp1: str) -> float:
    """Convert one unit of measurement to another."""
    if __tmp8 not in VALID_UNITS:
        raise ValueError(
            UNIT_NOT_RECOGNIZED_TEMPLATE.format(__tmp8, LENGTH))
    if __tmp1 not in VALID_UNITS:
        raise ValueError(
            UNIT_NOT_RECOGNIZED_TEMPLATE.format(__tmp1, LENGTH))

    if not isinstance(__tmp5, Number):
        raise TypeError('{} is not of numeric type'.format(__tmp5))

    if __tmp8 == __tmp1 or __tmp8 not in VALID_UNITS:
        return __tmp5

    __tmp4 = __tmp5

    if __tmp8 == LENGTH_MILES:
        __tmp4 = __tmp10(__tmp5)
    elif __tmp8 == LENGTH_FEET:
        __tmp4 = __tmp9(__tmp5)
    elif __tmp8 == LENGTH_KILOMETERS:
        __tmp4 = __kilometers_to_meters(__tmp5)

    result = __tmp4

    if __tmp1 == LENGTH_MILES:
        result = __tmp3(__tmp4)
    elif __tmp1 == LENGTH_FEET:
        result = __meters_to_feet(__tmp4)
    elif __tmp1 == LENGTH_KILOMETERS:
        result = __meters_to_kilometers(__tmp4)

    return result


def __tmp10(__tmp2: float) :
    """Convert miles to meters."""
    return __tmp2 * 1609.344


def __tmp9(__tmp6: <FILL>) :
    """Convert feet to meters."""
    return __tmp6 * 0.3048


def __kilometers_to_meters(__tmp7: float) :
    """Convert kilometers to meters."""
    return __tmp7 * 1000


def __tmp3(__tmp4) -> float:
    """Convert meters to miles."""
    return __tmp4 * 0.000621371


def __meters_to_feet(__tmp4: float) -> float:
    """Convert meters to feet."""
    return __tmp4 * 3.28084


def __meters_to_kilometers(__tmp4: float) -> float:
    """Convert meters to kilometers."""
    return __tmp4 * 0.001
