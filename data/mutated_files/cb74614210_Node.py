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

    def __tmp0(__tmp1, node: <FILL>) :
        __tmp1.graph.merge(node)

    def __tmp3(__tmp1, source, destination, cost) :
        pass

    def __tmp2(__tmp1, id) :
        pass

    def __tmp4(__tmp1, source, destination) -> Any:
        pass
