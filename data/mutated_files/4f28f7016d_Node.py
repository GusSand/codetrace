from typing import TypeAlias
__typ2 : TypeAlias = "int"
__typ1 : TypeAlias = "str"
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

    def save(__tmp1, __tmp3) -> None:
        __tmp1.graph.merge(__tmp3)

    def add_edge(__tmp1, source, __tmp0: <FILL>, cost) :
        pass

    def __tmp2(__tmp1, id) :
        pass

    def find_shortest_path(__tmp1, source: Node, __tmp0) :
        pass
