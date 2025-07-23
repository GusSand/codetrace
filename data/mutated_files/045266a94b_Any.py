from typing import TypeAlias
__typ2 : TypeAlias = "float"
__typ3 : TypeAlias = "bool"
__typ0 : TypeAlias = "str"
__typ1 : TypeAlias = "int"
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
"""IdentityGate."""

from typing import Any, Dict, Optional, Tuple, TYPE_CHECKING, Sequence

import numpy as np
import sympy

from cirq import protocols, value
from cirq._doc import document
from cirq.ops import raw_types

if TYPE_CHECKING:
    import cirq


@value.value_equality
class IdentityGate(raw_types.Gate):
    """A Gate that perform no operation on qubits.

    The unitary matrix of this gate is a diagonal matrix with all 1s on the
    diagonal and all 0s off the diagonal in any basis.

    `cirq.I` is the single qubit identity gate.
    """

    def __init__(
        __tmp0, num_qubits: Optional[__typ1] = None, qid_shape: Optional[Tuple[__typ1, ...]] = None
    ) -> None:
        """Inits IdentityGate.

        Args:
            num_qubits: The number of qubits for the idenity gate.
            qid_shape: Specifies the dimension of each qid the measurement
                applies to.  The default is 2 for every qubit.

        Raises:
            ValueError: If the length of qid_shape doesn't equal num_qubits, or
                neither `num_qubits` or `qid_shape` is supplied.

        """
        if qid_shape is None:
            if num_qubits is None:
                raise ValueError('Specify either the num_qubits or qid_shape argument.')
            qid_shape = (2,) * num_qubits
        elif num_qubits is None:
            num_qubits = len(qid_shape)
        __tmp0._qid_shape = qid_shape
        if len(__tmp0._qid_shape) != num_qubits:
            raise ValueError('len(qid_shape) != num_qubits')

    def _act_on_(__tmp0, args: 'cirq.OperationTarget', __tmp3: Sequence['cirq.Qid']):
        return True

    def _qid_shape_(__tmp0) -> Tuple[__typ1, ...]:
        return __tmp0._qid_shape

    def num_qubits(__tmp0) -> __typ1:
        return len(__tmp0._qid_shape)

    def __pow__(__tmp0, power: <FILL>) :
        if isinstance(power, (__typ1, __typ2, complex, sympy.Basic)):
            return __tmp0
        return NotImplemented

    def _has_unitary_(__tmp0) -> __typ3:
        return True

    def _unitary_(__tmp0) -> np.ndarray:
        return np.identity(np.prod(__tmp0._qid_shape, dtype=np.int64).item())

    def __tmp4(__tmp0, args: 'protocols.ApplyUnitaryArgs') -> Optional[np.ndarray]:
        return args.target_tensor

    def _pauli_expansion_(__tmp0) -> value.LinearDict[__typ0]:
        if not all(d == 2 for d in __tmp0._qid_shape):
            return NotImplemented
        return value.LinearDict({'I' * __tmp0.num_qubits(): 1.0})

    def __repr__(__tmp0) -> __typ0:
        if __tmp0._qid_shape == (2,):
            return 'cirq.I'
        if all(e == 2 for e in __tmp0._qid_shape):
            return f'cirq.IdentityGate({len(__tmp0._qid_shape)})'
        return f'cirq.IdentityGate(qid_shape={__tmp0._qid_shape!r})'

    def _decompose_(__tmp0, __tmp3) -> 'cirq.OP_TREE':
        return []

    def __tmp5(__tmp0) -> __typ0:
        if __tmp0.num_qubits() == 1:
            return 'I'
        return f'I({__tmp0.num_qubits()})'

    def _value_equality_values_(__tmp0) -> Any:
        return __tmp0._qid_shape

    def _trace_distance_bound_(__tmp0) -> __typ2:
        return 0.0

    def _json_dict_(__tmp0) -> Dict[__typ0, Any]:
        other = {}
        if not all(d == 2 for d in __tmp0._qid_shape):
            other['qid_shape'] = __tmp0._qid_shape
        return {
            'num_qubits': len(__tmp0._qid_shape),
            **other,
        }

    def _mul_with_qubits(__tmp0, __tmp3, other):
        if isinstance(other, raw_types.Operation):
            return other
        if isinstance(other, (complex, __typ2, __typ1)):
            from cirq.ops.pauli_string import PauliString

            return PauliString(coefficient=other)
        return NotImplemented

    _rmul_with_qubits = _mul_with_qubits

    def _circuit_diagram_info_(__tmp0, args) :
        return ('I',) * __tmp0.num_qubits()

    def _qasm_(__tmp0, args: 'cirq.QasmArgs', __tmp3: Tuple['cirq.Qid', ...]) -> Optional[__typ0]:
        args.validate_version('2.0')
        return ''.join([args.format('id {0};\n', qubit) for qubit in __tmp3])

    def _quil_(
        __tmp0, __tmp3, formatter: 'cirq.QuilFormatter'
    ) -> Optional[__typ0]:
        return ''.join(formatter.format('I {0}\n', qubit) for qubit in __tmp3)

    @classmethod
    def __tmp2(cls, num_qubits, qid_shape=None, **kwargs):
        return cls(num_qubits=num_qubits, qid_shape=None if qid_shape is None else tuple(qid_shape))


I = IdentityGate(num_qubits=1)
document(
    I,
    """The one qubit identity gate.

    Matrix:
    ```
        [[1, 0],
         [0, 1]]
    ```
    """,
)


def __tmp1(*__tmp3: 'cirq.Qid') -> 'cirq.Operation':
    """Returns a single IdentityGate applied to all the given qubits.

    Args:
        *qubits: The qubits that the identity gate will apply to.

    Returns:
        An identity operation on the given qubits.

    Raises:
        ValueError: If the qubits are not instances of Qid.
    """
    for qubit in __tmp3:
        if not isinstance(qubit, raw_types.Qid):
            raise ValueError(f'Not a cirq.Qid: {qubit!r}.')
    return IdentityGate(qid_shape=protocols.qid_shape(__tmp3)).on(*__tmp3)
