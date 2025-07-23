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
from typing import Iterator

from cirq.interop.quirk.cells.cell import (
    CellMaker,
    CELL_SIZES,
)


def __tmp1() -> Iterator[CellMaker]:
    # Post selection.
    yield from __tmp3(
        "|0⟩⟨0|",
        "|1⟩⟨1|",
        "|+⟩⟨+|",
        "|-⟩⟨-|",
        "|X⟩⟨X|",
        "|/⟩⟨/|",
        "0",
        __tmp2='postselection is not implemented in Cirq',
    )

    # Non-physical operations.
    yield from __tmp3(
        "__error__", "__unstable__UniversalNot", __tmp2="unphysical operation."
    )

    # Measurement.
    yield from __tmp3(
        "XDetectControlReset",
        "YDetectControlReset",
        "ZDetectControlReset",
        __tmp2="classical feedback is not implemented in Cirq.",
    )

    # Dynamic gates with discretized actions.
    yield from __tmp3("X^⌈t⌉", "X^⌈t-¼⌉", __tmp2="discrete parameter")
    yield from _unsupported_family("Counting", __tmp2="discrete parameter")
    yield from _unsupported_family("Uncounting", __tmp2="discrete parameter")
    yield from _unsupported_family(">>t", __tmp2="discrete parameter")
    yield from _unsupported_family("<<t", __tmp2="discrete parameter")

    # Gates that are no longer in the toolbox and have dominant replacements.
    yield from _unsupported_family("add", __tmp2="deprecated; use +=A instead")
    yield from _unsupported_family("sub", __tmp2="deprecated; use -=A instead")
    yield from _unsupported_family("c+=ab", __tmp2="deprecated; use +=AB instead")
    yield from _unsupported_family("c-=ab", __tmp2="deprecated; use -=AB instead")


def _unsupported_gate(__tmp4: <FILL>, __tmp2: str) -> CellMaker:
    def __tmp0(_):
        raise NotImplementedError(
            f'Converting the Quirk gate {__tmp4} is not implemented yet. Reason: {__tmp2}'
        )

    return CellMaker(__tmp4, 0, __tmp0)


def __tmp3(*identifiers: str, __tmp2: str) -> Iterator[CellMaker]:
    for __tmp4 in identifiers:
        yield _unsupported_gate(__tmp4, __tmp2)


def _unsupported_family(identifier_prefix: str, __tmp2: str) -> Iterator[CellMaker]:
    for i in CELL_SIZES:
        yield _unsupported_gate(identifier_prefix + str(i), __tmp2)
