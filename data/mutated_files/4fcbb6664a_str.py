from typing import TypeAlias
__typ0 : TypeAlias = "Task"
__typ2 : TypeAlias = "bool"
__typ3 : TypeAlias = "Any"
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


async def gather_with_concurrency(__tmp1, __tmp9) -> __typ3:
    """
    gather tasks with the specific number concurrency
    Args:
        n_task: the number of tasks
        tasks: task objects
    """
    semaphore = asyncio.Semaphore(__tmp1)

    async def __tmp2(__tmp4) -> __typ3:
        async with semaphore:
            return await __tmp4
    return await asyncio.gather(*(__tmp2(__tmp4) for __tmp4 in __tmp9))


class __typ1:
    """Store the Message Id Container"""
    _instance: Optional[__typ1] = None

    def __init__(__tmp0) :
        __tmp0.ids: Set[str] = set()
        __tmp0.max_size: int = 100000

    def exist(__tmp0, message_id: <FILL>) :
        """exist if the message has been emitted

        Args:
            message_id (str): the identifier of message

        Returns:
            bool: if the message is the first message
        """
        if message_id in __tmp0.ids:
            return True
        __tmp0.ids.add(message_id)
        return False
    
    @classmethod
    def instance(__tmp6) :
        """singleton pattern for MessageIdContainer"""
        if __tmp6._instance is None or len(__tmp6._instance.ids) > __tmp6._instance.max_size:
            __tmp6._instance = __typ1()

        return __tmp6._instance


def __tmp8(__tmp5):    # type: ignore
    """single message decorator"""
    @functools.wraps(__tmp5)
    async def __tmp3(__tmp7: WechatyPlugin, message) :
        if not __typ1.instance().exist(message.message_id):
            await __tmp5(__tmp7, message)
    return __tmp3
