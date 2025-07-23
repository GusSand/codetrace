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

    def __tmp4(__tmp2, qubits, letter):
        __tmp2.qubits = tuple(qubits)
        __tmp2.letter = letter

    def gate_count(__tmp2) -> __typ1:
        return 0

    def with_line_qubits_mapped_to(__tmp2, qubits) -> 'Cell':
        return __typ0(qubits=Cell._replace_qubits(__tmp2.qubits, qubits), letter=__tmp2.letter)

    def modify_column(__tmp2, __tmp5):
        for i in range(len(__tmp5)):
            cell = __tmp5[i]
            if cell is not None:
                __tmp5[i] = cell.with_input(__tmp2.letter, __tmp2.qubits)


class __typ2(Cell):
    """A persistent modifier that provides a fallback classical input."""

    def __tmp4(__tmp2, letter: <FILL>, value):
        __tmp2.letter = letter
        __tmp2.value = value

    def gate_count(__tmp2) :
        return 0

    def with_line_qubits_mapped_to(__tmp2, qubits: List['cirq.Qid']) -> 'Cell':
        return __tmp2

    def __tmp3(__tmp2):
        return {f'set_default_{__tmp2.letter}': lambda cell: cell.with_input(__tmp2.letter, __tmp2.value)}


def __tmp1() :
    # Quantum inputs.
    yield from __tmp6("inputA", "a")
    yield from __tmp6("inputB", "b")
    yield from __tmp6("inputR", "r")
    yield from __tmp6("revinputA", "a", rev=True)
    yield from __tmp6("revinputB", "b", rev=True)

    # Classical inputs.
    yield CellMaker("setA", 2, lambda args: __typ2('a', args.value))
    yield CellMaker("setB", 2, lambda args: __typ2('b', args.value))
    yield CellMaker("setR", 2, lambda args: __typ2('r', args.value))


def __tmp6(__tmp0, letter, rev: bool = False) :
    for n in CELL_SIZES:
        yield CellMaker(
            identifier=__tmp0 + str(n),
            size=n,
            maker=lambda args: __typ0(
                qubits=args.qubits[::-1] if rev else args.qubits, letter=letter
            ),
        )
