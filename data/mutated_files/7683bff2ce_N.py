from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar, Any, List

N = TypeVar('N')
__typ1 = TypeVar('E')


class __typ0(Generic[N, __typ1], metaclass=ABCMeta):
    @abstractmethod
    def save(__tmp0, __tmp6) :
        """ ads a node to the graph
                Args:
                    node (N): The node entity
                Returns:
                    None
        """
        pass

    @abstractmethod
    def __tmp2(__tmp0) :
        """ returns a list of nodes
                Returns:
                    List[N] list of nodes
        """
        pass

    @abstractmethod
    def __tmp7(__tmp0, __tmp5) -> None:
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
    def __tmp1(__tmp0, id) -> N:
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
    def find_shortest_path(__tmp0, __tmp3, __tmp4: <FILL>) :
        """ finds the shortest path
                Args:
                    source: Source node
                    destination: Destination node
                Returns:
                    Any should be shortest path object
        """
