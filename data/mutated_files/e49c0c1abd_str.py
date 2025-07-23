from typing import TypeAlias
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


def __tmp1(unit, unit_type: <FILL>) -> bool:
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

    def __tmp3(__tmp2, name, temperature, __tmp0: str,
                 volume, mass) -> None:
        """Initialize the unit system object."""
        errors = \
            ', '.join(UNIT_NOT_RECOGNIZED_TEMPLATE.format(unit, unit_type)
                      for unit, unit_type in [
                          (temperature, TEMPERATURE),
                          (__tmp0, LENGTH),
                          (volume, VOLUME),
                          (mass, MASS), ]
                      if not __tmp1(unit, unit_type))  # type: str

        if errors:
            raise ValueError(errors)

        __tmp2.name = name
        __tmp2.temperature_unit = temperature
        __tmp2.length_unit = __tmp0
        __tmp2.mass_unit = mass
        __tmp2.volume_unit = volume

    @property
    def is_metric(__tmp2) :
        """Determine if this is the metric unit system."""
        return __tmp2.name == CONF_UNIT_SYSTEM_METRIC

    def temperature(__tmp2, temperature, from_unit) :
        """Convert the given temperature to this unit system."""
        if not isinstance(temperature, Number):
            raise TypeError(
                '{} is not a numeric value.'.format(str(temperature)))

        return temperature_util.convert(temperature,
                                        from_unit, __tmp2.temperature_unit)

    def __tmp0(__tmp2, __tmp0: Optional[__typ0], from_unit) :
        """Convert the given length to this unit system."""
        if not isinstance(__tmp0, Number):
            raise TypeError('{} is not a numeric value.'.format(str(__tmp0)))

        return distance_util.convert(__tmp0, from_unit,
                                     __tmp2.length_unit)

    def volume(__tmp2, volume, from_unit) :
        """Convert the given volume to this unit system."""
        if not isinstance(volume, Number):
            raise TypeError('{} is not a numeric value.'.format(str(volume)))

        return volume_util.convert(volume, from_unit, __tmp2.volume_unit)

    def as_dict(__tmp2) -> dict:
        """Convert the unit system to a dictionary."""
        return {
            LENGTH: __tmp2.length_unit,
            MASS: __tmp2.mass_unit,
            TEMPERATURE: __tmp2.temperature_unit,
            VOLUME: __tmp2.volume_unit
        }


METRIC_SYSTEM = UnitSystem(CONF_UNIT_SYSTEM_METRIC, TEMP_CELSIUS,
                           LENGTH_KILOMETERS, VOLUME_LITERS, MASS_GRAMS)

IMPERIAL_SYSTEM = UnitSystem(CONF_UNIT_SYSTEM_IMPERIAL, TEMP_FAHRENHEIT,
                             LENGTH_MILES, VOLUME_GALLONS, MASS_POUNDS)
