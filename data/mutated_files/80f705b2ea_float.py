from typing import TypeAlias
__typ0 : TypeAlias = "str"
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


def __tmp0(__tmp2: float, __tmp7: __typ0, unit_2: __typ0) :
    """Convert one unit of measurement to another."""
    if __tmp7 not in VALID_UNITS:
        raise ValueError(
            UNIT_NOT_RECOGNIZED_TEMPLATE.format(__tmp7, LENGTH))
    if unit_2 not in VALID_UNITS:
        raise ValueError(
            UNIT_NOT_RECOGNIZED_TEMPLATE.format(unit_2, LENGTH))

    if not isinstance(__tmp2, Number):
        raise TypeError('{} is not of numeric type'.format(__tmp2))

    if __tmp7 == unit_2 or __tmp7 not in VALID_UNITS:
        return __tmp2

    __tmp3 = __tmp2

    if __tmp7 == LENGTH_MILES:
        __tmp3 = __miles_to_meters(__tmp2)
    elif __tmp7 == LENGTH_FEET:
        __tmp3 = __feet_to_meters(__tmp2)
    elif __tmp7 == LENGTH_KILOMETERS:
        __tmp3 = __kilometers_to_meters(__tmp2)

    result = __tmp3

    if unit_2 == LENGTH_MILES:
        result = __meters_to_miles(__tmp3)
    elif unit_2 == LENGTH_FEET:
        result = __tmp8(__tmp3)
    elif unit_2 == LENGTH_KILOMETERS:
        result = __tmp4(__tmp3)

    return result


def __miles_to_meters(__tmp1: float) :
    """Convert miles to meters."""
    return __tmp1 * 1609.344


def __feet_to_meters(__tmp5: float) :
    """Convert feet to meters."""
    return __tmp5 * 0.3048


def __kilometers_to_meters(__tmp6: float) -> float:
    """Convert kilometers to meters."""
    return __tmp6 * 1000


def __meters_to_miles(__tmp3: float) -> float:
    """Convert meters to miles."""
    return __tmp3 * 0.000621371


def __tmp8(__tmp3) -> float:
    """Convert meters to feet."""
    return __tmp3 * 3.28084


def __tmp4(__tmp3: <FILL>) -> float:
    """Convert meters to kilometers."""
    return __tmp3 * 0.001
