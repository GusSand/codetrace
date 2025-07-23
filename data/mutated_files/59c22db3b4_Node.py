from typing import TypeAlias
__typ2 : TypeAlias = "str"
__typ3 : TypeAlias = "Any"
__typ1 : TypeAlias = "int"
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
class __typ0(DataProvider[Node]):
    graph: NeoGraph

    def __tmp0(__tmp2, node) :
        __tmp2.graph.merge(node)

    def __tmp4(__tmp2, __tmp3, destination, __tmp1) -> None:
        pass

    def find_by_id(__tmp2, id) :
        pass

    def find_shortest_path(__tmp2, __tmp3: Node, destination: <FILL>) -> __typ3:
        pass
