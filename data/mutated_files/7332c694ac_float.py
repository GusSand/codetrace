from typing import TypeAlias
__typ0 : TypeAlias = "str"
"""Temperature util functions."""
from homeassistant.const import (
    TEMP_CELSIUS, TEMP_FAHRENHEIT, UNIT_NOT_RECOGNIZED_TEMPLATE, TEMPERATURE)


def __tmp1(fahrenheit: <FILL>) :
    """Convert a temperature in Fahrenheit to Celsius."""
    return (fahrenheit - 32.0) / 1.8


def __tmp2(celsius) :
    """Convert a temperature in Celsius to Fahrenheit."""
    return celsius * 1.8 + 32.0


def __tmp0(__tmp3: float, from_unit, to_unit: __typ0) :
    """Convert a temperature from one unit to another."""
    if from_unit not in (TEMP_CELSIUS, TEMP_FAHRENHEIT):
        raise ValueError(UNIT_NOT_RECOGNIZED_TEMPLATE.format(
            from_unit, TEMPERATURE))
    if to_unit not in (TEMP_CELSIUS, TEMP_FAHRENHEIT):
        raise ValueError(UNIT_NOT_RECOGNIZED_TEMPLATE.format(
            to_unit, TEMPERATURE))

    if from_unit == to_unit:
        return __tmp3
    elif from_unit == TEMP_CELSIUS:
        return __tmp2(__tmp3)
    return __tmp1(__tmp3)
