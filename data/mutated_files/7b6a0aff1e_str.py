from typing import TypeAlias
__typ0 : TypeAlias = "float"
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


def convert(__tmp3, __tmp7: str, __tmp0: <FILL>) -> __typ0:
    """Convert one unit of measurement to another."""
    if __tmp7 not in VALID_UNITS:
        raise ValueError(
            UNIT_NOT_RECOGNIZED_TEMPLATE.format(__tmp7, LENGTH))
    if __tmp0 not in VALID_UNITS:
        raise ValueError(
            UNIT_NOT_RECOGNIZED_TEMPLATE.format(__tmp0, LENGTH))

    if not isinstance(__tmp3, Number):
        raise TypeError('{} is not of numeric type'.format(__tmp3))

    if __tmp7 == __tmp0 or __tmp7 not in VALID_UNITS:
        return __tmp3

    __tmp4 = __tmp3

    if __tmp7 == LENGTH_MILES:
        __tmp4 = __tmp9(__tmp3)
    elif __tmp7 == LENGTH_FEET:
        __tmp4 = __tmp8(__tmp3)
    elif __tmp7 == LENGTH_KILOMETERS:
        __tmp4 = __tmp11(__tmp3)

    result = __tmp4

    if __tmp0 == LENGTH_MILES:
        result = __tmp2(__tmp4)
    elif __tmp0 == LENGTH_FEET:
        result = __tmp10(__tmp4)
    elif __tmp0 == LENGTH_KILOMETERS:
        result = __meters_to_kilometers(__tmp4)

    return result


def __tmp9(__tmp1: __typ0) :
    """Convert miles to meters."""
    return __tmp1 * 1609.344


def __tmp8(__tmp5: __typ0) :
    """Convert feet to meters."""
    return __tmp5 * 0.3048


def __tmp11(__tmp6) :
    """Convert kilometers to meters."""
    return __tmp6 * 1000


def __tmp2(__tmp4) -> __typ0:
    """Convert meters to miles."""
    return __tmp4 * 0.000621371


def __tmp10(__tmp4) :
    """Convert meters to feet."""
    return __tmp4 * 3.28084


def __meters_to_kilometers(__tmp4: __typ0) -> __typ0:
    """Convert meters to kilometers."""
    return __tmp4 * 0.001
