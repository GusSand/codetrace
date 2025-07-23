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

    def __init__(__tmp1, *, rads: <FILL>):  # Forces keyword args.
        ops.XXPowGate.__init__(__tmp1, exponent=rads * 2 / np.pi, global_shift=-0.5)
        __tmp1.rads = rads

    def _with_exponent(__tmp1, exponent) :
        return type(__tmp1)(rads=exponent * np.pi / 2)

    def __tmp2(
        __tmp1, __tmp0
    ) :
        angle_str = __tmp1._format_exponent_as_angle(__tmp0, order=4)
        symbol = f'MS({angle_str})'
        return protocols.CircuitDiagramInfo(wire_symbols=(symbol, symbol))

    def __str__(__tmp1) :
        if __tmp1._exponent == 1:
            return 'MS(π/2)'
        return f'MS({__tmp1._exponent!r}π/2)'

    def __tmp4(__tmp1) :
        if __tmp1._exponent == 1:
            return 'cirq.ms(np.pi/2)'
        return f'cirq.ms({__tmp1._exponent!r}*np.pi/2)'

    def _json_dict_(__tmp1) :
        return protocols.obj_to_dict_helper(__tmp1, ["rads"])

    @classmethod
    def _from_json_dict_(__tmp3, rads, **kwargs) :
        return __tmp3(rads=rads)


def ms(rads) :
    """A helper to construct the `cirq.MSGate` for the given angle specified in radians.

    Args:
        rads: The rotation angle in radians.

    Returns:
        Mølmer–Sørensen gate rotating by the desired amount.
    """
    return MSGate(rads=rads)
