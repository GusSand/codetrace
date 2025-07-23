from typing import TypeAlias
__typ0 : TypeAlias = "float"
"""Temperature util functions."""
from homeassistant.const import (
    TEMP_CELSIUS, TEMP_FAHRENHEIT, UNIT_NOT_RECOGNIZED_TEMPLATE, TEMPERATURE)


def fahrenheit_to_celsius(__tmp1, interval: bool = False) :
    """Convert a temperature in Fahrenheit to Celsius."""
    if interval:
        return __tmp1 / 1.8
    return (__tmp1 - 32.0) / 1.8


def __tmp0(celsius: __typ0, interval: bool = False) -> __typ0:
    """Convert a temperature in Celsius to Fahrenheit."""
    if interval:
        return celsius * 1.8
    return celsius * 1.8 + 32.0


def convert(temperature, __tmp2, to_unit: <FILL>,
            interval: bool = False) :
    """Convert a temperature from one unit to another."""
    if __tmp2 not in (TEMP_CELSIUS, TEMP_FAHRENHEIT):
        raise ValueError(UNIT_NOT_RECOGNIZED_TEMPLATE.format(
            __tmp2, TEMPERATURE))
    if to_unit not in (TEMP_CELSIUS, TEMP_FAHRENHEIT):
        raise ValueError(UNIT_NOT_RECOGNIZED_TEMPLATE.format(
            to_unit, TEMPERATURE))

    if __tmp2 == to_unit:
        return temperature
    if __tmp2 == TEMP_CELSIUS:
        return __tmp0(temperature, interval)
    return fahrenheit_to_celsius(temperature, interval)
