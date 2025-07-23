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

from typing import Any, Optional, Tuple

import numpy as np

import cirq


_MIN_DURATION = cirq.Duration(nanos=0)
_MAX_DURATION = cirq.Duration(nanos=200)


@cirq.value_equality(approximate=True)
class CouplerPulse(cirq.ops.Gate):
    r"""Tunable pulse for entangling adjacent qubits.

    For experimental usage only.

    This operation sends a trapezoidal pulse to the coupler between two
    adjacent qubits placed in resonance.

    Note that this gate does not have a unitary matrix and must be
    characterized by the user in order to determine its effects.

    ```
                     __________
                    /          \
    _______________/            \________________
     |<---------->|  |<------>|  |<----------->|
      padding_time   hold_time     padding_time
                 ->  <-      ->   <-
                rise_time   rise_time
    ```

    Args:
            hold_time: Length of the 'plateau' part of the coupler trajectory.
            coupling_mhz: Target qubit-qubit coupling reached at the plateau.
            rise_time: Width of the rising (or falling) section of the trapezoidal pulse.
            padding_time: Symmetric padding around the coupler pulse.
    """

    def __tmp4(
        __tmp1,
        hold_time: cirq.Duration,
        coupling_mhz: <FILL>,
        rise_time: Optional[cirq.Duration] = cirq.Duration(nanos=8),
        padding_time: Optional[cirq.Duration] = cirq.Duration(nanos=2.5),
    ):
        """Inits CouplerPulse.

        Args:
            hold_time: Length of the 'plateau' part of the coupler trajectory.
            coupling_mhz: Target qubit-qubit coupling reached at the plateau.
            rise_time: Width of the rising (or falling) action of the trapezoidal pulse.
            padding_time: Symmetric padding around the coupler pulse.

        Raises:
            ValueError: If any time is negative or if the total pulse is too long.
        """
        if hold_time < _MIN_DURATION:
            raise ValueError(f'hold_time must be greater than {_MIN_DURATION}')
        if padding_time < _MIN_DURATION:
            raise ValueError(f'padding_time must be greater than {_MIN_DURATION}')
        if rise_time < _MIN_DURATION:
            raise ValueError(f'rise_time must be greater than {_MIN_DURATION}')

        __tmp1.hold_time = hold_time
        __tmp1.coupling_mhz = coupling_mhz
        __tmp1.rise_time = rise_time or cirq.Duration(nanos=8)
        __tmp1.padding_time = padding_time or cirq.Duration(nanos=2.5)

        total_time = hold_time + 2 * __tmp1.rise_time + 2 * __tmp1.padding_time
        if total_time > _MAX_DURATION:
            raise ValueError(
                f'Total time of coupler pulse ({total_time}) '
                f'cannot be greater than {_MAX_DURATION}'
            )

    def __tmp6(__tmp1) -> int:
        return 2

    def _unitary_(__tmp1) -> np.ndarray:
        return NotImplemented

    def __tmp3(__tmp1) -> __typ0:
        return (
            'cirq_google.experimental.ops.coupler_pulse.'
            + f'CouplerPulse(hold_time={__tmp1.hold_time!r}, '
            + f'coupling_mhz={__tmp1.coupling_mhz}, '
            + f'rise_time={__tmp1.rise_time!r}, '
            + f'padding_time={__tmp1.padding_time!r})'
        )

    def __tmp7(__tmp1) -> __typ0:
        return (
            f'CouplerPulse(hold_time={__tmp1.hold_time}, '
            + f'coupling_mhz={__tmp1.coupling_mhz}, '
            + f'rise_time={__tmp1.rise_time}, '
            + f'padding_time={__tmp1.padding_time})'
        )

    def __tmp5(__tmp1) -> Any:
        return __tmp1.hold_time, __tmp1.coupling_mhz, __tmp1.rise_time, __tmp1.padding_time

    def __tmp0(__tmp1, __tmp2) -> Tuple[__typ0, ...]:
        s = f'/‾‾({__tmp1.hold_time}@{__tmp1.coupling_mhz}MHz)‾‾\\'
        return (s, s)

    def _json_dict_(__tmp1):
        return cirq.obj_to_dict_helper(
            __tmp1, ['hold_time', 'coupling_mhz', 'rise_time', 'padding_time']
        )
