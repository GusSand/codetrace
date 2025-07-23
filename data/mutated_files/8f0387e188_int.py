from typing import TypeAlias
__typ2 : TypeAlias = "AbstractProgram"
__typ0 : TypeAlias = "str"
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
import datetime
from typing import Dict, List, Optional, Union
import pytest

import cirq

from cirq_google.engine.abstract_local_job_test import NothingJob
from cirq_google.engine.abstract_local_program_test import NothingProgram
from cirq_google.engine.abstract_local_engine import AbstractLocalEngine
from cirq_google.engine.abstract_local_processor import AbstractLocalProcessor
from cirq_google.engine.abstract_program import AbstractProgram
import cirq_google.engine.calibration as calibration


class ProgramDictProcessor(AbstractLocalProcessor):
    """A processor that has a dictionary of programs for testing."""

    def __init__(__tmp1, programs: Dict[__typ0, __typ2], **kwargs):
        super().__init__(**kwargs)
        __tmp1._programs = programs

    def get_calibration(__tmp1, *args, **kwargs):
        pass

    def __tmp9(__tmp1, __tmp11: <FILL>) -> Optional[calibration.Calibration]:
        return calibration.Calibration()

    def __tmp8(__tmp1, *args, **kwargs):
        pass

    def __tmp6(__tmp1, *args, **kwargs):
        pass

    def __tmp18(__tmp1, *args, **kwargs):
        pass

    def __tmp5(__tmp1, *args, **kwargs):
        pass

    def __tmp4(__tmp1, *args, **kwargs):
        pass

    def __tmp17(__tmp1, *args, **kwargs):
        pass

    def __tmp0(__tmp1, *args, **kwargs):
        pass

    def __tmp15(__tmp1, *args, **kwargs):
        pass

    def __tmp12(__tmp1, *args, **kwargs):
        pass

    def get_sampler(__tmp1, *args, **kwargs):
        return cirq.Simulator()

    def __tmp3(__tmp1, *args, **kwargs):
        pass

    def list_programs(
        __tmp1,
        created_before: Optional[Union[datetime.datetime, datetime.date]] = None,
        created_after: Optional[Union[datetime.datetime, datetime.date]] = None,
        has_labels: Optional[Dict[__typ0, __typ0]] = None,
    ):
        """Lists all programs regardless of filters.

        This isn't really correct, but we don't want to test test functionality."""
        return __tmp1._programs.values()

    def get_program(__tmp1, __tmp10: __typ0) -> __typ2:
        return __tmp1._programs[__tmp10]


class __typ1(AbstractLocalEngine):
    """Engine for Testing."""

    def __init__(__tmp1, __tmp7):
        super().__init__(__tmp7)


def __tmp13():
    processor1 = ProgramDictProcessor(programs=[], processor_id='test')
    engine = __typ1([processor1])
    assert engine.get_processor('test') == processor1
    assert engine.get_processor('test').engine() == engine

    with pytest.raises(KeyError):
        _ = engine.get_processor('invalid')


def __tmp14():
    processor1 = ProgramDictProcessor(programs=[], processor_id='proc')
    processor2 = ProgramDictProcessor(programs=[], processor_id='crop')
    engine = __typ1([processor1, processor2])
    assert engine.get_processor('proc') == processor1
    assert engine.get_processor('crop') == processor2
    assert engine.get_processor('proc').engine() == engine
    assert engine.get_processor('crop').engine() == engine
    assert set(engine.list_processors()) == {processor1, processor2}


def __tmp16():
    program1 = NothingProgram([cirq.Circuit()], None)
    job1 = NothingJob(
        job_id='test3', processor_id='proc', parent_program=program1, repetitions=100, sweeps=[]
    )
    program1.add_job('jerb', job1)
    job1.add_labels({'color': 'blue'})

    program2 = NothingProgram([cirq.Circuit()], None)
    job2 = NothingJob(
        job_id='test4', processor_id='crop', parent_program=program2, repetitions=100, sweeps=[]
    )
    program2.add_job('jerb2', job2)
    job2.add_labels({'color': 'red'})

    processor1 = ProgramDictProcessor(programs={'prog1': program1}, processor_id='proc')
    processor2 = ProgramDictProcessor(programs={'prog2': program2}, processor_id='crop')
    engine = __typ1([processor1, processor2])

    assert engine.get_program('prog1') == program1

    with pytest.raises(KeyError, match='does not exist'):
        engine.get_program('invalid_id')

    assert set(engine.list_programs()) == {program1, program2}
    assert set(engine.list_jobs()) == {job1, job2}
    assert engine.list_jobs(has_labels={'color': 'blue'}) == [job1]
    assert engine.list_jobs(has_labels={'color': 'red'}) == [job2]

    program3 = NothingProgram([cirq.Circuit()], engine)
    assert program3.engine() == engine

    job3 = NothingJob(
        job_id='test5', processor_id='crop', parent_program=program3, repetitions=100, sweeps=[]
    )
    assert job3.program() == program3
    assert job3.engine() == engine
    assert job3.get_processor() == processor2
    assert job3.get_calibration() == calibration.Calibration()


def __tmp2():
    processor = ProgramDictProcessor(programs={}, processor_id='grocery')
    engine = __typ1([processor])
    assert isinstance(engine.get_sampler('grocery'), cirq.Sampler)
    with pytest.raises(ValueError, match='Invalid processor'):
        engine.get_sampler(['blah'])
