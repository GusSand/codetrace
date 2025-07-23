from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ3 : TypeAlias = "object"
__typ0 : TypeAlias = "str"
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


def __tmp2(unit, __tmp4: __typ0) :
    """Check if the unit is valid for it's type."""
    if __tmp4 == LENGTH:
        units = LENGTH_UNITS
    elif __tmp4 == TEMPERATURE:
        units = TEMPERATURE_UNITS
    elif __tmp4 == MASS:
        units = MASS_UNITS
    elif __tmp4 == VOLUME:
        units = VOLUME_UNITS
    else:
        return False

    return unit in units


class __typ1(__typ3):
    """A container for units of measure."""

    def __init__(self, name, temperature, length,
                 __tmp1, __tmp0) :
        """Initialize the unit system object."""
        errors = \
            ', '.join(UNIT_NOT_RECOGNIZED_TEMPLATE.format(unit, __tmp4)
                      for unit, __tmp4 in [
                          (temperature, TEMPERATURE),
                          (length, LENGTH),
                          (__tmp1, VOLUME),
                          (__tmp0, MASS), ]
                      if not __tmp2(unit, __tmp4))  # type: str

        if errors:
            raise ValueError(errors)

        self.name = name
        self.temperature_unit = temperature
        self.length_unit = length
        self.mass_unit = __tmp0
        self.volume_unit = __tmp1

    @property
    def __tmp6(self) :
        """Determine if this is the metric unit system."""
        return self.name == CONF_UNIT_SYSTEM_METRIC

    def temperature(self, temperature: <FILL>, __tmp3) :
        """Convert the given temperature to this unit system."""
        if not isinstance(temperature, Number):
            raise TypeError(
                '{} is not a numeric value.'.format(__typ0(temperature)))

        return temperature_util.convert(temperature,
                                        __tmp3, self.temperature_unit)

    def length(self, length, __tmp3) :
        """Convert the given length to this unit system."""
        if not isinstance(length, Number):
            raise TypeError('{} is not a numeric value.'.format(__typ0(length)))

        return distance_util.convert(length, __tmp3,
                                     self.length_unit)  # type: float

    def __tmp5(self) :
        """Convert the unit system to a dictionary."""
        return {
            LENGTH: self.length_unit,
            MASS: self.mass_unit,
            TEMPERATURE: self.temperature_unit,
            VOLUME: self.volume_unit
        }


METRIC_SYSTEM = __typ1(CONF_UNIT_SYSTEM_METRIC, TEMP_CELSIUS,
                           LENGTH_KILOMETERS, VOLUME_LITERS, MASS_GRAMS)

IMPERIAL_SYSTEM = __typ1(CONF_UNIT_SYSTEM_IMPERIAL, TEMP_FAHRENHEIT,
                             LENGTH_MILES, VOLUME_GALLONS, MASS_POUNDS)
