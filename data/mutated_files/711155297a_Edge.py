from typing import TypeAlias
__typ0 : TypeAlias = "Node"
__typ1 : TypeAlias = "str"
from dataclasses import dataclass, field
from typing import Any, List, Dict

from graphx.core.data_providers.data_provider import DataProvider
from graphx.core.entities import Edge, Node
from graphx.core.exceptions import EntityAlreadyExistsException

@dataclass
class __typ2(DataProvider[__typ0, Edge]):
    nodes: Dict[__typ1, __typ0] = field(default_factory=lambda: {})
    edges: List[Edge] = field(default_factory=lambda: [])

    def __tmp0(__tmp1, __tmp5: __typ0) :
        if __tmp5.id in __tmp1.nodes:
            raise EntityAlreadyExistsException('Node already exists!')
        __tmp1.nodes[__tmp5.id] = __tmp5

    def __tmp6(__tmp1, __tmp4) -> None:
        if __tmp1.edge_exists(__tmp4):
            raise EntityAlreadyExistsException('Edge already exists')
        __tmp1.edges.append(__tmp4)

    def edge_exists(__tmp1, __tmp4: <FILL>):
        # todo shall only compare source and dest
        duplicates = [existing_edge for existing_edge in __tmp1.edges if __tmp4 == existing_edge]
        return len(duplicates) > 0

    def find_all_nodes(__tmp1) -> List[__typ0]:
        return [v for k, v in __tmp1.nodes.items()]

    def __tmp3(__tmp1, id) -> __typ0:
        pass

    def __tmp2(__tmp1) -> List[Edge]:
        return __tmp1.edges

    def find_shortest_path(__tmp1, source: __typ0, destination: __typ0) :
        pass
