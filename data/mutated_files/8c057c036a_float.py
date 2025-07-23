from typing import TypeAlias
__typ0 : TypeAlias = "str"
"""Temperature util functions."""
from homeassistant.const import (
    TEMP_CELSIUS, TEMP_FAHRENHEIT, UNIT_NOT_RECOGNIZED_TEMPLATE, TEMPERATURE)


def __tmp6(__tmp5: <FILL>, interval: bool = False) :
    """Convert a temperature in Fahrenheit to Celsius."""
    if interval:
        return __tmp5 / 1.8
    return (__tmp5 - 32.0) / 1.8


def celsius_to_fahrenheit(__tmp1, interval: bool = False) :
    """Convert a temperature in Celsius to Fahrenheit."""
    if interval:
        return __tmp1 * 1.8
    return __tmp1 * 1.8 + 32.0


def __tmp0(__tmp4, __tmp2, __tmp3,
            interval: bool = False) :
    """Convert a temperature from one unit to another."""
    if __tmp2 not in (TEMP_CELSIUS, TEMP_FAHRENHEIT):
        raise ValueError(UNIT_NOT_RECOGNIZED_TEMPLATE.format(
            __tmp2, TEMPERATURE))
    if __tmp3 not in (TEMP_CELSIUS, TEMP_FAHRENHEIT):
        raise ValueError(UNIT_NOT_RECOGNIZED_TEMPLATE.format(
            __tmp3, TEMPERATURE))

    if __tmp2 == __tmp3:
        return __tmp4
    if __tmp2 == TEMP_CELSIUS:
        return celsius_to_fahrenheit(__tmp4, interval)
    return __tmp6(__tmp4, interval)
