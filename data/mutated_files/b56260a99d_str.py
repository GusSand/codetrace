from typing import TypeAlias
__typ1 : TypeAlias = "CellMaker"
# Copyright 2019 The Cirq Developers
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

from typing import Any, Iterable, Iterator, List, Optional, TYPE_CHECKING, Union

from cirq import ops, value
from cirq.interop.quirk.cells.cell import Cell, CellMaker

if TYPE_CHECKING:
    import cirq


@value.value_equality
class __typ0(Cell):
    """A modifier that adds controls to other cells in the column."""

    def __tmp8(__tmp3, qubit: 'cirq.Qid', __tmp4):
        __tmp3.qubit = qubit
        __tmp3._basis_change = tuple(__tmp4)

    def _value_equality_values_(__tmp3) -> Any:
        return __tmp3.qubit, __tmp3._basis_change

    def __tmp9(__tmp3) -> str:
        return (
            f'cirq.interop.quirk.cells.control_cells.ControlCell('
            f'\n    {__tmp3.qubit!r},'
            f'\n    {__tmp3._basis_change!r})'
        )

    def __tmp2(__tmp3) :
        return 0

    def __tmp6(__tmp3, qubits) -> 'Cell':
        return __typ0(
            qubit=Cell._replace_qubit(__tmp3.qubit, qubits),
            __tmp4=tuple(
                op.with_qubits(*Cell._replace_qubits(op.qubits, qubits))
                for op in __tmp3._basis_change
            ),
        )

    def __tmp7(__tmp3, __tmp10: List[Optional['Cell']]):
        for i in range(len(__tmp10)):
            gate = __tmp10[i]
            if gate is not None:
                __tmp10[i] = gate.controlled_by(__tmp3.qubit)

    def __tmp4(__tmp3) :
        return __tmp3._basis_change


@value.value_equality(unhashable=True)
class ParityControlCell(Cell):
    """A modifier that adds a group parity control to other cells in the column.

    The parity controls in a column are satisfied *as a group* if an odd number
    of them are individually satisfied.
    """

    def __tmp8(__tmp3, qubits: Iterable['cirq.Qid'], __tmp4: Iterable['cirq.Operation']):
        __tmp3.qubits = list(qubits)
        __tmp3._basis_change = list(__tmp4)

    def _value_equality_values_(__tmp3) -> Any:
        return __tmp3.qubits, __tmp3._basis_change

    def __tmp9(__tmp3) -> str:
        return (
            f'cirq.interop.quirk.cells.control_cells.ParityControlCell('
            f'\n    {__tmp3.qubits!r},'
            f'\n    {__tmp3._basis_change!r})'
        )

    def __tmp2(__tmp3) :
        return 0

    def __tmp6(__tmp3, qubits: List['cirq.Qid']) -> 'Cell':
        return ParityControlCell(
            qubits=Cell._replace_qubits(__tmp3.qubits, qubits),
            __tmp4=tuple(
                op.with_qubits(*Cell._replace_qubits(op.qubits, qubits))
                for op in __tmp3._basis_change
            ),
        )

    def __tmp7(__tmp3, __tmp10):
        for i in range(len(__tmp10)):
            gate = __tmp10[i]
            if gate is __tmp3:
                continue
            elif isinstance(gate, ParityControlCell):
                # The first parity control to modify the column must merge all
                # of the other parity controls into itself.
                __tmp10[i] = None
                __tmp3._basis_change += gate._basis_change
                __tmp3.qubits += gate.qubits
            elif gate is not None:
                __tmp10[i] = gate.controlled_by(__tmp3.qubits[0])

    def __tmp4(__tmp3) :
        yield from __tmp3._basis_change

        # Temporarily move the ZZZ..Z parity observable onto a single qubit.
        for q in __tmp3.qubits[1:]:
            yield ops.CNOT(q, __tmp3.qubits[0])


def generate_all_control_cell_makers() -> Iterator[__typ1]:
    # Controls.
    yield __tmp0("•", __tmp4=None)
    yield __tmp0("◦", __tmp4=ops.X)
    yield __tmp0("⊕", __tmp4=ops.Y ** 0.5)
    yield __tmp0("⊖", __tmp4=ops.Y ** -0.5)
    yield __tmp0("⊗", __tmp4=ops.X ** -0.5)
    yield __tmp0("(/)", __tmp4=ops.X ** 0.5)

    # Parity controls.
    yield _reg_parity_control("xpar", __tmp4=ops.Y ** 0.5)
    yield _reg_parity_control("ypar", __tmp4=ops.X ** -0.5)
    yield _reg_parity_control("zpar", __tmp4=None)


def __tmp0(__tmp11: <FILL>, *, __tmp4) :
    return __typ1(
        __tmp11=__tmp11,
        size=1,
        maker=lambda args: __typ0(
            qubit=args.qubits[0], __tmp4=__tmp1(__tmp4, args.qubits[0])
        ),
    )


def _reg_parity_control(
    __tmp11: str, *, __tmp4: Optional['cirq.SingleQubitGate'] = None
) :
    return __typ1(
        __tmp11=__tmp11,
        size=1,
        maker=lambda args: ParityControlCell(
            qubits=args.qubits, __tmp4=__tmp1(__tmp4, args.qubits)
        ),
    )


def __tmp1(
    __tmp4: Optional['cirq.SingleQubitGate'], __tmp5
) -> Iterable['cirq.Operation']:
    if __tmp4 is None:
        return ()
    return __tmp4.on_each(__tmp5)
