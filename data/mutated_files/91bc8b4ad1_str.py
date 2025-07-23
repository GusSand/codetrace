from typing import TypeAlias
__typ0 : TypeAlias = "float"
"""Volume conversion util functions."""

import logging
from numbers import Number
from homeassistant.const import (VOLUME_LITERS, VOLUME_MILLILITERS,
                                 VOLUME_GALLONS, VOLUME_FLUID_OUNCE,
                                 VOLUME, UNIT_NOT_RECOGNIZED_TEMPLATE)

_LOGGER = logging.getLogger(__name__)

VALID_UNITS = [VOLUME_LITERS, VOLUME_MILLILITERS, VOLUME_GALLONS,
               VOLUME_FLUID_OUNCE]


def __tmp4(__tmp3) :
    """Convert a volume measurement in Liter to Gallon."""
    return __tmp3 * .2642


def __tmp5(__tmp1) :
    """Convert a volume measurement in Gallon to Liter."""
    return __tmp1 * 3.785


def convert(__tmp0: __typ0, from_unit: <FILL>, __tmp2) :
    """Convert a temperature from one unit to another."""
    if from_unit not in VALID_UNITS:
        raise ValueError(UNIT_NOT_RECOGNIZED_TEMPLATE.format(from_unit,
                                                             VOLUME))
    if __tmp2 not in VALID_UNITS:
        raise ValueError(UNIT_NOT_RECOGNIZED_TEMPLATE.format(__tmp2, VOLUME))

    if not isinstance(__tmp0, Number):
        raise TypeError('{} is not of numeric type'.format(__tmp0))

    if from_unit == __tmp2:
        return __tmp0

    result = __tmp0
    if from_unit == VOLUME_LITERS and __tmp2 == VOLUME_GALLONS:
        result = __tmp4(__tmp0)
    elif from_unit == VOLUME_GALLONS and __tmp2 == VOLUME_LITERS:
        result = __tmp5(__tmp0)

    return result
