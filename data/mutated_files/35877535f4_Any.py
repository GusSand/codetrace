from typing import TypeAlias
__typ0 : TypeAlias = "bool"
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

from typing import (
    Any,
    Optional,
)

from cirq.ops.clifford_gate import SingleQubitCliffordGate

from cirq import protocols


def __tmp4(__tmp0: Any) -> __typ0:
    """Returns whether the input has a stabilizer effect.

    For 1-qubit gates always returns correct result. For other operations relies
    on the operation to define whether it has stabilizer effect.
    """
    strats = [
        __tmp2,
        __tmp1,
        __tmp3,
    ]
    for strat in strats:
        result = strat(__tmp0)
        if result is not None:
            return result

    # If you can't determine if it has stabilizer effect,  it does not.
    return False


def __tmp2(__tmp0) -> Optional[__typ0]:
    """Infer whether val has stabilizer effect via its `_has_stabilizer_effect_` method."""
    if hasattr(__tmp0, '_has_stabilizer_effect_'):
        result = __tmp0._has_stabilizer_effect_()
        if result is not NotImplemented and result is not None:
            return result
    return None


def __tmp1(__tmp0: <FILL>) :
    """Infer whether val's gate has stabilizer effect via the _has_stabilizer_effect_ method."""
    if hasattr(__tmp0, 'gate'):
        return __tmp2(__tmp0.gate)
    return None


def __tmp3(__tmp0: Any) :
    """Attempts to infer whether val has stabilizer effect from its unitary.

    Returns whether unitary of `val` normalizes the Pauli group. Works only for
    2x2 unitaries.
    """
    # Do not try this strategy if there is no unitary or if the number of
    # qubits is not 1 since that would be expensive.
    if not protocols.has_unitary(__tmp0) or protocols.num_qubits(__tmp0) != 1:
        return None
    unitary = protocols.unitary(__tmp0)
    return SingleQubitCliffordGate.from_unitary(unitary) is not None
