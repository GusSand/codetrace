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
from typing import List

import time
import requests

import cirq
import cirq_pasqal


class __typ0(cirq.work.Sampler):
    def __tmp5(
        __tmp2, remote_host: str, access_token: str = '', device: cirq_pasqal.PasqalDevice = None
    ) :
        """Inits PasqalSampler.

        Args:
            remote_host: Address of the remote device.
            access_token: Access token for the remote api.
            device: Optional cirq_pasqal.PasqalDevice to use with
                the sampler.
        """
        __tmp2.remote_host = remote_host
        __tmp2._authorization_header = {"Authorization": access_token}
        __tmp2._device = device

    def _serialize_circuit(
        __tmp2,
        __tmp3: cirq.circuits.AbstractCircuit,
        __tmp6,
    ) -> str:
        """Serialize a given Circuit.
        Args:
            circuit: The circuit to be run
            param_resolver: Param resolver for the
        Returns:
            json serialized string
        """
        __tmp3 = cirq.protocols.resolve_parameters(__tmp3, __tmp6)
        serialized_circuit = cirq.to_json(__tmp3)

        return serialized_circuit

    def _retrieve_serialized_result(__tmp2, __tmp0: <FILL>) :
        """Retrieves the results from the remote Pasqal device
        Args:
            task_id: id of the current task.
        Returns:
            json representation of the results
        """

        url = f'{__tmp2.remote_host}/get-result/{__tmp0}'
        while True:
            response = requests.get(
                url,
                headers=__tmp2._authorization_header,
                verify=False,
            )
            response.raise_for_status()

            result = response.text
            if result:
                return result

            time.sleep(1.0)

    def _send_serialized_circuit(
        __tmp2, __tmp8, repetitions: int = 1
    ) :
        """Sends the json string to the remote Pasqal device
        Args:
            serialization_str: Json representation of the circuit.
            repetitions: Number of repetitions.
        Returns:
            json representation of the results
        """
        simulate_url = f'{__tmp2.remote_host}/simulate/no-noise/submit'
        submit_response = requests.post(
            simulate_url,
            verify=False,
            headers={
                "Repetitions": str(repetitions),
                **__tmp2._authorization_header,
            },
            data=__tmp8,
        )
        submit_response.raise_for_status()

        __tmp0 = submit_response.text

        result_serialized = __tmp2._retrieve_serialized_result(__tmp0)
        result = cirq.read_json(json_text=result_serialized)

        return result

    @cirq._compat.deprecated_parameter(
        deadline='v0.15',
        fix='The program.device component is going away.'
        'Attaching a device to PasqalSampler is now done in __init__.',
        parameter_desc='program',
        match=lambda args, kwargs: (
            len(args) >= 2
            and isinstance(args[1], cirq.AbstractCircuit)
            and args[1]._device != cirq.UNCONSTRAINED_DEVICE
        )
        or 'program' in kwargs
        and isinstance(kwargs['program'], cirq.AbstractCircuit)
        and kwargs['program']._device != cirq.UNCONSTRAINED_DEVICE,
    )
    def __tmp7(
        __tmp2, __tmp4, __tmp1, repetitions: int = 1
    ) :
        """Samples from the given Circuit.
        In contrast to run, this allows for sweeping over different parameter
        values.
        Args:
            program: The circuit to simulate.
            params: Parameters to run with the program.
            repetitions: The number of repetitions to simulate.
        Returns:
            Result list for this run; one for each possible parameter
            resolver.
        """
        device = __tmp4._device if __tmp4._device != cirq.UNCONSTRAINED_DEVICE else __tmp2._device
        assert isinstance(
            device, cirq_pasqal.PasqalDevice
        ), "Device must inherit from cirq.PasqalDevice."
        device.validate_circuit(__tmp4)
        trial_results = []

        for __tmp6 in cirq.study.to_resolvers(__tmp1):
            json_str = __tmp2._serialize_circuit(__tmp3=__tmp4, __tmp6=__tmp6)
            results = __tmp2._send_serialized_circuit(
                __tmp8=json_str, repetitions=repetitions
            )
            trial_results.append(results)

        return trial_results
