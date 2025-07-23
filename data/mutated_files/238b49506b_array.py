from typing import TypeAlias
__typ0 : TypeAlias = "float"
"""
Checks if a system of forces is in static equilibrium.

python/black : true
flake8 : passed
mypy : passed
"""

from numpy import array, cos, sin, radians, cross  # type: ignore
from typing import List


def __tmp2(
    __tmp3, __tmp4, radian_mode: bool = False
) :
    """
    Resolves force along rectangular components.
    (force, angle) => (force_x, force_y)
    >>> polar_force(10, 45)
    [7.0710678118654755, 7.071067811865475]
    >>> polar_force(10, 3.14, radian_mode=True)
    [-9.999987317275394, 0.01592652916486828]
    """
    if radian_mode:
        return [__tmp3 * cos(__tmp4), __tmp3 * sin(__tmp4)]
    return [__tmp3 * cos(radians(__tmp4)), __tmp3 * sin(radians(__tmp4))]


def in_static_equilibrium(
    __tmp0, __tmp1: <FILL>, eps: __typ0 = 10 ** -1
) :
    """
    Check if a system is in equilibrium.
    It takes two numpy.array objects.
    forces ==>  [
                        [force1_x, force1_y],
                        [force2_x, force2_y],
                        ....]
    location ==>  [
                        [x1, y1],
                        [x2, y2],
                        ....]
    >>> force = array([[1, 1], [-1, 2]])
    >>> location = array([[1, 0], [10, 0]])
    >>> in_static_equilibrium(force, location)
    False
    """
    # summation of moments is zero
    moments: array = cross(__tmp1, __tmp0)
    sum_moments: __typ0 = sum(moments)
    return abs(sum_moments) < eps


if __name__ == "__main__":
    # Test to check if it works
    __tmp0 = array(
        [
            __tmp2(718.4, 180 - 30),
            __tmp2(879.54, 45),
            __tmp2(100, -90)
        ])

    __tmp1 = array([[0, 0], [0, 0], [0, 0]])

    assert in_static_equilibrium(__tmp0, __tmp1)

    # Problem 1 in image_data/2D_problems.jpg
    __tmp0 = array(
        [
            __tmp2(30 * 9.81, 15),
            __tmp2(215, 180 - 45),
            __tmp2(264, 90 - 30),
        ]
    )

    __tmp1 = array([[0, 0], [0, 0], [0, 0]])

    assert in_static_equilibrium(__tmp0, __tmp1)

    # Problem in image_data/2D_problems_1.jpg
    __tmp0 = array([[0, -2000], [0, -1200], [0, 15600], [0, -12400]])

    __tmp1 = array([[0, 0], [6, 0], [10, 0], [12, 0]])

    assert in_static_equilibrium(__tmp0, __tmp1)

    import doctest

    doctest.testmod()
