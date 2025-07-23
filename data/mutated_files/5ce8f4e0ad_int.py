from typing import TypeAlias
__typ1 : TypeAlias = "str"
__typ0 : TypeAlias = "float"
from typing import Any
from typing import List

import numpy

from ..io import manual_input


def __tmp1(__tmp2: List[__typ0]) :
    """Calculate structure depth.
    API for manual parameters setting.

    :time: list of time points
    :return: list of depth points

    """
    layers = manual_input.read_int(message="Input layers number: ")
    while layers <= 0:
        print("Layers value must be positive!")
        layers = manual_input.read_int(message="Input layers number: ")

    if layers == 1:
        print("Calculating depth for homostructure")
        speed = manual_input.read_float(message="Input speed: ")
        result = calculate(__tmp2, speed)

    else:
        print("Calculating depth for heterostructure")
        indexes = _get_list_of_values(
            layers, values_type="int", message="Input index of layer changing: "
        )
        speed = _get_list_of_values(
            layers, values_type="float", message="Input speed of the layer: "
        )
        result = calculate(__tmp2, speed, indexes)

    return result


def _get_list_of_values(layers: <FILL>, values_type, message: __typ1) -> List[Any]:
    """Get list of positive and nonrepetative values of integers or floats."""
    if values_type == "int":  # if we reading indexes
        read_value = manual_input.read_int
        n = layers - 1
    else:  # if we reading speed
        read_value = manual_input.read_float
        n = layers

    values: List[Any] = []
    for _ in range(n):
        value = read_value(message=message)
        while value <= 0 or value in values:
            print("Value must be positive and do not repeat")
            value = read_value(message=message)
        values.append(value)
    return values


def calculate(__tmp2, speed: Any, indexes: List[int] = None) -> List[__typ0]:
    """Calculate structure depth. API for automatic calculation in case we already have
    all needed data (for future modules).

    :time: list of time points
    :speed: float variable OR list of float variables
    :indexes: indexes of points of layer conversion (if exist) (counting from 1)

    """
    if isinstance(speed, list) and indexes is not None:
        depth = __tmp0(__tmp2, speed, indexes)
    elif isinstance(speed, __typ0) and indexes is None:
        depth = __tmp3(__tmp2, speed)
    else:
        raise ValueError("Invalid variables")
    return depth


def __tmp3(__tmp2: List[__typ0], speed) -> List[__typ0]:
    return [i * speed for i in __tmp2]


def __tmp0(
    __tmp2, speed, indexes
) :

    depth = [__tmp2[0] * speed[0]]
    layers = len(indexes) + 1
    indexes.append(len(__tmp2))
    delta_x = numpy.diff(__tmp2).mean()

    i = 1
    for layer in range(layers):
        while i != indexes[layer]:
            depth.append(depth[-1] + delta_x * speed[layer])
            i += 1
    return depth
