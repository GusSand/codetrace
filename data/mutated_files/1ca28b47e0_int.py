from typing import TypeAlias
__typ0 : TypeAlias = "bool"
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
from typing import List, Optional

import cirq


class ConvertToXmonGates(cirq.PointOptimizer):
    """Attempts to convert strange gates into XmonGates.

    First, checks if the given operation is already a native xmon operation.

    Second, checks if the operation has a known unitary. If so, and the gate
        is a 1-qubit or 2-qubit gate, then performs circuit synthesis of the
        operation.

    Third, attempts to `cirq.decompose` to the operation.

    Fourth, if ignore_failures is set, gives up and returns the gate unchanged.
        Otherwise raises a TypeError.
    """

    def __init__(__tmp1, ignore_failures=False) :
        """Inits ConvertToXmonGates.

        Args:
            ignore_failures: If set, gates that fail to convert are forwarded
                unchanged. If not set, conversion failures raise a TypeError.
        """
        super().__init__()
        __tmp1.ignore_failures = ignore_failures

    def _convert_one(__tmp1, __tmp0: cirq.Operation) -> cirq.OP_TREE:
        # Known matrix?
        mat = cirq.unitary(__tmp0, None) if len(__tmp0.qubits) <= 2 else None
        if mat is not None and len(__tmp0.qubits) == 1:
            gates = cirq.single_qubit_matrix_to_phased_x_z(mat)
            return [g.on(__tmp0.qubits[0]) for g in gates]
        if mat is not None and len(__tmp0.qubits) == 2:
            return cirq.two_qubit_matrix_to_operations(
                __tmp0.qubits[0], __tmp0.qubits[1], mat, allow_partial_czs=True, clean_operations=False
            )

        return NotImplemented

    def _is_native_xmon_op(__tmp1, __tmp0) :
        """Check if the gate within an operation is a native xmon gate.

        Args:
            op: Input operation.

        Returns:
            True if the operation is native to the xmon, false otherwise.
        """
        from cirq_google.devices import XmonDevice

        return __tmp0.gate is not None and XmonDevice.is_supported_gate(__tmp0.gate)

    def convert(__tmp1, __tmp0: cirq.Operation) :
        def __tmp2(bad):
            return TypeError(
                "Don't know how to work with {!r}. "
                "It isn't a native xmon operation, "
                "a 1 or 2 qubit gate with a known unitary, "
                "or composite.".format(bad)
            )

        return cirq.decompose(
            __tmp0,
            keep=__tmp1._is_native_xmon_op,
            intercepting_decomposer=__tmp1._convert_one,
            __tmp2=None if __tmp1.ignore_failures else __tmp2,
        )

    def optimization_at(
        __tmp1, circuit, __tmp3: <FILL>, __tmp0
    ) :
        if __tmp0.gate is None:
            return None

        converted = __tmp1.convert(__tmp0)
        if len(converted) == 1 and converted[0] is __tmp0:
            return None

        return cirq.PointOptimizationSummary(
            clear_span=1, new_operations=converted, clear_qubits=__tmp0.qubits
        )
