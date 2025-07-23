# Copyright 2018 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Optional, overload
import numpy as np
import sympy
from cirq.value import type_alias


def chosen_angle_to_half_turns(
    __tmp2: Optional[type_alias.TParamVal] = None,
    rads: Optional[float] = None,
    degs: Optional[float] = None,
    default: float = 1.0,
) :
    """Returns a half_turns value based on the given arguments.

    At most one of half_turns, rads, degs must be specified. If none are
    specified, the output defaults to half_turns=1.

    Args:
        half_turns: The number of half turns to rotate by.
        rads: The number of radians to rotate by.
        degs: The number of degrees to rotate by
        default: The half turns angle to use if nothing else is specified.

    Returns:
        A number of half turns.

    Raises:
        ValueError: If more than one of `half_turn`, `rads`, or `degs` is given.
    """

    if len([1 for e in [__tmp2, rads, degs] if e is not None]) > 1:
        raise ValueError('Redundant angle specification. Use ONE of half_turns, rads, or degs.')

    if rads is not None:
        return rads / np.pi

    if degs is not None:
        return degs / 180

    if __tmp2 is not None:
        return __tmp2

    return default


def __tmp1(
    __tmp2: Optional[type_alias.TParamVal] = None,
    rads: Optional[float] = None,
    degs: Optional[float] = None,
    default: float = 1.0,
) :
    """Returns a canonicalized half_turns based on the given arguments.

    At most one of half_turns, rads, degs must be specified. If none are
    specified, the output defaults to half_turns=1.

    Args:
        half_turns: The number of half turns to rotate by.
        rads: The number of radians to rotate by.
        degs: The number of degrees to rotate by
        default: The half turns angle to use if nothing else is specified.

    Returns:
        A number of half turns.
    """
    return __tmp0(
        chosen_angle_to_half_turns(__tmp2=__tmp2, rads=rads, degs=degs, default=default)
    )


# pylint: disable=function-redefined
@overload
def __tmp0(__tmp2: <FILL>) :
    pass


@overload
def __tmp0(__tmp2) :
    pass


def __tmp0(__tmp2) :
    """Wraps the input into the range (-1, +1]."""
    if isinstance(__tmp2, sympy.Basic):
        if not __tmp2.is_constant():
            return __tmp2
        __tmp2 = float(__tmp2)
    __tmp2 %= 2
    if __tmp2 > 1:
        __tmp2 -= 2
    return __tmp2


# pylint: enable=function-redefined
