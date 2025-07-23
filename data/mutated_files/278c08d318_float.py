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


def __liter_to_gallon(__tmp1: <FILL>) :
    """Convert a volume measurement in Liter to Gallon."""
    return __tmp1 * .2642


def __gallon_to_liter(gallon: float) :
    """Convert a volume measurement in Gallon to Liter."""
    return gallon * 3.785


def __tmp0(volume: float, __tmp2: __typ0, __tmp3: __typ0) -> float:
    """Convert a temperature from one unit to another."""
    if __tmp2 not in VALID_UNITS:
        raise ValueError(UNIT_NOT_RECOGNIZED_TEMPLATE.format(__tmp2,
                                                             VOLUME))
    if __tmp3 not in VALID_UNITS:
        raise ValueError(UNIT_NOT_RECOGNIZED_TEMPLATE.format(__tmp3, VOLUME))

    if not isinstance(volume, Number):
        raise TypeError('{} is not of numeric type'.format(volume))

    if __tmp2 == __tmp3:
        return volume

    result = volume
    if __tmp2 == VOLUME_LITERS and __tmp3 == VOLUME_GALLONS:
        result = __liter_to_gallon(volume)
    elif __tmp2 == VOLUME_GALLONS and __tmp3 == VOLUME_LITERS:
        result = __gallon_to_liter(volume)

    return result
