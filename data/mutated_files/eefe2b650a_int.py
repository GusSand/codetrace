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

from typing import (
    List,
    TYPE_CHECKING,
    Callable,
    Optional,
    Iterator,
    cast,
    Iterable,
    TypeVar,
    Union,
    Sequence,
)

from cirq import circuits
from cirq.interop.quirk.cells.cell import Cell

if TYPE_CHECKING:
    import cirq


class CompositeCell(Cell):
    """A cell made up of a grid of sub-cells.

    This is used for custom circuit gates.
    """

    def __init__(
        __tmp1,
        height: <FILL>,
        __tmp0,
        *,
        __tmp3,
    ):
        """Inits CompositeCell.

        Args:
            height: The number of qubits spanned by this composite cell. Note
                that the height may be larger than the number of affected
                qubits (e.g. the custom gate X⊗I⊗X has a height of 3 despite
                only operating on two qubits)..
            sub_cell_cols_generator: The columns making up the contents of this
                composite cell. These columns may only be generated when
                iterating this iterable for the first time.

                CAUTION: Iterating this value may be exponentially expensive in
                adversarial conditions, due to billion laugh attacks. The caller
                is responsible for providing an accurate `gate_count` value that
                allows us to check for high costs before paying them.
            gate_count: An upper bound on the number of operations in the
                circuit produced by this cell.

                CAUTION: If this value is set to 0, the
                `sub_cell_cols_generator` argument is replaced by the empty
                list. This behavior is required for efficient handling of
                billion laugh attacks that use exponentially large number of
                gate modifiers (such as controls or inputs) but no actual
                gates.
        """
        __tmp1.height = height
        __tmp1._sub_cell_cols_generator = __tmp0
        __tmp1._gate_count = __tmp3
        if __tmp3 <= 0:
            __tmp1._sub_cell_cols_generator = []

    def __tmp3(__tmp1) :
        return __tmp1._gate_count

    def _transform_cells(__tmp1, __tmp5) -> 'CompositeCell':
        return CompositeCell(
            height=__tmp1.height,
            # It is important that this is a generator instead of a list!
            # We must not list until after global operation counting.
            __tmp0=_iterator_to_iterable(
                [None if cell is None else __tmp5(cell) for cell in col]
                for col in __tmp1._sub_cell_cols_generator
            ),
            __tmp3=__tmp1._gate_count,
        )

    def _sub_cell_cols_sealed(__tmp1) :
        if not isinstance(__tmp1._sub_cell_cols_generator, list):
            __tmp1._sub_cell_cols_generator = list(__tmp1._sub_cell_cols_generator)
        return cast(List[List[Optional[Cell]]], __tmp1._sub_cell_cols_generator)

    def with_line_qubits_mapped_to(__tmp1, qubits: List['cirq.Qid']) :
        return __tmp1._transform_cells(lambda cell: cell.with_line_qubits_mapped_to(qubits))

    def with_input(
        __tmp1, letter, __tmp2
    ) :
        return __tmp1._transform_cells(lambda cell: cell.with_input(letter, __tmp2))

    def controlled_by(__tmp1, __tmp7) :
        return __tmp1._transform_cells(lambda cell: cell.controlled_by(__tmp7))

    def circuit(__tmp1) :
        result = circuits.Circuit()
        for col in __tmp1._sub_cell_cols_sealed():
            body = circuits.Circuit(cell.operations() for cell in col if cell is not None)
            if body:
                basis_change = circuits.Circuit(
                    cell.basis_change() for cell in col if cell is not None
                )
                result += basis_change
                result += body
                result += basis_change ** -1
        return result

    def operations(__tmp1) :
        return __tmp1.circuit()


T = TypeVar('T')


def _iterator_to_iterable(__tmp4) :
    done = False
    items: List[T] = []

    class IterIntoItems:
        def __tmp6(__tmp1):
            nonlocal done
            i = 0
            while True:
                if i == len(items) and not done:
                    try:
                        items.append(next(__tmp4))
                    except StopIteration:
                        done = True
                if i < len(items):
                    yield items[i]
                    i += 1
                elif done:
                    break

    return IterIntoItems()
