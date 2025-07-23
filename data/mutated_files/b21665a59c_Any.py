from typing import TypeAlias
__typ1 : TypeAlias = "bool"
# Copyright 2019 The Cirq Developers
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

import numbers
from collections.abc import Iterable
from typing import Any, Union

import numpy as np
from typing_extensions import Protocol

from cirq import linalg
from cirq._doc import doc_private
from cirq.protocols.approximate_equality_protocol import approx_eq


class __typ0(Protocol):
    """Object which can be compared for equality mod global phase."""

    @doc_private
    def __tmp3(__tmp1, __tmp4, *, __tmp2: Union[int, float]) -> __typ1:
        """Approximate comparator.

        Types implementing this protocol define their own logic for comparison
        with other types.

        Args:
            other: Target object for comparison of equality up to global phase.
            atol: The minimum absolute tolerance. See `np.isclose()`
                documentation for details.

        Returns:
            True if objects are equal up to a global phase, False otherwise.
            Returns NotImplemented when checking equality up to a global phase
            is not implemented for given types.
        """


def __tmp5(__tmp0, __tmp4: <FILL>, *, __tmp2: Union[int, float] = 1e-8) -> __typ1:
    """Determine whether two objects are equal up to global phase.

    If `val` implements a `_equal_up_to_global_phase_` method then it is
    invoked and takes precedence over all other checks:
     - For complex primitive type the magnitudes of the values are compared.
     - For `val` and `other` both iterable of the same length, consecutive
       elements are compared recursively. Types of `val` and `other` does not
       necessarily needs to match each other. They just need to be iterable and
       have the same structure.
     - For all other types, fall back to `_approx_eq_`

    Args:
        val: Source object for approximate comparison.
        other: Target object for approximate comparison.
        atol: The minimum absolute tolerance. This places an upper bound on
        the differences in *magnitudes* of two compared complex numbers.

    Returns:
        True if objects are approximately equal up to phase, False otherwise.
    """

    # Attempt _equal_up_to_global_phase_ for val.
    eq_up_to_phase_getter = getattr(__tmp0, '_equal_up_to_global_phase_', None)
    if eq_up_to_phase_getter is not None:
        result = eq_up_to_phase_getter(__tmp4, __tmp2)
        if result is not NotImplemented:
            return result

    # Fall back to _equal_up_to_global_phase_ for other.
    other_eq_up_to_phase_getter = getattr(__tmp4, '_equal_up_to_global_phase_', None)
    if other_eq_up_to_phase_getter is not None:
        result = other_eq_up_to_phase_getter(__tmp0, __tmp2)
        if result is not NotImplemented:
            return result

    # Fall back to special check for numeric arrays.
    # Defer to numpy automatic type casting to determine numeric type.
    if isinstance(__tmp0, Iterable) and isinstance(__tmp4, Iterable):
        a = np.asarray(__tmp0)
        b = np.asarray(__tmp4)
        if a.dtype.kind in 'uifc' and b.dtype.kind in 'uifc':
            return linalg.allclose_up_to_global_phase(a, b, __tmp2=__tmp2)

    # Fall back to approx_eq for compare the magnitude of two numbers.
    if isinstance(__tmp0, numbers.Number) and isinstance(__tmp4, numbers.Number):
        result = approx_eq(abs(__tmp0), abs(__tmp4), __tmp2=__tmp2)  # type: ignore
        if result is not NotImplemented:
            return result

    # Fall back to cirq approx_eq for remaining types.
    return approx_eq(__tmp0, __tmp4, __tmp2=__tmp2)
