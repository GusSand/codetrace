from typing import TypeAlias
__typ0 : TypeAlias = "Message"
__typ2 : TypeAlias = "Any"
__typ3 : TypeAlias = "Task"
__typ1 : TypeAlias = "bool"
"""
async helpers
"""
from __future__ import annotations
import asyncio
from asyncio import Task
from typing import (
    List,
    Any,
    Optional,
    Set,
    TYPE_CHECKING
)
import functools

if TYPE_CHECKING:
    from wechaty import Message, WechatyPlugin


async def gather_with_concurrency(__tmp2: <FILL>, __tmp11: List[__typ3]) -> __typ2:
    """
    gather tasks with the specific number concurrency
    Args:
        n_task: the number of tasks
        tasks: task objects
    """
    semaphore = asyncio.Semaphore(__tmp2)

    async def __tmp3(__tmp5: __typ3) -> __typ2:
        async with semaphore:
            return await __tmp5
    return await asyncio.gather(*(__tmp3(__tmp5) for __tmp5 in __tmp11))


class __typ4:
    """Store the Message Id Container"""
    _instance: Optional[__typ4] = None

    def __tmp9(__tmp1) -> None:
        __tmp1.ids: Set[str] = set()
        __tmp1.max_size: int = 100000

    def exist(__tmp1, message_id: str) -> __typ1:
        """exist if the message has been emitted

        Args:
            message_id (str): the identifier of message

        Returns:
            bool: if the message is the first message
        """
        if message_id in __tmp1.ids:
            return True
        __tmp1.ids.add(message_id)
        return False
    
    @classmethod
    def instance(__tmp7) -> __typ4:
        """singleton pattern for MessageIdContainer"""
        if __tmp7._instance is None or len(__tmp7._instance.ids) > __tmp7._instance.max_size:
            __tmp7._instance = __typ4()

        return __tmp7._instance


def __tmp10(__tmp6):    # type: ignore
    """single message decorator"""
    @functools.wraps(__tmp6)
    async def __tmp4(__tmp8, __tmp0: __typ0) -> None:
        if not __typ4.instance().exist(__tmp0.message_id):
            await __tmp6(__tmp8, __tmp0)
    return __tmp4
