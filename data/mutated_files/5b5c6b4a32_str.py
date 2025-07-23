"""Volume conversion util functions."""

import logging
from numbers import Number
from homeassistant.const import (VOLUME_LITERS, VOLUME_MILLILITERS,
                                 VOLUME_GALLONS, VOLUME_FLUID_OUNCE,
                                 VOLUME, UNIT_NOT_RECOGNIZED_TEMPLATE)

_LOGGER = logging.getLogger(__name__)

VALID_UNITS = [VOLUME_LITERS, VOLUME_MILLILITERS, VOLUME_GALLONS,
               VOLUME_FLUID_OUNCE]


def __liter_to_gallon(__tmp5) -> float:
    """Convert a volume measurement in Liter to Gallon."""
    return __tmp5 * .2642


def __tmp6(__tmp4: float) -> float:
    """Convert a volume measurement in Gallon to Liter."""
    return __tmp4 * 3.785


def __tmp0(__tmp1, __tmp2: str, __tmp3: <FILL>) -> float:
    """Convert a temperature from one unit to another."""
    if __tmp2 not in VALID_UNITS:
        raise ValueError(UNIT_NOT_RECOGNIZED_TEMPLATE.format(__tmp2,
                                                             VOLUME))
    if __tmp3 not in VALID_UNITS:
        raise ValueError(UNIT_NOT_RECOGNIZED_TEMPLATE.format(__tmp3, VOLUME))

    if not isinstance(__tmp1, Number):
        raise TypeError('{} is not of numeric type'.format(__tmp1))

    if __tmp2 == __tmp3:
        return __tmp1

    result = __tmp1
    if __tmp2 == VOLUME_LITERS and __tmp3 == VOLUME_GALLONS:
        result = __liter_to_gallon(__tmp1)
    elif __tmp2 == VOLUME_GALLONS and __tmp3 == VOLUME_LITERS:
        result = __tmp6(__tmp1)

    return result
