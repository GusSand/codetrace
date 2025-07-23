from typing import TypeAlias
__typ0 : TypeAlias = "str"
from py2neo.ogm import GraphObject, Property, RelatedTo
from typing import Any

from py2neo import Graph as NeoGraph
from injector import inject
from dataclasses import dataclass

from graphx.core.data_providers.data_provider import DataProvider


class Node(GraphObject):
    __primarykey__ = "id"

    id = Property()
    name = Property()

    edges = RelatedTo('Node')


@inject
@dataclass
class NeoNodeRepository(DataProvider[Node]):
    graph: NeoGraph

    def __tmp0(__tmp2, __tmp5: Node) :
        __tmp2.graph.merge(__tmp5)

    def __tmp6(__tmp2, __tmp3: <FILL>, __tmp4: Node, __tmp1: int) -> None:
        pass

    def find_by_id(__tmp2, id: __typ0) -> Node:
        pass

    def find_shortest_path(__tmp2, __tmp3: Node, __tmp4: Node) -> Any:
        pass
