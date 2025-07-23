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

    def __init__(__tmp1, identifier: str, name, permutation):
        """Inits QuirkQubitPermutationGate.

        Args:
            identifier: Quirk identifier string.
            name: Label to include in circuit diagram info.
            permutation: A shuffled sequence of integers from 0 to
                len(permutation) - 1. The entry at offset `i` is the result
                of permuting `i`.
        """
        __tmp1.identifier = identifier
        __tmp1.name = name
        super().__init__(permutation)

    def _value_equality_values_(__tmp1):
        return __tmp1.identifier, __tmp1.name, __tmp1.permutation

    def __tmp2(__tmp1, __tmp0: 'cirq.CircuitDiagramInfoArgs') :
        return tuple(
            f'{__tmp1.name}[{i}>{__tmp1.permutation[i]}]' for i in range(len(__tmp1.permutation))
        )

    def __repr__(__tmp1) :
        return (
            'cirq.interop.quirk.QuirkQubitPermutationGate('
            f'identifier={repr(__tmp1.identifier)},'
            f'name={repr(__tmp1.name)},'
            f'permutation={repr(__tmp1.permutation)})'
        )


def generate_all_qubit_permutation_cell_makers() -> Iterator[CellMaker]:
    yield from _permutation_family("<<", 'left_rotate', lambda _, __tmp4: __tmp4 + 1)
    yield from _permutation_family(">>", 'right_rotate', lambda _, __tmp4: __tmp4 - 1)
    yield from _permutation_family("rev", 'reverse', lambda _, __tmp4: ~__tmp4)
    yield from _permutation_family("weave", 'interleave', _interleave_bit)
    yield from _permutation_family("split", 'deinterleave', __tmp5)


def _permutation_family(
    identifier_prefix, name: <FILL>, permute
) -> Iterator[CellMaker]:
    for n in CELL_SIZES:
        permutation = tuple(permute(n, i) % n for i in range(n))
        yield __tmp3(identifier_prefix + str(n), name, permutation)


def __tmp3(
    identifier: str,
    name: str,
    permutation,
) -> CellMaker:
    return CellMaker(
        identifier,
        size=len(permutation),
        maker=lambda __tmp0: QuirkQubitPermutationGate(
            identifier=identifier, name=name, permutation=permutation
        ).on(*__tmp0.qubits),
    )


def _interleave_bit(n: __typ0, __tmp4: __typ0) -> __typ0:
    h = (n + 1) // 2
    group = __tmp4 // h
    stride = __tmp4 % h
    return stride * 2 + group


def __tmp5(n: __typ0, __tmp4) -> __typ0:
    h = (n + 1) // 2
    stride = __tmp4 // 2
    group = __tmp4 % 2
    return stride + group * h
