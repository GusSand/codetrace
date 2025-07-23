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


def convert(__tmp2: <FILL>, __tmp4, __tmp0) :
    """Convert one unit of measurement to another."""
    if __tmp4 not in VALID_UNITS:
        raise ValueError(
            UNIT_NOT_RECOGNIZED_TEMPLATE.format(__tmp4, LENGTH))
    if __tmp0 not in VALID_UNITS:
        raise ValueError(
            UNIT_NOT_RECOGNIZED_TEMPLATE.format(__tmp0, LENGTH))

    if not isinstance(__tmp2, Number):
        raise TypeError('{} is not of numeric type'.format(__tmp2))

    if __tmp4 == __tmp0 or __tmp4 not in VALID_UNITS:
        return __tmp2

    __tmp1 = __tmp2

    if __tmp4 == LENGTH_MILES:
        __tmp1 = __miles_to_meters(__tmp2)
    elif __tmp4 == LENGTH_FEET:
        __tmp1 = __tmp5(__tmp2)
    elif __tmp4 == LENGTH_KILOMETERS:
        __tmp1 = __kilometers_to_meters(__tmp2)

    result = __tmp1

    if __tmp0 == LENGTH_MILES:
        result = __meters_to_miles(__tmp1)
    elif __tmp0 == LENGTH_FEET:
        result = __meters_to_feet(__tmp1)
    elif __tmp0 == LENGTH_KILOMETERS:
        result = __tmp3(__tmp1)

    return result


def __miles_to_meters(miles) :
    """Convert miles to meters."""
    return miles * 1609.344


def __tmp5(feet) -> float:
    """Convert feet to meters."""
    return feet * 0.3048


def __kilometers_to_meters(kilometers: float) :
    """Convert kilometers to meters."""
    return kilometers * 1000


def __meters_to_miles(__tmp1) :
    """Convert meters to miles."""
    return __tmp1 * 0.000621371


def __meters_to_feet(__tmp1) :
    """Convert meters to feet."""
    return __tmp1 * 3.28084


def __tmp3(__tmp1) :
    """Convert meters to kilometers."""
    return __tmp1 * 0.001
