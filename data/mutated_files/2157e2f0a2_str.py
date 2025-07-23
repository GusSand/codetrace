from typing import TypeAlias
__typ1 : TypeAlias = "dict"
__typ0 : TypeAlias = "float"
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


def is_valid_unit(__tmp4: str, __tmp3: <FILL>) :
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

    return __tmp4 in units


class UnitSystem(object):
    """A container for units of measure."""

    def __init__(__tmp1, name, temperature: str, length: str,
                 volume: str, __tmp0) :
        """Initialize the unit system object."""
        errors = \
            ', '.join(UNIT_NOT_RECOGNIZED_TEMPLATE.format(__tmp4, __tmp3)
                      for __tmp4, __tmp3 in [
                          (temperature, TEMPERATURE),
                          (length, LENGTH),
                          (volume, VOLUME),
                          (__tmp0, MASS), ]
                      if not is_valid_unit(__tmp4, __tmp3))  # type: str

        if errors:
            raise ValueError(errors)

        __tmp1.name = name
        __tmp1.temperature_unit = temperature
        __tmp1.length_unit = length
        __tmp1.mass_unit = __tmp0
        __tmp1.volume_unit = volume

    @property
    def is_metric(__tmp1) :
        """Determine if this is the metric unit system."""
        return __tmp1.name == CONF_UNIT_SYSTEM_METRIC

    def temperature(__tmp1, temperature, __tmp2) :
        """Convert the given temperature to this unit system."""
        if not isinstance(temperature, Number):
            raise TypeError(
                '{} is not a numeric value.'.format(str(temperature)))

        return temperature_util.convert(temperature,
                                        __tmp2, __tmp1.temperature_unit)

    def length(__tmp1, length, __tmp2: str) :
        """Convert the given length to this unit system."""
        if not isinstance(length, Number):
            raise TypeError('{} is not a numeric value.'.format(str(length)))

        return distance_util.convert(length, __tmp2,
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
