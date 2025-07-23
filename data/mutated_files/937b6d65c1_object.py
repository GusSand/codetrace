import asyncio

from protoactor.actor.actor_context import AbstractContext
from protoactor.actor.utils import Stack


class Behavior:
    def __init__(__tmp0, receive: asyncio.Future = None) :
        __tmp0._behaviors = Stack()
        __tmp0.become(receive)

    def become(__tmp0, receive: object):
        __tmp0._behaviors.clear()
        __tmp0._behaviors.push(receive)

    def become_stacked(__tmp0, receive: <FILL>):
        __tmp0._behaviors.push(receive)

    def unbecome_stacked(__tmp0) :
        __tmp0._behaviors.pop()

    def receive_async(__tmp0, context) :
        behavior = __tmp0._behaviors.peek()
        return behavior(context)
