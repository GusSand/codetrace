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
from typing import Optional, TYPE_CHECKING, Set, List

import pytest
import cirq
from cirq import PointOptimizer, PointOptimizationSummary, Operation
from cirq.testing import EqualsTester

if TYPE_CHECKING:
    import cirq


def __tmp4():
    a = cirq.NamedQubit('a')
    b = cirq.NamedQubit('b')
    xa = cirq.X(a)
    ya = cirq.Y(a)

    eq = EqualsTester()

    eq.make_equality_group(
        lambda: PointOptimizationSummary(clear_span=0, clear_qubits=[], new_operations=[])
    )
    eq.add_equality_group(
        PointOptimizationSummary(clear_span=1, clear_qubits=[a], new_operations=[])
    )
    eq.add_equality_group(
        PointOptimizationSummary(clear_span=1, clear_qubits=[a], new_operations=[xa])
    )
    eq.add_equality_group(
        PointOptimizationSummary(clear_span=1, clear_qubits=[a, b], new_operations=[xa])
    )
    eq.add_equality_group(
        PointOptimizationSummary(clear_span=2, clear_qubits=[a], new_operations=[xa])
    )
    eq.add_equality_group(
        PointOptimizationSummary(clear_span=1, clear_qubits=[a], new_operations=[ya])
    )
    eq.add_equality_group(
        PointOptimizationSummary(clear_span=1, clear_qubits=[a], new_operations=[xa, xa])
    )


class __typ1(PointOptimizer):
    """Replaces a block of operations with X gates.

    Searches ahead for gates covering a subset of the focused operation's
    qubits, clears the whole range, and inserts X gates for each cleared
    operation's qubits.
    """

    def __tmp5(
        __tmp1, __tmp3, __tmp11: <FILL>, __tmp10: 'cirq.Operation'
    ) -> Optional['cirq.PointOptimizationSummary']:
        end = __tmp11 + 1
        new_ops = [cirq.X(q) for q in __tmp10.qubits]
        done = False
        while not done:
            n = __tmp3.next_moment_operating_on(__tmp10.qubits, end)
            if n is None:
                break
            next_ops: Set[Optional[Operation]] = {__tmp3.operation_at(q, n) for q in __tmp10.qubits}
            next_ops_list: List[Operation] = [e for e in next_ops if e]
            next_ops_sorted = sorted(next_ops_list, key=lambda e: str(e.qubits))
            for next_op in next_ops_sorted:
                if next_op:
                    if set(next_op.qubits).issubset(__tmp10.qubits):
                        end = n + 1
                        new_ops.extend(cirq.X(q) for q in next_op.qubits)
                    else:
                        done = True

        return PointOptimizationSummary(
            clear_span=end - __tmp11, clear_qubits=__tmp10.qubits, new_operations=new_ops
        )


def __tmp6():
    x = cirq.NamedQubit('x')
    y = cirq.NamedQubit('y')
    z = cirq.NamedQubit('z')
    c = cirq.Circuit(
        cirq.CZ(x, y),
        cirq.Y(x),
        cirq.Z(x),
        cirq.X(y),
        cirq.CNOT(y, z),
        cirq.Z(y),
        cirq.Z(x),
        cirq.CNOT(y, z),
        cirq.CNOT(z, y),
    )

    __typ1()(c)

    actual_text_diagram = c.to_text_diagram().strip()
    expected_text_diagram = """
x: ───X───X───X───X───────────

y: ───X───X───────X───X───X───

z: ───────────────────X───X───
    """.strip()

    assert actual_text_diagram == expected_text_diagram


def __tmp8():
    x = cirq.NamedQubit('x')
    y = cirq.NamedQubit('y')
    z = cirq.NamedQubit('z')
    c = cirq.Circuit(
        cirq.CZ(x, y),
        cirq.Y(x),
        cirq.Z(x),
        cirq.X(y),
        cirq.CNOT(y, z),
        cirq.Z(y),
        cirq.Z(x),
        cirq.CNOT(y, z),
        cirq.CNOT(z, y),
    )

    def __tmp9(__tmp2):
        for __tmp10 in __tmp2:
            yield __tmp10 ** 0.5

    __typ1(post_clean_up=__tmp9)(c)

    actual_text_diagram = c.to_text_diagram().strip()
    expected_text_diagram = """
x: ───X^0.5───X^0.5───X^0.5───X^0.5───────────────────

y: ───X^0.5───X^0.5───────────X^0.5───X^0.5───X^0.5───

z: ───────────────────────────────────X^0.5───X^0.5───
    """.strip()

    assert actual_text_diagram == expected_text_diagram


def __tmp0():
    class __typ0(cirq.PointOptimizer):
        """Changes all single qubit operations to act on LineQubit(42)"""

        def __tmp5(
            __tmp1, __tmp3: 'cirq.Circuit', __tmp11: int, __tmp10: 'cirq.Operation'
        ) :
            new_op = __tmp10
            if len(__tmp10.qubits) == 1 and isinstance(__tmp10, cirq.GateOperation):
                new_op = __tmp10.gate(cirq.LineQubit(42))

            return cirq.PointOptimizationSummary(
                clear_span=1, clear_qubits=__tmp10.qubits, new_operations=new_op
            )

    c = cirq.Circuit(cirq.X(cirq.LineQubit(0)), cirq.X(cirq.LineQubit(1)))

    with pytest.raises(ValueError, match='new qubits'):
        __typ0().optimize_circuit(c)


def __tmp7():
    assert (
        repr(cirq.PointOptimizationSummary(clear_span=0, clear_qubits=[], new_operations=[]))
        == 'cirq.PointOptimizationSummary(0, (), ())'
    )
