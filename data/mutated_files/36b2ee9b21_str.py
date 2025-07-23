import asyncio

from protoactor.actor.props import Props
from protoactor.actor.actor_context import RootContext


class __typ0:
    def __init__(__tmp0, text: <FILL>):
        __tmp0.text = text


async def hello_function(context):
    message = context.message
    if isinstance(message, __typ0):
        await context.respond("hey")


async def main():
    context = RootContext()
    props = Props.from_func(hello_function)
    pid = context.spawn(props)

    reply = await context.request_future(pid, __typ0('Hello'))
    print(reply)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
