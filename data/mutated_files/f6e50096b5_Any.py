from typing import TypeAlias
__typ1 : TypeAlias = "bool"
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
class TwoQubitDiagonalGate(raw_types.Gate):
    """A gate given by a diagonal 4\\times 4 matrix."""

    def __init__(__tmp1, diag_angles_radians: Sequence[value.TParamVal]) -> None:
        r"""A two qubit gate with only diagonal elements.

        This gate's off-diagonal elements are zero and it's on diagonal
        elements are all phases.

        Args:
            diag_angles_radians: The list of angles on the diagonal in radians.
                If these values are $(x_0, x_1, \ldots , x_3)$ then the unitary
                has diagonal values $(e^{i x_0}, e^{i x_1}, \ldots, e^{i x_3})$.
        """
        __tmp1._diag_angles_radians: Tuple[value.TParamVal, ...] = tuple(diag_angles_radians)

    def __tmp2(__tmp1) -> __typ0:
        return 2

    def _is_parameterized_(__tmp1) -> __typ1:
        return any(protocols.is_parameterized(angle) for angle in __tmp1._diag_angles_radians)

    def __tmp8(__tmp1) -> AbstractSet[str]:
        return {
            name for angle in __tmp1._diag_angles_radians for name in protocols.parameter_names(angle)
        }

    def __tmp9(
        __tmp1, resolver: 'cirq.ParamResolver', recursive: __typ1
    ) -> 'TwoQubitDiagonalGate':
        return TwoQubitDiagonalGate(
            protocols.resolve_parameters(__tmp1._diag_angles_radians, resolver, recursive)
        )

    def _has_unitary_(__tmp1) -> __typ1:
        return not __tmp1._is_parameterized_()

    def __tmp4(__tmp1) -> Optional[np.ndarray]:
        if __tmp1._is_parameterized_():
            return None
        return np.diag([np.exp(1j * angle) for angle in __tmp1._diag_angles_radians])

    def __tmp12(__tmp1, args: 'protocols.ApplyUnitaryArgs') -> np.ndarray:
        if __tmp1._is_parameterized_():
            return NotImplemented
        for index, angle in enumerate(__tmp1._diag_angles_radians):
            subspace_index = args.subspace_index(big_endian_bits_int=index)
            args.target_tensor[subspace_index] *= np.exp(1j * angle)
        return args.target_tensor

    def __tmp0(
        __tmp1, args: 'cirq.CircuitDiagramInfoArgs'
    ) -> 'cirq.CircuitDiagramInfo':
        rounded_angles = np.array(__tmp1._diag_angles_radians)
        if args.precision is not None:
            rounded_angles = rounded_angles.round(args.precision)
        diag_str = f"diag({', '.join(proper_repr(angle) for angle in rounded_angles)})"
        return protocols.CircuitDiagramInfo((diag_str, '#2'))

    def __tmp3(__tmp1, __tmp5: <FILL>) -> 'TwoQubitDiagonalGate':
        if not isinstance(__tmp5, (__typ0, float, sympy.Basic)):
            return NotImplemented
        angles = []
        for angle in __tmp1._diag_angles_radians:
            mulAngle = protocols.mul(angle, __tmp5, NotImplemented)
            if mulAngle == NotImplemented:
                return NotImplemented
            angles.append(mulAngle)
        return TwoQubitDiagonalGate(angles)

    def __tmp11(__tmp1) -> Any:
        return tuple(__tmp1._diag_angles_radians)

    def __repr__(__tmp1) :
        return 'cirq.TwoQubitDiagonalGate([{}])'.format(
            ','.join(proper_repr(angle) for angle in __tmp1._diag_angles_radians)
        )

    def __tmp6(
        __tmp1, __tmp7: Tuple['cirq.Qid', ...], __tmp10: 'cirq.QuilFormatter'
    ) -> Optional[str]:
        if np.count_nonzero(__tmp1._diag_angles_radians) == 1:
            if __tmp1._diag_angles_radians[0] != 0:
                return __tmp10.format(
                    'CPHASE00({0}) {1} {2}\n', __tmp1._diag_angles_radians[0], __tmp7[0], __tmp7[1]
                )
            elif __tmp1._diag_angles_radians[1] != 0:
                return __tmp10.format(
                    'CPHASE01({0}) {1} {2}\n', __tmp1._diag_angles_radians[1], __tmp7[0], __tmp7[1]
                )
            elif __tmp1._diag_angles_radians[2] != 0:
                return __tmp10.format(
                    'CPHASE10({0}) {1} {2}\n', __tmp1._diag_angles_radians[2], __tmp7[0], __tmp7[1]
                )
            elif __tmp1._diag_angles_radians[3] != 0:
                return __tmp10.format(
                    'CPHASE({0}) {1} {2}\n', __tmp1._diag_angles_radians[3], __tmp7[0], __tmp7[1]
                )
        return None
