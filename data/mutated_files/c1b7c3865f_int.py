from typing import TypeAlias
__typ4 : TypeAlias = "float"
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
    def __init__(__tmp1, e):
        __tmp1.e = e

    def _unitary_(__tmp1):
        return np.array([[0, 1j ** -__tmp1.e], [1j ** __tmp1.e, 0]])

    def _phase_by_(__tmp1, __tmp0: __typ4, qubit_index: int):
        return __typ0(__tmp1.e + __tmp0 * 4)

    def _resolve_parameters_(__tmp1, resolver, recursive):
        return __typ0(resolver.value_of(__tmp1.e, recursive))


class __typ2:
    def __init__(__tmp1, e):
        __tmp1.e = e

    def _qid_shape_(__tmp1):
        return (3,)

    def _unitary_(__tmp1):
        return np.array(
            [
                [0, 1j ** -__tmp1.e, 0],
                [0, 0, 1j ** __tmp1.e],
                [1, 0, 0],
            ]
        )

    def _phase_by_(__tmp1, __tmp0, qubit_index: <FILL>):
        return __typ2(__tmp1.e + __tmp0 * 4)

    def _resolve_parameters_(__tmp1, resolver, recursive):
        return __typ2(resolver.value_of(__tmp1.e, recursive))


class __typ1:
    def __init__(__tmp1, e):
        __tmp1.e = e

    def _unitary_(__tmp1):
        return np.array([[0, 1j ** -(__tmp1.e * 2)], [1j ** __tmp1.e, 0]])

    def _phase_by_(__tmp1, __tmp0, qubit_index):
        return __typ1(__tmp1.e + __tmp0 * 4)

    def _resolve_parameters_(__tmp1, resolver, recursive):
        return __typ1(resolver.value_of(__tmp1.e, recursive))


class __typ3:
    def _unitary_(__tmp1):
        return np.array([[0, 1], [1, 0]])

    def _phase_by_(__tmp1, __tmp0, qubit_index: int):
        return NotImplemented


class SemiBadPhaser:
    def __init__(__tmp1, e):
        __tmp1.e = e

    def _unitary_(__tmp1):
        a1 = cirq.unitary(__typ0(__tmp1.e[0]))
        a2 = cirq.unitary(__typ1(__tmp1.e[1]))
        return np.kron(a1, a2)

    def _phase_by_(__tmp1, __tmp0: __typ4, qubit_index):
        r = list(__tmp1.e)
        r[qubit_index] += __tmp0 * 4
        return SemiBadPhaser(r)

    def _resolve_parameters_(__tmp1, resolver, recursive):
        return SemiBadPhaser([resolver.value_of(val, recursive) for val in __tmp1.e])


def test_assert_phase_by_is_consistent_with_unitary():
    cirq.testing.assert_phase_by_is_consistent_with_unitary(__typ0(0.5))

    cirq.testing.assert_phase_by_is_consistent_with_unitary(__typ2(0.5))

    with pytest.raises(AssertionError, match='Phased unitary was incorrect for index #0'):
        cirq.testing.assert_phase_by_is_consistent_with_unitary(__typ1(0.5))

    with pytest.raises(AssertionError, match='Phased unitary was incorrect for index #1'):
        cirq.testing.assert_phase_by_is_consistent_with_unitary(SemiBadPhaser([0.5, 0.25]))

    # Vacuous success.
    cirq.testing.assert_phase_by_is_consistent_with_unitary(__typ3())
