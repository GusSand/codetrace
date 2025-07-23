from typing import TypeAlias
__typ0 : TypeAlias = "AbstractContext"
import asyncio
import datetime
import time
from threading import Event

from examples.remote_benchmark.messages.protos_pb2 import Pong, DESCRIPTOR, StartRemote, Ping
from protoactor.actor import PID
from protoactor.actor.actor import Actor
from protoactor.actor.actor_context import AbstractContext, RootContext
from protoactor.actor.props import Props
from protoactor.remote.remote import Remote
from protoactor.remote.serialization import Serialization


class __typ1(Actor):
    def __tmp4(__tmp0, count: <FILL>, __tmp1: int, __tmp2, __tmp3):
        __tmp0._count = count
        __tmp0._message_count = __tmp1
        __tmp0._wg = __tmp2
        __tmp0._loop = __tmp3

    async def notify(__tmp0) :
        __tmp0._wg.set()

    async def receive(__tmp0, context) :
        message = context.message
        if isinstance(message, Pong):
            __tmp0._count += 1
            if __tmp0._count % 5 == 0:
                print(__tmp0._count)
            if __tmp0._count == __tmp0._message_count:
                asyncio.run_coroutine_threadsafe(__tmp0.notify(), __tmp0._loop)



async def main():
    context = RootContext()
    Serialization().register_file_descriptor(DESCRIPTOR)
    Remote().start("192.168.1.129", 12001)

    __tmp2 = asyncio.Event()
    __tmp1 = 10000

    props = Props.from_producer(lambda: __typ1(0, __tmp1, __tmp2, asyncio.get_event_loop()))

    pid = context.spawn(props)
    remote = PID(address="192.168.1.77:12000", id="remote")

    await context.request_future(remote, StartRemote(Sender=pid))

    start = datetime.datetime.now()
    print('Starting to send')
    for i in range(__tmp1):
        await context.send(remote, Ping())
    await __tmp2.wait()

    elapsed = datetime.datetime.now() - start
    print(f'Elapsed {elapsed}')

    t = __tmp1 * 2.0 / elapsed.total_seconds()
    print(f'Throughput {t} msg / sec')

    input()


if __name__ == "__main__":
    asyncio.run(main())

