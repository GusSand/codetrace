from typing import TypeAlias
__typ0 : TypeAlias = "Any"
from dataclasses import dataclass, field
from typing import Any, List, Dict

from graphx.core.data_providers.data_provider import DataProvider
from graphx.core.entities import Edge, Node
from graphx.core.exceptions import EntityAlreadyExistsException

@dataclass
class __typ1(DataProvider[Node, Edge]):
    nodes: Dict[str, Node] = field(default_factory=lambda: {})
    edges: List[Edge] = field(default_factory=lambda: [])

    def save(__tmp0, __tmp4: <FILL>) -> None:
        if __tmp4.id in __tmp0.nodes:
            raise EntityAlreadyExistsException('Node already exists!')
        __tmp0.nodes[__tmp4.id] = __tmp4

    def __tmp5(__tmp0, __tmp3) :
        if __tmp0.edge_exists(__tmp3):
            raise EntityAlreadyExistsException('Edge already exists')
        __tmp0.edges.append(__tmp3)

    def edge_exists(__tmp0, __tmp3):
        # todo shall only compare source and dest
        duplicates = [existing_edge for existing_edge in __tmp0.edges if __tmp3 == existing_edge]
        return len(duplicates) > 0

    def find_all_nodes(__tmp0) -> List[Node]:
        return [v for k, v in __tmp0.nodes.items()]

    def find_by_id(__tmp0, id: str) -> Node:
        pass

    def find_all_edges(__tmp0) :
        return __tmp0.edges

    def find_shortest_path(__tmp0, __tmp1, __tmp2) :
        pass
