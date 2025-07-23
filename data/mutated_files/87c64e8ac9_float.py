from typing import TypeAlias
__typ0 : TypeAlias = "int"
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


class GoodPhaser:
    def __tmp8(__tmp0, e):
        __tmp0.e = e

    def __tmp4(__tmp0):
        return np.array([[0, 1j ** -__tmp0.e], [1j ** __tmp0.e, 0]])

    def __tmp1(__tmp0, __tmp10, __tmp3):
        return GoodPhaser(__tmp0.e + __tmp10 * 4)

    def __tmp6(__tmp0, __tmp7, __tmp9):
        return GoodPhaser(__tmp7.value_of(__tmp0.e, __tmp9))


class GoodQuditPhaser:
    def __tmp8(__tmp0, e):
        __tmp0.e = e

    def __tmp2(__tmp0):
        return (3,)

    def __tmp4(__tmp0):
        return np.array(
            [
                [0, 1j ** -__tmp0.e, 0],
                [0, 0, 1j ** __tmp0.e],
                [1, 0, 0],
            ]
        )

    def __tmp1(__tmp0, __tmp10, __tmp3: __typ0):
        return GoodQuditPhaser(__tmp0.e + __tmp10 * 4)

    def __tmp6(__tmp0, __tmp7, __tmp9):
        return GoodQuditPhaser(__tmp7.value_of(__tmp0.e, __tmp9))


class BadPhaser:
    def __tmp8(__tmp0, e):
        __tmp0.e = e

    def __tmp4(__tmp0):
        return np.array([[0, 1j ** -(__tmp0.e * 2)], [1j ** __tmp0.e, 0]])

    def __tmp1(__tmp0, __tmp10: <FILL>, __tmp3):
        return BadPhaser(__tmp0.e + __tmp10 * 4)

    def __tmp6(__tmp0, __tmp7, __tmp9):
        return BadPhaser(__tmp7.value_of(__tmp0.e, __tmp9))


class NotPhaser:
    def __tmp4(__tmp0):
        return np.array([[0, 1], [1, 0]])

    def __tmp1(__tmp0, __tmp10, __tmp3):
        return NotImplemented


class SemiBadPhaser:
    def __tmp8(__tmp0, e):
        __tmp0.e = e

    def __tmp4(__tmp0):
        a1 = cirq.unitary(GoodPhaser(__tmp0.e[0]))
        a2 = cirq.unitary(BadPhaser(__tmp0.e[1]))
        return np.kron(a1, a2)

    def __tmp1(__tmp0, __tmp10, __tmp3):
        r = list(__tmp0.e)
        r[__tmp3] += __tmp10 * 4
        return SemiBadPhaser(r)

    def __tmp6(__tmp0, __tmp7, __tmp9):
        return SemiBadPhaser([__tmp7.value_of(val, __tmp9) for val in __tmp0.e])


def __tmp5():
    cirq.testing.assert_phase_by_is_consistent_with_unitary(GoodPhaser(0.5))

    cirq.testing.assert_phase_by_is_consistent_with_unitary(GoodQuditPhaser(0.5))

    with pytest.raises(AssertionError, match='Phased unitary was incorrect for index #0'):
        cirq.testing.assert_phase_by_is_consistent_with_unitary(BadPhaser(0.5))

    with pytest.raises(AssertionError, match='Phased unitary was incorrect for index #1'):
        cirq.testing.assert_phase_by_is_consistent_with_unitary(SemiBadPhaser([0.5, 0.25]))

    # Vacuous success.
    cirq.testing.assert_phase_by_is_consistent_with_unitary(NotPhaser())
