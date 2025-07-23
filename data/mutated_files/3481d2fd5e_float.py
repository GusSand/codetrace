from typing import TypeAlias
__typ0 : TypeAlias = "str"
"""Temperature util functions."""
from homeassistant.const import (
    TEMP_CELSIUS, TEMP_FAHRENHEIT, UNIT_NOT_RECOGNIZED_TEMPLATE, TEMPERATURE)


def __tmp5(__tmp4, interval: bool = False) :
    """Convert a temperature in Fahrenheit to Celsius."""
    if interval:
        return __tmp4 / 1.8
    return (__tmp4 - 32.0) / 1.8


def __tmp1(celsius: <FILL>, interval: bool = False) -> float:
    """Convert a temperature in Celsius to Fahrenheit."""
    if interval:
        return celsius * 1.8
    return celsius * 1.8 + 32.0


def __tmp0(__tmp3, __tmp2: __typ0, to_unit: __typ0,
            interval: bool = False) -> float:
    """Convert a temperature from one unit to another."""
    if __tmp2 not in (TEMP_CELSIUS, TEMP_FAHRENHEIT):
        raise ValueError(UNIT_NOT_RECOGNIZED_TEMPLATE.format(
            __tmp2, TEMPERATURE))
    if to_unit not in (TEMP_CELSIUS, TEMP_FAHRENHEIT):
        raise ValueError(UNIT_NOT_RECOGNIZED_TEMPLATE.format(
            to_unit, TEMPERATURE))

    if __tmp2 == to_unit:
        return __tmp3
    if __tmp2 == TEMP_CELSIUS:
        return __tmp1(__tmp3, interval)
    return __tmp5(__tmp3, interval)
