from typing import TypeAlias
__typ0 : TypeAlias = "str"
"""Volume conversion util functions."""

import logging
from numbers import Number
from homeassistant.const import (VOLUME_LITERS, VOLUME_MILLILITERS,
                                 VOLUME_GALLONS, VOLUME_FLUID_OUNCE,
                                 VOLUME, UNIT_NOT_RECOGNIZED_TEMPLATE)

_LOGGER = logging.getLogger(__name__)

VALID_UNITS = [VOLUME_LITERS, VOLUME_MILLILITERS, VOLUME_GALLONS,
               VOLUME_FLUID_OUNCE]


def __tmp3(__tmp2) -> float:
    """Convert a volume measurement in Liter to Gallon."""
    return __tmp2 * .2642


def __tmp4(gallon: <FILL>) -> float:
    """Convert a volume measurement in Gallon to Liter."""
    return gallon * 3.785


def convert(__tmp0: float, __tmp1: __typ0, to_unit) -> float:
    """Convert a temperature from one unit to another."""
    if __tmp1 not in VALID_UNITS:
        raise ValueError(UNIT_NOT_RECOGNIZED_TEMPLATE.format(__tmp1,
                                                             VOLUME))
    if to_unit not in VALID_UNITS:
        raise ValueError(UNIT_NOT_RECOGNIZED_TEMPLATE.format(to_unit, VOLUME))

    if not isinstance(__tmp0, Number):
        raise TypeError('{} is not of numeric type'.format(__tmp0))

    if __tmp1 == to_unit:
        return __tmp0

    result = __tmp0
    if __tmp1 == VOLUME_LITERS and to_unit == VOLUME_GALLONS:
        result = __tmp3(__tmp0)
    elif __tmp1 == VOLUME_GALLONS and to_unit == VOLUME_LITERS:
        result = __tmp4(__tmp0)

    return result
