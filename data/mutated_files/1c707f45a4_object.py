from typing import TypeAlias
__typ0 : TypeAlias = "AbstractContext"
import asyncio

from protoactor.actor.actor_context import AbstractContext
from protoactor.actor.utils import Stack


class Behavior:
    def __tmp2(__tmp1, receive: asyncio.Future = None) :
        __tmp1._behaviors = Stack()
        __tmp1.become(receive)

    def become(__tmp1, receive: <FILL>):
        __tmp1._behaviors.clear()
        __tmp1._behaviors.push(receive)

    def __tmp0(__tmp1, receive):
        __tmp1._behaviors.push(receive)

    def unbecome_stacked(__tmp1) :
        __tmp1._behaviors.pop()

    def receive_async(__tmp1, context) :
        behavior = __tmp1._behaviors.peek()
        return behavior(context)
