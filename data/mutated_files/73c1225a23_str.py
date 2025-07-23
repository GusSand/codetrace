from typing import TypeAlias
__typ0 : TypeAlias = "CellMaker"
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


def generate_all_unsupported_cell_makers() -> Iterator[__typ0]:
    # Post selection.
    yield from __tmp2(
        "|0⟩⟨0|",
        "|1⟩⟨1|",
        "|+⟩⟨+|",
        "|-⟩⟨-|",
        "|X⟩⟨X|",
        "|/⟩⟨/|",
        "0",
        __tmp0='postselection is not implemented in Cirq',
    )

    # Non-physical operations.
    yield from __tmp2(
        "__error__", "__unstable__UniversalNot", __tmp0="unphysical operation."
    )

    # Measurement.
    yield from __tmp2(
        "XDetectControlReset",
        "YDetectControlReset",
        "ZDetectControlReset",
        __tmp0="classical feedback is not implemented in Cirq.",
    )

    # Dynamic gates with discretized actions.
    yield from __tmp2("X^⌈t⌉", "X^⌈t-¼⌉", __tmp0="discrete parameter")
    yield from _unsupported_family("Counting", __tmp0="discrete parameter")
    yield from _unsupported_family("Uncounting", __tmp0="discrete parameter")
    yield from _unsupported_family(">>t", __tmp0="discrete parameter")
    yield from _unsupported_family("<<t", __tmp0="discrete parameter")

    # Gates that are no longer in the toolbox and have dominant replacements.
    yield from _unsupported_family("add", __tmp0="deprecated; use +=A instead")
    yield from _unsupported_family("sub", __tmp0="deprecated; use -=A instead")
    yield from _unsupported_family("c+=ab", __tmp0="deprecated; use +=AB instead")
    yield from _unsupported_family("c-=ab", __tmp0="deprecated; use -=AB instead")


def __tmp1(identifier: str, __tmp0: str) -> __typ0:
    def fail(_):
        raise NotImplementedError(
            f'Converting the Quirk gate {identifier} is not implemented yet. Reason: {__tmp0}'
        )

    return __typ0(identifier, 0, fail)


def __tmp2(*identifiers: <FILL>, __tmp0: str) -> Iterator[__typ0]:
    for identifier in identifiers:
        yield __tmp1(identifier, __tmp0)


def _unsupported_family(identifier_prefix, __tmp0: str) :
    for i in CELL_SIZES:
        yield __tmp1(identifier_prefix + str(i), __tmp0)
