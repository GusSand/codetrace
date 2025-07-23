from typing import TypeAlias
__typ3 : TypeAlias = "Any"
__typ2 : TypeAlias = "int"
__typ0 : TypeAlias = "str"
# Copyright 2021 The Cirq Developers
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
from typing import Any, Iterator, Tuple, Union, TYPE_CHECKING

import numpy as np
import sympy

from cirq import linalg, protocols, value
from cirq.ops import linear_combinations, pauli_string_phasor

if TYPE_CHECKING:
    import cirq


def __tmp10(pauli_sum) :
    for x in pauli_sum:
        for y in pauli_sum:
            if not protocols.commutes(x, y):
                return False
    return True


@value.value_equality(approximate=True)
class __typ1:
    """Represents an operator defined by the exponential of a PauliSum.

    Given a hermitian/anti-hermitian PauliSum PS_1 + PS_2 + ... + PS_N, this
    class returns an operation which is equivalent to
    exp(j * exponent * (PS_1 + PS_2 + ... + PS_N)).

    This class only supports commuting Pauli terms.
    """

    def __tmp9(
        __tmp0,
        __tmp2,
        __tmp3: Union[__typ2, float, sympy.Basic] = 1,
        atol: float = 1e-8,
    ):
        pauli_sum = linear_combinations.PauliSum.wrap(__tmp2)
        if not __tmp10(pauli_sum):
            raise ValueError("PauliSumExponential defined only for commuting pauli sums.")
        __tmp0._multiplier = None
        for pauli_string in pauli_sum:
            coeff = pauli_string.coefficient
            curr_multiplier = -1j if abs(coeff.imag) > atol else 1.0
            if not __tmp0._multiplier:
                __tmp0._multiplier = curr_multiplier
            if (
                abs(coeff.real) > atol and abs(coeff.imag) > atol
            ) or curr_multiplier != __tmp0._multiplier:
                raise ValueError(
                    pauli_sum, "PauliSum should be either hermitian or anti-hermitian."
                )
        if not __tmp0._multiplier:
            __tmp0._multiplier = 1.0
        __tmp0._exponent = __tmp3
        __tmp0._pauli_sum = pauli_sum

    @property
    def qubits(__tmp0) -> Tuple['cirq.Qid', ...]:
        return __tmp0._pauli_sum.qubits

    def __tmp12(__tmp0) :
        return (__tmp0._pauli_sum, __tmp0._exponent)

    def with_qubits(__tmp0, *new_qubits) :
        return __typ1(__tmp0._pauli_sum.with_qubits(*new_qubits), __tmp0._exponent)

    def __tmp6(
        __tmp0, __tmp7, __tmp13: <FILL>
    ) :
        return __typ1(
            __tmp0._pauli_sum,
            __tmp3=protocols.resolve_parameters(__tmp0._exponent, __tmp7, __tmp13),
        )

    def __tmp11(__tmp0) -> Iterator['cirq.PauliStringPhasor']:
        for pauli_string in __tmp0._pauli_sum:
            theta = pauli_string.coefficient * __tmp0._multiplier
            theta *= __tmp0._exponent / np.pi
            if isinstance(theta, complex):
                theta = theta.real
            yield pauli_string_phasor.PauliStringPhasor(
                pauli_string.with_coefficient(1.0), exponent_neg=-theta, exponent_pos=theta
            )

    def matrix(__tmp0) :
        """Reconstructs matrix of self from underlying Pauli sum exponentials.

        Raises:
            ValueError: if exponent is parameterized.
        """
        if protocols.is_parameterized(__tmp0._exponent):
            raise ValueError("Exponent should not parameterized.")
        ret = np.ones(1)
        for pauli_string_exp in __tmp0:
            ret = np.kron(ret, protocols.unitary(pauli_string_exp))
        return ret

    def __tmp5(__tmp0) :
        return linalg.is_unitary(__tmp0.matrix())

    def __tmp4(__tmp0) -> np.ndarray:
        return __tmp0.matrix()

    def __tmp1(__tmp0, __tmp3) :
        return __typ1(__tmp0._pauli_sum, __tmp0._exponent * __tmp3)

    def __tmp8(__tmp0) :
        class_name = __tmp0.__class__.__name__
        return f'cirq.{class_name}({__tmp0._pauli_sum!r}, {__tmp0._exponent!r})'

    def __tmp14(__tmp0) :
        if __tmp0._multiplier == 1:
            return f'exp(j * {__tmp0._exponent!s} * ({__tmp0._pauli_sum!s}))'
        else:
            return f'exp({__tmp0._exponent!s} * ({__tmp0._pauli_sum!s}))'
