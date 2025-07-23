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

from cirq.interop.quirk.cells.cell import CellMaker, CELL_SIZES


def __tmp0() -> Iterator[__typ0]:
    # Spacer.
    yield __tmp1("…")

    # Displays.
    yield __tmp1("Bloch")
    yield from _ignored_family("Amps")
    yield from _ignored_family("Chance")
    yield from _ignored_family("Sample")
    yield from _ignored_family("Density")


def _ignored_family(__tmp2) :
    yield __tmp1(__tmp2)
    for i in CELL_SIZES:
        yield __tmp1(__tmp2 + str(i))


def __tmp1(identifier: <FILL>) -> __typ0:
    # No matter the arguments (qubit, position, etc), map to nothing.
    return __typ0(identifier, size=0, maker=lambda _: None)
