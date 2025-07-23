from typing import TypeAlias
__typ1 : TypeAlias = "Any"
from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar, Any, List

N = TypeVar('N')
E = TypeVar('E')


class __typ0(Generic[N, E], metaclass=ABCMeta):
    @abstractmethod
    def __tmp0(__tmp1, __tmp6: N) :
        """ ads a node to the graph
                Args:
                    node (N): The node entity
                Returns:
                    None
        """
        pass

    @abstractmethod
    def __tmp3(__tmp1) -> List[N]:
        """ returns a list of nodes
                Returns:
                    List[N] list of nodes
        """
        pass

    @abstractmethod
    def __tmp7(__tmp1, __tmp5) :
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
    def __tmp2(__tmp1, id) :
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
    def __tmp8(__tmp1, source: <FILL>, __tmp4) :
        """ finds the shortest path
                Args:
                    source: Source node
                    destination: Destination node
                Returns:
                    Any should be shortest path object
        """
