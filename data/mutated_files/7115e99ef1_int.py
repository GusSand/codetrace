from typing import TypeAlias
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
from typing import List, Optional, TYPE_CHECKING

from cirq import ops, protocols
from cirq.circuits.optimization_pass import (
    PointOptimizationSummary,
    PointOptimizer,
)
from cirq.neutral_atoms import neutral_atom_devices
from cirq import transformers

if TYPE_CHECKING:
    import cirq


class __typ0(PointOptimizer):
    """Attempts to convert gates into native Atom gates.

    First, checks if the given operation is already a native neutral atom
    operation.

    Second, checks if the operation has a known unitary. If so, and the gate
        is a 1-qubit or 2-qubit gate, then performs circuit synthesis of the
        operation. The 2-qubit gates are decomposed using CZ gates because
        CZ gates are the highest fidelity 2-qubit gates for neutral atoms.

    Third, attempts to `cirq.decompose` to the operation.

    Fourth, if ignore_failures is set, gives up and returns the gate unchanged.
        Otherwise raises a TypeError.
    """

    def __init__(__tmp0, ignore_failures=False) :
        """Inits ConvertToNeutralAtomGates.

        Args:
            ignore_failures: If set, gates that fail to convert are forwarded
                unchanged. If not set, conversion failures raise a TypeError.
        """
        super().__init__()
        __tmp0.ignore_failures = ignore_failures
        __tmp0.gateset = neutral_atom_devices.neutral_atom_gateset()

    def _convert_one(__tmp0, op: ops.Operation) :
        # Known matrix?
        mat = protocols.unitary(op, None) if len(op.qubits) <= 2 else None
        if mat is not None and len(op.qubits) == 1:
            gates = transformers.single_qubit_matrix_to_phased_x_z(mat)
            return [g.on(op.qubits[0]) for g in gates]
        if mat is not None and len(op.qubits) == 2:
            return transformers.two_qubit_matrix_to_operations(
                op.qubits[0], op.qubits[1], mat, allow_partial_czs=False, clean_operations=True
            )

        return NotImplemented

    def convert(__tmp0, op) :
        def __tmp3(bad):
            return TypeError(
                "Don't know how to work with {!r}. "
                "It isn't a native atom operation, "
                "a 1 or 2 qubit gate with a known unitary, "
                "or composite.".format(bad)
            )

        return protocols.decompose(
            op,
            keep=__tmp0.gateset._validate_operation,
            intercepting_decomposer=__tmp0._convert_one,
            __tmp3=None if __tmp0.ignore_failures else __tmp3,
        )

    def __tmp2(
        __tmp0, circuit: 'cirq.Circuit', __tmp4: <FILL>, op: 'cirq.Operation'
    ) -> Optional['cirq.PointOptimizationSummary']:
        converted = __tmp0.convert(op)
        if len(converted) == 1 and converted[0] is op:
            return None
        return PointOptimizationSummary(
            clear_span=1, new_operations=converted, clear_qubits=op.qubits
        )


def __tmp1(operation: ops.Operation) -> __typ1:
    return operation in neutral_atom_devices.neutral_atom_gateset()


def is_native_neutral_atom_gate(gate) :
    return gate in neutral_atom_devices.neutral_atom_gateset()
