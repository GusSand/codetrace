from typing import TypeAlias
__typ2 : TypeAlias = "str"
__typ1 : TypeAlias = "int"
__typ0 : TypeAlias = "float"
from typing import Any
from typing import List

import numpy

from ..io import manual_input


def __tmp1(__tmp4) :
    """Calculate structure depth.
    API for manual parameters setting.

    :time: list of time points
    :return: list of depth points

    """
    __tmp5 = manual_input.read_int(__tmp0="Input layers number: ")
    while __tmp5 <= 0:
        print("Layers value must be positive!")
        __tmp5 = manual_input.read_int(__tmp0="Input layers number: ")

    if __tmp5 == 1:
        print("Calculating depth for homostructure")
        __tmp6 = manual_input.read_float(__tmp0="Input speed: ")
        result = __tmp10(__tmp4, __tmp6)

    else:
        print("Calculating depth for heterostructure")
        __tmp3 = __tmp2(
            __tmp5, __tmp7="int", __tmp0="Input index of layer changing: "
        )
        __tmp6 = __tmp2(
            __tmp5, __tmp7="float", __tmp0="Input speed of the layer: "
        )
        result = __tmp10(__tmp4, __tmp6, __tmp3)

    return result


def __tmp2(__tmp5, __tmp7, __tmp0) -> List[Any]:
    """Get list of positive and nonrepetative values of integers or floats."""
    if __tmp7 == "int":  # if we reading indexes
        read_value = manual_input.read_int
        n = __tmp5 - 1
    else:  # if we reading speed
        read_value = manual_input.read_float
        n = __tmp5

    values: List[Any] = []
    for _ in range(n):
        value = read_value(__tmp0=__tmp0)
        while value <= 0 or value in values:
            print("Value must be positive and do not repeat")
            value = read_value(__tmp0=__tmp0)
        values.append(value)
    return values


def __tmp10(__tmp4, __tmp6: <FILL>, __tmp3: List[__typ1] = None) :
    """Calculate structure depth. API for automatic calculation in case we already have
    all needed data (for future modules).

    :time: list of time points
    :speed: float variable OR list of float variables
    :indexes: indexes of points of layer conversion (if exist) (counting from 1)

    """
    if isinstance(__tmp6, list) and __tmp3 is not None:
        depth = __tmp9(__tmp4, __tmp6, __tmp3)
    elif isinstance(__tmp6, __typ0) and __tmp3 is None:
        depth = __tmp8(__tmp4, __tmp6)
    else:
        raise ValueError("Invalid variables")
    return depth


def __tmp8(__tmp4, __tmp6) :
    return [i * __tmp6 for i in __tmp4]


def __tmp9(
    __tmp4, __tmp6, __tmp3
) :

    depth = [__tmp4[0] * __tmp6[0]]
    __tmp5 = len(__tmp3) + 1
    __tmp3.append(len(__tmp4))
    delta_x = numpy.diff(__tmp4).mean()

    i = 1
    for layer in range(__tmp5):
        while i != __tmp3[layer]:
            depth.append(depth[-1] + delta_x * __tmp6[layer])
            i += 1
    return depth
