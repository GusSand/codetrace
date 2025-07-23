from typing import TypeAlias
__typ0 : TypeAlias = "str"
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

"""Tool to benchmarking simulators against a random circuit."""

import argparse
import sys
import timeit

import numpy as np

import cirq

_UNITARY = 'unitary'
_DENSITY = 'density_matrix'


def __tmp3(__tmp7, __tmp8, __tmp5, __tmp6: int = 1) :
    """"Runs the simulator."""
    circuit = cirq.Circuit()

    for _ in range(__tmp5):
        which = np.random.choice(['expz', 'expw', 'exp11'])
        if which == 'expw':
            q1 = cirq.GridQubit(0, np.random.randint(__tmp8))
            circuit.append(
                cirq.PhasedXPowGate(
                    phase_exponent=np.random.random(), exponent=np.random.random()
                ).on(q1)
            )
        elif which == 'expz':
            q1 = cirq.GridQubit(0, np.random.randint(__tmp8))
            circuit.append(cirq.Z(q1) ** np.random.random())
        elif which == 'exp11':
            q1 = cirq.GridQubit(0, np.random.randint(__tmp8 - 1))
            q2 = cirq.GridQubit(0, q1.col + 1)
            circuit.append(cirq.CZ(q1, q2) ** np.random.random())
    circuit.append([cirq.measure(*[cirq.GridQubit(0, i) for i in range(__tmp8)], key='meas')])

    if __tmp7 == _DENSITY:
        for i in range(__tmp8):
            circuit.append(cirq.H(cirq.GridQubit(0, i)))
            circuit.append(cirq.measure(cirq.GridQubit(0, i), key=f"meas{i}."))

    if __tmp7 == _UNITARY:
        circuit.final_state_vector(initial_state=0)
    elif __tmp7 == _DENSITY:
        cirq.DensityMatrixSimulator().run(circuit, repetitions=__tmp6)


def __tmp1(
    __tmp7,
    __tmp9,
    __tmp10,
    __tmp5: <FILL>,
    __tmp4,
    __tmp6,
    setup: __typ0 = 'from __main__ import simulate',
):
    print('num_qubits,seconds per gate')
    for __tmp8 in range(__tmp9, __tmp10 + 1):
        command = 'simulate(\'{}\', {}, {}, {})'.format(
            __tmp7, __tmp8, __tmp5, __tmp6
        )
        time = timeit.timeit(command, setup, number=__tmp4)
        print(f'{__tmp8},{time / (__tmp4 * __tmp5)}')


def __tmp2(__tmp0):
    parser = argparse.ArgumentParser('Benchmark a simulator.')
    parser.add_argument(
        '--sim_type',
        choices=[_UNITARY, _DENSITY],
        default=_UNITARY,
        help='Which simulator to benchmark.',
        type=__typ0,
    )
    parser.add_argument(
        '--min_num_qubits', default=4, type=int, help='Minimum number of qubits to benchmark.'
    )
    parser.add_argument(
        '--max_num_qubits', default=26, type=int, help='Maximum number of qubits to benchmark.'
    )
    parser.add_argument(
        '--num_gates', default=100, type=int, help='Number of gates in a single run.'
    )
    parser.add_argument(
        '--num_repetitions', default=10, type=int, help='Number of times to repeat a simulation'
    )
    parser.add_argument(
        '--run_repetitions',
        default=1,
        type=int,
        help='Number of repetitions in the run (density matrix only).',
    )
    return vars(parser.parse_args(__tmp0))


if __name__ == '__main__':
    __tmp1(**__tmp2(sys.argv[1:]))
