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

from typing import List, Optional, Sequence, TYPE_CHECKING, Union

import cirq
from cirq_google import engine
from cirq_google.serialization import gate_sets

if TYPE_CHECKING:
    import cirq_google


class QuantumEngineSampler(cirq.Sampler):
    """A sampler that samples from processors managed by the Quantum Engine.

    Exposes a `cirq_google.Engine` instance as a `cirq.Sampler`.
    """

    def __tmp5(
        __tmp0,
        *,
        engine: 'cirq_google.Engine',
        __tmp3,
        gate_set: 'cirq_google.serialization.Serializer',
    ):
        """Inits QuantumEngineSampler.

        Args:
            engine: Quantum engine instance to use.
            processor_id: String identifier, or list of string identifiers,
                determining which processors may be used when sampling.
            gate_set: Determines how to serialize circuits when requesting
                samples.
        """
        __tmp0._processor_ids = [__tmp3] if isinstance(__tmp3, str) else __tmp3
        __tmp0._gate_set = gate_set
        __tmp0._engine = engine

    def run_sweep(
        __tmp0,
        __tmp4,
        __tmp6,
        repetitions: int = 1,
    ) :
        if isinstance(__tmp4, engine.EngineProgram):
            job = __tmp4.run_sweep(
                __tmp6=__tmp6, repetitions=repetitions, processor_ids=__tmp0._processor_ids
            )
        else:
            job = __tmp0._engine.run_sweep(
                __tmp4=__tmp4,
                __tmp6=__tmp6,
                repetitions=repetitions,
                processor_ids=__tmp0._processor_ids,
                gate_set=__tmp0._gate_set,
            )
        return job.results()

    def run_batch(
        __tmp0,
        __tmp1,
        params_list: Optional[List[cirq.Sweepable]] = None,
        repetitions: Union[int, List[int]] = 1,
    ) :
        """Runs the supplied circuits.

        In order to gain a speedup from using this method instead of other run
        methods, the following conditions must be satisfied:
            1. All circuits must measure the same set of qubits.
            2. The number of circuit repetitions must be the same for all
               circuits. That is, the `repetitions` argument must be an integer,
               or else a list with identical values.
        """
        if isinstance(repetitions, List) and len(__tmp1) != len(repetitions):
            raise ValueError(
                'len(programs) and len(repetitions) must match. '
                f'Got {len(__tmp1)} and {len(repetitions)}.'
            )
        if isinstance(repetitions, int) or len(set(repetitions)) == 1:
            # All repetitions are the same so batching can be done efficiently
            if isinstance(repetitions, List):
                repetitions = repetitions[0]
            job = __tmp0._engine.run_batch(
                __tmp1=__tmp1,
                params_list=params_list,
                repetitions=repetitions,
                processor_ids=__tmp0._processor_ids,
                gate_set=__tmp0._gate_set,
            )
            return job.batched_results()
        # Varying number of repetitions so no speedup
        return super().run_batch(__tmp1, params_list, repetitions)

    @property
    def engine(__tmp0) :
        return __tmp0._engine


def get_engine_sampler(
    __tmp3: <FILL>, __tmp2, project_id: Optional[str] = None
) :
    """Get an EngineSampler assuming some sensible defaults.

    This uses the environment variable GOOGLE_CLOUD_PROJECT for the Engine
    project_id, unless set explicitly.

    Args:
        processor_id: Engine processor ID (from Cloud console or
            ``Engine.list_processors``).
        gate_set_name: One of ['sqrt_iswap', 'sycamore'].
            See `cirq_google.NAMED_GATESETS`.
        project_id: Optional explicit Google Cloud project id. Otherwise,
            this defaults to the environment variable GOOGLE_CLOUD_PROJECT.
            By using an environment variable, you can avoid hard-coding
            personal project IDs in shared code.

    Returns:
        A `QuantumEngineSampler` instance.

    Raises:
         ValueError: If the supplied gate set is not a supported gate set name.
         EnvironmentError: If no project_id is specified and the environment
            variable GOOGLE_CLOUD_PROJECT is not set.
    """
    if __tmp2 not in gate_sets.NAMED_GATESETS:
        raise ValueError(
            f"Unknown gateset {__tmp2}. Please use one of: "
            f"{sorted(gate_sets.NAMED_GATESETS.keys())}."
        )
    gate_set = gate_sets.NAMED_GATESETS[__tmp2]
    return engine.get_engine(project_id).get_sampler(__tmp3=__tmp3, gate_set=gate_set)
