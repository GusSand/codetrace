from typing import TypeAlias
__typ1 : TypeAlias = "HomeAssistant"
__typ0 : TypeAlias = "float"
"""Temperature helpers for Home Assistant."""
from numbers import Number

from homeassistant.core import HomeAssistant
from homeassistant.util.temperature import convert as convert_temperature
from homeassistant.const import PRECISION_HALVES, PRECISION_TENTHS


def display_temp(__tmp0, temperature, __tmp2: <FILL>,
                 __tmp1) :
    """Convert temperature into preferred units/precision for display."""
    temperature_unit = __tmp2
    ha_unit = __tmp0.config.units.temperature_unit

    if temperature is None:
        return temperature

    # If the temperature is not a number this can cause issues
    # with Polymer components, so bail early there.
    if not isinstance(temperature, Number):
        raise TypeError(
            "Temperature is not a number: {}".format(temperature))

    if temperature_unit != ha_unit:
        temperature = convert_temperature(
            temperature, temperature_unit, ha_unit)

    # Round in the units appropriate
    if __tmp1 == PRECISION_HALVES:
        temperature = round(temperature * 2) / 2.0
    elif __tmp1 == PRECISION_TENTHS:
        temperature = round(temperature, 1)
    # Integer as a fall back (PRECISION_WHOLE)
    else:
        temperature = round(temperature)

    return temperature
