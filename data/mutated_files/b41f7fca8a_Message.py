from typing import TypeAlias
__typ2 : TypeAlias = "bool"
__typ4 : TypeAlias = "Task"
__typ0 : TypeAlias = "int"
__typ3 : TypeAlias = "Any"
__typ1 : TypeAlias = "str"
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


async def __tmp1(__tmp3, tasks) -> __typ3:
    """
    gather tasks with the specific number concurrency
    Args:
        n_task: the number of tasks
        tasks: task objects
    """
    semaphore = asyncio.Semaphore(__tmp3)

    async def sem_task(__tmp4) -> __typ3:
        async with semaphore:
            return await __tmp4
    return await asyncio.gather(*(sem_task(__tmp4) for __tmp4 in tasks))


class __typ5:
    """Store the Message Id Container"""
    _instance: Optional[__typ5] = None

    def __tmp8(__tmp2) :
        __tmp2.ids: Set[__typ1] = set()
        __tmp2.max_size: __typ0 = 100000

    def exist(__tmp2, message_id) :
        """exist if the message has been emitted

        Args:
            message_id (str): the identifier of message

        Returns:
            bool: if the message is the first message
        """
        if message_id in __tmp2.ids:
            return True
        __tmp2.ids.add(message_id)
        return False
    
    @classmethod
    def instance(__tmp6) :
        """singleton pattern for MessageIdContainer"""
        if __tmp6._instance is None or len(__tmp6._instance.ids) > __tmp6._instance.max_size:
            __tmp6._instance = __typ5()

        return __tmp6._instance


def single_message(__tmp5):    # type: ignore
    """single message decorator"""
    @functools.wraps(__tmp5)
    async def wrapper(__tmp7, __tmp0: <FILL>) :
        if not __typ5.instance().exist(__tmp0.message_id):
            await __tmp5(__tmp7, __tmp0)
    return wrapper
