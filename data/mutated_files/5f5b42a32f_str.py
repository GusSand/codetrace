from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ1 : TypeAlias = "dict"
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


def __tmp1(unit: str, unit_type: str) -> __typ2:
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


class UnitSystem:
    """A container for units of measure."""

    def __init__(__tmp0, name: str, temperature: str, __tmp3,
                 volume: <FILL>, mass) :
        """Initialize the unit system object."""
        errors = \
            ', '.join(UNIT_NOT_RECOGNIZED_TEMPLATE.format(unit, unit_type)
                      for unit, unit_type in [
                          (temperature, TEMPERATURE),
                          (__tmp3, LENGTH),
                          (volume, VOLUME),
                          (mass, MASS), ]
                      if not __tmp1(unit, unit_type))  # type: str

        if errors:
            raise ValueError(errors)

        __tmp0.name = name
        __tmp0.temperature_unit = temperature
        __tmp0.length_unit = __tmp3
        __tmp0.mass_unit = mass
        __tmp0.volume_unit = volume

    @property
    def __tmp4(__tmp0) :
        """Determine if this is the metric unit system."""
        return __tmp0.name == CONF_UNIT_SYSTEM_METRIC

    def temperature(__tmp0, temperature, __tmp2: str) :
        """Convert the given temperature to this unit system."""
        if not isinstance(temperature, Number):
            raise TypeError(
                '{} is not a numeric value.'.format(str(temperature)))

        return temperature_util.convert(temperature,
                                        __tmp2, __tmp0.temperature_unit)

    def __tmp3(__tmp0, __tmp3, __tmp2: str) -> __typ0:
        """Convert the given length to this unit system."""
        if not isinstance(__tmp3, Number):
            raise TypeError('{} is not a numeric value.'.format(str(__tmp3)))

        return distance_util.convert(__tmp3, __tmp2,
                                     __tmp0.length_unit)

    def volume(__tmp0, volume, __tmp2) :
        """Convert the given volume to this unit system."""
        if not isinstance(volume, Number):
            raise TypeError('{} is not a numeric value.'.format(str(volume)))

        return volume_util.convert(volume, __tmp2, __tmp0.volume_unit)

    def as_dict(__tmp0) -> __typ1:
        """Convert the unit system to a dictionary."""
        return {
            LENGTH: __tmp0.length_unit,
            MASS: __tmp0.mass_unit,
            TEMPERATURE: __tmp0.temperature_unit,
            VOLUME: __tmp0.volume_unit
        }


METRIC_SYSTEM = UnitSystem(CONF_UNIT_SYSTEM_METRIC, TEMP_CELSIUS,
                           LENGTH_KILOMETERS, VOLUME_LITERS, MASS_GRAMS)

IMPERIAL_SYSTEM = UnitSystem(CONF_UNIT_SYSTEM_IMPERIAL, TEMP_FAHRENHEIT,
                             LENGTH_MILES, VOLUME_GALLONS, MASS_POUNDS)
