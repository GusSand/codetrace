from typing import TypeAlias
__typ0 : TypeAlias = "float"
__typ1 : TypeAlias = "bool"
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

from typing import AbstractSet, Any, TYPE_CHECKING, Union

import sympy

from cirq._compat import proper_repr


if TYPE_CHECKING:
    import cirq


class PeriodicValue:
    """Wrapper for periodic numerical values.

    Wrapper for periodic numerical types which implements `__eq__`, `__ne__`,
    `__hash__` and `_approx_eq_` so that values which are in the same
    equivalence class are treated as equal.

    Internally the `value` passed to `__init__` is normalized to the interval
    [0, `period`) and stored as that. Specialized version of `_approx_eq_` is
    provided to cover values which end up at the opposite edges of this
    interval.
    """

    def __init__(__tmp1, value: Union[int, __typ0], period: Union[int, __typ0]):
        """Initializes the equivalence class.

        Args:
            value: numerical value to wrap.
            period: periodicity of the numerical value.
        """
        __tmp1.value = value % period
        __tmp1.period = period

    def __tmp3(__tmp1, __tmp0) -> __typ1:
        if not isinstance(__tmp0, type(__tmp1)):
            return NotImplemented
        return (__tmp1.value, __tmp1.period) == (__tmp0.value, __tmp0.period)

    def __ne__(__tmp1, __tmp0: <FILL>) -> __typ1:
        return not __tmp1 == __tmp0

    def __hash__(__tmp1) :
        return hash((type(__tmp1), __tmp1.value, __tmp1.period))

    def _approx_eq_(__tmp1, __tmp0, __tmp2) :
        """Implementation of `SupportsApproximateEquality` protocol."""
        # HACK: Avoids circular dependencies.
        from cirq.protocols import approx_eq

        if not isinstance(__tmp0, type(__tmp1)):
            return NotImplemented

        # self.value = value % period in __init__() creates a Mod
        if isinstance(__tmp0.value, sympy.Mod):
            return __tmp1.value == __tmp0.value
        # Periods must be exactly equal to avoid drift of normalized value when
        # original value increases.
        if __tmp1.period != __tmp0.period:
            return False

        low = min(__tmp1.value, __tmp0.value)
        high = max(__tmp1.value, __tmp0.value)

        # Shift lower value outside of normalization interval in case low and
        # high values are at the opposite borders of normalization interval.
        if high - low > __tmp1.period / 2:
            low += __tmp1.period

        return approx_eq(low, high, __tmp2=__tmp2)

    def __repr__(__tmp1) :
        v = proper_repr(__tmp1.value)
        p = proper_repr(__tmp1.period)
        return f'cirq.PeriodicValue({v}, {p})'

    def _is_parameterized_(__tmp1) -> __typ1:
        # HACK: Avoids circular dependencies.
        from cirq.protocols import is_parameterized

        return is_parameterized(__tmp1.value) or is_parameterized(__tmp1.period)

    def _parameter_names_(__tmp1) -> AbstractSet[str]:
        # HACK: Avoids circular dependencies.
        from cirq.protocols import parameter_names

        return parameter_names(__tmp1.value) | parameter_names(__tmp1.period)

    def _resolve_parameters_(
        __tmp1, resolver: 'cirq.ParamResolver', recursive: __typ1
    ) -> 'PeriodicValue':
        # HACK: Avoids circular dependencies.
        from cirq.protocols import resolve_parameters

        return PeriodicValue(
            value=resolve_parameters(__tmp1.value, resolver, recursive),
            period=resolve_parameters(__tmp1.period, resolver, recursive),
        )
