from typing import TypeAlias
__typ0 : TypeAlias = "str"
# Copyright 2019 The Cirq Developers
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
from typing import AbstractSet, Any, Dict, Optional, Tuple, TYPE_CHECKING, Union

import sympy

from cirq import value, protocols
from cirq.ops import raw_types

if TYPE_CHECKING:
    import cirq


@value.value_equality
class WaitGate(raw_types.Gate):
    """A single-qubit idle gate that represents waiting.

    In non-noisy simulators, this gate is just an identity gate. But noisy
    simulators and noise models may insert more error for longer waits.
    """

    def __tmp10(
        __tmp1,
        duration,
        num_qubits: Optional[int] = None,
        qid_shape: Tuple[int, ...] = None,
    ) -> None:
        """Initialize a wait gate with the given duration.

        Args:
            duration: A constant or parameterized wait duration. This can be
                an instance of `datetime.timedelta` or `cirq.Duration`.
            num_qubits: The number of qubits the gate operates on. If None and `qid_shape` is None,
                this defaults to one qubit.
            qid_shape: Can be specified instead of `num_qubits` for the case that the gate should
                act on qudits.

        Raises:
            ValueError: If the `qid_shape` provided is empty or `num_qubits` contradicts
                `qid_shape`.
        """
        __tmp1.duration = value.Duration(duration)
        if not protocols.is_parameterized(__tmp1.duration) and __tmp1.duration < 0:
            raise ValueError('duration < 0')
        if qid_shape is None:
            if num_qubits is None:
                # Assume one qubit for backwards compatibility
                qid_shape = (2,)
            else:
                qid_shape = (2,) * num_qubits
        if num_qubits is None:
            num_qubits = len(qid_shape)
        if not qid_shape:
            raise ValueError('Waiting on an empty set of qubits.')
        if num_qubits != len(qid_shape):
            raise ValueError('len(qid_shape) != num_qubits')
        __tmp1._qid_shape = qid_shape

    def _is_parameterized_(__tmp1) :
        return protocols.is_parameterized(__tmp1.duration)

    def __tmp6(__tmp1) -> AbstractSet[__typ0]:
        return protocols.parameter_names(__tmp1.duration)

    def __tmp8(__tmp1, resolver, __tmp13: <FILL>) :
        return WaitGate(protocols.resolve_parameters(__tmp1.duration, resolver, __tmp13))

    def __tmp3(__tmp1) -> Tuple[int, ...]:
        return __tmp1._qid_shape

    def __tmp9(__tmp1) :
        return True

    def _apply_unitary_(__tmp1, __tmp0):
        return __tmp0.target_tensor  # Identity.

    def _decompose_(__tmp1, __tmp7):
        return []

    def _trace_distance_bound_(__tmp1):
        return 0

    def __tmp4(__tmp1, __tmp2):
        if __tmp2 == 1 or __tmp2 == -1:
            # The inverse of a wait is still a wait.
            return __tmp1
        # Other scalar exponents could scale the wait... but ultimately it is
        # ambiguous whether the user wanted to scale the duration or just wanted
        # to affect the unitary. Play it safe and fail.
        return NotImplemented

    def __tmp14(__tmp1) :
        return f'WaitGate({__tmp1.duration})'

    def __tmp12(__tmp1) -> __typ0:
        return f'cirq.WaitGate({repr(__tmp1.duration)})'

    def _json_dict_(__tmp1) :
        d = protocols.obj_to_dict_helper(__tmp1, ['duration'])
        if len(__tmp1._qid_shape) != 1:
            d['num_qubits'] = len(__tmp1._qid_shape)
        if any(d != 2 for d in __tmp1._qid_shape):
            d['qid_shape'] = __tmp1._qid_shape
        return d

    @classmethod
    def _from_json_dict_(__tmp5, duration, num_qubits=None, qid_shape=None, **kwargs):
        return __tmp5(
            duration=duration,
            num_qubits=num_qubits,
            qid_shape=None if qid_shape is None else tuple(qid_shape),
        )

    def _value_equality_values_(__tmp1) -> Any:
        return __tmp1.duration

    def _quil_(__tmp1, __tmp7, __tmp11: 'cirq.QuilFormatter'):
        return 'WAIT\n'


def wait(
    *target: 'cirq.Qid',
    duration: 'cirq.DURATION_LIKE' = None,
    picos: Union[int, float, sympy.Basic] = 0,
    nanos: Union[int, float, sympy.Basic] = 0,
    micros: Union[int, float, sympy.Basic] = 0,
    millis: Union[int, float, sympy.Basic] = 0,
) -> raw_types.Operation:
    """Creates a WaitGate applied to all the given qubits.

    The duration can be specified as a DURATION_LIKE or using keyword args with
    numbers in the appropriate units. See Duration for details.

    Args:
        *target: The qubits that should wait.
        duration: Wait duration (see Duration).
        picos: Picoseconds to wait (see Duration).
        nanos: Nanoseconds to wait (see Duration).
        micros: Microseconds to wait (see Duration).
        millis: Milliseconds to wait (see Duration).
    """
    return WaitGate(
        duration=value.Duration(
            duration,
            picos=picos,
            nanos=nanos,
            micros=micros,
            millis=millis,
        ),
        qid_shape=protocols.qid_shape(target),
    ).on(*target)
