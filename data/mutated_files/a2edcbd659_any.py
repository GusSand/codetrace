import asyncio
import sys

import opentracing
from jaeger_client import Span, Config

from examples.chat.messages.chat_pb2 import DESCRIPTOR, Connect, SayRequest, NickRequest, Connected, SayResponse, \
    NickResponse
from protoactor.actor.actor_context import AbstractContext, GlobalRootContext, RootContext
from protoactor.actor.props import Props
from protoactor.remote.remote import Remote
from protoactor.remote.serialization import Serialization
from protoactor.tracing.opentracing.open_tracing_factory import OpenTracingFactory

from protoactor.actor.actor_context import RootContext


async def main():
    tracer = __tmp2()
    opentracing.set_global_tracer(tracer)

    context = RootContext()

    Serialization().register_file_descriptor(DESCRIPTOR)
    Remote().start("127.0.0.1", 8000)
    clients = []

    async def process_message(__tmp3: AbstractContext):
        msg = __tmp3.message
        if isinstance(msg, Connect):
            print(f'Client {msg.sender} connected')
            clients.append(msg.sender)
            await __tmp3.send(msg.sender, Connected(message='Welcome!'))
        elif isinstance(msg, SayRequest):
            for client in clients:
                await __tmp3.send(client, SayResponse(user_name=msg.user_name, message=msg.message))
        elif isinstance(msg, NickRequest):
            for client in clients:
                await __tmp3.send(client, NickResponse(old_user_name=msg.old_user_name, new_user_name=msg.new_user_name))

    props = OpenTracingFactory.get_props_with_open_tracing(Props.from_func(process_message), __tmp1, __tmp1)
    context.spawn_named(props, 'chatserver')

    input()


def __tmp2(service_name='proto.chat.server'):
    config = Config(config={'sampler': {
        'type': 'const',
        'param': 1,
    },
        'logging': True, }, service_name=service_name, validate=True)
    return config.initialize_tracer()


def __tmp1(__tmp0, message: <FILL>):
    if message is not None:
        __tmp0.log_kv({'message': str(message)})


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
