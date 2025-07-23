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


def __tmp0(__tmp3, unit_1, __tmp1) :
    """Convert one unit of measurement to another."""
    if unit_1 not in VALID_UNITS:
        raise ValueError(
            UNIT_NOT_RECOGNIZED_TEMPLATE.format(unit_1, LENGTH))
    if __tmp1 not in VALID_UNITS:
        raise ValueError(
            UNIT_NOT_RECOGNIZED_TEMPLATE.format(__tmp1, LENGTH))

    if not isinstance(__tmp3, Number):
        raise TypeError('{} is not of numeric type'.format(__tmp3))

    if unit_1 == __tmp1 or unit_1 not in VALID_UNITS:
        return __tmp3

    __tmp4 = __tmp3

    if unit_1 == LENGTH_MILES:
        __tmp4 = __tmp8(__tmp3)
    elif unit_1 == LENGTH_FEET:
        __tmp4 = __tmp7(__tmp3)
    elif unit_1 == LENGTH_KILOMETERS:
        __tmp4 = __tmp10(__tmp3)

    result = __tmp4

    if __tmp1 == LENGTH_MILES:
        result = __meters_to_miles(__tmp4)
    elif __tmp1 == LENGTH_FEET:
        result = __tmp9(__tmp4)
    elif __tmp1 == LENGTH_KILOMETERS:
        result = __tmp5(__tmp4)

    return result


def __tmp8(__tmp2) -> float:
    """Convert miles to meters."""
    return __tmp2 * 1609.344


def __tmp7(feet: float) -> float:
    """Convert feet to meters."""
    return feet * 0.3048


def __tmp10(__tmp6) :
    """Convert kilometers to meters."""
    return __tmp6 * 1000


def __meters_to_miles(__tmp4: <FILL>) -> float:
    """Convert meters to miles."""
    return __tmp4 * 0.000621371


def __tmp9(__tmp4: float) -> float:
    """Convert meters to feet."""
    return __tmp4 * 3.28084


def __tmp5(__tmp4) :
    """Convert meters to kilometers."""
    return __tmp4 * 0.001
