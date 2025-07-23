# Copyright 2019-2020 the ProGraML authors.
#
# Contact Chris Cummins <chrisc.101@gmail.com>.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Benchmarks for //deeplearning/ml4pl/graphs:programl."""
from typing import List

import networkx as nx

from deeplearning.ml4pl.graphs import programl
from deeplearning.ml4pl.graphs import programl_pb2
from deeplearning.ml4pl.testing import random_programl_generator
from labm8.py import test

FLAGS = test.FLAGS

###############################################################################
# Fixtures.
###############################################################################


@test.Fixture(scope="session", params=(1, 2))
def __tmp6(__tmp4) -> int:
  """A test fixture which enumerates dimensionalities."""
  return __tmp4.param


@test.Fixture(scope="session", params=(0, 2))
def node_y_dimensionality(__tmp4) -> int:
  """A test fixture which enumerates dimensionalities."""
  return __tmp4.param


@test.Fixture(scope="session", params=(0, 2))
def __tmp3(__tmp4) :
  """A test fixture which enumerates dimensionalities."""
  return __tmp4.param


@test.Fixture(scope="session", params=(0, 2))
def graph_y_dimensionality(__tmp4) :
  """A test fixture which enumerates dimensionalities."""
  return __tmp4.param


@test.Fixture(scope="session", params=(None, 10, 100))
def __tmp2(__tmp4) :
  """A test fixture which enumerates node_counts."""
  return __tmp4.param


###############################################################################
# Benchmarks.
###############################################################################


@test.Fixture(scope="session")
def __tmp8(
  __tmp6: int,
  node_y_dimensionality: <FILL>,
  __tmp3,
  graph_y_dimensionality: int,
  __tmp2: int,
) -> List[programl_pb2.ProgramGraph]:
  """A fixture which returns 10 protos for benchmarking."""
  return [
    random_programl_generator.CreateRandomProto(
      __tmp6=__tmp6,
      node_y_dimensionality=node_y_dimensionality,
      __tmp3=__tmp3,
      graph_y_dimensionality=graph_y_dimensionality,
      __tmp2=__tmp2,
    )
    for _ in range(10)
  ]


@test.Fixture(scope="session")
def __tmp7(
  __tmp8: List[programl_pb2.ProgramGraph],
) :
  """A fixture which returns 10 graphs for benchmarking."""
  return [programl.ProgramGraphToNetworkX(p) for p in __tmp8]


def __tmp0(fn, inputs):
  """A micro-benchmark which calls the given function over all inputs."""
  for element in inputs:
    fn(element)


def test_benchmark_proto_to_networkx(
  __tmp1, __tmp8: List[programl_pb2.ProgramGraph]
):
  """Benchmark proto -> networkx."""
  __tmp1(__tmp0, programl.ProgramGraphToNetworkX, __tmp8)


def __tmp5(
  __tmp1, __tmp8: List[programl_pb2.ProgramGraph]
):
  """Benchmark proto -> graphviz."""
  __tmp1(__tmp0, programl.ProgramGraphToGraphviz, __tmp8)


def test_benchmark_networkx_to_proto(
  __tmp1, __tmp7: List[nx.MultiDiGraph]
):
  """Benchmark networkx -> proto."""
  __tmp1(__tmp0, programl.NetworkXToProgramGraph, __tmp7)


if __name__ == "__main__":
  test.Main()
