from typing import TypeAlias
__typ2 : TypeAlias = "int"
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


class __typ0:
    def __init__(__tmp0, e):
        __tmp0.e = e

    def __tmp2(__tmp0):
        return np.array([[0, 1j ** -__tmp0.e], [1j ** __tmp0.e, 0]])

    def __tmp5(__tmp0, __tmp6: float, qubit_index: __typ2):
        return __typ0(__tmp0.e + __tmp6 * 4)

    def __tmp3(__tmp0, __tmp4, recursive):
        return __typ0(__tmp4.value_of(__tmp0.e, recursive))


class __typ4:
    def __init__(__tmp0, e):
        __tmp0.e = e

    def __tmp1(__tmp0):
        return (3,)

    def __tmp2(__tmp0):
        return np.array(
            [
                [0, 1j ** -__tmp0.e, 0],
                [0, 0, 1j ** __tmp0.e],
                [1, 0, 0],
            ]
        )

    def __tmp5(__tmp0, __tmp6: <FILL>, qubit_index):
        return __typ4(__tmp0.e + __tmp6 * 4)

    def __tmp3(__tmp0, __tmp4, recursive):
        return __typ4(__tmp4.value_of(__tmp0.e, recursive))


class __typ3:
    def __init__(__tmp0, e):
        __tmp0.e = e

    def __tmp2(__tmp0):
        return np.array([[0, 1j ** -(__tmp0.e * 2)], [1j ** __tmp0.e, 0]])

    def __tmp5(__tmp0, __tmp6: float, qubit_index: __typ2):
        return __typ3(__tmp0.e + __tmp6 * 4)

    def __tmp3(__tmp0, __tmp4, recursive):
        return __typ3(__tmp4.value_of(__tmp0.e, recursive))


class __typ5:
    def __tmp2(__tmp0):
        return np.array([[0, 1], [1, 0]])

    def __tmp5(__tmp0, __tmp6: float, qubit_index: __typ2):
        return NotImplemented


class __typ1:
    def __init__(__tmp0, e):
        __tmp0.e = e

    def __tmp2(__tmp0):
        a1 = cirq.unitary(__typ0(__tmp0.e[0]))
        a2 = cirq.unitary(__typ3(__tmp0.e[1]))
        return np.kron(a1, a2)

    def __tmp5(__tmp0, __tmp6: float, qubit_index: __typ2):
        r = list(__tmp0.e)
        r[qubit_index] += __tmp6 * 4
        return __typ1(r)

    def __tmp3(__tmp0, __tmp4, recursive):
        return __typ1([__tmp4.value_of(val, recursive) for val in __tmp0.e])


def test_assert_phase_by_is_consistent_with_unitary():
    cirq.testing.assert_phase_by_is_consistent_with_unitary(__typ0(0.5))

    cirq.testing.assert_phase_by_is_consistent_with_unitary(__typ4(0.5))

    with pytest.raises(AssertionError, match='Phased unitary was incorrect for index #0'):
        cirq.testing.assert_phase_by_is_consistent_with_unitary(__typ3(0.5))

    with pytest.raises(AssertionError, match='Phased unitary was incorrect for index #1'):
        cirq.testing.assert_phase_by_is_consistent_with_unitary(__typ1([0.5, 0.25]))

    # Vacuous success.
    cirq.testing.assert_phase_by_is_consistent_with_unitary(__typ5())
