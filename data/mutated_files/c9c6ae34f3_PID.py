from typing import TypeAlias
__typ4 : TypeAlias = "str"
__typ3 : TypeAlias = "AbstractContext"
import asyncio
import logging
import sys
import traceback

from protoactor.actor import PID, log
from protoactor.actor.actor import Actor
from protoactor.actor.actor_context import AbstractContext, RootContext
from protoactor.actor.messages import Started, Stopping, Stopped
from protoactor.actor.props import Props
from protoactor.actor.protos_pb2 import Terminated
from protoactor.actor.supervision import SupervisorDirective, OneForOneStrategy


class Hello:
    def __tmp4(__tmp1, who):
        __tmp1.who = who


class __typ6:
    pass


class __typ2:
    pass


class FatalException(Exception):
    pass


class __typ5(Exception):
    pass


class __typ1:
    @staticmethod
    def decide(__tmp3: <FILL>, __tmp2):
        if isinstance(__tmp2, __typ5):
            return SupervisorDirective.Restart
        elif isinstance(__tmp2, FatalException):
            return SupervisorDirective.Stop
        else:
            return SupervisorDirective.Escalate


class ChildActor(Actor):
    def __tmp4(__tmp1):
        __tmp1._logger = log.create_logger(logging.DEBUG, context=ChildActor)

    async def __tmp5(__tmp1, context):
        msg = context.message

        if isinstance(msg, Hello):
            __tmp1._logger.debug(f'Hello {msg.who}')
        elif isinstance(msg, __typ2):
            raise __typ5()
        elif isinstance(msg, __typ6):
            raise FatalException()
        elif isinstance(msg, Started):
            __tmp1._logger.debug('Started, initialize actor here')
        elif isinstance(msg, Stopping):
            __tmp1._logger.debug('Stopping, actor is about shut down')
        elif isinstance(msg, Stopped):
            __tmp1._logger.debug("Stopped, actor and it's children are stopped")
        elif isinstance(msg, Stopping):
            __tmp1._logger.debug('Restarting, actor is about restart')


class __typ0(Actor):
    def __tmp4(__tmp1):
        pass

    async def __tmp5(__tmp1, context):
        if context.children is None or len(context.children) == 0:
            props = Props.from_producer(lambda: ChildActor())
            child = context.spawn(props)
        else:
            child = context.children[0]

        msg = context.message
        if isinstance(msg, Hello) or \
           isinstance(msg, __typ2) or \
           isinstance(msg, __typ6):
            await context.forward(child)
        elif isinstance(msg, Terminated):
            print(f'Watched actor was Terminated, {msg.who}')


async def __tmp0():
    context = RootContext()

    logging.basicConfig(
        format='%(name)s - %(levelname)s - %(message)s %(stack_info)s',
        level=logging.DEBUG,
        handlers = [logging.StreamHandler(sys.stdout)]
    )

    props = Props.from_producer(lambda: __typ0()).with_child_supervisor_strategy(OneForOneStrategy(__typ1.decide,
                                                                                                        1, None))
    actor = context.spawn(props)
    await context.send(actor, Hello('Alex'))
    await context.send(actor, __typ2())
    await context.send(actor, __typ6())

    await asyncio.sleep(1)
    await context.stop(actor)

    input()


if __name__ == "__main__":
    asyncio.run(__tmp0())
