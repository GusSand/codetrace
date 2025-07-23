from typing import TypeAlias
__typ0 : TypeAlias = "CellMaker"
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

    def __init__(__tmp2, identifier: __typ1, name, permutation: Sequence[int]):
        """Inits QuirkQubitPermutationGate.

        Args:
            identifier: Quirk identifier string.
            name: Label to include in circuit diagram info.
            permutation: A shuffled sequence of integers from 0 to
                len(permutation) - 1. The entry at offset `i` is the result
                of permuting `i`.
        """
        __tmp2.identifier = identifier
        __tmp2.name = name
        super().__init__(permutation)

    def __tmp4(__tmp2):
        return __tmp2.identifier, __tmp2.name, __tmp2.permutation

    def __tmp0(__tmp2, __tmp5: 'cirq.CircuitDiagramInfoArgs') -> Tuple[__typ1, ...]:
        return tuple(
            f'{__tmp2.name}[{i}>{__tmp2.permutation[i]}]' for i in range(len(__tmp2.permutation))
        )

    def __tmp8(__tmp2) :
        return (
            'cirq.interop.quirk.QuirkQubitPermutationGate('
            f'identifier={repr(__tmp2.identifier)},'
            f'name={repr(__tmp2.name)},'
            f'permutation={repr(__tmp2.permutation)})'
        )


def __tmp6() -> Iterator[__typ0]:
    yield from __tmp1("<<", 'left_rotate', lambda _, __tmp10: __tmp10 + 1)
    yield from __tmp1(">>", 'right_rotate', lambda _, __tmp10: __tmp10 - 1)
    yield from __tmp1("rev", 'reverse', lambda _, __tmp10: ~__tmp10)
    yield from __tmp1("weave", 'interleave', __tmp9)
    yield from __tmp1("split", 'deinterleave', __tmp11)


def __tmp1(
    __tmp3: __typ1, name: __typ1, permute: Callable[[int, int], int]
) :
    for n in CELL_SIZES:
        permutation = tuple(permute(n, i) % n for i in range(n))
        yield __tmp7(__tmp3 + __typ1(n), name, permutation)


def __tmp7(
    identifier: __typ1,
    name: __typ1,
    permutation: Tuple[int, ...],
) :
    return __typ0(
        identifier,
        size=len(permutation),
        maker=lambda __tmp5: __typ2(
            identifier=identifier, name=name, permutation=permutation
        ).on(*__tmp5.qubits),
    )


def __tmp9(n: int, __tmp10: <FILL>) -> int:
    h = (n + 1) // 2
    group = __tmp10 // h
    stride = __tmp10 % h
    return stride * 2 + group


def __tmp11(n: int, __tmp10) -> int:
    h = (n + 1) // 2
    stride = __tmp10 // 2
    group = __tmp10 % 2
    return stride + group * h
