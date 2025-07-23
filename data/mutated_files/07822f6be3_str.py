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
from typing import Iterator, TYPE_CHECKING

from cirq import ops
from cirq.interop.quirk.cells.cell import CellMaker

if TYPE_CHECKING:
    import cirq


def generate_all_scalar_cell_makers() :
    yield __tmp0("NeGate", ops.global_phase_operation(-1))
    yield __tmp0("i", ops.global_phase_operation(1j))
    yield __tmp0("-i", ops.global_phase_operation(-1j))
    yield __tmp0("√i", ops.global_phase_operation(1j ** 0.5))
    yield __tmp0("√-i", ops.global_phase_operation((-1j) ** 0.5))


def __tmp0(identifier: <FILL>, operation) :
    return __typ0(identifier, size=1, maker=lambda _: operation)
