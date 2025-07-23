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

from typing import List, Sequence, Tuple, cast, Dict, TYPE_CHECKING

import numpy as np

from cirq import value, protocols
from cirq._compat import proper_repr
from cirq.ops import gate_features, common_gates, eigen_gate, pauli_gates
from cirq.ops.clifford_gate import SingleQubitCliffordGate

if TYPE_CHECKING:
    import cirq

pauli_eigen_map = cast(
    Dict[pauli_gates.Pauli, np.ndarray],
    {
        pauli_gates.X: (np.array([[0.5, 0.5], [0.5, 0.5]]), np.array([[0.5, -0.5], [-0.5, 0.5]])),
        pauli_gates.Y: (
            np.array([[0.5, -0.5j], [0.5j, 0.5]]),
            np.array([[0.5, 0.5j], [-0.5j, 0.5]]),
        ),
        pauli_gates.Z: (np.diag([1, 0]), np.diag([0, 1])),
    },
)


@value.value_equality
class PauliInteractionGate(gate_features.InterchangeableQubitsGate, eigen_gate.EigenGate):
    """A CZ conjugated by arbitrary single qubit Cliffords."""

    CZ: 'PauliInteractionGate'
    CNOT: 'PauliInteractionGate'

    def __init__(
        __tmp0,
        pauli0,
        invert0,
        pauli1,
        invert1,
        *,
        exponent: value.TParamVal = 1.0,
    ) :
        """Inits PauliInteractionGate.

        Args:
            pauli0: The interaction axis for the first qubit.
            invert0: Whether to condition on the +1 or -1 eigenvector of the
                first qubit's interaction axis.
            pauli1: The interaction axis for the second qubit.
            invert1: Whether to condition on the +1 or -1 eigenvector of the
                second qubit's interaction axis.
            exponent: Determines the amount of phasing to apply to the vector
                equal to the tensor product of the two conditions.
        """
        super().__init__(exponent=exponent)
        __tmp0.pauli0 = pauli0
        __tmp0.invert0 = invert0
        __tmp0.pauli1 = pauli1
        __tmp0.invert1 = invert1

    def _num_qubits_(__tmp0) :
        return 2

    def _value_equality_values_(__tmp0):
        return (__tmp0.pauli0, __tmp0.invert0, __tmp0.pauli1, __tmp0.invert1, __tmp0._canonical_exponent)

    def qubit_index_to_equivalence_group_key(__tmp0, __tmp1: <FILL>) :
        if __tmp0.pauli0 == __tmp0.pauli1 and __tmp0.invert0 == __tmp0.invert1:
            return 0
        return __tmp1

    def _with_exponent(__tmp0, exponent) :
        return PauliInteractionGate(
            __tmp0.pauli0, __tmp0.invert0, __tmp0.pauli1, __tmp0.invert1, exponent=exponent
        )

    def _eigen_shifts(__tmp0) :
        return [0.0, 1.0]

    def _eigen_components(__tmp0) :
        comp1 = np.kron(
            pauli_eigen_map[__tmp0.pauli0][not __tmp0.invert0],
            pauli_eigen_map[__tmp0.pauli1][not __tmp0.invert1],
        )
        comp0 = np.eye(4) - comp1
        return [(0, comp0), (1, comp1)]

    def _decompose_(__tmp0, qubits) :
        q0, q1 = qubits
        right_gate0 = SingleQubitCliffordGate.from_single_map(z_to=(__tmp0.pauli0, __tmp0.invert0))
        right_gate1 = SingleQubitCliffordGate.from_single_map(z_to=(__tmp0.pauli1, __tmp0.invert1))

        left_gate0 = right_gate0 ** -1
        left_gate1 = right_gate1 ** -1
        yield left_gate0(q0)
        yield left_gate1(q1)
        yield common_gates.CZ(q0, q1) ** __tmp0._exponent
        yield right_gate0(q0)
        yield right_gate1(q1)

    def _circuit_diagram_info_(
        __tmp0, args
    ) :
        labels: Dict['cirq.Pauli', str] = {
            pauli_gates.X: 'X',
            pauli_gates.Y: 'Y',
            pauli_gates.Z: '@',
        }
        l0 = labels[__tmp0.pauli0]
        l1 = labels[__tmp0.pauli1]
        # Add brackets around letter if inverted
        l0 = f'(-{l0})' if __tmp0.invert0 else l0
        l1 = f'(-{l1})' if __tmp0.invert1 else l1
        return protocols.CircuitDiagramInfo(
            wire_symbols=(l0, l1), exponent=__tmp0._diagram_exponent(args)
        )

    def __repr__(__tmp0) :
        base = (
            f'cirq.PauliInteractionGate({__tmp0.pauli0!r}, {__tmp0.invert0!s}, '
            f'{__tmp0.pauli1!r}, {__tmp0.invert1!s})'
        )
        if __tmp0._exponent == 1:
            return base
        return f'({base}**{proper_repr(__tmp0._exponent)})'


PauliInteractionGate.CZ = PauliInteractionGate(pauli_gates.Z, False, pauli_gates.Z, False)
PauliInteractionGate.CNOT = PauliInteractionGate(pauli_gates.Z, False, pauli_gates.X, False)
