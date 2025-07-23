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
def node_x_dimensionality(__tmp4) :
  """A test fixture which enumerates dimensionalities."""
  return __tmp4.param


@test.Fixture(scope="session", params=(0, 2))
def __tmp0(__tmp4) :
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
def node_count(__tmp4) :
  """A test fixture which enumerates node_counts."""
  return __tmp4.param


###############################################################################
# Benchmarks.
###############################################################################


@test.Fixture(scope="session")
def benchmark_proto(
  node_x_dimensionality: <FILL>,
  __tmp0,
  __tmp3,
  graph_y_dimensionality,
  node_count,
) :
  """A fixture which returns 10 protos for benchmarking."""
  return [
    random_programl_generator.CreateRandomProto(
      node_x_dimensionality=node_x_dimensionality,
      __tmp0=__tmp0,
      __tmp3=__tmp3,
      graph_y_dimensionality=graph_y_dimensionality,
      node_count=node_count,
    )
    for _ in range(10)
  ]


@test.Fixture(scope="session")
def __tmp5(
  benchmark_proto,
) :
  """A fixture which returns 10 graphs for benchmarking."""
  return [programl.ProgramGraphToNetworkX(p) for p in benchmark_proto]


def Benchmark(__tmp2, inputs):
  """A micro-benchmark which calls the given function over all inputs."""
  for element in inputs:
    __tmp2(element)


def __tmp1(
  benchmark, benchmark_proto
):
  """Benchmark proto -> networkx."""
  benchmark(Benchmark, programl.ProgramGraphToNetworkX, benchmark_proto)


def test_benchmark_proto_to_graphviz(
  benchmark, benchmark_proto
):
  """Benchmark proto -> graphviz."""
  benchmark(Benchmark, programl.ProgramGraphToGraphviz, benchmark_proto)


def __tmp6(
  benchmark, __tmp5
):
  """Benchmark networkx -> proto."""
  benchmark(Benchmark, programl.NetworkXToProgramGraph, __tmp5)


if __name__ == "__main__":
  test.Main()
