from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ1 : TypeAlias = "str"
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


class __typ0(raw_types.Gate):
    """A channel which prepares any state provided as the state vector on it's target qubits."""

    def __tmp13(__tmp1, __tmp6, *, name: __typ1 = "StatePreparation") -> None:
        """Initializes a State Preparation channel.

        Args:
            target_state: The state vector that this gate should prepare.
            name: the name of the gate, used when printing it in the circuit diagram

        Raises:
            ValueError: if the array is not 1D, or does not have 2**n elements for some integer n.
        """
        if len(__tmp6.shape) != 1:
            raise ValueError('`target_state` must be a 1d numpy array.')

        n = int(np.round(np.log2(__tmp6.shape[0] or 1)))
        if 2 ** n != __tmp6.shape[0]:
            raise ValueError(f'Matrix width ({__tmp6.shape[0]}) is not a power of 2')

        __tmp1._state = __tmp6.astype(np.complex128) / np.linalg.norm(__tmp6)
        __tmp1._num_qubits = n
        __tmp1._name = name
        __tmp1._qid_shape = (2,) * n

    def __tmp11(__tmp1) :
        """Checks and returns if the gate has a unitary representation.
        It doesn't, since the resetting of the channels is a non-unitary operations,
        it involves measurement."""
        return False

    def _json_dict_(__tmp1) :
        """Converts the gate object into a serializable dictionary"""
        return {
            'target_state': __tmp1._state.tolist(),
            'name': __tmp1._name,
        }

    @classmethod
    def __tmp4(
        __tmp10, __tmp6, name, **kwargs
    ) :
        """Recreates the channel object from it's serialized form

        Args:
            target_state: the state to prepare using this channel
            name: the name of the gate for printing in circuit diagrams
            kwargs: other keyword arguments, ignored
        """
        return __tmp10(__tmp6=np.array(__tmp6), name=name)

    def _num_qubits_(__tmp1) :
        return __tmp1._num_qubits

    def __tmp3(__tmp1) :
        return __tmp1._qid_shape

    def __tmp0(
        __tmp1, __tmp9
    ) -> 'cirq.CircuitDiagramInfo':
        """Returns the information required to draw out the circuit diagram for this channel."""
        symbols = (
            [__tmp1._name]
            if __tmp1._num_qubits == 1
            else [f'{__tmp1._name}[{i+1}]' for i in range(0, __tmp1._num_qubits)]
        )
        return protocols.CircuitDiagramInfo(wire_symbols=symbols)

    def __tmp15(__tmp1) -> __typ2:
        return True

    def __tmp14(__tmp1) -> Iterable[np.ndarray]:
        """Returns the Kraus operator for this gate

        The Kraus Operator is |Psi><i| for all |i>, where |Psi> is the target state.
        This allows is to take any input state to the target state.
        The operator satisfies the completeness relation Sum(E^ E) = I.
        """
        operator = np.zeros(shape=(2 ** __tmp1._num_qubits,) * 3, dtype=np.complex128)
        for i in range(len(operator)):
            operator[i, :, i] = __tmp1._state
        return operator

    def __repr__(__tmp1) -> __typ1:
        return (
            f'cirq.StatePreparationChannel('
            f'target_state={proper_repr(__tmp1.state)}, name="{__tmp1._name}")'
        )

    def __tmp7(__tmp1) :
        return f'StatePreparationChannel({__tmp1.state})'

    def __tmp5(__tmp1, __tmp12: <FILL>, __tmp8) -> __typ2:
        if not isinstance(__tmp12, __typ0):
            return False
        return np.allclose(__tmp1.state, __tmp12.state, rtol=0, __tmp8=__tmp8)

    def __tmp2(__tmp1, __tmp12) -> __typ2:
        if not isinstance(__tmp12, __typ0):
            return False
        return np.array_equal(__tmp1.state, __tmp12.state)

    @property
    def state(__tmp1) -> np.ndarray:
        return __tmp1._state
