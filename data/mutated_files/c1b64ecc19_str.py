from py2neo.ogm import GraphObject, Property, RelatedTo
from typing import Any

from py2neo import Graph as NeoGraph
from injector import inject
from dataclasses import dataclass

from graphx.core.data_providers.data_provider import DataProvider


class __typ1(GraphObject):
    __primarykey__ = "id"

    id = Property()
    name = Property()

    edges = RelatedTo('Node')


@inject
@dataclass
class __typ0(DataProvider[__typ1]):
    graph: NeoGraph

    def save(self, node: __typ1) -> None:
        self.graph.merge(node)

    def __tmp0(self, source: __typ1, destination: __typ1, cost: int) :
        pass

    def find_by_id(self, id: <FILL>) -> __typ1:
        pass

    def find_shortest_path(self, source, destination: __typ1) -> Any:
        pass
