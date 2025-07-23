from typing import TypeAlias
__typ1 : TypeAlias = "Any"
__typ0 : TypeAlias = "str"
from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar, Any, List

N = TypeVar('N')
__typ3 = TypeVar('E')


class __typ2(Generic[N, __typ3], metaclass=ABCMeta):
    @abstractmethod
    def save(__tmp1, node: <FILL>) :
        """ ads a node to the graph
                Args:
                    node (N): The node entity
                Returns:
                    None
        """
        pass

    @abstractmethod
    def find_all_nodes(__tmp1) -> List[N]:
        """ returns a list of nodes
                Returns:
                    List[N] list of nodes
        """
        pass

    @abstractmethod
    def add_edge(__tmp1, __tmp2: __typ3) -> None:
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
    def find_by_id(__tmp1, id) :
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
    def find_shortest_path(__tmp1, __tmp0, destination: N) :
        """ finds the shortest path
                Args:
                    source: Source node
                    destination: Destination node
                Returns:
                    Any should be shortest path object
        """
