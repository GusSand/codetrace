from typing import TypeAlias
__typ7 : TypeAlias = "Exception"
__typ5 : TypeAlias = "AbstractContext"
__typ2 : TypeAlias = "PID"
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


class __typ8:
    def __tmp1(__tmp0, who: <FILL>):
        __tmp0.who = who


class __typ9:
    pass


class __typ1:
    pass


class __typ4(__typ7):
    pass


class __typ6(__typ7):
    pass


class Decider:
    @staticmethod
    def decide(pid, reason: __typ7):
        if isinstance(reason, __typ6):
            return SupervisorDirective.Restart
        elif isinstance(reason, __typ4):
            return SupervisorDirective.Stop
        else:
            return SupervisorDirective.Escalate


class __typ3(Actor):
    def __tmp1(__tmp0):
        __tmp0._logger = log.create_logger(logging.DEBUG, context=__typ3)

    async def __tmp2(__tmp0, context: __typ5):
        msg = context.message

        if isinstance(msg, __typ8):
            __tmp0._logger.debug(f'Hello {msg.who}')
        elif isinstance(msg, __typ1):
            raise __typ6()
        elif isinstance(msg, __typ9):
            raise __typ4()
        elif isinstance(msg, Started):
            __tmp0._logger.debug('Started, initialize actor here')
        elif isinstance(msg, Stopping):
            __tmp0._logger.debug('Stopping, actor is about shut down')
        elif isinstance(msg, Stopped):
            __tmp0._logger.debug("Stopped, actor and it's children are stopped")
        elif isinstance(msg, Stopping):
            __tmp0._logger.debug('Restarting, actor is about restart')


class __typ0(Actor):
    def __tmp1(__tmp0):
        pass

    async def __tmp2(__tmp0, context):
        if context.children is None or len(context.children) == 0:
            props = Props.from_producer(lambda: __typ3())
            child = context.spawn(props)
        else:
            child = context.children[0]

        msg = context.message
        if isinstance(msg, __typ8) or \
           isinstance(msg, __typ1) or \
           isinstance(msg, __typ9):
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

    props = Props.from_producer(lambda: __typ0()).with_child_supervisor_strategy(OneForOneStrategy(Decider.decide,
                                                                                                        1, None))
    actor = context.spawn(props)
    await context.send(actor, __typ8('Alex'))
    await context.send(actor, __typ1())
    await context.send(actor, __typ9())

    await asyncio.sleep(1)
    await context.stop(actor)

    input()


if __name__ == "__main__":
    asyncio.run(main())
