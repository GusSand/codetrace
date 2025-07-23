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


def __tmp0(__tmp4: float, __tmp9: __typ0, __tmp1: __typ0) :
    """Convert one unit of measurement to another."""
    if __tmp9 not in VALID_UNITS:
        raise ValueError(
            UNIT_NOT_RECOGNIZED_TEMPLATE.format(__tmp9, LENGTH))
    if __tmp1 not in VALID_UNITS:
        raise ValueError(
            UNIT_NOT_RECOGNIZED_TEMPLATE.format(__tmp1, LENGTH))

    if not isinstance(__tmp4, Number):
        raise TypeError('{} is not of numeric type'.format(__tmp4))

    if __tmp9 == __tmp1 or __tmp9 not in VALID_UNITS:
        return __tmp4

    __tmp5 = __tmp4

    if __tmp9 == LENGTH_MILES:
        __tmp5 = __tmp11(__tmp4)
    elif __tmp9 == LENGTH_FEET:
        __tmp5 = __tmp10(__tmp4)
    elif __tmp9 == LENGTH_KILOMETERS:
        __tmp5 = __tmp13(__tmp4)

    result = __tmp5

    if __tmp1 == LENGTH_MILES:
        result = __tmp3(__tmp5)
    elif __tmp1 == LENGTH_FEET:
        result = __tmp12(__tmp5)
    elif __tmp1 == LENGTH_KILOMETERS:
        result = __tmp6(__tmp5)

    return result


def __tmp11(__tmp2: float) -> float:
    """Convert miles to meters."""
    return __tmp2 * 1609.344


def __tmp10(__tmp7: float) -> float:
    """Convert feet to meters."""
    return __tmp7 * 0.3048


def __tmp13(__tmp8: float) -> float:
    """Convert kilometers to meters."""
    return __tmp8 * 1000


def __tmp3(__tmp5: <FILL>) -> float:
    """Convert meters to miles."""
    return __tmp5 * 0.000621371


def __tmp12(__tmp5: float) -> float:
    """Convert meters to feet."""
    return __tmp5 * 3.28084


def __tmp6(__tmp5: float) -> float:
    """Convert meters to kilometers."""
    return __tmp5 * 0.001
