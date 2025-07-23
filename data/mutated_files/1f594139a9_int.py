from typing import TypeAlias
__typ1 : TypeAlias = "CellMaker"
__typ0 : TypeAlias = "str"
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
class __typ2(ops.QubitPermutationGate):
    """A qubit permutation gate specified by a permutation list."""

    def __init__(__tmp1, identifier: __typ0, name, permutation: Sequence[int]):
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

    def __tmp0(__tmp1, args: 'cirq.CircuitDiagramInfoArgs') -> Tuple[__typ0, ...]:
        return tuple(
            f'{__tmp1.name}[{i}>{__tmp1.permutation[i]}]' for i in range(len(__tmp1.permutation))
        )

    def __repr__(__tmp1) -> __typ0:
        return (
            'cirq.interop.quirk.QuirkQubitPermutationGate('
            f'identifier={repr(__tmp1.identifier)},'
            f'name={repr(__tmp1.name)},'
            f'permutation={repr(__tmp1.permutation)})'
        )


def generate_all_qubit_permutation_cell_makers() -> Iterator[__typ1]:
    yield from _permutation_family("<<", 'left_rotate', lambda _, __tmp3: __tmp3 + 1)
    yield from _permutation_family(">>", 'right_rotate', lambda _, __tmp3: __tmp3 - 1)
    yield from _permutation_family("rev", 'reverse', lambda _, __tmp3: ~__tmp3)
    yield from _permutation_family("weave", 'interleave', _interleave_bit)
    yield from _permutation_family("split", 'deinterleave', _deinterleave_bit)


def _permutation_family(
    identifier_prefix, name, __tmp2: Callable[[int, int], int]
) -> Iterator[__typ1]:
    for n in CELL_SIZES:
        permutation = tuple(__tmp2(n, i) % n for i in range(n))
        yield _permutation(identifier_prefix + __typ0(n), name, permutation)


def _permutation(
    identifier: __typ0,
    name: __typ0,
    permutation: Tuple[int, ...],
) -> __typ1:
    return __typ1(
        identifier,
        size=len(permutation),
        maker=lambda args: __typ2(
            identifier=identifier, name=name, permutation=permutation
        ).on(*args.qubits),
    )


def _interleave_bit(n: int, __tmp3: int) -> int:
    h = (n + 1) // 2
    group = __tmp3 // h
    stride = __tmp3 % h
    return stride * 2 + group


def _deinterleave_bit(n: int, __tmp3: <FILL>) -> int:
    h = (n + 1) // 2
    stride = __tmp3 // 2
    group = __tmp3 % 2
    return stride + group * h
