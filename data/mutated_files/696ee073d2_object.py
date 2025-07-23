from typing import TypeAlias
__typ0 : TypeAlias = "AbstractRootContext"
import asyncio
from datetime import timedelta

from protoactor.actor import PID
from protoactor.actor.actor_context import AbstractRootContext, AbstractContext, RootContext
from protoactor.actor.cancel_token import CancelToken
from protoactor.actor.context_decorator import RootContextDecorator, ActorContextDecorator
from protoactor.actor.props import Props


class LoggingRootDecorator(RootContextDecorator):
    def __init__(__tmp1, context: __typ0):
        super().__init__(context)

    async def request_future(__tmp1, __tmp0: PID, message: object, timeout: timedelta = None,
                             cancellation_token: CancelToken = None) :
        print('Enter request future')
        res = await super().request_future(__tmp0, message)
        print('Exit request future')
        return res


class LoggingDecorator(ActorContextDecorator):
    def __init__(__tmp1, context: AbstractContext, __tmp2):
        super().__init__(context)
        __tmp1._logger_name = __tmp2

    async def respond(__tmp1, message: <FILL>):
        print(f'{__tmp1._logger_name} : Enter respond')
        await super().respond(message)
        print(f'{__tmp1._logger_name} : Exit respond')


async def main():
    context = LoggingRootDecorator(RootContext())

    async def fn(context: AbstractContext):
        message = context.message
        if isinstance(message, str):
            print(f'Inside Actor: {message}')
            await context.respond("Yo!")

    props = Props.from_func(fn).with_context_decorator([lambda c: LoggingDecorator(c, 'logger1'),
                                                        lambda c: LoggingDecorator(c, 'logger2')])
    pid = context.spawn(props)

    res = await context.request_future(pid, 'Hello')
    print(f'Got result {res}')
    input()


if __name__ == "__main__":
    asyncio.run(main())
