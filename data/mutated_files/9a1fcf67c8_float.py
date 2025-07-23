from typing import TypeAlias
__typ0 : TypeAlias = "Circuit"
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

from typing import Optional, TYPE_CHECKING

import numpy as np

from cirq import ops, protocols, transformers, linalg
from cirq.circuits.circuit import Circuit
from cirq.circuits.optimization_pass import (
    PointOptimizationSummary,
    PointOptimizer,
)

if TYPE_CHECKING:
    import cirq


class ConvertToSingleQubitCliffordGates(PointOptimizer):
    """Attempts to convert single-qubit gates into single-qubit
    SingleQubitCliffordGates.

    First, checks if the operation has a known unitary effect. If so, and the
        gate is a 1-qubit gate, then decomposes it and tries to make a
        SingleQubitCliffordGate. It fails if the operation is not in the
    Clifford group.

    Second, attempts to `cirq.decompose` to the operation.
    """

    def __init__(__tmp0, ignore_failures: bool = False, atol: float = 0) :
        """Inits ConvertToSingleQubitCliffordGates.

        Args:
            ignore_failures: If set, gates that fail to convert are forwarded
                unchanged. If not set, conversion failures raise a TypeError.
            atol: Maximum absolute error tolerance. The optimization is
                permitted to round angles with a threshold determined by this
                tolerance.
        """
        super().__init__()
        __tmp0.ignore_failures = ignore_failures
        __tmp0.atol = atol

    def _rotation_to_clifford_gate(
        __tmp0, __tmp2: ops.Pauli, __tmp1: <FILL>
    ) -> ops.SingleQubitCliffordGate:
        quarter_turns = round(__tmp1 * 2) % 4
        if quarter_turns == 1:
            return ops.SingleQubitCliffordGate.from_pauli(__tmp2, True)
        if quarter_turns == 2:
            return ops.SingleQubitCliffordGate.from_pauli(__tmp2)
        if quarter_turns == 3:
            return ops.SingleQubitCliffordGate.from_pauli(__tmp2, True) ** -1

        return ops.SingleQubitCliffordGate.I

    def _matrix_to_clifford_op(__tmp0, __tmp4: np.ndarray, qubit: 'cirq.Qid') -> Optional[ops.Operation]:
        rotations = transformers.single_qubit_matrix_to_pauli_rotations(__tmp4, __tmp0.atol)
        clifford_gate = ops.SingleQubitCliffordGate.I
        for __tmp2, __tmp1 in rotations:
            if linalg.all_near_zero_mod(__tmp1, 0.5):
                clifford_gate = clifford_gate.merged_with(
                    __tmp0._rotation_to_clifford_gate(__tmp2, __tmp1)
                )
            else:
                return None
        return clifford_gate(qubit)

    def _keep(__tmp0, op: ops.Operation) -> bool:
        # Don't change if it's already a SingleQubitCliffordGate
        return isinstance(op.gate, ops.SingleQubitCliffordGate)

    def _convert_one(__tmp0, op: ops.Operation) -> ops.OP_TREE:
        # Single qubit gate with known matrix?
        if len(op.qubits) == 1:
            __tmp4 = protocols.unitary(op, None)
            if __tmp4 is not None:
                cliff_op = __tmp0._matrix_to_clifford_op(__tmp4, op.qubits[0])
                if cliff_op is not None:
                    return cliff_op

        return NotImplemented

    def _on_stuck_raise(__tmp0, op: ops.Operation):
        if len(op.qubits) == 1 and protocols.has_unitary(op):
            raise ValueError(f'Single qubit operation is not in the Clifford group: {op!r}')

        raise TypeError(
            "Don't know how to work with {!r}. "
            "It isn't composite or a 1-qubit operation "
            "with a known unitary effect.".format(op)
        )

    def convert(__tmp0, op: ops.Operation) :
        return protocols.decompose(
            op,
            intercepting_decomposer=__tmp0._convert_one,
            keep=__tmp0._keep,
            on_stuck_raise=(None if __tmp0.ignore_failures else __tmp0._on_stuck_raise),
        )

    def __tmp3(
        __tmp0, circuit: __typ0, index: int, op: ops.Operation
    ) -> Optional[PointOptimizationSummary]:
        converted = __tmp0.convert(op)
        if converted is op:
            return None

        return PointOptimizationSummary(
            clear_span=1, new_operations=converted, clear_qubits=op.qubits
        )
