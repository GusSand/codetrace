from typing import TypeAlias
__typ1 : TypeAlias = "object"
__typ0 : TypeAlias = "bool"
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


def __tmp2(unit: str, __tmp4) :
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


class UnitSystem(__typ1):
    """A container for units of measure."""

    def __tmp6(__tmp1, name: str, temperature: <FILL>, __tmp5,
                 __tmp0, mass: str) :
        """Initialize the unit system object."""
        errors = \
            ', '.join(UNIT_NOT_RECOGNIZED_TEMPLATE.format(unit, __tmp4)
                      for unit, __tmp4 in [
                          (temperature, TEMPERATURE),
                          (__tmp5, LENGTH),
                          (__tmp0, VOLUME),
                          (mass, MASS), ]
                      if not __tmp2(unit, __tmp4))  # type: str

        if errors:
            raise ValueError(errors)

        __tmp1.name = name
        __tmp1.temperature_unit = temperature
        __tmp1.length_unit = __tmp5
        __tmp1.mass_unit = mass
        __tmp1.volume_unit = __tmp0

    @property
    def __tmp7(__tmp1) -> __typ0:
        """Determine if this is the metric unit system."""
        return __tmp1.name == CONF_UNIT_SYSTEM_METRIC

    def temperature(__tmp1, temperature, __tmp3) :
        """Convert the given temperature to this unit system."""
        if not isinstance(temperature, Number):
            raise TypeError(
                '{} is not a numeric value.'.format(str(temperature)))

        return temperature_util.convert(temperature,
                                        __tmp3, __tmp1.temperature_unit)

    def __tmp5(__tmp1, __tmp5, __tmp3) :
        """Convert the given length to this unit system."""
        if not isinstance(__tmp5, Number):
            raise TypeError('{} is not a numeric value.'.format(str(__tmp5)))

        return distance_util.convert(__tmp5, __tmp3,
                                     __tmp1.length_unit)  # type: float

    def as_dict(__tmp1) :
        """Convert the unit system to a dictionary."""
        return {
            LENGTH: __tmp1.length_unit,
            MASS: __tmp1.mass_unit,
            TEMPERATURE: __tmp1.temperature_unit,
            VOLUME: __tmp1.volume_unit
        }


METRIC_SYSTEM = UnitSystem(CONF_UNIT_SYSTEM_METRIC, TEMP_CELSIUS,
                           LENGTH_KILOMETERS, VOLUME_LITERS, MASS_GRAMS)

IMPERIAL_SYSTEM = UnitSystem(CONF_UNIT_SYSTEM_IMPERIAL, TEMP_FAHRENHEIT,
                             LENGTH_MILES, VOLUME_GALLONS, MASS_POUNDS)
