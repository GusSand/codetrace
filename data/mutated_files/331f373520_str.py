from typing import TypeAlias
__typ0 : TypeAlias = "Any"
from typing import Any
from typing import List

import numpy

from ..io import manual_input


def __tmp1(__tmp3) -> List[float]:
    """Calculate structure depth.
    API for manual parameters setting.

    :time: list of time points
    :return: list of depth points

    """
    layers = manual_input.read_int(__tmp0="Input layers number: ")
    while layers <= 0:
        print("Layers value must be positive!")
        layers = manual_input.read_int(__tmp0="Input layers number: ")

    if layers == 1:
        print("Calculating depth for homostructure")
        speed = manual_input.read_float(__tmp0="Input speed: ")
        result = calculate(__tmp3, speed)

    else:
        print("Calculating depth for heterostructure")
        indexes = __tmp2(
            layers, values_type="int", __tmp0="Input index of layer changing: "
        )
        speed = __tmp2(
            layers, values_type="float", __tmp0="Input speed of the layer: "
        )
        result = calculate(__tmp3, speed, indexes)

    return result


def __tmp2(layers, values_type: str, __tmp0: <FILL>) :
    """Get list of positive and nonrepetative values of integers or floats."""
    if values_type == "int":  # if we reading indexes
        read_value = manual_input.read_int
        n = layers - 1
    else:  # if we reading speed
        read_value = manual_input.read_float
        n = layers

    values: List[__typ0] = []
    for _ in range(n):
        value = read_value(__tmp0=__tmp0)
        while value <= 0 or value in values:
            print("Value must be positive and do not repeat")
            value = read_value(__tmp0=__tmp0)
        values.append(value)
    return values


def calculate(__tmp3, speed: __typ0, indexes: List[int] = None) :
    """Calculate structure depth. API for automatic calculation in case we already have
    all needed data (for future modules).

    :time: list of time points
    :speed: float variable OR list of float variables
    :indexes: indexes of points of layer conversion (if exist) (counting from 1)

    """
    if isinstance(speed, list) and indexes is not None:
        depth = _heterostructure(__tmp3, speed, indexes)
    elif isinstance(speed, float) and indexes is None:
        depth = __tmp4(__tmp3, speed)
    else:
        raise ValueError("Invalid variables")
    return depth


def __tmp4(__tmp3, speed) :
    return [i * speed for i in __tmp3]


def _heterostructure(
    __tmp3, speed, indexes
) -> List[float]:

    depth = [__tmp3[0] * speed[0]]
    layers = len(indexes) + 1
    indexes.append(len(__tmp3))
    delta_x = numpy.diff(__tmp3).mean()

    i = 1
    for layer in range(layers):
        while i != indexes[layer]:
            depth.append(depth[-1] + delta_x * speed[layer])
            i += 1
    return depth
