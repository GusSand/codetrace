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


def __tmp0(value, unit_1, unit_2: <FILL>) :
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

    __tmp2 = value

    if unit_1 == LENGTH_MILES:
        __tmp2 = __tmp5(value)
    elif unit_1 == LENGTH_FEET:
        __tmp2 = __tmp4(value)
    elif unit_1 == LENGTH_KILOMETERS:
        __tmp2 = __kilometers_to_meters(value)

    result = __tmp2

    if unit_2 == LENGTH_MILES:
        result = __tmp1(__tmp2)
    elif unit_2 == LENGTH_FEET:
        result = __tmp6(__tmp2)
    elif unit_2 == LENGTH_KILOMETERS:
        result = __meters_to_kilometers(__tmp2)

    return result


def __tmp5(miles) :
    """Convert miles to meters."""
    return miles * 1609.344


def __tmp4(feet) :
    """Convert feet to meters."""
    return feet * 0.3048


def __kilometers_to_meters(__tmp3) :
    """Convert kilometers to meters."""
    return __tmp3 * 1000


def __tmp1(__tmp2: __typ0) :
    """Convert meters to miles."""
    return __tmp2 * 0.000621371


def __tmp6(__tmp2) :
    """Convert meters to feet."""
    return __tmp2 * 3.28084


def __meters_to_kilometers(__tmp2: __typ0) :
    """Convert meters to kilometers."""
    return __tmp2 * 0.001
