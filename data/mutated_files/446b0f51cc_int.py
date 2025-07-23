from typing import TypeAlias
__typ0 : TypeAlias = "str"
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
"""A CLSmith program generator."""
import math
import typing

from compilers.clsmith import clsmith
from deeplearning.deepsmith import services
from deeplearning.deepsmith.generators import generator
from deeplearning.deepsmith.proto import deepsmith_pb2
from deeplearning.deepsmith.proto import generator_pb2
from deeplearning.deepsmith.proto import generator_pb2_grpc
from deeplearning.deepsmith.proto import service_pb2
from labm8.py import app
from labm8.py import labdate

FLAGS = app.FLAGS


def __tmp3(
  config,
) :
  """Convert a config proto to a DeepSmith generator proto."""
  g = deepsmith_pb2.Generator()
  g.name = "clsmith"
  g.opts["opts"] = " ".join(config.opt)
  return g


class ClsmithGenerator(
  generator.GeneratorServiceBase, generator_pb2_grpc.GeneratorServiceServicer
):
  def __init__(__tmp2, config):
    super(ClsmithGenerator, __tmp2).__init__(config)
    __tmp2.toolchain = "opencl"
    __tmp2.generator = __tmp3(__tmp2.config)
    if not __tmp2.config.testcase_skeleton:
      raise ValueError("No testcase skeletons provided")
    for skeleton in __tmp2.config.testcase_skeleton:
      skeleton.generator.CopyFrom(__tmp2.generator)

  def __tmp6(
    __tmp2, __tmp5, __tmp1
  ) -> generator_pb2.GenerateTestcasesResponse:
    del __tmp1
    num_programs = int(
      math.ceil(__tmp5.num_testcases / len(__tmp2.config.testcase_skeleton))
    )
    response = services.BuildDefaultResponse(
      generator_pb2.GenerateTestcasesResponse
    )
    try:
      for i in range(num_programs):
        response.testcases.extend(
          __tmp2.SourceToTestcases(*__tmp2.GenerateOneSource())
        )
        app.Log(1, "Generated file %d.", i + 1)
    except clsmith.CLSmithError as e:
      response.status.returncode = service_pb2.ServiceStatus.ERROR
      response.status.error_message = __typ0(e)
    return response

  def GenerateOneSource(__tmp2) :
    """Generate and return a single CLSmith program.

    Returns:
      A tuple of the source code as a string, the generation time, and the start
      time.
    """
    __tmp4 = labdate.MillisecondsTimestamp()
    __tmp7 = clsmith.Exec(*list(__tmp2.config.opt))
    __tmp0 = labdate.MillisecondsTimestamp() - __tmp4
    return __tmp7, __tmp0, __tmp4

  def SourceToTestcases(
    __tmp2, __tmp7, __tmp0, __tmp4: <FILL>
  ) :
    """Make testcases from a CLSmith generated source."""
    testcases = []
    for skeleton in __tmp2.config.testcase_skeleton:
      t = deepsmith_pb2.Testcase()
      t.CopyFrom(skeleton)
      p = t.profiling_events.add()
      p.type = "generation"
      p.duration_ms = __tmp0
      p.event_start_epoch_ms = __tmp4
      t.inputs["src"] = __tmp7
      testcases.append(t)
    return testcases


if __name__ == "__main__":
  app.RunWithArgs(ClsmithGenerator.Main(generator_pb2.ClsmithGenerator))
