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

from typing import Any, List, overload, Tuple, TYPE_CHECKING, TypeVar, Union, Iterable

from cirq import ops

if TYPE_CHECKING:
    import cirq

# This is a special indicator value used by the inverse method to determine
# whether or not the caller provided a 'default' argument.
RaiseTypeErrorIfNotProvided: Tuple[List[Any]] = ([],)

__typ0 = TypeVar('TDefault')


# pylint: disable=function-redefined
@overload
def __tmp1(__tmp0) :
    pass


@overload
def __tmp1(__tmp0: 'cirq.Operation') :
    pass


@overload
def __tmp1(__tmp0) :
    pass


@overload
def __tmp1(__tmp0) :
    pass


@overload
def __tmp1(__tmp0: 'cirq.Gate', __tmp2: __typ0) :
    pass


@overload
def __tmp1(__tmp0, __tmp2) :
    pass


@overload
def __tmp1(__tmp0, __tmp2) -> Union[__typ0, 'cirq.Circuit']:
    pass


@overload
def __tmp1(__tmp0, __tmp2) :
    pass


def __tmp1(__tmp0: <FILL>, __tmp2: Any = RaiseTypeErrorIfNotProvided) :
    """Returns the inverse `val**-1` of the given value, if defined.

    An object can define an inverse by defining a __pow__(self, exponent) method
    that returns something besides NotImplemented when given the exponent -1.
    The inverse of iterables is by default defined to be the iterable's items,
    each inverted, in reverse order.

    Args:
        val: The value (or iterable of invertible values) to invert.
        default: Determines the fallback behavior when `val` doesn't have
            an inverse defined. If `default` is not set, a TypeError is raised.
            If `default` is set to a value, that value is returned.

    Returns:
        If `val` has a __pow__ method that returns something besides
        NotImplemented when given an exponent of -1, that result is returned.
        Otherwise, if `val` is iterable, the result is a tuple with the same
        items as `val` but in reverse order and with each item inverted.
        Otherwise, if a `default` argument was specified, it is returned.

    Raises:
        TypeError: `val` doesn't have a __pow__ method, or that method returned
            NotImplemented when given -1. Furthermore `val` isn't an
            iterable containing invertible items. Also, no `default` argument
            was specified.
    """

    # Check if object defines an inverse via __pow__.
    raiser = getattr(__tmp0, '__pow__', None)

    # pylint: disable=not-callable
    result = NotImplemented if raiser is None else raiser(-1)
    if result is not NotImplemented:
        return result

    # Maybe it's an iterable of invertible items?
    # Note: we avoid str because 'a'[0] == 'a', which creates an infinite loop.
    if isinstance(__tmp0, Iterable) and not isinstance(__tmp0, (str, ops.Operation)):
        unique_indicator: List[Any] = []
        results = tuple(__tmp1(e, unique_indicator) for e in __tmp0)
        if all(e is not unique_indicator for e in results):
            return results[::-1]

    # Can't invert.
    if __tmp2 is not RaiseTypeErrorIfNotProvided:
        return __tmp2
    raise TypeError(
        "object of type '{}' isn't invertible. "
        "It has no __pow__ method (or the method returned NotImplemented) "
        "and it isn't an iterable of invertible objects.".format(type(__tmp0))
    )


# pylint: enable=function-redefined
