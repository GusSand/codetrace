from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ0 : TypeAlias = "float"
"""Unit system helper class and methods."""

import logging
from typing import Optional
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
from homeassistant.util import volume as volume_util

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


def is_valid_unit(unit, unit_type) :
    """Check if the unit is valid for it's type."""
    if unit_type == LENGTH:
        units = LENGTH_UNITS
    elif unit_type == TEMPERATURE:
        units = TEMPERATURE_UNITS
    elif unit_type == MASS:
        units = MASS_UNITS
    elif unit_type == VOLUME:
        units = VOLUME_UNITS
    else:
        return False

    return unit in units


class __typ1:
    """A container for units of measure."""

    def __init__(__tmp1, name, temperature: <FILL>, length,
                 volume, __tmp0: str) :
        """Initialize the unit system object."""
        errors = \
            ', '.join(UNIT_NOT_RECOGNIZED_TEMPLATE.format(unit, unit_type)
                      for unit, unit_type in [
                          (temperature, TEMPERATURE),
                          (length, LENGTH),
                          (volume, VOLUME),
                          (__tmp0, MASS), ]
                      if not is_valid_unit(unit, unit_type))  # type: str

        if errors:
            raise ValueError(errors)

        __tmp1.name = name
        __tmp1.temperature_unit = temperature
        __tmp1.length_unit = length
        __tmp1.mass_unit = __tmp0
        __tmp1.volume_unit = volume

    @property
    def __tmp3(__tmp1) :
        """Determine if this is the metric unit system."""
        return __tmp1.name == CONF_UNIT_SYSTEM_METRIC

    def temperature(__tmp1, temperature, __tmp2) :
        """Convert the given temperature to this unit system."""
        if not isinstance(temperature, Number):
            raise TypeError(
                '{} is not a numeric value.'.format(str(temperature)))

        return temperature_util.convert(temperature,
                                        __tmp2, __tmp1.temperature_unit)

    def length(__tmp1, length, __tmp2) :
        """Convert the given length to this unit system."""
        if not isinstance(length, Number):
            raise TypeError('{} is not a numeric value.'.format(str(length)))

        return distance_util.convert(length, __tmp2,
                                     __tmp1.length_unit)

    def volume(__tmp1, volume, __tmp2) :
        """Convert the given volume to this unit system."""
        if not isinstance(volume, Number):
            raise TypeError('{} is not a numeric value.'.format(str(volume)))

        return volume_util.convert(volume, __tmp2, __tmp1.volume_unit)

    def as_dict(__tmp1) :
        """Convert the unit system to a dictionary."""
        return {
            LENGTH: __tmp1.length_unit,
            MASS: __tmp1.mass_unit,
            TEMPERATURE: __tmp1.temperature_unit,
            VOLUME: __tmp1.volume_unit
        }


METRIC_SYSTEM = __typ1(CONF_UNIT_SYSTEM_METRIC, TEMP_CELSIUS,
                           LENGTH_KILOMETERS, VOLUME_LITERS, MASS_GRAMS)

IMPERIAL_SYSTEM = __typ1(CONF_UNIT_SYSTEM_IMPERIAL, TEMP_FAHRENHEIT,
                             LENGTH_MILES, VOLUME_GALLONS, MASS_POUNDS)
