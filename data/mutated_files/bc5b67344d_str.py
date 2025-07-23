from typing import TypeAlias
__typ0 : TypeAlias = "float"
"""Temperature util functions."""
from homeassistant.const import (
    TEMP_CELSIUS, TEMP_FAHRENHEIT, UNIT_NOT_RECOGNIZED_TEMPLATE, TEMPERATURE)


def __tmp5(fahrenheit: __typ0) -> __typ0:
    """Convert a temperature in Fahrenheit to Celsius."""
    return (fahrenheit - 32.0) / 1.8


def __tmp2(__tmp1: __typ0) -> __typ0:
    """Convert a temperature in Celsius to Fahrenheit."""
    return __tmp1 * 1.8 + 32.0


def __tmp0(__tmp4: __typ0, from_unit: str, __tmp3: <FILL>) :
    """Convert a temperature from one unit to another."""
    if from_unit not in (TEMP_CELSIUS, TEMP_FAHRENHEIT):
        raise ValueError(UNIT_NOT_RECOGNIZED_TEMPLATE.format(
            from_unit, TEMPERATURE))
    if __tmp3 not in (TEMP_CELSIUS, TEMP_FAHRENHEIT):
        raise ValueError(UNIT_NOT_RECOGNIZED_TEMPLATE.format(
            __tmp3, TEMPERATURE))

    if from_unit == __tmp3:
        return __tmp4
    elif from_unit == TEMP_CELSIUS:
        return __tmp2(__tmp4)
    return __tmp5(__tmp4)
