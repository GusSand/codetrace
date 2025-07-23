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


def convert(value, unit_1: __typ0, unit_2) -> float:
    """Convert one unit of measurement to another."""
    if unit_1 not in VALID_UNITS:
        raise ValueError(
            UNIT_NOT_RECOGNIZED_TEMPLATE.format(unit_1, LENGTH))
    if unit_2 not in VALID_UNITS:
        raise ValueError(
            UNIT_NOT_RECOGNIZED_TEMPLATE.format(unit_2, LENGTH))

    if not isinstance(value, Number):
        raise TypeError('{} is not of numeric type'.format(value))

    if unit_1 == unit_2 or unit_1 not in VALID_UNITS:
        return value

    __tmp1 = value

    if unit_1 == LENGTH_MILES:
        __tmp1 = __tmp3(value)
    elif unit_1 == LENGTH_FEET:
        __tmp1 = __feet_to_meters(value)
    elif unit_1 == LENGTH_KILOMETERS:
        __tmp1 = __tmp5(value)

    result = __tmp1

    if unit_2 == LENGTH_MILES:
        result = __tmp0(__tmp1)
    elif unit_2 == LENGTH_FEET:
        result = __tmp4(__tmp1)
    elif unit_2 == LENGTH_KILOMETERS:
        result = __meters_to_kilometers(__tmp1)

    return result


def __tmp3(miles: float) :
    """Convert miles to meters."""
    return miles * 1609.344


def __feet_to_meters(__tmp2: float) -> float:
    """Convert feet to meters."""
    return __tmp2 * 0.3048


def __tmp5(kilometers: <FILL>) -> float:
    """Convert kilometers to meters."""
    return kilometers * 1000


def __tmp0(__tmp1) -> float:
    """Convert meters to miles."""
    return __tmp1 * 0.000621371


def __tmp4(__tmp1: float) -> float:
    """Convert meters to feet."""
    return __tmp1 * 3.28084


def __meters_to_kilometers(__tmp1) -> float:
    """Convert meters to kilometers."""
    return __tmp1 * 0.001
