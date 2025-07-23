from typing import TypeAlias
__typ0 : TypeAlias = "Node"
from dataclasses import dataclass, field
from typing import Any, List, Dict

from graphx.core.data_providers.data_provider import DataProvider
from graphx.core.entities import Edge, Node
from graphx.core.exceptions import EntityAlreadyExistsException

@dataclass
class MemoryNodeRepository(DataProvider[__typ0, Edge]):
    nodes: Dict[str, __typ0] = field(default_factory=lambda: {})
    edges: List[Edge] = field(default_factory=lambda: [])

    def save(self, node) :
        if node.id in self.nodes:
            raise EntityAlreadyExistsException('Node already exists!')
        self.nodes[node.id] = node

    def add_edge(self, __tmp1: <FILL>) :
        if self.edge_exists(__tmp1):
            raise EntityAlreadyExistsException('Edge already exists')
        self.edges.append(__tmp1)

    def edge_exists(self, __tmp1):
        # todo shall only compare source and dest
        duplicates = [existing_edge for existing_edge in self.edges if __tmp1 == existing_edge]
        return len(duplicates) > 0

    def find_all_nodes(self) :
        return [v for k, v in self.nodes.items()]

    def find_by_id(self, id: str) :
        pass

    def find_all_edges(self) -> List[Edge]:
        return self.edges

    def find_shortest_path(self, source, __tmp0) :
        pass
