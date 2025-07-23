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
"""Unit tests for //deeplearning/ml4pl/graphs/labelled:graph_batcher."""
from typing import Iterable
from typing import List

from deeplearning.ml4pl.graphs.labelled import graph_batcher
from deeplearning.ml4pl.graphs.labelled import graph_tuple
from deeplearning.ml4pl.testing import random_graph_tuple_generator
from labm8.py import decorators
from labm8.py import test


FLAGS = test.FLAGS


def MockIterator(
  graphs: List[graph_tuple.GraphTuple],
) :
  """Return an iterator over graphs."""
  for graph in graphs:
    yield graph


def __tmp1():
  """Test input with empty graph """
  batcher = graph_batcher.GraphBatcher(MockIterator([]))
  with test.Raises(StopIteration):
    next(batcher)


@test.Parametrize("graph_count", (1, 5, 10))
def test_GraphBatcher_collect_all_inputs(__tmp9):
  batcher = graph_batcher.GraphBatcher(
    MockIterator(
      [
        random_graph_tuple_generator.CreateRandomGraphTuple()
        for _ in range(__tmp9)
      ]
    )
  )
  batches = list(batcher)
  assert len(batches) == 1
  assert batches[0].is_disjoint_graph
  assert batches[0].disjoint_graph_count == __tmp9


def __tmp4():
  """Test that error is raised when graph is larger than max node count."""
  big_graph = random_graph_tuple_generator.CreateRandomGraphTuple(node_count=10)

  batcher = graph_batcher.GraphBatcher(
    MockIterator([big_graph]),
    __tmp3=5,
    max_node_count_limit_handler="error",
  )

  with test.Raises(ValueError):
    next(batcher)


def __tmp8():
  """Test that graph is included when larger than max node count."""
  big_graph = random_graph_tuple_generator.CreateRandomGraphTuple(node_count=10)

  batcher = graph_batcher.GraphBatcher(
    MockIterator([big_graph]),
    __tmp3=5,
    max_node_count_limit_handler="include",
  )

  assert next(batcher)


def __tmp8():
  """Test that graph is skipped when larger than max node count."""
  big_graph = random_graph_tuple_generator.CreateRandomGraphTuple(node_count=10)

  batcher = graph_batcher.GraphBatcher(
    MockIterator([big_graph]),
    __tmp3=5,
    max_node_count_limit_handler="skip",
  )

  try:
    next(batcher)
  except StopIteration:
    pass


def __tmp2():
  """Test the number of batches returned with evenly divisible node counts."""
  batcher = graph_batcher.GraphBatcher(
    MockIterator(
      [
        random_graph_tuple_generator.CreateRandomGraphTuple(node_count=5),
        random_graph_tuple_generator.CreateRandomGraphTuple(node_count=5),
        random_graph_tuple_generator.CreateRandomGraphTuple(node_count=5),
        random_graph_tuple_generator.CreateRandomGraphTuple(node_count=5),
      ]
    ),
    __tmp3=10,
  )

  batches = list(batcher)
  assert len(batches) == 2
  assert batches[0].is_disjoint_graph
  assert batches[0].disjoint_graph_count == 2
  assert batches[1].is_disjoint_graph
  assert batches[1].disjoint_graph_count == 2


def __tmp7():
  """Test the number of batches when max graphs are filtered."""
  batcher = graph_batcher.GraphBatcher(
    MockIterator(
      [random_graph_tuple_generator.CreateRandomGraphTuple() for _ in range(7)]
    ),
    __tmp5=3,
  )

  batches = list(batcher)
  assert len(batches) == 3
  assert batches[0].disjoint_graph_count == 3
  assert batches[1].disjoint_graph_count == 3
  assert batches[2].disjoint_graph_count == 1


def __tmp6():
  """Test the number of batches when exact graph counts are required."""
  batcher = graph_batcher.GraphBatcher(
    MockIterator(
      [random_graph_tuple_generator.CreateRandomGraphTuple() for _ in range(7)]
    ),
    exact_graph_count=3,
  )

  batches = list(batcher)
  assert len(batches) == 2
  assert batches[0].disjoint_graph_count == 3
  assert batches[1].disjoint_graph_count == 3
  # The last graph is ignored because we have exactly the right number of
  # graphs.


@decorators.loop_for(seconds=5)
@test.Parametrize("graph_count", (1, 10, 100))
@test.Parametrize("max_node_count", (50, 100))
@test.Parametrize("max_graph_count", (0, 3, 10))
def __tmp0(
  __tmp9: <FILL>, __tmp5, __tmp3: int
):
  """Fuzz the graph batcher with a range of parameter choices and input
  sizes.
  """
  graphs = MockIterator(
    [
      random_graph_tuple_generator.CreateRandomGraphTuple()
      for _ in range(__tmp9)
    ]
  )
  batcher = graph_batcher.GraphBatcher(
    graphs, __tmp3=__tmp3, __tmp5=__tmp5
  )
  batches = list(batcher)
  assert sum(b.disjoint_graph_count for b in batches) == __tmp9


if __name__ == "__main__":
  test.Main()
