from typing import TypeAlias
__typ2 : TypeAlias = "str"
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

    def save(__tmp0, node: __typ1) -> None:
        __tmp0.graph.merge(node)

    def add_edge(__tmp0, source: __typ1, destination, cost: <FILL>) -> None:
        pass

    def find_by_id(__tmp0, id) -> __typ1:
        pass

    def find_shortest_path(__tmp0, source: __typ1, destination: __typ1) -> Any:
        pass
