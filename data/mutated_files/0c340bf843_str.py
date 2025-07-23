from typing import TypeAlias
__typ4 : TypeAlias = "float"
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "dict"
__typ3 : TypeAlias = "object"
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


def is_valid_unit(__tmp6, __tmp3) -> __typ2:
    """Check if the unit is valid for it's type."""
    if __tmp3 == LENGTH:
        units = LENGTH_UNITS
    elif __tmp3 == TEMPERATURE:
        units = TEMPERATURE_UNITS
    elif __tmp3 == MASS:
        units = MASS_UNITS
    elif __tmp3 == VOLUME:
        units = VOLUME_UNITS
    else:
        return False

    return __tmp6 in units


class __typ1(__typ3):
    """A container for units of measure."""

    def __tmp4(__tmp0, name: <FILL>, temperature, __tmp2,
                 volume, mass) :
        """Initialize the unit system object."""
        errors = \
            ', '.join(UNIT_NOT_RECOGNIZED_TEMPLATE.format(__tmp6, __tmp3)
                      for __tmp6, __tmp3 in [
                          (temperature, TEMPERATURE),
                          (__tmp2, LENGTH),
                          (volume, VOLUME),
                          (mass, MASS), ]
                      if not is_valid_unit(__tmp6, __tmp3))  # type: str

        if errors:
            raise ValueError(errors)

        __tmp0.name = name
        __tmp0.temperature_unit = temperature
        __tmp0.length_unit = __tmp2
        __tmp0.mass_unit = mass
        __tmp0.volume_unit = volume

    @property
    def __tmp5(__tmp0) :
        """Determine if this is the metric unit system."""
        return __tmp0.name == CONF_UNIT_SYSTEM_METRIC

    def temperature(__tmp0, temperature, __tmp1) :
        """Convert the given temperature to this unit system."""
        if not isinstance(temperature, Number):
            raise TypeError(
                '{} is not a numeric value.'.format(str(temperature)))

        return temperature_util.convert(temperature,
                                        __tmp1, __tmp0.temperature_unit)

    def __tmp2(__tmp0, __tmp2, __tmp1) :
        """Convert the given length to this unit system."""
        if not isinstance(__tmp2, Number):
            raise TypeError('{} is not a numeric value.'.format(str(__tmp2)))

        return distance_util.convert(__tmp2, __tmp1,
                                     __tmp0.length_unit)  # type: float

    def as_dict(__tmp0) :
        """Convert the unit system to a dictionary."""
        return {
            LENGTH: __tmp0.length_unit,
            MASS: __tmp0.mass_unit,
            TEMPERATURE: __tmp0.temperature_unit,
            VOLUME: __tmp0.volume_unit
        }


METRIC_SYSTEM = __typ1(CONF_UNIT_SYSTEM_METRIC, TEMP_CELSIUS,
                           LENGTH_KILOMETERS, VOLUME_LITERS, MASS_GRAMS)

IMPERIAL_SYSTEM = __typ1(CONF_UNIT_SYSTEM_IMPERIAL, TEMP_FAHRENHEIT,
                             LENGTH_MILES, VOLUME_GALLONS, MASS_POUNDS)
