from typing import TypeAlias
__typ1 : TypeAlias = "str"
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

    def __tmp7(__tmp1, qubits, letter: __typ1):
        __tmp1.qubits = tuple(qubits)
        __tmp1.letter = letter

    def __tmp0(__tmp1) :
        return 0

    def __tmp5(__tmp1, qubits) :
        return __typ0(qubits=Cell._replace_qubits(__tmp1.qubits, qubits), letter=__tmp1.letter)

    def __tmp6(__tmp1, __tmp8):
        for i in range(len(__tmp8)):
            cell = __tmp8[i]
            if cell is not None:
                __tmp8[i] = cell.with_input(__tmp1.letter, __tmp1.qubits)


class SetDefaultInputCell(Cell):
    """A persistent modifier that provides a fallback classical input."""

    def __tmp7(__tmp1, letter, value: <FILL>):
        __tmp1.letter = letter
        __tmp1.value = value

    def __tmp0(__tmp1) :
        return 0

    def __tmp5(__tmp1, qubits) :
        return __tmp1

    def __tmp4(__tmp1):
        return {f'set_default_{__tmp1.letter}': lambda cell: cell.with_input(__tmp1.letter, __tmp1.value)}


def __tmp2() :
    # Quantum inputs.
    yield from __tmp9("inputA", "a")
    yield from __tmp9("inputB", "b")
    yield from __tmp9("inputR", "r")
    yield from __tmp9("revinputA", "a", rev=True)
    yield from __tmp9("revinputB", "b", rev=True)

    # Classical inputs.
    yield CellMaker("setA", 2, lambda args: SetDefaultInputCell('a', args.value))
    yield CellMaker("setB", 2, lambda args: SetDefaultInputCell('b', args.value))
    yield CellMaker("setR", 2, lambda args: SetDefaultInputCell('r', args.value))


def __tmp9(__tmp3, letter, rev: bool = False) :
    for n in CELL_SIZES:
        yield CellMaker(
            identifier=__tmp3 + __typ1(n),
            size=n,
            maker=lambda args: __typ0(
                qubits=args.qubits[::-1] if rev else args.qubits, letter=letter
            ),
        )
