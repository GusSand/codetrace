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
    def __init__(__tmp2, e):
        __tmp2.e = e

    def _unitary_(__tmp2):
        return np.array([[0, 1j ** -__tmp2.e], [1j ** __tmp2.e, 0]])

    def __tmp0(__tmp2, phase_turns, __tmp3: __typ0):
        return GoodPhaser(__tmp2.e + phase_turns * 4)

    def _resolve_parameters_(__tmp2, __tmp1, recursive):
        return GoodPhaser(__tmp1.value_of(__tmp2.e, recursive))


class GoodQuditPhaser:
    def __init__(__tmp2, e):
        __tmp2.e = e

    def _qid_shape_(__tmp2):
        return (3,)

    def _unitary_(__tmp2):
        return np.array(
            [
                [0, 1j ** -__tmp2.e, 0],
                [0, 0, 1j ** __tmp2.e],
                [1, 0, 0],
            ]
        )

    def __tmp0(__tmp2, phase_turns, __tmp3: __typ0):
        return GoodQuditPhaser(__tmp2.e + phase_turns * 4)

    def _resolve_parameters_(__tmp2, __tmp1, recursive):
        return GoodQuditPhaser(__tmp1.value_of(__tmp2.e, recursive))


class BadPhaser:
    def __init__(__tmp2, e):
        __tmp2.e = e

    def _unitary_(__tmp2):
        return np.array([[0, 1j ** -(__tmp2.e * 2)], [1j ** __tmp2.e, 0]])

    def __tmp0(__tmp2, phase_turns, __tmp3):
        return BadPhaser(__tmp2.e + phase_turns * 4)

    def _resolve_parameters_(__tmp2, __tmp1, recursive):
        return BadPhaser(__tmp1.value_of(__tmp2.e, recursive))


class NotPhaser:
    def _unitary_(__tmp2):
        return np.array([[0, 1], [1, 0]])

    def __tmp0(__tmp2, phase_turns: <FILL>, __tmp3: __typ0):
        return NotImplemented


class SemiBadPhaser:
    def __init__(__tmp2, e):
        __tmp2.e = e

    def _unitary_(__tmp2):
        a1 = cirq.unitary(GoodPhaser(__tmp2.e[0]))
        a2 = cirq.unitary(BadPhaser(__tmp2.e[1]))
        return np.kron(a1, a2)

    def __tmp0(__tmp2, phase_turns: float, __tmp3):
        r = list(__tmp2.e)
        r[__tmp3] += phase_turns * 4
        return SemiBadPhaser(r)

    def _resolve_parameters_(__tmp2, __tmp1, recursive):
        return SemiBadPhaser([__tmp1.value_of(val, recursive) for val in __tmp2.e])


def test_assert_phase_by_is_consistent_with_unitary():
    cirq.testing.assert_phase_by_is_consistent_with_unitary(GoodPhaser(0.5))

    cirq.testing.assert_phase_by_is_consistent_with_unitary(GoodQuditPhaser(0.5))

    with pytest.raises(AssertionError, match='Phased unitary was incorrect for index #0'):
        cirq.testing.assert_phase_by_is_consistent_with_unitary(BadPhaser(0.5))

    with pytest.raises(AssertionError, match='Phased unitary was incorrect for index #1'):
        cirq.testing.assert_phase_by_is_consistent_with_unitary(SemiBadPhaser([0.5, 0.25]))

    # Vacuous success.
    cirq.testing.assert_phase_by_is_consistent_with_unitary(NotPhaser())
