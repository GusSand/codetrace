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

import pytest
import numpy as np

import cirq


def __tmp4(__tmp9: <FILL>, __tmp0) :
    result = np.zeros((__tmp9, __tmp9))
    for i in range(__tmp9):
        result[(i + __tmp0) % __tmp9, i] = 1
    return result


def adder_matrix(__tmp3, source_width) :
    t, s = __tmp3, source_width
    result = np.zeros((t, s, t, s))
    for k in range(s):
        result[:, k, :, k] = __tmp4(t, k)
    result.shape = (t * s, t * s)
    return result


def __tmp8():
    np.testing.assert_allclose(
        __tmp4(4, 1),
        np.array(
            [
                [0, 0, 0, 1],
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
            ]
        ),
        atol=1e-8,
    )
    np.testing.assert_allclose(
        __tmp4(8, -1),
        np.array(
            [
                [0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0],
            ]
        ),
        atol=1e-8,
    )
    np.testing.assert_allclose(
        adder_matrix(4, 2),
        np.array(
            [
                [1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 1, 0, 0],
            ]
        ),
        atol=1e-8,
    )


def test_arithmetic_operation_apply_unitary():
    class __typ1(cirq.ArithmeticOperation):
        def __tmp6(__tmp2, target_register, input_register):
            __tmp2.target_register = target_register
            __tmp2.input_register = input_register

        def registers(__tmp2):
            return __tmp2.target_register, __tmp2.input_register

        def with_registers(__tmp2, *new_registers):
            raise NotImplementedError()

        def __tmp1(__tmp2, __tmp10, __tmp11):
            return __tmp10 + __tmp11

    inc2 = __typ1(cirq.LineQubit.range(2), 1)
    np.testing.assert_allclose(cirq.unitary(inc2), __tmp4(4, 1), atol=1e-8)

    dec3 = __typ1(cirq.LineQubit.range(3), -1)
    np.testing.assert_allclose(cirq.unitary(dec3), __tmp4(8, -1), atol=1e-8)

    add3from2 = __typ1(cirq.LineQubit.range(3), cirq.LineQubit.range(2))
    np.testing.assert_allclose(cirq.unitary(add3from2), adder_matrix(8, 4), atol=1e-8)

    add2from3 = __typ1(cirq.LineQubit.range(2), cirq.LineQubit.range(3))
    np.testing.assert_allclose(cirq.unitary(add2from3), adder_matrix(4, 8), atol=1e-8)

    with pytest.raises(ValueError, match='affected by the operation'):
        _ = cirq.unitary(__typ1(1, cirq.LineQubit.range(2)))

    with pytest.raises(ValueError, match='affected by the operation'):
        _ = cirq.unitary(__typ1(1, 1))

    np.testing.assert_allclose(cirq.unitary(__typ1(1, 0)), np.eye(1))

    cirq.testing.assert_has_consistent_apply_unitary(
        __typ1(cirq.LineQubit.range(2), cirq.LineQubit.range(2))
    )


def __tmp7():
    class __typ2(cirq.ArithmeticOperation):
        def __tmp6(__tmp2, a, b, c):
            __tmp2.a = a
            __tmp2.b = b
            __tmp2.c = c

        def registers(__tmp2):
            return __tmp2.a, __tmp2.b, __tmp2.c

        def with_registers(__tmp2, *new_registers):
            return __typ2(*new_registers)

        def __tmp1(__tmp2, __tmp10, __tmp11):
            raise NotImplementedError()

    q0, q1, q2, q3, q4, q5 = cirq.LineQubit.range(6)
    op = __typ2([q0], [], [q4, q5])
    assert op.qubits == (q0, q4, q5)
    assert op.registers() == ([q0], [], [q4, q5])

    op2 = op.with_qubits(q2, q4, q1)
    assert op2.qubits == (q2, q4, q1)
    assert op2.registers() == ([q2], [], [q4, q1])

    op3 = op.with_registers([q0, q1, q3], [q5], 1)
    assert op3.qubits == (q0, q1, q3, q5)
    assert op3.registers() == ([q0, q1, q3], [q5], 1)

    op4 = op3.with_qubits(q0, q1, q2, q3)
    assert op4.registers() == ([q0, q1, q2], [q3], 1)
    assert op4.qubits == (q0, q1, q2, q3)


def __tmp5():
    class __typ0(cirq.ArithmeticOperation):
        def __tmp1(__tmp2, *register_values: int):
            return register_values[0] + 1

        def registers(__tmp2):
            return [cirq.LineQubit.range(2)[::-1]]

        def with_registers(__tmp2, *new_registers):
            raise NotImplementedError()

    state = np.ones(4, dtype=np.complex64) / 2
    output = cirq.final_state_vector(cirq.Circuit(__typ0()), initial_state=state)
    np.testing.assert_allclose(state, output)
