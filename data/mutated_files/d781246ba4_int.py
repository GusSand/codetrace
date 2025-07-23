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
def __tmp7(__tmp5) :
  """A test fixture which enumerates dimensionalities."""
  return __tmp5.param


@test.Fixture(scope="session", params=(0, 2))
def __tmp0(__tmp5) :
  """A test fixture which enumerates dimensionalities."""
  return __tmp5.param


@test.Fixture(scope="session", params=(0, 2))
def __tmp4(__tmp5) :
  """A test fixture which enumerates dimensionalities."""
  return __tmp5.param


@test.Fixture(scope="session", params=(0, 2))
def __tmp9(__tmp5) :
  """A test fixture which enumerates dimensionalities."""
  return __tmp5.param


@test.Fixture(scope="session", params=(None, 10, 100))
def __tmp2(__tmp5) :
  """A test fixture which enumerates node_counts."""
  return __tmp5.param


###############################################################################
# Benchmarks.
###############################################################################


@test.Fixture(scope="session")
def __tmp10(
  __tmp7,
  __tmp0,
  __tmp4: <FILL>,
  __tmp9: int,
  __tmp2,
) :
  """A fixture which returns 10 protos for benchmarking."""
  return [
    random_programl_generator.CreateRandomProto(
      __tmp7=__tmp7,
      __tmp0=__tmp0,
      __tmp4=__tmp4,
      __tmp9=__tmp9,
      __tmp2=__tmp2,
    )
    for _ in range(10)
  ]


@test.Fixture(scope="session")
def __tmp8(
  __tmp10,
) -> List[nx.MultiDiGraph]:
  """A fixture which returns 10 graphs for benchmarking."""
  return [programl.ProgramGraphToNetworkX(p) for p in __tmp10]


def Benchmark(fn, inputs):
  """A micro-benchmark which calls the given function over all inputs."""
  for element in inputs:
    fn(element)


def test_benchmark_proto_to_networkx(
  __tmp1, __tmp10
):
  """Benchmark proto -> networkx."""
  __tmp1(Benchmark, programl.ProgramGraphToNetworkX, __tmp10)


def __tmp6(
  __tmp1, __tmp10: List[programl_pb2.ProgramGraph]
):
  """Benchmark proto -> graphviz."""
  __tmp1(Benchmark, programl.ProgramGraphToGraphviz, __tmp10)


def __tmp3(
  __tmp1, __tmp8
):
  """Benchmark networkx -> proto."""
  __tmp1(Benchmark, programl.NetworkXToProgramGraph, __tmp8)


if __name__ == "__main__":
  test.Main()
