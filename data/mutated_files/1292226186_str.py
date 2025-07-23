from typing import TypeAlias
__typ1 : TypeAlias = "int"
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

from typing import Optional, List, Iterator, Iterable, TYPE_CHECKING

from cirq.interop.quirk.cells.cell import Cell, CELL_SIZES, CellMaker

if TYPE_CHECKING:
    import cirq


class __typ0(Cell):
    """A modifier that provides a quantum input to gates in the same column."""

    def __init__(__tmp1, qubits: Iterable['cirq.Qid'], letter: <FILL>):
        __tmp1.qubits = tuple(qubits)
        __tmp1.letter = letter

    def gate_count(__tmp1) -> __typ1:
        return 0

    def __tmp0(__tmp1, qubits) :
        return __typ0(qubits=Cell._replace_qubits(__tmp1.qubits, qubits), letter=__tmp1.letter)

    def modify_column(__tmp1, column):
        for i in range(len(column)):
            cell = column[i]
            if cell is not None:
                column[i] = cell.with_input(__tmp1.letter, __tmp1.qubits)


class __typ2(Cell):
    """A persistent modifier that provides a fallback classical input."""

    def __init__(__tmp1, letter: str, value: __typ1):
        __tmp1.letter = letter
        __tmp1.value = value

    def gate_count(__tmp1) -> __typ1:
        return 0

    def __tmp0(__tmp1, qubits: List['cirq.Qid']) -> 'Cell':
        return __tmp1

    def __tmp2(__tmp1):
        return {f'set_default_{__tmp1.letter}': lambda cell: cell.with_input(__tmp1.letter, __tmp1.value)}


def generate_all_input_cell_makers() -> Iterator[CellMaker]:
    # Quantum inputs.
    yield from __tmp3("inputA", "a")
    yield from __tmp3("inputB", "b")
    yield from __tmp3("inputR", "r")
    yield from __tmp3("revinputA", "a", rev=True)
    yield from __tmp3("revinputB", "b", rev=True)

    # Classical inputs.
    yield CellMaker("setA", 2, lambda args: __typ2('a', args.value))
    yield CellMaker("setB", 2, lambda args: __typ2('b', args.value))
    yield CellMaker("setR", 2, lambda args: __typ2('r', args.value))


def __tmp3(identifier_prefix: str, letter: str, rev: bool = False) -> Iterator[CellMaker]:
    for n in CELL_SIZES:
        yield CellMaker(
            identifier=identifier_prefix + str(n),
            size=n,
            maker=lambda args: __typ0(
                qubits=args.qubits[::-1] if rev else args.qubits, letter=letter
            ),
        )
