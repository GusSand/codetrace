from typing import TypeAlias
__typ1 : TypeAlias = "Any"
from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar, Any, List

__typ0 = TypeVar('N')
E = TypeVar('E')


class DataProvider(Generic[__typ0, E], metaclass=ABCMeta):
    @abstractmethod
    def __tmp0(__tmp1, node) -> None:
        """ ads a node to the graph
                Args:
                    node (N): The node entity
                Returns:
                    None
        """
        pass

    @abstractmethod
    def __tmp3(__tmp1) -> List[__typ0]:
        """ returns a list of nodes
                Returns:
                    List[N] list of nodes
        """
        pass

    @abstractmethod
    def __tmp5(__tmp1, edge: E) -> None:
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
    def __tmp2(__tmp1, id: <FILL>) -> __typ0:
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
    def __tmp6(__tmp1, source: __typ0, __tmp4: __typ0) -> __typ1:
        """ finds the shortest path
                Args:
                    source: Source node
                    destination: Destination node
                Returns:
                    Any should be shortest path object
        """
