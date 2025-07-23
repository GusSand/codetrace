from typing import TypeAlias
__typ0 : TypeAlias = "float"
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

import numbers
from typing import (
    AbstractSet,
    Tuple,
    TYPE_CHECKING,
    Dict,
    Any,
    cast,
    SupportsFloat,
    Optional,
)

import numpy as np

from cirq import protocols, value
from cirq.ops import raw_types
from cirq._compat import proper_repr

if TYPE_CHECKING:
    import cirq


@value.value_equality(approximate=True)
class RandomGateChannel(raw_types.Gate):
    """Applies a sub gate with some probability."""

    def __init__(__tmp1, *, sub_gate, probability):
        if (
            isinstance(probability, numbers.Number)
            and not 0 <= __typ0(cast(SupportsFloat, probability)) <= 1
        ):
            raise ValueError("not 0 <= probability <= 1")

        __tmp1.sub_gate = sub_gate
        __tmp1.probability = probability

        # Auto flatten.
        if isinstance(__tmp1.sub_gate, RandomGateChannel):
            __tmp1.probability *= __tmp1.sub_gate.probability
            __tmp1.sub_gate = __tmp1.sub_gate.sub_gate

    def _qid_shape_(__tmp1) :
        return protocols.qid_shape(__tmp1.sub_gate)

    def __tmp4(__tmp1):
        return __tmp1.sub_gate, __tmp1.probability

    def _has_unitary_(__tmp1):
        return False

    def _has_mixture_(__tmp1):
        return not __tmp1._is_parameterized_() and protocols.has_mixture(__tmp1.sub_gate)

    def __tmp7(__tmp1):
        return not __tmp1._is_parameterized_() and protocols.has_kraus(__tmp1.sub_gate)

    def _is_parameterized_(__tmp1) :
        return protocols.is_parameterized(__tmp1.probability) or protocols.is_parameterized(
            __tmp1.sub_gate
        )

    def _parameter_names_(__tmp1) :
        return protocols.parameter_names(__tmp1.probability) | protocols.parameter_names(
            __tmp1.sub_gate
        )

    def _resolve_parameters_(
        __tmp1, resolver, recursive: <FILL>
    ) :
        return RandomGateChannel(
            sub_gate=protocols.resolve_parameters(__tmp1.sub_gate, resolver, recursive),
            probability=protocols.resolve_parameters(__tmp1.probability, resolver, recursive),
        )

    def _mixture_(__tmp1):
        if __tmp1._is_parameterized_():
            return NotImplemented

        mixture = protocols.mixture(__tmp1.sub_gate, None)
        if mixture is None:
            return None

        do_nothing = np.eye(
            np.prod(protocols.qid_shape(__tmp1.sub_gate), dtype=np.int64), dtype=np.float64
        )
        result = [(p * __typ0(__tmp1.probability), m) for p, m in mixture]
        result.append((1 - __typ0(__tmp1.probability), do_nothing))
        return result

    def __tmp6(__tmp1):
        if __tmp1._is_parameterized_():
            return NotImplemented

        channel = protocols.kraus(__tmp1.sub_gate, None)
        if channel is None:
            return NotImplemented

        do_nothing = np.eye(
            np.prod(protocols.qid_shape(__tmp1.sub_gate), dtype=np.int64), dtype=np.float64
        )
        result = [e * np.sqrt(__tmp1.probability) for e in channel]
        result.append(np.sqrt(1 - __typ0(__tmp1.probability)) * do_nothing)
        return result

    def _trace_distance_bound_(__tmp1) :
        result = protocols.trace_distance_bound(__tmp1.sub_gate)
        if not __tmp1._is_parameterized_():
            result *= __typ0(__tmp1.probability)
        return result

    def __tmp5(__tmp1) :
        return protocols.obj_to_dict_helper(__tmp1, ['sub_gate', 'probability'])

    @classmethod
    def __tmp2(__tmp3, sub_gate, probability, **kwargs):
        return __tmp3(sub_gate=sub_gate, probability=probability)

    def __tmp0(
        __tmp1, args
    ) :
        result = protocols.circuit_diagram_info(__tmp1.sub_gate, args, None)
        if result is None:
            return None
        wires = list(result.wire_symbols)
        if wires:
            wires[0] += f'[prob={args.format_real(__tmp1.probability)}]'
        return result.with_wire_symbols(wires)

    def __str__(__tmp1):
        return f'{__tmp1.sub_gate}[prob={__tmp1.probability}]'

    def __repr__(__tmp1):
        if __tmp1.probability == 1:
            return f'cirq.RandomGateChannel(sub_gate={__tmp1.sub_gate!r}, probability=1)'
        return f'{__tmp1.sub_gate!r}.with_probability({proper_repr(__tmp1.probability)})'
