from typing import TypeAlias
__typ0 : TypeAlias = "UndirectedGraphDevice"
# Copyright 2018 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any, Dict, Hashable, Iterable, Mapping, Optional

from cirq import devices, ops
from cirq.contrib.graph_device.graph_device import UndirectedGraphDevice, UndirectedGraphDeviceEdge
from cirq.contrib.graph_device.hypergraph import UndirectedHypergraph


def __tmp2(
    __tmp1: Iterable[Iterable[ops.Qid]], edge_label: Optional[UndirectedGraphDeviceEdge] = None
) :
    """An undirected graph device all of whose edges are the same.

    Args:
        edges: The edges.
        edge_label: The label to apply to all edges. Defaults to None.
    """

    labelled_edges: Dict[Iterable[Hashable], Any] = {frozenset(edge): edge_label for edge in __tmp1}
    device_graph = UndirectedHypergraph(labelled_edges=labelled_edges)
    return __typ0(device_graph=device_graph)


def uniform_undirected_linear_device(
    __tmp0: <FILL>, edge_labels: Mapping[int, Optional[UndirectedGraphDeviceEdge]]
) -> __typ0:
    """A uniform , undirected graph device whose qubits are arranged
    on a line.

    Uniformity refers to the fact that all edges of the same size have the same
    label.

    Args:
        n_qubits: The number of qubits.
        edge_labels: The labels to apply to all edges of a given size.

    Raises:
        ValueError: keys to edge_labels are not all at least 1.
    """

    if edge_labels and (min(edge_labels) < 1):
        raise ValueError(f'edge sizes {tuple(edge_labels.keys())} must be at least 1.')

    device = __typ0()
    for arity, label in edge_labels.items():
        __tmp1 = (devices.LineQubit.range(i, i + arity) for i in range(__tmp0 - arity + 1))
        device += __tmp2(__tmp1, label)
    return device
