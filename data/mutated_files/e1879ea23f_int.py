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


def __tmp2(
  config: generator_pb2.ClsmithGenerator,
) -> deepsmith_pb2.Generator:
  """Convert a config proto to a DeepSmith generator proto."""
  g = deepsmith_pb2.Generator()
  g.name = "clsmith"
  g.opts["opts"] = " ".join(config.opt)
  return g


class ClsmithGenerator(
  generator.GeneratorServiceBase, generator_pb2_grpc.GeneratorServiceServicer
):
  def __init__(__tmp1, config):
    super(ClsmithGenerator, __tmp1).__init__(config)
    __tmp1.toolchain = "opencl"
    __tmp1.generator = __tmp2(__tmp1.config)
    if not __tmp1.config.testcase_skeleton:
      raise ValueError("No testcase skeletons provided")
    for skeleton in __tmp1.config.testcase_skeleton:
      skeleton.generator.CopyFrom(__tmp1.generator)

  def __tmp5(
    __tmp1, __tmp4: generator_pb2.GenerateTestcasesRequest, __tmp0
  ) :
    del __tmp0
    num_programs = int(
      math.ceil(__tmp4.num_testcases / len(__tmp1.config.testcase_skeleton))
    )
    response = services.BuildDefaultResponse(
      generator_pb2.GenerateTestcasesResponse
    )
    try:
      for i in range(num_programs):
        response.testcases.extend(
          __tmp1.SourceToTestcases(*__tmp1.GenerateOneSource())
        )
        app.Log(1, "Generated file %d.", i + 1)
    except clsmith.CLSmithError as e:
      response.status.returncode = service_pb2.ServiceStatus.ERROR
      response.status.error_message = __typ0(e)
    return response

  def GenerateOneSource(__tmp1) -> typing.Tuple[__typ0, int, int]:
    """Generate and return a single CLSmith program.

    Returns:
      A tuple of the source code as a string, the generation time, and the start
      time.
    """
    __tmp3 = labdate.MillisecondsTimestamp()
    src = clsmith.Exec(*list(__tmp1.config.opt))
    wall_time_ms = labdate.MillisecondsTimestamp() - __tmp3
    return src, wall_time_ms, __tmp3

  def SourceToTestcases(
    __tmp1, src, wall_time_ms: <FILL>, __tmp3
  ) -> typing.List[deepsmith_pb2.Testcase]:
    """Make testcases from a CLSmith generated source."""
    testcases = []
    for skeleton in __tmp1.config.testcase_skeleton:
      t = deepsmith_pb2.Testcase()
      t.CopyFrom(skeleton)
      p = t.profiling_events.add()
      p.type = "generation"
      p.duration_ms = wall_time_ms
      p.event_start_epoch_ms = __tmp3
      t.inputs["src"] = src
      testcases.append(t)
    return testcases


if __name__ == "__main__":
  app.RunWithArgs(ClsmithGenerator.Main(generator_pb2.ClsmithGenerator))
