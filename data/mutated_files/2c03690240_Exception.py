from typing import TypeAlias
__typ1 : TypeAlias = "PID"
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
    def __tmp3(__tmp0, who):
        __tmp0.who = who


class Fatal:
    pass


class Recoverable:
    pass


class FatalException(Exception):
    pass


class RecoverableException(Exception):
    pass


class __typ0:
    @staticmethod
    def decide(__tmp2, __tmp1: <FILL>):
        if isinstance(__tmp1, RecoverableException):
            return SupervisorDirective.Restart
        elif isinstance(__tmp1, FatalException):
            return SupervisorDirective.Stop
        else:
            return SupervisorDirective.Escalate


class ChildActor(Actor):
    def __tmp3(__tmp0):
        __tmp0._logger = log.create_logger(logging.DEBUG, context=ChildActor)

    async def __tmp4(__tmp0, context):
        msg = context.message

        if isinstance(msg, Hello):
            __tmp0._logger.debug(f'Hello {msg.who}')
        elif isinstance(msg, Recoverable):
            raise RecoverableException()
        elif isinstance(msg, Fatal):
            raise FatalException()
        elif isinstance(msg, Started):
            __tmp0._logger.debug('Started, initialize actor here')
        elif isinstance(msg, Stopping):
            __tmp0._logger.debug('Stopping, actor is about shut down')
        elif isinstance(msg, Stopped):
            __tmp0._logger.debug("Stopped, actor and it's children are stopped")
        elif isinstance(msg, Stopping):
            __tmp0._logger.debug('Restarting, actor is about restart')


class ParentActor(Actor):
    def __tmp3(__tmp0):
        pass

    async def __tmp4(__tmp0, context):
        if context.children is None or len(context.children) == 0:
            props = Props.from_producer(lambda: ChildActor())
            child = context.spawn(props)
        else:
            child = context.children[0]

        msg = context.message
        if isinstance(msg, Hello) or \
           isinstance(msg, Recoverable) or \
           isinstance(msg, Fatal):
            await context.forward(child)
        elif isinstance(msg, Terminated):
            print(f'Watched actor was Terminated, {msg.who}')


async def main():
    context = RootContext()

    logging.basicConfig(
        format='%(name)s - %(levelname)s - %(message)s %(stack_info)s',
        level=logging.DEBUG,
        handlers = [logging.StreamHandler(sys.stdout)]
    )

    props = Props.from_producer(lambda: ParentActor()).with_child_supervisor_strategy(OneForOneStrategy(__typ0.decide,
                                                                                                        1, None))
    actor = context.spawn(props)
    await context.send(actor, Hello('Alex'))
    await context.send(actor, Recoverable())
    await context.send(actor, Fatal())

    await asyncio.sleep(1)
    await context.stop(actor)

    input()


if __name__ == "__main__":
    asyncio.run(main())
