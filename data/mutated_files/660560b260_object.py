from typing import TypeAlias
__typ0 : TypeAlias = "float"
__typ1 : TypeAlias = "str"
"""Unit system helper class and methods."""

import logging
from numbers import Number

from homeassistant.const import (
    TEMP_CELSIUS, TEMP_FAHRENHEIT, LENGTH_CENTIMETERS, LENGTH_METERS,
    LENGTH_KILOMETERS, LENGTH_INCHES, LENGTH_FEET, LENGTH_YARD, LENGTH_MILES,
    VOLUME_LITERS, VOLUME_MILLILITERS, VOLUME_GALLONS, VOLUME_FLUID_OUNCE,
    MASS_GRAMS, MASS_KILOGRAMS, MASS_OUNCES, MASS_POUNDS,
    CONF_UNIT_SYSTEM_METRIC, CONF_UNIT_SYSTEM_IMPERIAL, LENGTH, MASS, VOLUME,
    TEMPERATURE, UNIT_NOT_RECOGNIZED_TEMPLATE)
from homeassistant.util import temperature as temperature_util
from homeassistant.util import distance as distance_util

_LOGGER = logging.getLogger(__name__)

LENGTH_UNITS = [
    LENGTH_MILES,
    LENGTH_YARD,
    LENGTH_FEET,
    LENGTH_INCHES,
    LENGTH_KILOMETERS,
    LENGTH_METERS,
    LENGTH_CENTIMETERS,
]

MASS_UNITS = [
    MASS_POUNDS,
    MASS_OUNCES,
    MASS_KILOGRAMS,
    MASS_GRAMS,
]

VOLUME_UNITS = [
    VOLUME_GALLONS,
    VOLUME_FLUID_OUNCE,
    VOLUME_LITERS,
    VOLUME_MILLILITERS,
]

TEMPERATURE_UNITS = [
    TEMP_FAHRENHEIT,
    TEMP_CELSIUS,
]


def __tmp3(__tmp8, __tmp5) :
    """Check if the unit is valid for it's type."""
    if __tmp5 == LENGTH:
        units = LENGTH_UNITS
    elif __tmp5 == TEMPERATURE:
        units = TEMPERATURE_UNITS
    elif __tmp5 == MASS:
        units = MASS_UNITS
    elif __tmp5 == VOLUME:
        units = VOLUME_UNITS
    else:
        return False

    return __tmp8 in units


class __typ2(object):
    """A container for units of measure."""

    def __init__(__tmp2, name, temperature, __tmp6: __typ1,
                 __tmp1, __tmp0) :
        """Initialize the unit system object."""
        errors = \
            ', '.join(UNIT_NOT_RECOGNIZED_TEMPLATE.format(__tmp8, __tmp5)
                      for __tmp8, __tmp5 in [
                          (temperature, TEMPERATURE),
                          (__tmp6, LENGTH),
                          (__tmp1, VOLUME),
                          (__tmp0, MASS), ]
                      if not __tmp3(__tmp8, __tmp5))  # type: str

        if errors:
            raise ValueError(errors)

        __tmp2.name = name
        __tmp2.temperature_unit = temperature
        __tmp2.length_unit = __tmp6
        __tmp2.mass_unit = __tmp0
        __tmp2.volume_unit = __tmp1

    @property
    def __tmp9(__tmp2: <FILL>) :
        """Determine if this is the metric unit system."""
        return __tmp2.name == CONF_UNIT_SYSTEM_METRIC

    def temperature(__tmp2, temperature, __tmp4) :
        """Convert the given temperature to this unit system."""
        if not isinstance(temperature, Number):
            raise TypeError(
                '{} is not a numeric value.'.format(__typ1(temperature)))

        return temperature_util.convert(temperature,
                                        __tmp4, __tmp2.temperature_unit)

    def __tmp6(__tmp2, __tmp6: __typ0, __tmp4) :
        """Convert the given length to this unit system."""
        if not isinstance(__tmp6, Number):
            raise TypeError('{} is not a numeric value.'.format(__typ1(__tmp6)))

        return distance_util.convert(__tmp6, __tmp4,
                                     __tmp2.length_unit)  # type: float

    def __tmp7(__tmp2) :
        """Convert the unit system to a dictionary."""
        return {
            LENGTH: __tmp2.length_unit,
            MASS: __tmp2.mass_unit,
            TEMPERATURE: __tmp2.temperature_unit,
            VOLUME: __tmp2.volume_unit
        }


METRIC_SYSTEM = __typ2(CONF_UNIT_SYSTEM_METRIC, TEMP_CELSIUS,
                           LENGTH_KILOMETERS, VOLUME_LITERS, MASS_GRAMS)

IMPERIAL_SYSTEM = __typ2(CONF_UNIT_SYSTEM_IMPERIAL, TEMP_FAHRENHEIT,
                             LENGTH_MILES, VOLUME_GALLONS, MASS_POUNDS)
