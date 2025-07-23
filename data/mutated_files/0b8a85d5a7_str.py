from typing import TypeAlias
__typ0 : TypeAlias = "float"
"""Temperature util functions."""
from homeassistant.const import (
    TEMP_CELSIUS, TEMP_FAHRENHEIT, UNIT_NOT_RECOGNIZED_TEMPLATE, TEMPERATURE)


def fahrenheit_to_celsius(fahrenheit, interval: bool = False) :
    """Convert a temperature in Fahrenheit to Celsius."""
    if interval:
        return fahrenheit / 1.8
    return (fahrenheit - 32.0) / 1.8


def __tmp0(celsius, interval: bool = False) :
    """Convert a temperature in Celsius to Fahrenheit."""
    if interval:
        return celsius * 1.8
    return celsius * 1.8 + 32.0


def convert(temperature, from_unit: <FILL>, __tmp1,
            interval: bool = False) :
    """Convert a temperature from one unit to another."""
    if from_unit not in (TEMP_CELSIUS, TEMP_FAHRENHEIT):
        raise ValueError(UNIT_NOT_RECOGNIZED_TEMPLATE.format(
            from_unit, TEMPERATURE))
    if __tmp1 not in (TEMP_CELSIUS, TEMP_FAHRENHEIT):
        raise ValueError(UNIT_NOT_RECOGNIZED_TEMPLATE.format(
            __tmp1, TEMPERATURE))

    if from_unit == __tmp1:
        return temperature
    if from_unit == TEMP_CELSIUS:
        return __tmp0(temperature, interval)
    return fahrenheit_to_celsius(temperature, interval)
