from typing import TypeAlias
__typ0 : TypeAlias = "str"
# Copyright 2020 The Cirq Developers
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

from typing import Dict, Optional, Sequence
import numpy as np

import cirq
from cirq import circuits


def __tmp0(__tmp3, circuit: circuits.Circuit):
    """Ensure equivalence of basis state mapping.

    Args:
        maps: dictionary of test computational basis input states and
            the output computational basis states that they should be mapped to.
            The states are specified using little endian convention, meaning
            that the last bit of a binary literal will refer to the last qubit's
            value.
        circuit: the circuit to be tested
    Raises:
        AssertionError: Raised in case any basis state is mapped to the wrong
            basis state.
    """
    keys = sorted(__tmp3.keys())
    actual_map = __tmp1(keys, circuit)
    mbl = max(keys).bit_length()
    for k in keys:
        assert actual_map.get(k) == __tmp3[k], (
            f'{__tmp2(k, mbl)} was mapped to '
            f'{__tmp2(actual_map.get(k), mbl)} '
            f'instead of {__tmp2(__tmp3[k], mbl)}.'
        )


def __tmp1(
    inputs, circuit: circuits.Circuit
) :
    # Pick a unique amplitude for each computational basis input state.
    amps = [np.exp(1j * i / len(inputs)) / len(inputs) ** 0.5 for i in range(len(inputs))]

    # Permute the amplitudes using the circuit.
    input_state = np.zeros(1 << len(circuit.all_qubits()), dtype=np.complex128)
    for k, amp in zip(inputs, amps):
        input_state[k] = amp
    output_state = cirq.final_state_vector(circuit, initial_state=input_state)

    # Find where each amplitude went.
    actual_map = {}
    for k, amp in zip(inputs, amps):
        for i, amp2 in enumerate(output_state):
            if abs(amp2 - amp) < 1e-5:
                actual_map[k] = i

    return actual_map


def __tmp2(x, num_bits: <FILL>) :
    if x is None:
        return 'None'
    return f'0b{bin(x)[2:].zfill(num_bits)} ({x})'
