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

from typing import Callable, Iterator, Sequence, Tuple, TYPE_CHECKING

from cirq import ops, value
from cirq.interop.quirk.cells.cell import (
    CELL_SIZES,
    CellMaker,
)

if TYPE_CHECKING:
    import cirq


@value.value_equality
class QuirkQubitPermutationGate(ops.QubitPermutationGate):
    """A qubit permutation gate specified by a permutation list."""

    def __init__(self, identifier, name: str, permutation):
        """Inits QuirkQubitPermutationGate.

        Args:
            identifier: Quirk identifier string.
            name: Label to include in circuit diagram info.
            permutation: A shuffled sequence of integers from 0 to
                len(permutation) - 1. The entry at offset `i` is the result
                of permuting `i`.
        """
        self.identifier = identifier
        self.name = name
        super().__init__(permutation)

    def _value_equality_values_(self):
        return self.identifier, self.name, self.permutation

    def _circuit_diagram_info_(self, args) -> Tuple[str, ...]:
        return tuple(
            f'{self.name}[{i}>{self.permutation[i]}]' for i in range(len(self.permutation))
        )

    def __tmp0(self) -> str:
        return (
            'cirq.interop.quirk.QuirkQubitPermutationGate('
            f'identifier={repr(self.identifier)},'
            f'name={repr(self.name)},'
            f'permutation={repr(self.permutation)})'
        )


def generate_all_qubit_permutation_cell_makers() -> Iterator[CellMaker]:
    yield from __tmp1("<<", 'left_rotate', lambda _, x: x + 1)
    yield from __tmp1(">>", 'right_rotate', lambda _, x: x - 1)
    yield from __tmp1("rev", 'reverse', lambda _, x: ~x)
    yield from __tmp1("weave", 'interleave', _interleave_bit)
    yield from __tmp1("split", 'deinterleave', __tmp2)


def __tmp1(
    identifier_prefix, name, permute: Callable[[__typ0, __typ0], __typ0]
) -> Iterator[CellMaker]:
    for n in CELL_SIZES:
        permutation = tuple(permute(n, i) % n for i in range(n))
        yield _permutation(identifier_prefix + str(n), name, permutation)


def _permutation(
    identifier: <FILL>,
    name,
    permutation,
) :
    return CellMaker(
        identifier,
        size=len(permutation),
        maker=lambda args: QuirkQubitPermutationGate(
            identifier=identifier, name=name, permutation=permutation
        ).on(*args.qubits),
    )


def _interleave_bit(n: __typ0, x) :
    h = (n + 1) // 2
    group = x // h
    stride = x % h
    return stride * 2 + group


def __tmp2(n, x: __typ0) :
    h = (n + 1) // 2
    stride = x // 2
    group = x % 2
    return stride + group * h
