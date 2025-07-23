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


def __tmp0() -> Iterator[__typ0]:

    # Fixed single qubit rotations.
    yield __tmp5("H", ops.H)
    yield __tmp5("X", ops.X)
    yield __tmp5("Y", ops.Y)
    yield __tmp5("Z", ops.Z)
    yield __tmp5("X^½", ops.X ** (1 / 2))
    yield __tmp5("X^⅓", ops.X ** (1 / 3))
    yield __tmp5("X^¼", ops.X ** (1 / 4))
    yield __tmp5("X^⅛", ops.X ** (1 / 8))
    yield __tmp5("X^⅟₁₆", ops.X ** (1 / 16))
    yield __tmp5("X^⅟₃₂", ops.X ** (1 / 32))
    yield __tmp5("X^-½", ops.X ** (-1 / 2))
    yield __tmp5("X^-⅓", ops.X ** (-1 / 3))
    yield __tmp5("X^-¼", ops.X ** (-1 / 4))
    yield __tmp5("X^-⅛", ops.X ** (-1 / 8))
    yield __tmp5("X^-⅟₁₆", ops.X ** (-1 / 16))
    yield __tmp5("X^-⅟₃₂", ops.X ** (-1 / 32))
    yield __tmp5("Y^½", ops.Y ** (1 / 2))
    yield __tmp5("Y^⅓", ops.Y ** (1 / 3))
    yield __tmp5("Y^¼", ops.Y ** (1 / 4))
    yield __tmp5("Y^⅛", ops.Y ** (1 / 8))
    yield __tmp5("Y^⅟₁₆", ops.Y ** (1 / 16))
    yield __tmp5("Y^⅟₃₂", ops.Y ** (1 / 32))
    yield __tmp5("Y^-½", ops.Y ** (-1 / 2))
    yield __tmp5("Y^-⅓", ops.Y ** (-1 / 3))
    yield __tmp5("Y^-¼", ops.Y ** (-1 / 4))
    yield __tmp5("Y^-⅛", ops.Y ** (-1 / 8))
    yield __tmp5("Y^-⅟₁₆", ops.Y ** (-1 / 16))
    yield __tmp5("Y^-⅟₃₂", ops.Y ** (-1 / 32))
    yield __tmp5("Z^½", ops.Z ** (1 / 2))
    yield __tmp5("Z^⅓", ops.Z ** (1 / 3))
    yield __tmp5("Z^¼", ops.Z ** (1 / 4))
    yield __tmp5("Z^⅛", ops.Z ** (1 / 8))
    yield __tmp5("Z^⅟₁₆", ops.Z ** (1 / 16))
    yield __tmp5("Z^⅟₃₂", ops.Z ** (1 / 32))
    yield __tmp5("Z^⅟₆₄", ops.Z ** (1 / 64))
    yield __tmp5("Z^⅟₁₂₈", ops.Z ** (1 / 128))
    yield __tmp5("Z^-½", ops.Z ** (-1 / 2))
    yield __tmp5("Z^-⅓", ops.Z ** (-1 / 3))
    yield __tmp5("Z^-¼", ops.Z ** (-1 / 4))
    yield __tmp5("Z^-⅛", ops.Z ** (-1 / 8))
    yield __tmp5("Z^-⅟₁₆", ops.Z ** (-1 / 16))

    # Dynamic single qubit rotations.
    yield __tmp5("X^t", ops.X ** sympy.Symbol('t'))
    yield __tmp5("Y^t", ops.Y ** sympy.Symbol('t'))
    yield __tmp5("Z^t", ops.Z ** sympy.Symbol('t'))
    yield __tmp5("X^-t", ops.X ** -sympy.Symbol('t'))
    yield __tmp5("Y^-t", ops.Y ** -sympy.Symbol('t'))
    yield __tmp5("Z^-t", ops.Z ** -sympy.Symbol('t'))
    yield __tmp5("e^iXt", ops.rx(2 * sympy.pi * sympy.Symbol('t')))
    yield __tmp5("e^iYt", ops.ry(2 * sympy.pi * sympy.Symbol('t')))
    yield __tmp5("e^iZt", ops.rz(2 * sympy.pi * sympy.Symbol('t')))
    yield __tmp5("e^-iXt", ops.rx(-2 * sympy.pi * sympy.Symbol('t')))
    yield __tmp5("e^-iYt", ops.ry(-2 * sympy.pi * sympy.Symbol('t')))
    yield __tmp5("e^-iZt", ops.rz(-2 * sympy.pi * sympy.Symbol('t')))

    # Formulaic single qubit rotations.
    yield __tmp1("X^ft", "sin(pi*t)", lambda e: ops.X ** e)
    yield __tmp1("Y^ft", "sin(pi*t)", lambda e: ops.Y ** e)
    yield __tmp1("Z^ft", "sin(pi*t)", lambda e: ops.Z ** e)
    yield __tmp1("Rxft", "pi*t*t", ops.rx)
    yield __tmp1("Ryft", "pi*t*t", ops.ry)
    yield __tmp1("Rzft", "pi*t*t", ops.rz)


def __tmp5(__tmp6: <FILL>, __tmp3) -> __typ0:
    return __typ0(
        __tmp6=__tmp6, size=__tmp3.num_qubits(), maker=lambda args: __tmp3.on(*args.qubits)
    )


def __tmp1(
    __tmp6,
    __tmp2: str,
    __tmp4: Callable[[Union[sympy.Symbol, float]], 'cirq.Gate'],
) -> __typ0:
    return __typ0(
        __tmp6=__tmp6,
        size=__tmp4(0).num_qubits(),
        maker=lambda args: __tmp4(
            parse_formula(__tmp2 if args.value is None else args.value)
        ).on(*args.qubits),
    )
