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
from typing import Iterator, Callable, Union, TYPE_CHECKING

import sympy

from cirq import ops
from cirq.interop.quirk.cells.cell import CellMaker
from cirq.interop.quirk.cells.parse import parse_formula

if TYPE_CHECKING:
    import cirq


def __tmp0() :

    # Fixed single qubit rotations.
    yield __tmp4("H", ops.H)
    yield __tmp4("X", ops.X)
    yield __tmp4("Y", ops.Y)
    yield __tmp4("Z", ops.Z)
    yield __tmp4("X^½", ops.X ** (1 / 2))
    yield __tmp4("X^⅓", ops.X ** (1 / 3))
    yield __tmp4("X^¼", ops.X ** (1 / 4))
    yield __tmp4("X^⅛", ops.X ** (1 / 8))
    yield __tmp4("X^⅟₁₆", ops.X ** (1 / 16))
    yield __tmp4("X^⅟₃₂", ops.X ** (1 / 32))
    yield __tmp4("X^-½", ops.X ** (-1 / 2))
    yield __tmp4("X^-⅓", ops.X ** (-1 / 3))
    yield __tmp4("X^-¼", ops.X ** (-1 / 4))
    yield __tmp4("X^-⅛", ops.X ** (-1 / 8))
    yield __tmp4("X^-⅟₁₆", ops.X ** (-1 / 16))
    yield __tmp4("X^-⅟₃₂", ops.X ** (-1 / 32))
    yield __tmp4("Y^½", ops.Y ** (1 / 2))
    yield __tmp4("Y^⅓", ops.Y ** (1 / 3))
    yield __tmp4("Y^¼", ops.Y ** (1 / 4))
    yield __tmp4("Y^⅛", ops.Y ** (1 / 8))
    yield __tmp4("Y^⅟₁₆", ops.Y ** (1 / 16))
    yield __tmp4("Y^⅟₃₂", ops.Y ** (1 / 32))
    yield __tmp4("Y^-½", ops.Y ** (-1 / 2))
    yield __tmp4("Y^-⅓", ops.Y ** (-1 / 3))
    yield __tmp4("Y^-¼", ops.Y ** (-1 / 4))
    yield __tmp4("Y^-⅛", ops.Y ** (-1 / 8))
    yield __tmp4("Y^-⅟₁₆", ops.Y ** (-1 / 16))
    yield __tmp4("Y^-⅟₃₂", ops.Y ** (-1 / 32))
    yield __tmp4("Z^½", ops.Z ** (1 / 2))
    yield __tmp4("Z^⅓", ops.Z ** (1 / 3))
    yield __tmp4("Z^¼", ops.Z ** (1 / 4))
    yield __tmp4("Z^⅛", ops.Z ** (1 / 8))
    yield __tmp4("Z^⅟₁₆", ops.Z ** (1 / 16))
    yield __tmp4("Z^⅟₃₂", ops.Z ** (1 / 32))
    yield __tmp4("Z^⅟₆₄", ops.Z ** (1 / 64))
    yield __tmp4("Z^⅟₁₂₈", ops.Z ** (1 / 128))
    yield __tmp4("Z^-½", ops.Z ** (-1 / 2))
    yield __tmp4("Z^-⅓", ops.Z ** (-1 / 3))
    yield __tmp4("Z^-¼", ops.Z ** (-1 / 4))
    yield __tmp4("Z^-⅛", ops.Z ** (-1 / 8))
    yield __tmp4("Z^-⅟₁₆", ops.Z ** (-1 / 16))

    # Dynamic single qubit rotations.
    yield __tmp4("X^t", ops.X ** sympy.Symbol('t'))
    yield __tmp4("Y^t", ops.Y ** sympy.Symbol('t'))
    yield __tmp4("Z^t", ops.Z ** sympy.Symbol('t'))
    yield __tmp4("X^-t", ops.X ** -sympy.Symbol('t'))
    yield __tmp4("Y^-t", ops.Y ** -sympy.Symbol('t'))
    yield __tmp4("Z^-t", ops.Z ** -sympy.Symbol('t'))
    yield __tmp4("e^iXt", ops.rx(2 * sympy.pi * sympy.Symbol('t')))
    yield __tmp4("e^iYt", ops.ry(2 * sympy.pi * sympy.Symbol('t')))
    yield __tmp4("e^iZt", ops.rz(2 * sympy.pi * sympy.Symbol('t')))
    yield __tmp4("e^-iXt", ops.rx(-2 * sympy.pi * sympy.Symbol('t')))
    yield __tmp4("e^-iYt", ops.ry(-2 * sympy.pi * sympy.Symbol('t')))
    yield __tmp4("e^-iZt", ops.rz(-2 * sympy.pi * sympy.Symbol('t')))

    # Formulaic single qubit rotations.
    yield _formula_gate("X^ft", "sin(pi*t)", lambda e: ops.X ** e)
    yield _formula_gate("Y^ft", "sin(pi*t)", lambda e: ops.Y ** e)
    yield _formula_gate("Z^ft", "sin(pi*t)", lambda e: ops.Z ** e)
    yield _formula_gate("Rxft", "pi*t*t", ops.rx)
    yield _formula_gate("Ryft", "pi*t*t", ops.ry)
    yield _formula_gate("Rzft", "pi*t*t", ops.rz)


def __tmp4(__tmp5: str, __tmp2: 'cirq.Gate') -> __typ0:
    return __typ0(
        __tmp5=__tmp5, size=__tmp2.num_qubits(), maker=lambda args: __tmp2.on(*args.qubits)
    )


def _formula_gate(
    __tmp5: <FILL>,
    __tmp1: str,
    __tmp3: Callable[[Union[sympy.Symbol, float]], 'cirq.Gate'],
) -> __typ0:
    return __typ0(
        __tmp5=__tmp5,
        size=__tmp3(0).num_qubits(),
        maker=lambda args: __tmp3(
            parse_formula(__tmp1 if args.value is None else args.value)
        ).on(*args.qubits),
    )
