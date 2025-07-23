from typing import TypeAlias
__typ0 : TypeAlias = "str"
"""Temperature util functions."""
from homeassistant.const import (
    TEMP_CELSIUS, TEMP_FAHRENHEIT, UNIT_NOT_RECOGNIZED_TEMPLATE, TEMPERATURE)


def __tmp5(__tmp4) :
    """Convert a temperature in Fahrenheit to Celsius."""
    return (__tmp4 - 32.0) / 1.8


def __tmp1(celsius: <FILL>) :
    """Convert a temperature in Celsius to Fahrenheit."""
    return celsius * 1.8 + 32.0


def __tmp0(__tmp3, from_unit, __tmp2) :
    """Convert a temperature from one unit to another."""
    if from_unit not in (TEMP_CELSIUS, TEMP_FAHRENHEIT):
        raise ValueError(UNIT_NOT_RECOGNIZED_TEMPLATE.format(
            from_unit, TEMPERATURE))
    if __tmp2 not in (TEMP_CELSIUS, TEMP_FAHRENHEIT):
        raise ValueError(UNIT_NOT_RECOGNIZED_TEMPLATE.format(
            __tmp2, TEMPERATURE))

    if from_unit == __tmp2:
        return __tmp3
    elif from_unit == TEMP_CELSIUS:
        return __tmp1(__tmp3)
    return __tmp5(__tmp3)
