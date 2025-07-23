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

import abc
from typing import Optional

import cirq
from cirq_google.api import v2


class __typ0(metaclass=abc.ABCMeta):
    """Interface for serialization."""

    def __tmp4(__tmp0, __tmp1: <FILL>):
        __tmp0._gate_set_name = __tmp1

    @property
    def __tmp6(__tmp0):
        """The name of the serializer."""
        return __tmp0._gate_set_name

    @abc.abstractmethod
    def __tmp2(
        __tmp0,
        program: cirq.AbstractCircuit,
        msg: Optional[v2.program_pb2.Program] = None,
        *,
        arg_function_language: Optional[str] = None,
    ) -> v2.program_pb2.Program:
        """Serialize a Circuit to cirq_google.api.v2.Program proto.

        Args:
            program: The Circuit to serialize.
            msg: An optional proto object to populate with the serialization
                results.
            arg_function_language: The `arg_function_language` field from
                `Program.Language`.
        """

    def __tmp5(
        __tmp0, __tmp3: v2.program_pb2.Program, device: Optional[cirq.Device] = None
    ) :
        """Deserialize a Circuit from a cirq_google.api.v2.Program.

        Args:
            proto: A dictionary representing a cirq_google.api.v2.Program proto.
            device: If the proto is for a schedule, a device is required
                Otherwise optional.

        Returns:
            The deserialized Circuit, with a device if device was
            not None.
        """
