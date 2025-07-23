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

    def __init__(__tmp1, identifier, name: <FILL>, permutation: Sequence[__typ0]):
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

    def __tmp9(__tmp1):
        return __tmp1.identifier, __tmp1.name, __tmp1.permutation

    def __tmp5(__tmp1, __tmp0) -> Tuple[str, ...]:
        return tuple(
            f'{__tmp1.name}[{i}>{__tmp1.permutation[i]}]' for i in range(len(__tmp1.permutation))
        )

    def __tmp8(__tmp1) :
        return (
            'cirq.interop.quirk.QuirkQubitPermutationGate('
            f'identifier={repr(__tmp1.identifier)},'
            f'name={repr(__tmp1.name)},'
            f'permutation={repr(__tmp1.permutation)})'
        )


def __tmp6() :
    yield from __tmp2("<<", 'left_rotate', lambda _, __tmp11: __tmp11 + 1)
    yield from __tmp2(">>", 'right_rotate', lambda _, __tmp11: __tmp11 - 1)
    yield from __tmp2("rev", 'reverse', lambda _, __tmp11: ~__tmp11)
    yield from __tmp2("weave", 'interleave', __tmp10)
    yield from __tmp2("split", 'deinterleave', __tmp12)


def __tmp2(
    __tmp3, name, __tmp4: Callable[[__typ0, __typ0], __typ0]
) :
    for n in CELL_SIZES:
        permutation = tuple(__tmp4(n, i) % n for i in range(n))
        yield __tmp7(__tmp3 + str(n), name, permutation)


def __tmp7(
    identifier,
    name,
    permutation,
) -> CellMaker:
    return CellMaker(
        identifier,
        size=len(permutation),
        maker=lambda __tmp0: QuirkQubitPermutationGate(
            identifier=identifier, name=name, permutation=permutation
        ).on(*__tmp0.qubits),
    )


def __tmp10(n: __typ0, __tmp11) -> __typ0:
    h = (n + 1) // 2
    group = __tmp11 // h
    stride = __tmp11 % h
    return stride * 2 + group


def __tmp12(n: __typ0, __tmp11) :
    h = (n + 1) // 2
    stride = __tmp11 // 2
    group = __tmp11 % 2
    return stride + group * h
