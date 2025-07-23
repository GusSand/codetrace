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

import collections
from typing import cast, Dict, Optional, Union, TYPE_CHECKING

import numpy as np

from cirq import ops
from cirq.work import collector

if TYPE_CHECKING:
    import cirq


class __typ0(collector.Collector):
    """Estimates the energy of a linear combination of Pauli observables."""

    def __init__(
        __tmp2,
        __tmp0,
        observable: 'cirq.PauliSumLike',
        *,
        samples_per_term: <FILL>,
        max_samples_per_job: int = 1000000,
    ):
        """Inits PauliSumCollector.

        Args:
            circuit: Produces the state to be tested.
            observable: The pauli product observables to measure. Their sampled
                expectations will be scaled by their coefficients and their
                dictionary weights, and then added up to produce the final
                result.
            samples_per_term: The number of samples to collect for each
                PauliString term in order to estimate its expectation.
            max_samples_per_job: How many samples to request at a time.
        """
        observable = ops.PauliSum.wrap(observable)

        __tmp2._circuit = __tmp0
        __tmp2._samples_per_job = max_samples_per_job
        __tmp2._pauli_coef_terms = [(p / p.coefficient, p.coefficient) for p in observable if p]

        __tmp2._identity_offset = 0
        for p in observable:
            if not p:
                __tmp2._identity_offset += p.coefficient

        __tmp2._zeros: Dict[ops.PauliString, int] = collections.defaultdict(lambda: 0)
        __tmp2._ones: Dict[ops.PauliString, int] = collections.defaultdict(lambda: 0)
        __tmp2._samples_per_term = samples_per_term
        __tmp2._total_samples_requested = 0

    def next_job(__tmp2) :
        i = __tmp2._total_samples_requested // __tmp2._samples_per_term
        if i >= len(__tmp2._pauli_coef_terms):
            return None
        pauli, _ = __tmp2._pauli_coef_terms[i]
        remaining = __tmp2._samples_per_term * (i + 1) - __tmp2._total_samples_requested
        amount_to_request = min(remaining, __tmp2._samples_per_job)
        __tmp2._total_samples_requested += amount_to_request
        return collector.CircuitSampleJob(
            __tmp0=__tmp1(__tmp2._circuit, pauli),
            repetitions=amount_to_request,
            tag=pauli,
        )

    def on_job_result(__tmp2, job, result):
        job_id = cast(ops.PauliString, job.tag)
        parities = result.histogram(key='out', fold_func=lambda bits: np.sum(bits) % 2)
        __tmp2._zeros[job_id] += parities[0]
        __tmp2._ones[job_id] += parities[1]

    def estimated_energy(__tmp2) -> Union[float, complex]:
        """Sums up the sampled expectations, weighted by their coefficients."""
        energy = 0j
        for pauli_string, coef in __tmp2._pauli_coef_terms:
            a = __tmp2._zeros[pauli_string]
            b = __tmp2._ones[pauli_string]
            if a + b:
                energy += coef * (a - b) / (a + b)
        energy = complex(energy)
        energy += __tmp2._identity_offset
        if energy.imag == 0:
            energy = energy.real
        return energy


def __tmp1(
    __tmp0, pauli_string: 'cirq.PauliString'
) -> 'cirq.Circuit':
    """A circuit measuring the given observable at the end of the given circuit."""
    assert pauli_string
    __tmp0 = __tmp0.copy()
    __tmp0.append(ops.Moment(pauli_string.to_z_basis_ops()))
    __tmp0.append(ops.Moment([ops.measure(*sorted(pauli_string.keys()), key='out')]))
    return __tmp0
