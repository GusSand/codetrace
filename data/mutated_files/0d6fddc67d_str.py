from typing import TypeAlias
__typ2 : TypeAlias = "Any"
__typ1 : TypeAlias = "int"
__typ0 : TypeAlias = "float"
from typing import Any
from typing import List

import numpy

from ..io import manual_input


def __tmp0(__tmp2) :
    """Calculate structure depth.
    API for manual parameters setting.

    :time: list of time points
    :return: list of depth points

    """
    __tmp3 = manual_input.read_int(message="Input layers number: ")
    while __tmp3 <= 0:
        print("Layers value must be positive!")
        __tmp3 = manual_input.read_int(message="Input layers number: ")

    if __tmp3 == 1:
        print("Calculating depth for homostructure")
        speed = manual_input.read_float(message="Input speed: ")
        result = __tmp5(__tmp2, speed)

    else:
        print("Calculating depth for heterostructure")
        __tmp1 = _get_list_of_values(
            __tmp3, values_type="int", message="Input index of layer changing: "
        )
        speed = _get_list_of_values(
            __tmp3, values_type="float", message="Input speed of the layer: "
        )
        result = __tmp5(__tmp2, speed, __tmp1)

    return result


def _get_list_of_values(__tmp3, values_type: <FILL>, message) :
    """Get list of positive and nonrepetative values of integers or floats."""
    if values_type == "int":  # if we reading indexes
        read_value = manual_input.read_int
        n = __tmp3 - 1
    else:  # if we reading speed
        read_value = manual_input.read_float
        n = __tmp3

    values: List[__typ2] = []
    for _ in range(n):
        value = read_value(message=message)
        while value <= 0 or value in values:
            print("Value must be positive and do not repeat")
            value = read_value(message=message)
        values.append(value)
    return values


def __tmp5(__tmp2, speed: __typ2, __tmp1: List[__typ1] = None) :
    """Calculate structure depth. API for automatic calculation in case we already have
    all needed data (for future modules).

    :time: list of time points
    :speed: float variable OR list of float variables
    :indexes: indexes of points of layer conversion (if exist) (counting from 1)

    """
    if isinstance(speed, list) and __tmp1 is not None:
        depth = __tmp4(__tmp2, speed, __tmp1)
    elif isinstance(speed, __typ0) and __tmp1 is None:
        depth = _homostructure(__tmp2, speed)
    else:
        raise ValueError("Invalid variables")
    return depth


def _homostructure(__tmp2: List[__typ0], speed) -> List[__typ0]:
    return [i * speed for i in __tmp2]


def __tmp4(
    __tmp2, speed, __tmp1: List[__typ1]
) -> List[__typ0]:

    depth = [__tmp2[0] * speed[0]]
    __tmp3 = len(__tmp1) + 1
    __tmp1.append(len(__tmp2))
    delta_x = numpy.diff(__tmp2).mean()

    i = 1
    for layer in range(__tmp3):
        while i != __tmp1[layer]:
            depth.append(depth[-1] + delta_x * speed[layer])
            i += 1
    return depth
