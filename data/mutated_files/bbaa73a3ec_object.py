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


def __tmp1(unit: __typ1, __tmp0: __typ1) :
    """Check if the unit is valid for it's type."""
    if __tmp0 == LENGTH:
        units = LENGTH_UNITS
    elif __tmp0 == TEMPERATURE:
        units = TEMPERATURE_UNITS
    elif __tmp0 == MASS:
        units = MASS_UNITS
    elif __tmp0 == VOLUME:
        units = VOLUME_UNITS
    else:
        return False

    return unit in units


class UnitSystem(object):
    """A container for units of measure."""

    def __init__(__tmp3: <FILL>, name: __typ1, temperature: __typ1, __tmp2,
                 volume, mass: __typ1) -> None:
        """Initialize the unit system object."""
        errors = \
            ', '.join(UNIT_NOT_RECOGNIZED_TEMPLATE.format(unit, __tmp0)
                      for unit, __tmp0 in [
                          (temperature, TEMPERATURE),
                          (__tmp2, LENGTH),
                          (volume, VOLUME),
                          (mass, MASS), ]
                      if not __tmp1(unit, __tmp0))  # type: str

        if errors:
            raise ValueError(errors)

        __tmp3.name = name
        __tmp3.temperature_unit = temperature
        __tmp3.length_unit = __tmp2
        __tmp3.mass_unit = mass
        __tmp3.volume_unit = volume

    @property
    def is_metric(__tmp3) :
        """Determine if this is the metric unit system."""
        return __tmp3.name == CONF_UNIT_SYSTEM_METRIC

    def temperature(__tmp3, temperature, from_unit: __typ1) -> __typ0:
        """Convert the given temperature to this unit system."""
        if not isinstance(temperature, Number):
            raise TypeError(
                '{} is not a numeric value.'.format(__typ1(temperature)))

        return temperature_util.convert(temperature,
                                        from_unit, __tmp3.temperature_unit)

    def __tmp2(__tmp3, __tmp2: __typ0, from_unit: __typ1) -> __typ0:
        """Convert the given length to this unit system."""
        if not isinstance(__tmp2, Number):
            raise TypeError('{} is not a numeric value.'.format(__typ1(__tmp2)))

        return distance_util.convert(__tmp2, from_unit,
                                     __tmp3.length_unit)  # type: float

    def as_dict(__tmp3) -> dict:
        """Convert the unit system to a dictionary."""
        return {
            LENGTH: __tmp3.length_unit,
            MASS: __tmp3.mass_unit,
            TEMPERATURE: __tmp3.temperature_unit,
            VOLUME: __tmp3.volume_unit
        }


METRIC_SYSTEM = UnitSystem(CONF_UNIT_SYSTEM_METRIC, TEMP_CELSIUS,
                           LENGTH_KILOMETERS, VOLUME_LITERS, MASS_GRAMS)

IMPERIAL_SYSTEM = UnitSystem(CONF_UNIT_SYSTEM_IMPERIAL, TEMP_FAHRENHEIT,
                             LENGTH_MILES, VOLUME_GALLONS, MASS_POUNDS)
