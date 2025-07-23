# Copyright (c) 2017-2020 Chris Cummins.
#
# DeepSmith is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DeepSmith is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DeepSmith.  If not, see <https://www.gnu.org/licenses/>.
"""A clgen generator for pre-trained models.

By supporting only pre-trained models, this module does not depend on the CLgen
corpus implementation, allowing for a much smaller dependency set, i.e. without
pulling all of the LLVM libraries required by CLgen's corpus preprocessors.
"""
import typing

from deeplearning.clgen import sample
from deeplearning.clgen import sample_observers
from deeplearning.clgen.proto import model_pb2
from deeplearning.deepsmith import services
from deeplearning.deepsmith.generators import generator
from deeplearning.deepsmith.proto import deepsmith_pb2
from deeplearning.deepsmith.proto import generator_pb2
from deeplearning.deepsmith.proto import generator_pb2_grpc
from labm8.py import app

FLAGS = app.FLAGS


def __tmp5(
  instance: sample.Instance,
) :
  """Convert a CLgen instance to a DeepSmith generator proto."""
  g = deepsmith_pb2.Generator()
  g.name = "clgen"
  g.opts["model"] = str(instance.model.path)
  g.opts["sampler"] = instance.sampler.hash
  return g


class SampleObserver(sample_observers.SampleObserver):
  """A CLgen model sample observer."""

  def __init__(
    __tmp2,
    config,
    response: generator_pb2.GenerateTestcasesResponse,
    num_testcases: <FILL>,
  ):
    __tmp2.config = config
    __tmp2.response = response
    __tmp2.num_testcases = num_testcases
    __tmp2.sample_count = 0

  def __tmp4(__tmp2, sample: model_pb2.Sample) :
    """Sample observer."""
    __tmp2.sample_count += 1
    app.Log(1, "Generated sample %d.", __tmp2.sample_count)
    __tmp2.response.testcases.extend(__tmp2.SampleToTestcases(sample))
    return len(__tmp2.response.testcases) >= __tmp2.num_testcases

  def SampleToTestcases(
    __tmp2, sample_: model_pb2.Sample
  ) :
    """Convert a CLgen sample to a list of DeepSmith testcase protos."""
    testcases = []
    for skeleton in __tmp2.config.testcase_skeleton:
      t = deepsmith_pb2.Testcase()
      t.CopyFrom(skeleton)
      p = t.profiling_events.add()
      p.type = "generation"
      p.duration_ms = sample_.wall_time_ms
      p.event_start_epoch_ms = sample_.sample_start_epoch_ms_utc
      t.inputs["src"] = sample_.text
      testcases.append(t)
    return testcases


class ClgenGenerator(
  generator.GeneratorServiceBase, generator_pb2_grpc.GeneratorServiceServicer
):
  def __init__(
    __tmp2, config: generator_pb2.ClgenGenerator, no_init: bool = False
  ):
    """

    Args:
      config: The Generator config.
      no_init: If True, do not initialize the instance and generator values.
    """
    super(ClgenGenerator, __tmp2).__init__(config)
    if not no_init:
      __tmp2.instance = sample.Instance(__tmp2.config.instance)
      __tmp2.toolchain = "opencl"
      __tmp2.generator = __tmp5(__tmp2.instance)
      if not __tmp2.config.testcase_skeleton:
        raise ValueError("No testcase skeletons provided")
      for skeleton in __tmp2.config.testcase_skeleton:
        skeleton.generator.CopyFrom(__tmp2.generator)

  def __tmp1(
    __tmp2, __tmp3, __tmp0
  ) :
    del __tmp0
    response = services.BuildDefaultResponse(
      generator_pb2.GetGeneratorCapabilitiesRequest
    )
    response.toolchain = __tmp2.config.model.corpus.language
    response.generator = __tmp2.generator
    return response

  def GenerateTestcases(
    __tmp2, __tmp3: generator_pb2.GenerateTestcasesRequest, __tmp0
  ) -> generator_pb2.GenerateTestcasesResponse:
    del __tmp0
    response = services.BuildDefaultResponse(
      generator_pb2.GenerateTestcasesResponse
    )
    with __tmp2.instance.Session():
      sample_observer = SampleObserver(
        __tmp2.config, response, __tmp3.num_testcases
      )
      __tmp2.instance.model.Sample(__tmp2.instance.sampler, [sample_observer])

    return response


if __name__ == "__main__":
  app.RunWithArgs(ClgenGenerator.Main(generator_pb2.ClgenGenerator))
