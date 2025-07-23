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
"""Benchmarks for //deeplearning/ml4pl/graphs/labelled:graph_database_reader."""
import copy
import random
from typing import List

from deeplearning.ml4pl.graphs.labelled import graph_database_reader as reader
from deeplearning.ml4pl.graphs.labelled import graph_tuple_database
from deeplearning.ml4pl.testing import random_graph_tuple_database_generator
from deeplearning.ml4pl.testing import testing_databases
from labm8.py import test


FLAGS = test.FLAGS

MODULE_UNDER_TEST = None


@test.Fixture(
  scope="session",
  params=testing_databases.GetDatabaseUrls(),
  namer=testing_databases.DatabaseUrlNamer("graph_db"),
)
def empty_graph_db(request) :
  """A test fixture which yields an empty database."""
  yield from testing_databases.YieldDatabase(
    graph_tuple_database.Database, request.param
  )


@test.Fixture(scope="session")
def __tmp3(
  empty_graph_db,
) -> graph_tuple_database.Database:
  """Fixture which returns a database with 5000 + 2 graph tuples, where 2 of the
  graph tuples are empty.

  For the current implementation of CreateRandomGraphTuple(), a database of
  5000 graphs is ~14MB of data.
  """
  # Generate some random graph tuples.
  graph_pool = [
    random_graph_tuple_database_generator.CreateRandomGraphTuple()
    for _ in range(128)
  ]

  # Generate a full list of graphs by randomly selecting from the graph pool.
  random_graph_tuples: List[graph_tuple_database.GraphTuple] = [
    copy.deepcopy(random.choice(graph_pool)) for _ in range(10000)
  ]
  # Index the random graphs by ir_id.
  for i, t in enumerate(random_graph_tuples):
    t.ir_id = i
    t.data_flow_steps = i

  with empty_graph_db.Session(commit=True) as s:
    s.add_all(random_graph_tuples)
    # Create the empty graph tuples. These should be ignored by the graph
    # reader.
    s.add_all(
      [
        graph_tuple_database.GraphTuple.CreateEmpty(0),
        graph_tuple_database.GraphTuple.CreateEmpty(0),
      ]
    )

  return empty_graph_db


# Buffer sizes selected based on the size of the db_1000 fixture database.
READER_BUFFER_SIZES = [1, 4, 1024]


@test.Parametrize("buffer_size_mb", READER_BUFFER_SIZES)
def test_benchmark_BufferedGraphReader_in_order(
  __tmp2, __tmp3, __tmp4: int,
):
  """Benchmark in-order database reads."""
  __tmp2(
    list,
    reader.BufferedGraphReader(
      __tmp3,
      __tmp4=__tmp4,
      order=reader.BufferedGraphReaderOrder.IN_ORDER,
    ),
  )


@test.Parametrize("buffer_size_mb", READER_BUFFER_SIZES)
def __tmp1(
  __tmp2, __tmp3, __tmp4,
):
  """Benchmark global random database reads."""
  __tmp2(
    list,
    reader.BufferedGraphReader(
      __tmp3,
      __tmp4=__tmp4,
      order=reader.BufferedGraphReaderOrder.GLOBAL_RANDOM,
    ),
  )


@test.Parametrize("buffer_size_mb", READER_BUFFER_SIZES)
def __tmp0(
  __tmp2, __tmp3, __tmp4: <FILL>,
):
  """Benchmark batch random database reads."""
  __tmp2(
    list,
    reader.BufferedGraphReader(
      __tmp3,
      __tmp4=__tmp4,
      order=reader.BufferedGraphReaderOrder.BATCH_RANDOM,
    ),
  )


@test.Parametrize("buffer_size_mb", READER_BUFFER_SIZES)
def test_benchmark_BufferedGraphReader_data_flow_steps(
  __tmp2, __tmp3, __tmp4: int,
):
  """Benchmark ordered database reads."""
  __tmp2(
    list,
    reader.BufferedGraphReader(
      __tmp3,
      __tmp4=__tmp4,
      order=reader.BufferedGraphReaderOrder.DATA_FLOW_STEPS,
    ),
  )


if __name__ == "__main__":
  test.Main()
