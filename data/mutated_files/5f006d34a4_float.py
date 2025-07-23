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


def __tmp0(__tmp4: float, __tmp8, unit_2: __typ0) :
    """Convert one unit of measurement to another."""
    if __tmp8 not in VALID_UNITS:
        raise ValueError(
            UNIT_NOT_RECOGNIZED_TEMPLATE.format(__tmp8, LENGTH))
    if unit_2 not in VALID_UNITS:
        raise ValueError(
            UNIT_NOT_RECOGNIZED_TEMPLATE.format(unit_2, LENGTH))

    if not isinstance(__tmp4, Number):
        raise TypeError('{} is not of numeric type'.format(__tmp4))

    if __tmp8 == unit_2 or __tmp8 not in VALID_UNITS:
        return __tmp4

    __tmp3 = __tmp4

    if __tmp8 == LENGTH_MILES:
        __tmp3 = __tmp10(__tmp4)
    elif __tmp8 == LENGTH_FEET:
        __tmp3 = __tmp9(__tmp4)
    elif __tmp8 == LENGTH_KILOMETERS:
        __tmp3 = __tmp12(__tmp4)

    result = __tmp3

    if unit_2 == LENGTH_MILES:
        result = __tmp2(__tmp3)
    elif unit_2 == LENGTH_FEET:
        result = __tmp11(__tmp3)
    elif unit_2 == LENGTH_KILOMETERS:
        result = __tmp5(__tmp3)

    return result


def __tmp10(__tmp1) :
    """Convert miles to meters."""
    return __tmp1 * 1609.344


def __tmp9(__tmp6: float) :
    """Convert feet to meters."""
    return __tmp6 * 0.3048


def __tmp12(__tmp7: float) :
    """Convert kilometers to meters."""
    return __tmp7 * 1000


def __tmp2(__tmp3: float) -> float:
    """Convert meters to miles."""
    return __tmp3 * 0.000621371


def __tmp11(__tmp3: float) -> float:
    """Convert meters to feet."""
    return __tmp3 * 3.28084


def __tmp5(__tmp3: <FILL>) -> float:
    """Convert meters to kilometers."""
    return __tmp3 * 0.001
