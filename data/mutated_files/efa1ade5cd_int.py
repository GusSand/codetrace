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


class LocalClient(Actor):
    def __init__(self, __tmp0, __tmp1: <FILL>, wg, loop):
        self._count = __tmp0
        self._message_count = __tmp1
        self._wg = wg
        self._loop = loop

    async def notify(self) -> None:
        self._wg.set()

    async def receive(self, context) -> None:
        message = context.message
        if isinstance(message, Pong):
            self._count += 1
            if self._count % 5 == 0:
                print(self._count)
            if self._count == self._message_count:
                asyncio.run_coroutine_threadsafe(self.notify(), self._loop)



async def main():
    context = RootContext()
    Serialization().register_file_descriptor(DESCRIPTOR)
    Remote().start("192.168.1.129", 12001)

    wg = asyncio.Event()
    __tmp1 = 10000

    props = Props.from_producer(lambda: LocalClient(0, __tmp1, wg, asyncio.get_event_loop()))

    pid = context.spawn(props)
    remote = PID(address="192.168.1.77:12000", id="remote")

    await context.request_future(remote, StartRemote(Sender=pid))

    start = datetime.datetime.now()
    print('Starting to send')
    for i in range(__tmp1):
        await context.send(remote, Ping())
    await wg.wait()

    elapsed = datetime.datetime.now() - start
    print(f'Elapsed {elapsed}')

    t = __tmp1 * 2.0 / elapsed.total_seconds()
    print(f'Throughput {t} msg / sec')

    input()


if __name__ == "__main__":
    asyncio.run(main())

