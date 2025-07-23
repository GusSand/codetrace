from typing import Any
from typing import List

import numpy

from ..io import manual_input


def set_arguments_and_calculate(__tmp0: List[float]) -> List[float]:
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
        result = calculate(__tmp0, speed)

    else:
        print("Calculating depth for heterostructure")
        indexes = _get_list_of_values(
            layers, values_type="int", message="Input index of layer changing: "
        )
        speed = _get_list_of_values(
            layers, values_type="float", message="Input speed of the layer: "
        )
        result = calculate(__tmp0, speed, indexes)

    return result


def _get_list_of_values(layers: int, values_type: str, message: str) -> List[Any]:
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


def calculate(__tmp0, speed, indexes: List[int] = None) :
    """Calculate structure depth. API for automatic calculation in case we already have
    all needed data (for future modules).

    :time: list of time points
    :speed: float variable OR list of float variables
    :indexes: indexes of points of layer conversion (if exist) (counting from 1)

    """
    if isinstance(speed, list) and indexes is not None:
        depth = _heterostructure(__tmp0, speed, indexes)
    elif isinstance(speed, float) and indexes is None:
        depth = _homostructure(__tmp0, speed)
    else:
        raise ValueError("Invalid variables")
    return depth


def _homostructure(__tmp0: List[float], speed: <FILL>) :
    return [i * speed for i in __tmp0]


def _heterostructure(
    __tmp0, speed: List[float], indexes: List[int]
) -> List[float]:

    depth = [__tmp0[0] * speed[0]]
    layers = len(indexes) + 1
    indexes.append(len(__tmp0))
    delta_x = numpy.diff(__tmp0).mean()

    i = 1
    for layer in range(layers):
        while i != indexes[layer]:
            depth.append(depth[-1] + delta_x * speed[layer])
            i += 1
    return depth
