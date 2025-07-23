from typing import TypeAlias
__typ0 : TypeAlias = "AbstractContext"
__typ2 : TypeAlias = "str"
__typ3 : TypeAlias = "AbstractRootContext"
import asyncio
from datetime import timedelta

from protoactor.actor import PID
from protoactor.actor.actor_context import AbstractRootContext, AbstractContext, RootContext
from protoactor.actor.cancel_token import CancelToken
from protoactor.actor.context_decorator import RootContextDecorator, ActorContextDecorator
from protoactor.actor.props import Props


class LoggingRootDecorator(RootContextDecorator):
    def __init__(__tmp1, context: __typ3):
        super().__init__(context)

    async def request_future(__tmp1, __tmp0: PID, message: <FILL>, timeout: timedelta = None,
                             cancellation_token: CancelToken = None) -> asyncio.Future:
        print('Enter request future')
        res = await super().request_future(__tmp0, message)
        print('Exit request future')
        return res


class __typ1(ActorContextDecorator):
    def __init__(__tmp1, context, logger_name: __typ2):
        super().__init__(context)
        __tmp1._logger_name = logger_name

    async def respond(__tmp1, message):
        print(f'{__tmp1._logger_name} : Enter respond')
        await super().respond(message)
        print(f'{__tmp1._logger_name} : Exit respond')


async def main():
    context = LoggingRootDecorator(RootContext())

    async def fn(context: __typ0):
        message = context.message
        if isinstance(message, __typ2):
            print(f'Inside Actor: {message}')
            await context.respond("Yo!")

    props = Props.from_func(fn).with_context_decorator([lambda c: __typ1(c, 'logger1'),
                                                        lambda c: __typ1(c, 'logger2')])
    pid = context.spawn(props)

    res = await context.request_future(pid, 'Hello')
    print(f'Got result {res}')
    input()


if __name__ == "__main__":
    asyncio.run(main())
