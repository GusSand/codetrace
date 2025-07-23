from typing import TypeAlias
__typ2 : TypeAlias = "str"
__typ3 : TypeAlias = "Any"
__typ0 : TypeAlias = "int"
# Copyright 2020 The Cirq Developers
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
"""Creates the gate instance for a two qubit diagonal gate.

The gate is used to create a 4x4 matrix with the diagonal elements
passed as a list.
"""

from typing import AbstractSet, Any, Tuple, Optional, Sequence, TYPE_CHECKING
import numpy as np
import sympy

from cirq import protocols, value
from cirq._compat import proper_repr
from cirq.ops import raw_types

if TYPE_CHECKING:
    import cirq


@value.value_equality()
class __typ1(raw_types.Gate):
    """A gate given by a diagonal 4\\times 4 matrix."""

    def __tmp7(__tmp1, __tmp6) :
        r"""A two qubit gate with only diagonal elements.

        This gate's off-diagonal elements are zero and it's on diagonal
        elements are all phases.

        Args:
            diag_angles_radians: The list of angles on the diagonal in radians.
                If these values are $(x_0, x_1, \ldots , x_3)$ then the unitary
                has diagonal values $(e^{i x_0}, e^{i x_1}, \ldots, e^{i x_3})$.
        """
        __tmp1._diag_angles_radians: Tuple[value.TParamVal, ...] = tuple(__tmp6)

    def _num_qubits_(__tmp1) :
        return 2

    def _is_parameterized_(__tmp1) :
        return any(protocols.is_parameterized(angle) for angle in __tmp1._diag_angles_radians)

    def _parameter_names_(__tmp1) :
        return {
            name for angle in __tmp1._diag_angles_radians for name in protocols.parameter_names(angle)
        }

    def _resolve_parameters_(
        __tmp1, resolver, __tmp10: <FILL>
    ) :
        return __typ1(
            protocols.resolve_parameters(__tmp1._diag_angles_radians, resolver, __tmp10)
        )

    def _has_unitary_(__tmp1) :
        return not __tmp1._is_parameterized_()

    def _unitary_(__tmp1) :
        if __tmp1._is_parameterized_():
            return None
        return np.diag([np.exp(1j * angle) for angle in __tmp1._diag_angles_radians])

    def __tmp9(__tmp1, __tmp0: 'protocols.ApplyUnitaryArgs') :
        if __tmp1._is_parameterized_():
            return NotImplemented
        for index, angle in enumerate(__tmp1._diag_angles_radians):
            subspace_index = __tmp0.subspace_index(big_endian_bits_int=index)
            __tmp0.target_tensor[subspace_index] *= np.exp(1j * angle)
        return __tmp0.target_tensor

    def _circuit_diagram_info_(
        __tmp1, __tmp0
    ) -> 'cirq.CircuitDiagramInfo':
        rounded_angles = np.array(__tmp1._diag_angles_radians)
        if __tmp0.precision is not None:
            rounded_angles = rounded_angles.round(__tmp0.precision)
        diag_str = f"diag({', '.join(proper_repr(angle) for angle in rounded_angles)})"
        return protocols.CircuitDiagramInfo((diag_str, '#2'))

    def __tmp3(__tmp1, exponent) :
        if not isinstance(exponent, (__typ0, float, sympy.Basic)):
            return NotImplemented
        angles = []
        for angle in __tmp1._diag_angles_radians:
            mulAngle = protocols.mul(angle, exponent, NotImplemented)
            if mulAngle == NotImplemented:
                return NotImplemented
            angles.append(mulAngle)
        return __typ1(angles)

    def __tmp2(__tmp1) :
        return tuple(__tmp1._diag_angles_radians)

    def __tmp5(__tmp1) :
        return 'cirq.TwoQubitDiagonalGate([{}])'.format(
            ','.join(proper_repr(angle) for angle in __tmp1._diag_angles_radians)
        )

    def _quil_(
        __tmp1, __tmp4, __tmp8
    ) :
        if np.count_nonzero(__tmp1._diag_angles_radians) == 1:
            if __tmp1._diag_angles_radians[0] != 0:
                return __tmp8.format(
                    'CPHASE00({0}) {1} {2}\n', __tmp1._diag_angles_radians[0], __tmp4[0], __tmp4[1]
                )
            elif __tmp1._diag_angles_radians[1] != 0:
                return __tmp8.format(
                    'CPHASE01({0}) {1} {2}\n', __tmp1._diag_angles_radians[1], __tmp4[0], __tmp4[1]
                )
            elif __tmp1._diag_angles_radians[2] != 0:
                return __tmp8.format(
                    'CPHASE10({0}) {1} {2}\n', __tmp1._diag_angles_radians[2], __tmp4[0], __tmp4[1]
                )
            elif __tmp1._diag_angles_radians[3] != 0:
                return __tmp8.format(
                    'CPHASE({0}) {1} {2}\n', __tmp1._diag_angles_radians[3], __tmp4[0], __tmp4[1]
                )
        return None
