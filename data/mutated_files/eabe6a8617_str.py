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


def __tmp0() :
    # Post selection.
    yield from _unsupported_gates(
        "|0⟩⟨0|",
        "|1⟩⟨1|",
        "|+⟩⟨+|",
        "|-⟩⟨-|",
        "|X⟩⟨X|",
        "|/⟩⟨/|",
        "0",
        reason='postselection is not implemented in Cirq',
    )

    # Non-physical operations.
    yield from _unsupported_gates(
        "__error__", "__unstable__UniversalNot", reason="unphysical operation."
    )

    # Measurement.
    yield from _unsupported_gates(
        "XDetectControlReset",
        "YDetectControlReset",
        "ZDetectControlReset",
        reason="classical feedback is not implemented in Cirq.",
    )

    # Dynamic gates with discretized actions.
    yield from _unsupported_gates("X^⌈t⌉", "X^⌈t-¼⌉", reason="discrete parameter")
    yield from _unsupported_family("Counting", reason="discrete parameter")
    yield from _unsupported_family("Uncounting", reason="discrete parameter")
    yield from _unsupported_family(">>t", reason="discrete parameter")
    yield from _unsupported_family("<<t", reason="discrete parameter")

    # Gates that are no longer in the toolbox and have dominant replacements.
    yield from _unsupported_family("add", reason="deprecated; use +=A instead")
    yield from _unsupported_family("sub", reason="deprecated; use -=A instead")
    yield from _unsupported_family("c+=ab", reason="deprecated; use +=AB instead")
    yield from _unsupported_family("c-=ab", reason="deprecated; use -=AB instead")


def __tmp2(identifier, reason) :
    def fail(_):
        raise NotImplementedError(
            f'Converting the Quirk gate {identifier} is not implemented yet. Reason: {reason}'
        )

    return __typ0(identifier, 0, fail)


def _unsupported_gates(*identifiers, reason: <FILL>) :
    for identifier in identifiers:
        yield __tmp2(identifier, reason)


def _unsupported_family(__tmp1, reason) :
    for i in CELL_SIZES:
        yield __tmp2(__tmp1 + str(i), reason)
