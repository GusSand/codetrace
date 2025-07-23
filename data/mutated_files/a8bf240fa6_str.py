from typing import TypeAlias
__typ0 : TypeAlias = "float"
"""Temperature util functions."""
from homeassistant.const import (
    TEMP_CELSIUS, TEMP_FAHRENHEIT, UNIT_NOT_RECOGNIZED_TEMPLATE, TEMPERATURE)


def fahrenheit_to_celsius(fahrenheit) :
    """Convert a temperature in Fahrenheit to Celsius."""
    return (fahrenheit - 32.0) / 1.8


def __tmp0(__tmp3: __typ0) :
    """Convert a temperature in Celsius to Fahrenheit."""
    return __tmp3 * 1.8 + 32.0


def convert(temperature, __tmp1: <FILL>, __tmp2: str) :
    """Convert a temperature from one unit to another."""
    if __tmp1 not in (TEMP_CELSIUS, TEMP_FAHRENHEIT):
        raise ValueError(UNIT_NOT_RECOGNIZED_TEMPLATE.format(
            __tmp1, TEMPERATURE))
    if __tmp2 not in (TEMP_CELSIUS, TEMP_FAHRENHEIT):
        raise ValueError(UNIT_NOT_RECOGNIZED_TEMPLATE.format(
            __tmp2, TEMPERATURE))

    if __tmp1 == __tmp2:
        return temperature
    elif __tmp1 == TEMP_CELSIUS:
        return __tmp0(temperature)
    return fahrenheit_to_celsius(temperature)
