from typing import TypeAlias
__typ2 : TypeAlias = "int"
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
class __typ1(DataProvider[Node]):
    graph: NeoGraph

    def save(__tmp0, __tmp4) :
        __tmp0.graph.merge(__tmp4)

    def __tmp5(__tmp0, __tmp2, __tmp3, cost) :
        pass

    def __tmp1(__tmp0, id) :
        pass

    def __tmp6(__tmp0, __tmp2: <FILL>, __tmp3) :
        pass
