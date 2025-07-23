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
"""Module for labelling program graphs with dominator trees information."""
from typing import Dict
from typing import Set

import networkx as nx

from deeplearning.ml4pl.graphs import programl_pb2
from deeplearning.ml4pl.graphs.labelled.dataflow import data_flow_graphs
from labm8.py import app


FLAGS = app.FLAGS


# The node_y arrays for dominator trees:
NOT_DOMINATED = [1, 0]
DOMINATED = [0, 1]


def __tmp5(g, __tmp3: int) -> Set[int]:
  """Get the control predecessors of a node."""
  return set(
    src
    for src, _, flow in g.in_edges(__tmp3, data="flow")
    if flow == programl_pb2.Edge.CONTROL
  )


class __typ0(data_flow_graphs.NetworkXDataFlowGraphAnnotator):
  """Annotate graphs with dominator analysis.

  Statement node A dominates statement node B iff all control paths to B pass
  through A.
  """

  def __init__(__tmp1, *args, **kwargs):
    super(__typ0, __tmp1).__init__(*args, **kwargs)
    __tmp1.dominator_sets_by_function = {}
    __tmp1.data_flow_steps_by_function = {}

  def __tmp4(__tmp1, __tmp3, data) -> __typ1:
    """Dominator trees are a statement-based analysis."""
    return data["type"] == programl_pb2.Node.STATEMENT and data["function"]

  def __tmp2(__tmp1, g: nx.MultiDiGraph, __tmp0: <FILL>) -> None:
    """Annotate nodes in the graph with dominator trees.

    The 'root node' annotation is a [0,1] value appended to node x vectors.
    The node label is a 1-hot binary vector set to y node vectors.

    Args:
      g: The graph to annotate.
      root_node: The root node for building the dominator tree.

    Returns:
      A data flow annotated graph.
    """
    function = g.nodes[__tmp0]["function"]

    if function is None:
      # Root node is outside of a function, so cannot dominate any other nodes.
      g.graph["data_flow_root_node"] = __tmp0
      g.graph["data_flow_steps"] = 0
      g.graph["data_flow_positive_node_count"] = 0
      return

    if function in __tmp1.dominator_sets_by_function:
      dominators = __tmp1.dominator_sets_by_function[function]
    else:
      # Because a node may only be dominated by a node from within the same
      # function, we need only consider the statements nodes within the same
      # function as the root node.
      statement_nodes: Set[int] = {
        __tmp3
        for __tmp3, data in g.nodes(data=True)
        if data["type"] == programl_pb2.Node.STATEMENT
        and data["function"] == function
      }

      # A mapping from statement to statement predecessors. This is lazily
      # evaluated.
      predecessors: Dict[int, Set[int]] = {}

      # Initialize the dominator sets. These map nodes to the set of nodes that
      # dominate it.
      initial_dominators = statement_nodes - set([__tmp0])
      dominators: Dict[int, Set[int]] = {
        n: initial_dominators for n in statement_nodes
      }
      dominators[__tmp0] = set([__tmp0])

      changed = True
      data_flow_steps = 0
      while changed:
        changed = False
        data_flow_steps += 1
        for __tmp3 in dominators:
          if __tmp3 == __tmp0:
            continue

          # Get the predecessor nodes or compute them if required.
          pred = predecessors.get(__tmp3, __tmp5(g, __tmp3))
          predecessors[__tmp3] = pred

          dom_pred = [dominators[p] for p in pred]
          if dom_pred:
            dom_pred = set.intersection(*dom_pred)
          else:
            dom_pred = set()
          new_dom = {__tmp3}.union(dom_pred)
          if new_dom != dominators[__tmp3]:
            dominators[__tmp3] = new_dom
            changed = True

      # Cache the result for next time.
      __tmp1.dominator_sets_by_function[function] = dominators
      __tmp1.data_flow_steps_by_function[function] = data_flow_steps

    # Now that we have computed the dominator sets, assign labels and features
    # to all nodes.
    dominated_node_count = 0
    for __tmp3, data in g.nodes(data=True):
      data["x"].append(data_flow_graphs.ROOT_NODE_NO)
      if __tmp3 in dominators and __tmp0 in dominators[__tmp3]:
        dominated_node_count += 1
        data["y"] = DOMINATED
      else:
        data["y"] = NOT_DOMINATED

    g.nodes[__tmp0]["x"][-1] = data_flow_graphs.ROOT_NODE_YES

    g.graph["data_flow_root_node"] = __tmp0
    g.graph["data_flow_steps"] = __tmp1.data_flow_steps_by_function[function]
    g.graph["data_flow_positive_node_count"] = dominated_node_count
