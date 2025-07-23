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


def convert(value: float, unit_1, unit_2) -> float:
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

    __tmp0 = value

    if unit_1 == LENGTH_MILES:
        __tmp0 = __miles_to_meters(value)
    elif unit_1 == LENGTH_FEET:
        __tmp0 = __tmp1(value)
    elif unit_1 == LENGTH_KILOMETERS:
        __tmp0 = __kilometers_to_meters(value)

    result = __tmp0

    if unit_2 == LENGTH_MILES:
        result = __meters_to_miles(__tmp0)
    elif unit_2 == LENGTH_FEET:
        result = __meters_to_feet(__tmp0)
    elif unit_2 == LENGTH_KILOMETERS:
        result = __meters_to_kilometers(__tmp0)

    return result


def __miles_to_meters(miles: <FILL>) :
    """Convert miles to meters."""
    return miles * 1609.344


def __tmp1(feet: float) :
    """Convert feet to meters."""
    return feet * 0.3048


def __kilometers_to_meters(kilometers: float) -> float:
    """Convert kilometers to meters."""
    return kilometers * 1000


def __meters_to_miles(__tmp0: float) -> float:
    """Convert meters to miles."""
    return __tmp0 * 0.000621371


def __meters_to_feet(__tmp0: float) -> float:
    """Convert meters to feet."""
    return __tmp0 * 3.28084


def __meters_to_kilometers(__tmp0: float) -> float:
    """Convert meters to kilometers."""
    return __tmp0 * 0.001
