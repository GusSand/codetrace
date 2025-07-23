from typing import TypeAlias
__typ4 : TypeAlias = "float"
__typ1 : TypeAlias = "str"
__typ0 : TypeAlias = "int"
__typ3 : TypeAlias = "bool"
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


class __typ2:
    """Wrapper for periodic numerical values.

    Wrapper for periodic numerical types which implements `__eq__`, `__ne__`,
    `__hash__` and `_approx_eq_` so that values which are in the same
    equivalence class are treated as equal.

    Internally the `value` passed to `__init__` is normalized to the interval
    [0, `period`) and stored as that. Specialized version of `_approx_eq_` is
    provided to cover values which end up at the opposite edges of this
    interval.
    """

    def __tmp11(__tmp1, value: Union[__typ0, __typ4], period: Union[__typ0, __typ4]):
        """Initializes the equivalence class.

        Args:
            value: numerical value to wrap.
            period: periodicity of the numerical value.
        """
        __tmp1.value = value % period
        __tmp1.period = period

    def __tmp2(__tmp1, __tmp10: <FILL>) -> __typ3:
        if not isinstance(__tmp10, type(__tmp1)):
            return NotImplemented
        return (__tmp1.value, __tmp1.period) == (__tmp10.value, __tmp10.period)

    def __tmp0(__tmp1, __tmp10) :
        return not __tmp1 == __tmp10

    def __tmp6(__tmp1) -> __typ0:
        return hash((type(__tmp1), __tmp1.value, __tmp1.period))

    def __tmp3(__tmp1, __tmp10, __tmp5: __typ4) :
        """Implementation of `SupportsApproximateEquality` protocol."""
        # HACK: Avoids circular dependencies.
        from cirq.protocols import approx_eq

        if not isinstance(__tmp10, type(__tmp1)):
            return NotImplemented

        # self.value = value % period in __init__() creates a Mod
        if isinstance(__tmp10.value, sympy.Mod):
            return __tmp1.value == __tmp10.value
        # Periods must be exactly equal to avoid drift of normalized value when
        # original value increases.
        if __tmp1.period != __tmp10.period:
            return False

        low = min(__tmp1.value, __tmp10.value)
        high = max(__tmp1.value, __tmp10.value)

        # Shift lower value outside of normalization interval in case low and
        # high values are at the opposite borders of normalization interval.
        if high - low > __tmp1.period / 2:
            low += __tmp1.period

        return approx_eq(low, high, __tmp5=__tmp5)

    def __tmp12(__tmp1) -> __typ1:
        v = proper_repr(__tmp1.value)
        p = proper_repr(__tmp1.period)
        return f'cirq.PeriodicValue({v}, {p})'

    def __tmp4(__tmp1) -> __typ3:
        # HACK: Avoids circular dependencies.
        from cirq.protocols import is_parameterized

        return is_parameterized(__tmp1.value) or is_parameterized(__tmp1.period)

    def __tmp7(__tmp1) :
        # HACK: Avoids circular dependencies.
        from cirq.protocols import parameter_names

        return parameter_names(__tmp1.value) | parameter_names(__tmp1.period)

    def __tmp8(
        __tmp1, __tmp9: 'cirq.ParamResolver', __tmp13: __typ3
    ) -> 'PeriodicValue':
        # HACK: Avoids circular dependencies.
        from cirq.protocols import resolve_parameters

        return __typ2(
            value=resolve_parameters(__tmp1.value, __tmp9, __tmp13),
            period=resolve_parameters(__tmp1.period, __tmp9, __tmp13),
        )
