from typing import TypeAlias
__typ2 : TypeAlias = "AbstractContext"
__typ0 : TypeAlias = "PID"
__typ5 : TypeAlias = "object"
__typ4 : TypeAlias = "AbstractRootContext"
import asyncio
from datetime import timedelta

from protoactor.actor import PID
from protoactor.actor.actor_context import AbstractRootContext, AbstractContext, RootContext
from protoactor.actor.cancel_token import CancelToken
from protoactor.actor.context_decorator import RootContextDecorator, ActorContextDecorator
from protoactor.actor.props import Props


class __typ1(RootContextDecorator):
    def __init__(__tmp0, context):
        super().__init__(context)

    async def request_future(__tmp0, target, message, timeout: timedelta = None,
                             cancellation_token: CancelToken = None) :
        print('Enter request future')
        res = await super().request_future(target, message)
        print('Exit request future')
        return res


class __typ3(ActorContextDecorator):
    def __init__(__tmp0, context, logger_name: <FILL>):
        super().__init__(context)
        __tmp0._logger_name = logger_name

    async def respond(__tmp0, message):
        print(f'{__tmp0._logger_name} : Enter respond')
        await super().respond(message)
        print(f'{__tmp0._logger_name} : Exit respond')


async def main():
    context = __typ1(RootContext())

    async def fn(context):
        message = context.message
        if isinstance(message, str):
            print(f'Inside Actor: {message}')
            await context.respond("Yo!")

    props = Props.from_func(fn).with_context_decorator([lambda c: __typ3(c, 'logger1'),
                                                        lambda c: __typ3(c, 'logger2')])
    pid = context.spawn(props)

    res = await context.request_future(pid, 'Hello')
    print(f'Got result {res}')
    input()


if __name__ == "__main__":
    asyncio.run(main())
