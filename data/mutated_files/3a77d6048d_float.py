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

"""Utility methods related to optimizing quantum circuits using native iontrap operations.

Gate compilation methods implemented here are following the paper below:
    'Basic circuit compilation techniques for an ion-trap quantum machine'
    arXiv:1603.07678
"""

from typing import Iterable, List, Optional, cast, Tuple, TYPE_CHECKING

import numpy as np

from cirq import ops, linalg, protocols, optimizers, circuits, transformers
from cirq.ion import ms

if TYPE_CHECKING:
    import cirq


def __tmp7(
    __tmp6, __tmp0, __tmp10, __tmp5: float = 1e-8
) :
    """Decomposes a two-qubit operation into MS/single-qubit rotation gates.

    Args:
        q0: The first qubit being operated on.
        q1: The other qubit being operated on.
        mat: Defines the operation to apply to the pair of qubits.
        atol: A limit on the amount of error introduced by the
            construction.

    Returns:
        A list of operations implementing the matrix.
    """
    __tmp3 = linalg.kak_decomposition(__tmp10, __tmp5=__tmp5)
    __tmp2 = _kak_decomposition_to_operations(__tmp6, __tmp0, __tmp3, __tmp5)
    return __tmp4(__tmp2)


def __tmp4(__tmp2):
    circuit = circuits.Circuit(__tmp2)
    optimizers.merge_single_qubit_gates.merge_single_qubit_gates_into_phased_x_z(circuit)
    optimizers.eject_phased_paulis.EjectPhasedPaulis().optimize_circuit(circuit)
    optimizers.eject_z.EjectZ().optimize_circuit(circuit)
    circuit = circuits.Circuit(circuit.all_operations(), strategy=circuits.InsertStrategy.EARLIEST)
    return list(circuit.all_operations())


def _kak_decomposition_to_operations(
    __tmp6, __tmp0: 'cirq.Qid', __tmp3: linalg.KakDecomposition, __tmp5: float = 1e-8
) :
    """Assumes that the decomposition is canonical."""
    b0, b1 = __tmp3.single_qubit_operations_before
    pre = [__tmp9(b0, __tmp6, __tmp5), __tmp9(b1, __tmp0, __tmp5)]
    a0, a1 = __tmp3.single_qubit_operations_after
    post = [__tmp9(a0, __tmp6, __tmp5), __tmp9(a1, __tmp0, __tmp5)]

    return list(
        cast(
            Iterable[ops.Operation],
            ops.flatten_op_tree(
                [
                    pre,
                    __tmp1(__tmp6, __tmp0, __tmp3.interaction_coefficients, __tmp5),
                    post,
                ]
            ),
        )
    )


def __tmp9(u: np.ndarray, q, __tmp5: float = 1e-8):
    for gate in transformers.single_qubit_matrix_to_gates(u, __tmp5):
        yield gate(q)


def __tmp8(
    __tmp6, __tmp0, rads, __tmp5: <FILL>, gate: Optional[ops.Gate] = None
):
    """Yields an XX interaction framed by the given operation."""

    if abs(rads) < __tmp5:
        return

    if gate is not None:
        g = cast(ops.Gate, gate)
        yield g.on(__tmp6), g.on(__tmp0)

    yield ms(-1 * rads).on(__tmp6, __tmp0)

    if gate is not None:
        g = protocols.inverse(gate)
        yield g.on(__tmp6), g.on(__tmp0)


def __tmp1(
    __tmp6,
    __tmp0,
    interaction_coefficients,
    __tmp5: float = 1e-8,
):
    """Yields non-local operation of KAK decomposition."""

    x, y, z = interaction_coefficients

    return [
        __tmp8(__tmp6, __tmp0, x, __tmp5),
        __tmp8(__tmp6, __tmp0, y, __tmp5, ops.Z ** -0.5),
        __tmp8(__tmp6, __tmp0, z, __tmp5, ops.Y ** 0.5),
    ]
