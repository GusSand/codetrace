from typing import TypeAlias
__typ0 : TypeAlias = "int"
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


class InputCell(Cell):
    """A modifier that provides a quantum input to gates in the same column."""

    def __tmp0(__tmp1, qubits, letter):
        __tmp1.qubits = tuple(qubits)
        __tmp1.letter = letter

    def gate_count(__tmp1) :
        return 0

    def with_line_qubits_mapped_to(__tmp1, qubits) :
        return InputCell(qubits=Cell._replace_qubits(__tmp1.qubits, qubits), letter=__tmp1.letter)

    def modify_column(__tmp1, __tmp2):
        for i in range(len(__tmp2)):
            cell = __tmp2[i]
            if cell is not None:
                __tmp2[i] = cell.with_input(__tmp1.letter, __tmp1.qubits)


class __typ1(Cell):
    """A persistent modifier that provides a fallback classical input."""

    def __tmp0(__tmp1, letter: str, value: __typ0):
        __tmp1.letter = letter
        __tmp1.value = value

    def gate_count(__tmp1) :
        return 0

    def with_line_qubits_mapped_to(__tmp1, qubits) :
        return __tmp1

    def persistent_modifiers(__tmp1):
        return {f'set_default_{__tmp1.letter}': lambda cell: cell.with_input(__tmp1.letter, __tmp1.value)}


def generate_all_input_cell_makers() :
    # Quantum inputs.
    yield from _input_family("inputA", "a")
    yield from _input_family("inputB", "b")
    yield from _input_family("inputR", "r")
    yield from _input_family("revinputA", "a", rev=True)
    yield from _input_family("revinputB", "b", rev=True)

    # Classical inputs.
    yield CellMaker("setA", 2, lambda args: __typ1('a', args.value))
    yield CellMaker("setB", 2, lambda args: __typ1('b', args.value))
    yield CellMaker("setR", 2, lambda args: __typ1('r', args.value))


def _input_family(identifier_prefix: str, letter: <FILL>, rev: bool = False) :
    for n in CELL_SIZES:
        yield CellMaker(
            identifier=identifier_prefix + str(n),
            size=n,
            maker=lambda args: InputCell(
                qubits=args.qubits[::-1] if rev else args.qubits, letter=letter
            ),
        )
