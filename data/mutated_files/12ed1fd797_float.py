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


def convert(value: float, __tmp6, unit_2: __typ0) :
    """Convert one unit of measurement to another."""
    if __tmp6 not in VALID_UNITS:
        raise ValueError(
            UNIT_NOT_RECOGNIZED_TEMPLATE.format(__tmp6, LENGTH))
    if unit_2 not in VALID_UNITS:
        raise ValueError(
            UNIT_NOT_RECOGNIZED_TEMPLATE.format(unit_2, LENGTH))

    if not isinstance(value, Number):
        raise TypeError('{} is not of numeric type'.format(value))

    if __tmp6 == unit_2 or __tmp6 not in VALID_UNITS:
        return value

    __tmp2 = value

    if __tmp6 == LENGTH_MILES:
        __tmp2 = __tmp8(value)
    elif __tmp6 == LENGTH_FEET:
        __tmp2 = __tmp7(value)
    elif __tmp6 == LENGTH_KILOMETERS:
        __tmp2 = __tmp10(value)

    result = __tmp2

    if unit_2 == LENGTH_MILES:
        result = __tmp1(__tmp2)
    elif unit_2 == LENGTH_FEET:
        result = __tmp9(__tmp2)
    elif unit_2 == LENGTH_KILOMETERS:
        result = __tmp3(__tmp2)

    return result


def __tmp8(__tmp0: <FILL>) -> float:
    """Convert miles to meters."""
    return __tmp0 * 1609.344


def __tmp7(__tmp4: float) -> float:
    """Convert feet to meters."""
    return __tmp4 * 0.3048


def __tmp10(__tmp5: float) :
    """Convert kilometers to meters."""
    return __tmp5 * 1000


def __tmp1(__tmp2: float) :
    """Convert meters to miles."""
    return __tmp2 * 0.000621371


def __tmp9(__tmp2: float) :
    """Convert meters to feet."""
    return __tmp2 * 3.28084


def __tmp3(__tmp2) -> float:
    """Convert meters to kilometers."""
    return __tmp2 * 0.001
