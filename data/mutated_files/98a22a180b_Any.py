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

from typing import Any

from cirq.protocols.resolve_parameters import is_parameterized

# This is a special indicator value used to determine whether or not the caller
# provided a 'default' argument.
RaiseTypeErrorIfNotProvided: Any = ([],)


def __tmp0(__tmp1: Any, __tmp2: <FILL>, default: Any = RaiseTypeErrorIfNotProvided) :
    """Returns lhs * rhs, or else a default if the operator is not implemented.

    This method is mostly used by __pow__ methods trying to return
    NotImplemented instead of causing a TypeError.

    Args:
        lhs: Left hand side of the multiplication.
        rhs: Right hand side of the multiplication.
        default: Default value to return if the multiplication is not defined.
            If not default is specified, a type error is raised when the
            multiplication fails.

    Returns:
        The product of the two inputs, or else the default value if the product
        is not defined, or else raises a TypeError if no default is defined.

    Raises:
        TypeError:
            lhs doesn't have __mul__ or it returned NotImplemented
            AND lhs doesn't have __rmul__ or it returned NotImplemented
            AND a default value isn't specified.
    """
    # Use left-hand-side's __mul__.
    left_mul = getattr(__tmp1, '__mul__', None)
    result = NotImplemented if left_mul is None else left_mul(__tmp2)

    # Fallback to right-hand-side's __rmul__.
    if result is NotImplemented:
        right_mul = getattr(__tmp2, '__rmul__', None)
        result = NotImplemented if right_mul is None else right_mul(__tmp1)

    # Don't build up factors of 1.0 vs sympy Symbols.
    if __tmp1 == 1 and is_parameterized(__tmp2):
        result = __tmp2
    if __tmp2 == 1 and is_parameterized(__tmp1):
        result = __tmp1
    if __tmp1 == -1 and is_parameterized(__tmp2):
        result = -__tmp2
    if __tmp2 == -1 and is_parameterized(__tmp1):
        result = -__tmp1

    # Output.
    if result is not NotImplemented:
        return result
    if default is not RaiseTypeErrorIfNotProvided:
        return default
    raise TypeError(f"unsupported operand type(s) for *: '{type(__tmp1)}' and '{type(__tmp2)}'")


# pylint: enable=function-redefined, redefined-builtin
