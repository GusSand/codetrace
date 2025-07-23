from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar, Any, List

__typ1 = TypeVar('N')
E = TypeVar('E')


class __typ0(Generic[__typ1, E], metaclass=ABCMeta):
    @abstractmethod
    def save(self, node) :
        """ ads a node to the graph
                Args:
                    node (N): The node entity
                Returns:
                    None
        """
        pass

    @abstractmethod
    def find_all_nodes(self) :
        """ returns a list of nodes
                Returns:
                    List[N] list of nodes
        """
        pass

    @abstractmethod
    def add_edge(self, edge: <FILL>) :
        """ ads an edge
                Args:
                    source: source node
                    destination: destination node
                    cost: cost of distance
                Returns:
                    None
                """
        pass

    @abstractmethod
    def find_by_id(self, id) :
        """ finds a node by id
                Args:
                    id: Node id
                Returns:
                    N
                Raises:
                    EntityNotFoundException
        """
        pass

    @abstractmethod
    def find_shortest_path(self, source, destination) :
        """ finds the shortest path
                Args:
                    source: Source node
                    destination: Destination node
                Returns:
                    Any should be shortest path object
        """
