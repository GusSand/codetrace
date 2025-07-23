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


def __tmp2() :
    # Post selection.
    yield from __tmp4(
        "|0⟩⟨0|",
        "|1⟩⟨1|",
        "|+⟩⟨+|",
        "|-⟩⟨-|",
        "|X⟩⟨X|",
        "|/⟩⟨/|",
        "0",
        __tmp3='postselection is not implemented in Cirq',
    )

    # Non-physical operations.
    yield from __tmp4(
        "__error__", "__unstable__UniversalNot", __tmp3="unphysical operation."
    )

    # Measurement.
    yield from __tmp4(
        "XDetectControlReset",
        "YDetectControlReset",
        "ZDetectControlReset",
        __tmp3="classical feedback is not implemented in Cirq.",
    )

    # Dynamic gates with discretized actions.
    yield from __tmp4("X^⌈t⌉", "X^⌈t-¼⌉", __tmp3="discrete parameter")
    yield from __tmp0("Counting", __tmp3="discrete parameter")
    yield from __tmp0("Uncounting", __tmp3="discrete parameter")
    yield from __tmp0(">>t", __tmp3="discrete parameter")
    yield from __tmp0("<<t", __tmp3="discrete parameter")

    # Gates that are no longer in the toolbox and have dominant replacements.
    yield from __tmp0("add", __tmp3="deprecated; use +=A instead")
    yield from __tmp0("sub", __tmp3="deprecated; use -=A instead")
    yield from __tmp0("c+=ab", __tmp3="deprecated; use +=AB instead")
    yield from __tmp0("c-=ab", __tmp3="deprecated; use -=AB instead")


def _unsupported_gate(__tmp5, __tmp3: <FILL>) :
    def __tmp1(_):
        raise NotImplementedError(
            f'Converting the Quirk gate {__tmp5} is not implemented yet. Reason: {__tmp3}'
        )

    return __typ0(__tmp5, 0, __tmp1)


def __tmp4(*identifiers, __tmp3) :
    for __tmp5 in identifiers:
        yield _unsupported_gate(__tmp5, __tmp3)


def __tmp0(identifier_prefix, __tmp3) :
    for i in CELL_SIZES:
        yield _unsupported_gate(identifier_prefix + str(i), __tmp3)
