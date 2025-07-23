# Copyright 2018 The Cirq Developers
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

from typing import Tuple

import warnings
import numpy as np
import pytest

import cirq


class __typ1(cirq.Operation):
    def __tmp6(__tmp2, unitary: np.ndarray, qasm: <FILL>) -> None:
        __tmp2.unitary = unitary
        __tmp2.qasm = qasm

    def __tmp4(__tmp2):
        return __tmp2.unitary

    @property
    def qubits(__tmp2):
        return cirq.LineQubit.range(__tmp2.unitary.shape[0].bit_length() - 1)

    def __tmp7(__tmp2, *new_qubits):
        raise NotImplementedError()

    def __tmp0(__tmp2, __tmp1: cirq.QasmArgs):
        return __tmp1.format(__tmp2.qasm, *__tmp2.qubits)


class __typ0(cirq.Gate):
    def __tmp3(__tmp2) -> Tuple[int, ...]:
        return (3, 3)

    def __tmp4(__tmp2):
        return np.eye(9)

    def __tmp0(__tmp2, __tmp1: cirq.QasmArgs, qubits: Tuple[cirq.Qid, ...]):
        return NotImplemented


def __tmp5():
    try:
        import qiskit as _
    except ImportError:
        # coverage: ignore
        warnings.warn(
            "Skipped test_assert_qasm_is_consistent_with_unitary "
            "because qiskit isn't installed to verify against."
        )
        return

    # Checks matrix.
    cirq.testing.assert_qasm_is_consistent_with_unitary(
        __typ1(np.array([[1, 0], [0, 1]]), 'z {0}; z {0};')
    )
    cirq.testing.assert_qasm_is_consistent_with_unitary(
        __typ1(np.array([[1, 0], [0, -1]]), 'z {0};')
    )
    with pytest.raises(AssertionError, match='Not equal'):
        cirq.testing.assert_qasm_is_consistent_with_unitary(
            __typ1(np.array([[1, 0], [0, -1]]), 'x {0};')
        )

    # Checks qubit ordering.
    cirq.testing.assert_qasm_is_consistent_with_unitary(cirq.CNOT)
    cirq.testing.assert_qasm_is_consistent_with_unitary(
        cirq.CNOT.on(cirq.NamedQubit('a'), cirq.NamedQubit('b'))
    )
    cirq.testing.assert_qasm_is_consistent_with_unitary(
        cirq.CNOT.on(cirq.NamedQubit('b'), cirq.NamedQubit('a'))
    )

    # Checks that code is valid.
    with pytest.raises(AssertionError, match='Check your OPENQASM'):
        cirq.testing.assert_qasm_is_consistent_with_unitary(
            __typ1(np.array([[1, 0], [0, -1]]), 'JUNK$&*@($#::=[];')
        )

    # Checks that the test handles qudits
    cirq.testing.assert_qasm_is_consistent_with_unitary(__typ0())
