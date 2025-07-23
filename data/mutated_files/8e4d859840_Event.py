from typing import TypeAlias
__typ0 : TypeAlias = "AbstractContext"
__typ1 : TypeAlias = "int"
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


class __typ2(Actor):
    def __init__(__tmp1, count: __typ1, message_count: __typ1, __tmp2: <FILL>, loop):
        __tmp1._count = count
        __tmp1._message_count = message_count
        __tmp1._wg = __tmp2
        __tmp1._loop = loop

    async def notify(__tmp1) :
        __tmp1._wg.set()

    async def receive(__tmp1, context: __typ0) -> None:
        message = context.message
        if isinstance(message, Pong):
            __tmp1._count += 1
            if __tmp1._count % 5 == 0:
                print(__tmp1._count)
            if __tmp1._count == __tmp1._message_count:
                asyncio.run_coroutine_threadsafe(__tmp1.notify(), __tmp1._loop)



async def __tmp0():
    context = RootContext()
    Serialization().register_file_descriptor(DESCRIPTOR)
    Remote().start("192.168.1.129", 12001)

    __tmp2 = asyncio.Event()
    message_count = 10000

    props = Props.from_producer(lambda: __typ2(0, message_count, __tmp2, asyncio.get_event_loop()))

    pid = context.spawn(props)
    remote = PID(address="192.168.1.77:12000", id="remote")

    await context.request_future(remote, StartRemote(Sender=pid))

    start = datetime.datetime.now()
    print('Starting to send')
    for i in range(message_count):
        await context.send(remote, Ping())
    await __tmp2.wait()

    elapsed = datetime.datetime.now() - start
    print(f'Elapsed {elapsed}')

    t = message_count * 2.0 / elapsed.total_seconds()
    print(f'Throughput {t} msg / sec')

    input()


if __name__ == "__main__":
    asyncio.run(__tmp0())

