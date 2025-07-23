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


def convert(__tmp2: float, unit_1: __typ0, __tmp0) -> float:
    """Convert one unit of measurement to another."""
    if unit_1 not in VALID_UNITS:
        raise ValueError(
            UNIT_NOT_RECOGNIZED_TEMPLATE.format(unit_1, LENGTH))
    if __tmp0 not in VALID_UNITS:
        raise ValueError(
            UNIT_NOT_RECOGNIZED_TEMPLATE.format(__tmp0, LENGTH))

    if not isinstance(__tmp2, Number):
        raise TypeError('{} is not of numeric type'.format(__tmp2))

    if unit_1 == __tmp0 or unit_1 not in VALID_UNITS:
        return __tmp2

    __tmp3 = __tmp2

    if unit_1 == LENGTH_MILES:
        __tmp3 = __tmp6(__tmp2)
    elif unit_1 == LENGTH_FEET:
        __tmp3 = __tmp5(__tmp2)
    elif unit_1 == LENGTH_KILOMETERS:
        __tmp3 = __tmp7(__tmp2)

    result = __tmp3

    if __tmp0 == LENGTH_MILES:
        result = __tmp1(__tmp3)
    elif __tmp0 == LENGTH_FEET:
        result = __meters_to_feet(__tmp3)
    elif __tmp0 == LENGTH_KILOMETERS:
        result = __tmp4(__tmp3)

    return result


def __tmp6(miles: float) -> float:
    """Convert miles to meters."""
    return miles * 1609.344


def __tmp5(feet: float) :
    """Convert feet to meters."""
    return feet * 0.3048


def __tmp7(kilometers: float) -> float:
    """Convert kilometers to meters."""
    return kilometers * 1000


def __tmp1(__tmp3: float) -> float:
    """Convert meters to miles."""
    return __tmp3 * 0.000621371


def __meters_to_feet(__tmp3: <FILL>) -> float:
    """Convert meters to feet."""
    return __tmp3 * 3.28084


def __tmp4(__tmp3: float) -> float:
    """Convert meters to kilometers."""
    return __tmp3 * 0.001
