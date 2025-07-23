from typing import TypeAlias
__typ1 : TypeAlias = "bool"
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
"""Module for labelling program graphs with data dependencies."""
import collections
from typing import List
from typing import Tuple

import networkx as nx

from deeplearning.ml4pl.graphs import programl_pb2
from deeplearning.ml4pl.graphs.labelled.dataflow import data_flow_graphs
from labm8.py import app


FLAGS = app.FLAGS

app.DEFINE_boolean(
  "only_entry_blocks_for_liveness_root_nodes",
  False,
  "Use only program entry nodes as the root for creating liveness graphs.",
)


# The node label arrays:
NOT_LIVE_OUT = [1, 0]
LIVE_OUT = [0, 1]


def __tmp2(
  g, __tmp4
) :
  """Get the list of data elements that this statement defines, and the control
  successor statements."""
  defs, successors = [], []
  for src, dst, flow in g.out_edges(__tmp4, data="flow"):
    if flow == programl_pb2.Edge.DATA:
      defs.append(dst)
    elif flow == programl_pb2.Edge.CONTROL:
      successors.append(dst)
  return defs, successors


def GetUsesAndPredecessors(
  g, __tmp4: int
) -> Tuple[List[int], List[int]]:
  """Get the list of data elements which this statement uses, and control
  predecessor statements."""
  uses, predecessors = [], []
  for src, dst, flow in g.in_edges(__tmp4, data="flow"):
    if flow == programl_pb2.Edge.DATA:
      uses.append(src)
    elif flow == programl_pb2.Edge.CONTROL:
      predecessors.append(src)
  return uses, predecessors


def IsExitStatement(g, __tmp4):
  """Determine if a statement is an exit node."""
  for _, _, flow in g.out_edges(__tmp4, data="flow"):
    if flow == programl_pb2.Edge.CONTROL:
      break
  else:
    return True


class __typ0(data_flow_graphs.NetworkXDataFlowGraphAnnotator):
  """Annotate graphs with liveness."""

  def __init__(__tmp1, *args, **kwargs):
    super(__typ0, __tmp1).__init__(*args, **kwargs)
    # Liveness analysis begins at the exit block and works backwards.
    __tmp1.exit_nodes = [
      __tmp4
      for __tmp4, type_ in __tmp1.g.nodes(data="type")
      if type_ == programl_pb2.Node.STATEMENT and IsExitStatement(__tmp1.g, __tmp4)
    ]

    # Since we can't guarantee that input graphs have a single exit point, add
    # a temporary exit block which we will remove after computing liveness
    # results.
    liveness_start_node = __tmp1.g.number_of_nodes()
    assert liveness_start_node not in __tmp1.g.nodes
    __tmp1.g.add_node(liveness_start_node, type=programl_pb2.Node.STATEMENT)
    for exit_node in __tmp1.exit_nodes:
      __tmp1.g.add_edge(
        exit_node, liveness_start_node, flow=programl_pb2.Edge.CONTROL
      )

    # Ignore the liveness starting block when totalling up the data flow steps.
    data_flow_steps = -1

    # Create live-in and live-out maps that will be lazily evaluated.
    __tmp1.in_sets = collections.defaultdict(set)
    __tmp1.out_sets = collections.defaultdict(set)

    work_list = collections.deque([liveness_start_node])
    while work_list:
      data_flow_steps += 1
      __tmp4 = work_list.popleft()
      defs, successors = __tmp2(__tmp1.g, __tmp4)
      uses, predecessors = GetUsesAndPredecessors(__tmp1.g, __tmp4)

      # LiveOut(n) = U {LiveIn(p) for p in succ(n)}
      new_out_set = set().union(*[__tmp1.in_sets[p] for p in successors])

      # LiveIn(n) = Gen(n) U {LiveOut(n) - Kill(n)}
      new_in_set = set(uses).union(new_out_set - set(defs))

      # No need to visit predecessors if the in-set is non-empty and has not
      # changed.
      if not new_in_set or new_in_set != __tmp1.in_sets[__tmp4]:
        work_list.extend([p for p in predecessors if p not in work_list])

      __tmp1.in_sets[__tmp4] = new_in_set
      __tmp1.out_sets[__tmp4] = new_out_set

    # Remove the temporary node that we added.
    __tmp1.g.remove_node(liveness_start_node)

    __tmp1.data_flow_steps = data_flow_steps

  def __tmp5(__tmp1, __tmp4: int, data) :
    """Liveness is a statement-based analysis."""
    return data["type"] == programl_pb2.Node.STATEMENT

  def __tmp3(__tmp1, g, __tmp0: <FILL>) :
    """Annotate nodes in the graph with liveness."""

    # A graph may not have any exit blocks.
    if not __tmp1.exit_nodes:
      g.graph["data_flow_root_node"] = __tmp0
      g.graph["data_flow_steps"] = 0
      g.graph["data_flow_positive_node_count"] = 0
      return

    # We have already pre-computed the live-out sets, so just add the
    # annotations.
    for _, data in g.nodes(data=True):
      data["x"].append(data_flow_graphs.ROOT_NODE_NO)
      data["y"] = NOT_LIVE_OUT
    g.nodes[__tmp0]["x"][-1] = data_flow_graphs.ROOT_NODE_YES

    for __tmp4 in __tmp1.out_sets[__tmp0]:
      g.nodes[__tmp4]["y"] = LIVE_OUT

    g.graph["data_flow_root_node"] = __tmp0
    g.graph["data_flow_steps"] = __tmp1.data_flow_steps
    g.graph["data_flow_positive_node_count"] = len(__tmp1.out_sets[__tmp0])
