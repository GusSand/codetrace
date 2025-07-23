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
from typing import Dict, List, TYPE_CHECKING
from cirq_google.engine.abstract_job import AbstractJob

if TYPE_CHECKING:
    import datetime
    import cirq_google.engine.abstract_engine as abstract_engine
    import cirq_google.engine.abstract_processor as abstract_processor
    import cirq_google.engine.abstract_program as abstract_program


class MockJob(AbstractJob):
    def engine(__tmp2) -> 'abstract_engine.AbstractEngine':
        pass

    def id(__tmp2) :
        pass

    def program(__tmp2) :
        pass

    def create_time(__tmp2) :
        pass

    def __tmp0(__tmp2) :
        pass

    def description(__tmp2) :
        pass

    def set_description(__tmp2, description: <FILL>) :
        pass

    def __tmp6(__tmp2) :
        pass

    def set_labels(__tmp2, __tmp6: Dict[str, str]) :
        pass

    def __tmp4(__tmp2, __tmp6) :
        pass

    def __tmp1(__tmp2, keys) :
        pass

    def __tmp7(__tmp2):
        pass

    def __tmp3(__tmp2):
        pass

    def failure(__tmp2):
        pass

    def get_repetitions_and_sweeps(__tmp2):
        pass

    def get_processor(__tmp2):
        pass

    def __tmp5(__tmp2):
        pass

    def __tmp8(__tmp2) :
        pass

    def delete(__tmp2) -> None:
        pass

    def batched_results(__tmp2):
        pass

    def results(__tmp2):
        return list(range(5))

    def __tmp9(__tmp2):
        pass


def test_instantiation_and_iteration():
    job = MockJob()
    assert len(job) == 5
    assert job[3] == 3
    count = 0
    for num in job:
        assert num == count
        count += 1
