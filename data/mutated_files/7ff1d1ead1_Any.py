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

import string
from typing import Any, Optional, Dict, Iterable
import cirq


class QuilFormatter(string.Formatter):
    """A unique formatter to correctly output values to QUIL."""

    def __tmp5(
        __tmp2, qubit_id_map: Dict['cirq.Qid', __typ0], measurement_id_map: Dict[__typ0, __typ0]
    ) -> None:
        """Inits QuilFormatter.

        Args:
            qubit_id_map: A dictionary {qubit, quil_output_string} for
            the proper QUIL output for each qubit.
            measurement_id_map: A dictionary {measurement_key,
            quil_output_string} for the proper QUIL output for each
            measurement key.
        """
        __tmp2.qubit_id_map = {} if qubit_id_map is None else qubit_id_map
        __tmp2.measurement_id_map = {} if measurement_id_map is None else measurement_id_map

    def format_field(__tmp2, __tmp3: <FILL>, __tmp4: __typ0) :
        if isinstance(__tmp3, cirq.ops.Qid):
            __tmp3 = __tmp2.qubit_id_map[__tmp3]
        if isinstance(__tmp3, __typ0) and __tmp4 == 'meas':
            __tmp3 = __tmp2.measurement_id_map[__tmp3]
            __tmp4 = ''
        return super().format_field(__tmp3, __tmp4)


def __tmp1(
    __tmp0: Any,
    *,
    qubits: Optional[Iterable['cirq.Qid']] = None,
    formatter: Optional[QuilFormatter] = None,
):
    """Returns the QUIL code for the given value.

    Args:
        val: The value to turn into QUIL code.
        qubits: A list of qubits that the value is being applied to. This is
            needed for `cirq.Gate` values, which otherwise wouldn't know what
            qubits to talk about.
        formatter: A `QuilFormatter` object for properly ouputting the `_quil_`
            method in a QUIL format.

    Returns:
        The result of `val._quil_(...) if `val` has a `_quil_` method.
        Otherwise, returns `None`. (`None` normally indicates that the
        `_decompose_` function should be called on `val`)
    """
    method = getattr(__tmp0, '_quil_', None)
    result = NotImplemented
    if method is not None:
        kwargs: Dict[__typ0, Any] = {}
        if qubits is not None:
            kwargs['qubits'] = tuple(qubits)
        if formatter is not None:
            kwargs['formatter'] = formatter
        result = method(**kwargs)
    if result is not None and result is not NotImplemented:
        return result

    return None
