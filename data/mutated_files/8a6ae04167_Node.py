from typing import TypeAlias
__typ0 : TypeAlias = "Edge"
from dataclasses import dataclass, field
from typing import Any, List, Dict

from graphx.core.data_providers.data_provider import DataProvider
from graphx.core.entities import Edge, Node
from graphx.core.exceptions import EntityAlreadyExistsException

@dataclass
class __typ1(DataProvider[Node, __typ0]):
    nodes: Dict[str, Node] = field(default_factory=lambda: {})
    edges: List[__typ0] = field(default_factory=lambda: [])

    def save(__tmp1, node: Node) -> None:
        if node.id in __tmp1.nodes:
            raise EntityAlreadyExistsException('Node already exists!')
        __tmp1.nodes[node.id] = node

    def add_edge(__tmp1, __tmp2: __typ0) -> None:
        if __tmp1.edge_exists(__tmp2):
            raise EntityAlreadyExistsException('Edge already exists')
        __tmp1.edges.append(__tmp2)

    def edge_exists(__tmp1, __tmp2: __typ0):
        # todo shall only compare source and dest
        duplicates = [existing_edge for existing_edge in __tmp1.edges if __tmp2 == existing_edge]
        return len(duplicates) > 0

    def find_all_nodes(__tmp1) -> List[Node]:
        return [v for k, v in __tmp1.nodes.items()]

    def find_by_id(__tmp1, id: str) -> Node:
        pass

    def find_all_edges(__tmp1) -> List[__typ0]:
        return __tmp1.edges

    def find_shortest_path(__tmp1, source: <FILL>, __tmp0: Node) :
        pass
