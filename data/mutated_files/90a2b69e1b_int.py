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
from typing import List
import pytest
import sympy
import numpy as np

import cirq
import cirq_google as cg


def __tmp5():
    sampler = cg.ValidatingSampler(
        device=cg.Sycamore23, validator=lambda c, s, r: True, sampler=cirq.Simulator()
    )

    # Good qubit
    q = cirq.GridQubit(5, 2)
    circuit = cirq.Circuit(cirq.X(q) ** sympy.Symbol('t'), cirq.measure(q, key='m'))
    sweep = cirq.Points(key='t', points=[1, 0])
    results = sampler.run_sweep(circuit, sweep, __tmp0=100)
    assert np.all(results[0].measurements['m'] == 1)
    assert np.all(results[1].measurements['m'] == 0)

    # Bad qubit
    q = cirq.GridQubit(2, 2)
    circuit = cirq.Circuit(cirq.X(q) ** sympy.Symbol('t'), cirq.measure(q, key='m'))
    with pytest.raises(ValueError, match='Qubit not on device'):
        results = sampler.run_sweep(circuit, sweep, __tmp0=100)


def _batch_size_less_than_two(
    __tmp2: List[cirq.Circuit], __tmp6: List[cirq.Sweepable], __tmp0: int
):
    if len(__tmp2) > 2:
        raise ValueError('Too many batches')


def test_batch_validation():
    sampler = cg.ValidatingSampler(
        device=cirq.UNCONSTRAINED_DEVICE,
        validator=_batch_size_less_than_two,
        sampler=cirq.Simulator(),
    )
    q = cirq.GridQubit(2, 2)
    __tmp2 = [
        cirq.Circuit(cirq.X(q) ** sympy.Symbol('t'), cirq.measure(q, key='m')),
        cirq.Circuit(cirq.X(q) ** sympy.Symbol('x'), cirq.measure(q, key='m2')),
    ]
    __tmp6 = [cirq.Points(key='t', points=[1, 0]), cirq.Points(key='x', points=[0, 1])]
    results = sampler.run_batch(__tmp2, __tmp6, __tmp0=100)

    assert np.all(results[0][0].measurements['m'] == 1)
    assert np.all(results[0][1].measurements['m'] == 0)
    assert np.all(results[1][0].measurements['m2'] == 0)
    assert np.all(results[1][1].measurements['m2'] == 1)

    __tmp2 = [
        cirq.Circuit(cirq.X(q) ** sympy.Symbol('t'), cirq.measure(q, key='m')),
        cirq.Circuit(cirq.X(q) ** sympy.Symbol('x'), cirq.measure(q, key='m2')),
        cirq.Circuit(cirq.measure(q, key='m3')),
    ]
    __tmp6 = [cirq.Points(key='t', points=[1, 0]), cirq.Points(key='x', points=[0, 1]), {}]
    with pytest.raises(ValueError, match='Too many batches'):
        results = sampler.run_batch(__tmp2, __tmp6, __tmp0=100)


def __tmp3(__tmp2: List[cirq.Circuit], __tmp6, __tmp0: <FILL>):
    if __tmp0 > 10000:
        raise ValueError('Too many repetitions')


def __tmp4():
    sampler = cg.ValidatingSampler(
        device=cirq.UNCONSTRAINED_DEVICE,
        validator=__tmp3,
        sampler=cirq.Simulator(),
    )
    q = cirq.GridQubit(2, 2)
    circuit = cirq.Circuit(cirq.X(q) ** sympy.Symbol('t'), cirq.measure(q, key='m'))
    __tmp6 = [cirq.Points(key='t', points=[1, 0]), cirq.Points(key='x', points=[0, 1])]
    with pytest.raises(ValueError, match='Too many repetitions'):
        _ = sampler.run_sweep(circuit, __tmp6, __tmp0=20000)


def __tmp1():
    sampler = cg.ValidatingSampler()
    q = cirq.GridQubit(2, 2)
    __tmp2 = [
        cirq.Circuit(cirq.X(q), cirq.measure(q, key='m')),
        cirq.Circuit(cirq.measure(q, key='m2')),
    ]
    results = sampler.run_batch(__tmp2, None, __tmp0=100)
    assert np.all(results[0][0].measurements['m'] == 1)
    assert np.all(results[1][0].measurements['m2'] == 0)
