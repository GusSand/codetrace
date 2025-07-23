from typing import TypeAlias
__typ1 : TypeAlias = "Node"
__typ0 : TypeAlias = "Edge"
__typ2 : TypeAlias = "Any"
from dataclasses import dataclass, field
from typing import Any, List, Dict

from graphx.core.data_providers.data_provider import DataProvider
from graphx.core.entities import Edge, Node
from graphx.core.exceptions import EntityAlreadyExistsException

@dataclass
class __typ3(DataProvider[__typ1, __typ0]):
    nodes: Dict[str, __typ1] = field(default_factory=lambda: {})
    edges: List[__typ0] = field(default_factory=lambda: [])

    def __tmp0(__tmp1, __tmp8) -> None:
        if __tmp8.id in __tmp1.nodes:
            raise EntityAlreadyExistsException('Node already exists!')
        __tmp1.nodes[__tmp8.id] = __tmp8

    def __tmp9(__tmp1, __tmp7) :
        if __tmp1.edge_exists(__tmp7):
            raise EntityAlreadyExistsException('Edge already exists')
        __tmp1.edges.append(__tmp7)

    def edge_exists(__tmp1, __tmp7: __typ0):
        # todo shall only compare source and dest
        duplicates = [existing_edge for existing_edge in __tmp1.edges if __tmp7 == existing_edge]
        return len(duplicates) > 0

    def __tmp4(__tmp1) -> List[__typ1]:
        return [v for k, v in __tmp1.nodes.items()]

    def __tmp3(__tmp1, id: <FILL>) -> __typ1:
        pass

    def __tmp2(__tmp1) -> List[__typ0]:
        return __tmp1.edges

    def __tmp10(__tmp1, __tmp5: __typ1, __tmp6: __typ1) -> __typ2:
        pass
