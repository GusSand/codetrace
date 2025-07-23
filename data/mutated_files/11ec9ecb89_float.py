from typing import TypeAlias
__typ1 : TypeAlias = "Any"
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

"""Operations native to iontrap systems."""

from typing import Any, Dict, Union, TYPE_CHECKING
import numpy as np

from cirq import ops, value
from cirq import protocols

if TYPE_CHECKING:
    import cirq


class MSGate(ops.XXPowGate):
    """The Mølmer–Sørensen gate, a native two-qubit operation in ion traps.

    A rotation around the XX axis in the two-qubit bloch sphere.

    The gate implements the following unitary:

        exp(-i t XX) = [ cos(t)   0        0       -isin(t)]
                       [ 0        cos(t)  -isin(t)  0      ]
                       [ 0       -isin(t)  cos(t)   0      ]
                       [-isin(t)  0        0        cos(t) ]
    """

    def __init__(__tmp0, *, rads: float):  # Forces keyword args.
        ops.XXPowGate.__init__(__tmp0, __tmp2=rads * 2 / np.pi, global_shift=-0.5)
        __tmp0.rads = rads

    def __tmp5(__tmp0: 'MSGate', __tmp2: value.TParamVal) :
        return type(__tmp0)(rads=__tmp2 * np.pi / 2)

    def _circuit_diagram_info_(
        __tmp0, args: 'cirq.CircuitDiagramInfoArgs'
    ) :
        angle_str = __tmp0._format_exponent_as_angle(args, order=4)
        symbol = f'MS({angle_str})'
        return protocols.CircuitDiagramInfo(wire_symbols=(symbol, symbol))

    def __str__(__tmp0) -> __typ0:
        if __tmp0._exponent == 1:
            return 'MS(π/2)'
        return f'MS({__tmp0._exponent!r}π/2)'

    def __tmp4(__tmp0) :
        if __tmp0._exponent == 1:
            return 'cirq.ms(np.pi/2)'
        return f'cirq.ms({__tmp0._exponent!r}*np.pi/2)'

    def __tmp6(__tmp0) -> Dict[__typ0, __typ1]:
        return protocols.obj_to_dict_helper(__tmp0, ["rads"])

    @classmethod
    def __tmp1(__tmp3, rads: <FILL>, **kwargs) :
        return __tmp3(rads=rads)


def ms(rads) -> MSGate:
    """A helper to construct the `cirq.MSGate` for the given angle specified in radians.

    Args:
        rads: The rotation angle in radians.

    Returns:
        Mølmer–Sørensen gate rotating by the desired amount.
    """
    return MSGate(rads=rads)
