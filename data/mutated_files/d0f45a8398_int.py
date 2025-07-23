from typing import TypeAlias
__typ2 : TypeAlias = "Any"
__typ0 : TypeAlias = "str"
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

import itertools
from typing import Any, Dict, Sequence, Tuple, TYPE_CHECKING

from cirq import ops, value
from cirq.contrib.acquaintance.permutation import SwapPermutationGate, PermutationGate

if TYPE_CHECKING:
    import cirq


@value.value_equality
class __typ1(PermutationGate):
    """Performs a cyclical permutation of the qubits to the left by a specified amount."""

    def __init__(__tmp0, num_qubits: <FILL>, shift: int, swap_gate: 'cirq.Gate' = ops.SWAP) -> None:
        """Construct a circular shift gate.

        Args:
            num_qubits: The number of qubits to shift.
            shift: The number of positions to circularly left shift the qubits.
            swap_gate: The gate to use when decomposing.
        """
        super(__typ1, __tmp0).__init__(num_qubits, swap_gate)
        __tmp0.shift = shift

    def __repr__(__tmp0) -> __typ0:
        return (
            'cirq.contrib.acquaintance.CircularShiftGate('
            f'num_qubits={__tmp0.num_qubits()!r},'
            f'shift={__tmp0.shift!r}, swap_gate={__tmp0.swap_gate!r})'
        )

    def _value_equality_values_(__tmp0) :
        return __tmp0.shift, __tmp0.swap_gate, __tmp0.num_qubits()

    def _decompose_(__tmp0, qubits: Sequence['cirq.Qid']) :
        n = len(qubits)
        left_shift = __tmp0.shift % n
        right_shift = n - left_shift
        mins = itertools.chain(range(left_shift - 1, 0, -1), range(right_shift))
        maxs = itertools.chain(range(left_shift, n), range(n - 1, right_shift, -1))
        swap_gate = SwapPermutationGate(__tmp0.swap_gate)
        for i, j in zip(mins, maxs):
            for k in range(i, j, 2):
                yield swap_gate(*qubits[k : k + 2])

    def _circuit_diagram_info_(__tmp0, args: 'cirq.CircuitDiagramInfoArgs') -> Tuple[__typ0, ...]:
        if args.known_qubit_count is None:
            return NotImplemented
        direction_symbols = ('╲', '╱') if args.use_unicode_characters else ('\\', '/')
        wire_symbols = tuple(
            direction_symbols[int(i >= __tmp0.shift)]
            + __typ0(i)
            + direction_symbols[int(i < __tmp0.shift)]
            for i in range(__tmp0.num_qubits())
        )
        return wire_symbols

    def permutation(__tmp0) :
        shift = __tmp0.shift % __tmp0.num_qubits()
        permuted_indices = itertools.chain(range(shift, __tmp0.num_qubits()), range(shift))
        return {s: i for i, s in enumerate(permuted_indices)}
