from typing import TypeAlias
__typ0 : TypeAlias = "bool"
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
"""Unit tests for //deeplearning/ml4pl/graphs/labelled/dataflow/reachability."""
from typing import List
from typing import Optional

import networkx as nx

from deeplearning.ml4pl.graphs import programl
from deeplearning.ml4pl.graphs import programl_pb2
from deeplearning.ml4pl.graphs.labelled.dataflow import data_flow_graphs
from labm8.py import test


FLAGS = test.FLAGS


class __typ1(
  data_flow_graphs.NetworkXDataFlowGraphAnnotator
):
  """A mock networkx annotator for testing."""

  def __init__(__tmp2, *args, node_y: Optional[List[int]] = None, **kwargs):
    super(__typ1, __tmp2).__init__(*args, **kwargs)
    __tmp2.node_y = node_y

  def IsValidRootNode(__tmp2, node, data) :
    """The root node type."""
    return data["type"] == programl_pb2.Node.STATEMENT

  def __tmp3(__tmp2, g, __tmp1: <FILL>) :
    """Add annotations.

    If node_y was passed to constructor, then that value is set. The node x
    lists are concated with the node ID.
    """
    # Add a node x feature.
    for node, data in g.nodes(data=True):
      data["x"].append(node)

    # Set a node y vector if desired.
    if __tmp2.node_y:
      for _, data in g.nodes(data=True):
        data["y"] = __tmp2.node_y

    g.graph["data_flow_root_node"] = __tmp1
    g.graph["data_flow_steps"] = 1


def __tmp5():
  """Test that root nodes are correctly selected."""
  builder = programl.GraphBuilder()
  builder.AddNode(type=programl_pb2.Node.STATEMENT)
  builder.AddNode(type=programl_pb2.Node.IDENTIFIER)
  annotator = __typ1(builder.proto)
  assert annotator.root_nodes == [0]


def __tmp0():
  """Test that a graph with no root nodes produces no annotations."""
  builder = programl.GraphBuilder()
  annotator = __typ1(builder.proto)
  annotated = annotator.MakeAnnotated()
  assert len(annotated.graphs) == 0
  assert len(annotated.protos) == 0


def __tmp4():
  """Test annotator with no node labels."""
  builder = programl.GraphBuilder()
  builder.AddNode()
  annotator = __typ1(builder.proto)
  annotated = annotator.MakeAnnotated()
  assert len(annotated.graphs) == 1
  assert len(annotated.protos) == 1
  assert annotated.graphs[0].nodes[0]["y"] == []
  assert annotated.protos[0].node[0].y == []


def __tmp8():
  """Test annotator with node labels."""
  builder = programl.GraphBuilder()
  builder.AddNode()
  annotator = __typ1(builder.proto, node_y=[1, 2])
  annotated = annotator.MakeAnnotated()
  assert len(annotated.graphs) == 1
  assert len(annotated.protos) == 1
  assert annotated.graphs[0].nodes[0]["y"] == [1, 2]
  assert annotated.protos[0].node[0].y == [1, 2]


def __tmp6():
  """Test that node X values get appended."""
  builder = programl.GraphBuilder()
  for _ in range(10):
    builder.AddNode()
  annotator = __typ1(builder.proto)
  annotated = annotator.MakeAnnotated()
  assert len(annotated.graphs) == 10
  assert len(annotated.protos) == 10
  # Check each graph to ensure that each graph gets a fresh set of node x
  # arrays to append to, else these lists will graph in length.
  for graph, proto in zip(annotated.graphs, annotated.protos):
    assert graph.nodes[0]["x"] == [0]
    assert graph.nodes[1]["x"] == [1]
    assert graph.nodes[2]["x"] == [2]

    assert proto.node[0].x == [0]
    assert proto.node[1].x == [1]
    assert proto.node[2].x == [2]


def __tmp7():
  """Test annotator with node labels."""
  builder = programl.GraphBuilder()
  builder.AddNode()
  builder.AddNode()
  builder.AddNode()
  annotator = __typ1(builder.proto, node_y=[1, 2])
  annotated = annotator.MakeAnnotated()
  assert len(annotated.graphs) == 3
  assert len(annotated.protos) == 3


@test.Parametrize("n", (1, 10, 100))
def __tmp9(n):
  """Test annotator with node labels."""
  builder = programl.GraphBuilder()
  for _ in range(100):
    builder.AddNode()
  annotator = __typ1(builder.proto, node_y=[1, 2])
  annotated = annotator.MakeAnnotated(n)
  assert len(annotated.graphs) == n
  assert len(annotated.protos) == n


def __tmp10():
  """Test the number of graphs when only a subset of nodes are roots."""
  builder = programl.GraphBuilder()
  for i in range(50):
    if i % 2 == 0:
      builder.AddNode(type=programl_pb2.Node.STATEMENT)
    else:
      builder.AddNode(type=programl_pb2.Node.IDENTIFIER)
  annotator = __typ1(builder.proto, node_y=[1, 2])
  annotated = annotator.MakeAnnotated()
  # Only the 25 statement nodes are used as roots.
  assert len(annotated.graphs) == 25
  assert len(annotated.protos) == 25


if __name__ == "__main__":
  test.Main()
