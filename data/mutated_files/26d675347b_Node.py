from dataclasses import dataclass

from injector import inject

from graphx.core.data_providers.memory import Node, MemoryNodeRepository


@inject
@dataclass
class __typ0:
    repository: MemoryNodeRepository

    def __tmp0(__tmp1, __tmp2: <FILL>):
        __tmp1.repository.save(__tmp2)
