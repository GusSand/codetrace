from typing import TypeAlias
__typ0 : TypeAlias = "str"
__typ1 : TypeAlias = "HomeAssistant"
"""Temperature helpers for Home Assistant."""
from numbers import Number

from homeassistant.core import HomeAssistant
from homeassistant.util.temperature import convert as convert_temperature


def __tmp1(__tmp0, temperature, __tmp2,
                 precision: <FILL>) :
    """Convert temperature into preferred units for display purposes."""
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
    if precision == 0.5:
        return round(temperature * 2) / 2.0
    elif precision == 0.1:
        return round(temperature, 1)
    # Integer as a fall back (PRECISION_WHOLE)
    return round(temperature)
