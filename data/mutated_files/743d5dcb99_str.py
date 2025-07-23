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

"""Quantum gates to prepare a given target state."""

from typing import Any, Dict, Tuple, Iterable, TYPE_CHECKING

import numpy as np

from cirq import protocols
from cirq.ops import raw_types
from cirq._compat import proper_repr

if TYPE_CHECKING:
    import cirq


class StatePreparationChannel(raw_types.Gate):
    """A channel which prepares any state provided as the state vector on it's target qubits."""

    def __tmp7(__tmp0, __tmp2: np.ndarray, *, __tmp10: str = "StatePreparation") :
        """Initializes a State Preparation channel.

        Args:
            target_state: The state vector that this gate should prepare.
            name: the name of the gate, used when printing it in the circuit diagram

        Raises:
            ValueError: if the array is not 1D, or does not have 2**n elements for some integer n.
        """
        if len(__tmp2.shape) != 1:
            raise ValueError('`target_state` must be a 1d numpy array.')

        n = int(np.round(np.log2(__tmp2.shape[0] or 1)))
        if 2 ** n != __tmp2.shape[0]:
            raise ValueError(f'Matrix width ({__tmp2.shape[0]}) is not a power of 2')

        __tmp0._state = __tmp2.astype(np.complex128) / np.linalg.norm(__tmp2)
        __tmp0._num_qubits = n
        __tmp0._name = __tmp10
        __tmp0._qid_shape = (2,) * n

    def __tmp5(__tmp0) -> bool:
        """Checks and returns if the gate has a unitary representation.
        It doesn't, since the resetting of the channels is a non-unitary operations,
        it involves measurement."""
        return False

    def __tmp9(__tmp0) -> Dict[str, Any]:
        """Converts the gate object into a serializable dictionary"""
        return {
            'target_state': __tmp0._state.tolist(),
            'name': __tmp0._name,
        }

    @classmethod
    def _from_json_dict_(
        cls, __tmp2, __tmp10: <FILL>, **kwargs
    ) :
        """Recreates the channel object from it's serialized form

        Args:
            target_state: the state to prepare using this channel
            name: the name of the gate for printing in circuit diagrams
            kwargs: other keyword arguments, ignored
        """
        return cls(__tmp2=np.array(__tmp2), __tmp10=__tmp10)

    def _num_qubits_(__tmp0) :
        return __tmp0._num_qubits

    def _qid_shape_(__tmp0) :
        return __tmp0._qid_shape

    def _circuit_diagram_info_(
        __tmp0, __tmp4
    ) -> 'cirq.CircuitDiagramInfo':
        """Returns the information required to draw out the circuit diagram for this channel."""
        symbols = (
            [__tmp0._name]
            if __tmp0._num_qubits == 1
            else [f'{__tmp0._name}[{i+1}]' for i in range(0, __tmp0._num_qubits)]
        )
        return protocols.CircuitDiagramInfo(wire_symbols=symbols)

    def _has_kraus_(__tmp0) :
        return True

    def _kraus_(__tmp0) :
        """Returns the Kraus operator for this gate

        The Kraus Operator is |Psi><i| for all |i>, where |Psi> is the target state.
        This allows is to take any input state to the target state.
        The operator satisfies the completeness relation Sum(E^ E) = I.
        """
        operator = np.zeros(shape=(2 ** __tmp0._num_qubits,) * 3, dtype=np.complex128)
        for i in range(len(operator)):
            operator[i, :, i] = __tmp0._state
        return operator

    def __tmp8(__tmp0) :
        return (
            f'cirq.StatePreparationChannel('
            f'target_state={proper_repr(__tmp0.state)}, name="{__tmp0._name}")'
        )

    def __str__(__tmp0) :
        return f'StatePreparationChannel({__tmp0.state})'

    def _approx_eq_(__tmp0, __tmp6, __tmp3) :
        if not isinstance(__tmp6, StatePreparationChannel):
            return False
        return np.allclose(__tmp0.state, __tmp6.state, rtol=0, __tmp3=__tmp3)

    def __tmp1(__tmp0, __tmp6) -> bool:
        if not isinstance(__tmp6, StatePreparationChannel):
            return False
        return np.array_equal(__tmp0.state, __tmp6.state)

    @property
    def state(__tmp0) -> np.ndarray:
        return __tmp0._state
