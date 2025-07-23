import asyncio
from datetime import timedelta
from typing import Optional

from protoactor.actor.actor import Actor
from protoactor.actor.actor_context import AbstractContext, RootContext
from protoactor.actor.cancel_token import CancelToken
from protoactor.actor.messages import Started
from protoactor.actor.props import Props
from protoactor.schedulers.simple_scheduler import SimpleScheduler


class Hello:
    pass


class HickUp:
    pass


class AbortHickUp:
    pass


class Greet:
    def __tmp2(__tmp1, who: <FILL>):
        __tmp1._who = who

    def who(__tmp1) :
        return __tmp1._who


class SimpleMessage:
    def __tmp2(__tmp1, msg):
        __tmp1._msg = msg

    def msg(__tmp1) :
        return __tmp1._msg


class ScheduleGreetActor(Actor):
    def __tmp2(__tmp1):
        pass

    async def __tmp3(__tmp1, context: AbstractContext):
        msg = context.message
        if isinstance(msg, Greet):
            print(f"Hi {msg.who()}")
            await context.respond(Greet('Roger'))


class ScheduleActor(Actor):
    def __tmp2(__tmp1):
        __tmp1._scheduler: SimpleScheduler = SimpleScheduler()
        __tmp1._timer: CancelToken = CancelToken('')
        __tmp1._counter: int = 0

    async def __tmp3(__tmp1, context):
        msg = context.message
        if isinstance(msg, Started):
            pid = context.spawn(Props.from_producer(ScheduleGreetActor))
            await __tmp1._scheduler.schedule_tell_once(timedelta(milliseconds=100), context.my_self,
                                                     SimpleMessage('test 1'))
            await __tmp1._scheduler.schedule_tell_once(timedelta(milliseconds=200), context.my_self,
                                                     SimpleMessage('test 2'))
            await __tmp1._scheduler.schedule_tell_once(timedelta(milliseconds=300), context.my_self,
                                                     SimpleMessage('test 3'))
            await __tmp1._scheduler.schedule_tell_once(timedelta(milliseconds=400), context.my_self,
                                                     SimpleMessage('test 4'))
            await __tmp1._scheduler.schedule_tell_once(timedelta(milliseconds=500), context.my_self,
                                                     SimpleMessage('test 5'))
            await __tmp1._scheduler.schedule_request_once(timedelta(seconds=1), context.my_self, pid,
                                                     Greet('Daniel'))
            await __tmp1._scheduler.schedule_tell_once(timedelta(seconds=5), context.my_self,
                                                     Hello())
        elif isinstance(msg, Hello):
            print("Hello Once, let's give you a hickup every 0.5 second starting in 3 seconds!")
            await __tmp1._scheduler.schedule_tell_repeatedly(timedelta(seconds=3), timedelta(milliseconds=500),
                                                           context.my_self, HickUp(), __tmp1._timer)
        elif isinstance(msg, HickUp):
            __tmp1._counter += 1
            print('Hello!')
            if __tmp1._counter == 5:
                __tmp1._timer.trigger()
                await context.send(context.my_self, AbortHickUp())
        elif isinstance(msg, AbortHickUp):
            print(f'Aborted hickup after {__tmp1._counter} times')
            print('All this was scheduled calls, have fun!')
        elif isinstance(msg, Greet):
            print(f'Thanks {msg.who()}')
        elif isinstance(msg, SimpleMessage):
            print(msg.msg())


async def __tmp0():
    context = RootContext()
    props = Props.from_producer(ScheduleActor)
    pid = context.spawn(props)

    input()

if __name__ == "__main__":
    asyncio.run(__tmp0())
