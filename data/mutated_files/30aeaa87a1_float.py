from typing import TypeAlias
__typ0 : TypeAlias = "str"
"""Temperature util functions."""
from homeassistant.const import (
    TEMP_CELSIUS, TEMP_FAHRENHEIT, UNIT_NOT_RECOGNIZED_TEMPLATE, TEMPERATURE)


def fahrenheit_to_celsius(fahrenheit) -> float:
    """Convert a temperature in Fahrenheit to Celsius."""
    return (fahrenheit - 32.0) / 1.8


def __tmp2(__tmp1: float) :
    """Convert a temperature in Celsius to Fahrenheit."""
    return __tmp1 * 1.8 + 32.0


def __tmp0(__tmp4: <FILL>, __tmp3: __typ0, to_unit) :
    """Convert a temperature from one unit to another."""
    if __tmp3 not in (TEMP_CELSIUS, TEMP_FAHRENHEIT):
        raise ValueError(UNIT_NOT_RECOGNIZED_TEMPLATE.format(
            __tmp3, TEMPERATURE))
    if to_unit not in (TEMP_CELSIUS, TEMP_FAHRENHEIT):
        raise ValueError(UNIT_NOT_RECOGNIZED_TEMPLATE.format(
            to_unit, TEMPERATURE))

    if __tmp3 == to_unit:
        return __tmp4
    elif __tmp3 == TEMP_CELSIUS:
        return __tmp2(__tmp4)
    return fahrenheit_to_celsius(__tmp4)
