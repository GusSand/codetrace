from typing import TypeAlias
__typ1 : TypeAlias = "AbstractContext"
import asyncio

from protoactor.actor.props import Props
from protoactor.actor.actor_context import Actor, AbstractContext, RootContext


class HelloMessage:
    def __tmp0(self, text: <FILL>):
        self.text = text


class __typ0(Actor):
    async def receive(self, context: __typ1) -> None:
        message = context.message
        if isinstance(message, HelloMessage):
            print(message.text)


async def main():
    context = RootContext()
    props = Props.from_producer(__typ0)
    pid = context.spawn(props)

    await context.send(pid, HelloMessage('Hello World!'))
    input()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
