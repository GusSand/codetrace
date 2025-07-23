from typing import TypeAlias
__typ0 : TypeAlias = "AbstractContext"
from abc import ABCMeta, abstractmethod
from datetime import timedelta

from examples.cluster_grain_hello_world.messages.protos_pb2 import HelloRequest, HelloResponse
from protoactor.actor.actor_context import Actor, AbstractContext, RootContext, GlobalRootContext
from protoactor.actor.cancel_token import CancelToken
from protoactor.actor.messages import Started, ReceiveTimeout
from protoactor.actor.props import Props
from protoactor.remote.remote import Remote
from protoactor.remote.response import ResponseStatusCode
from protoactor.cluster.grain_call_options import GrainCallOptions
from protoactor.cluster.protos_pb2 import GrainRequest, GrainResponse, GrainErrorResponse
from protoactor.cluster.сluster import Cluster


class AbstractHelloGrain(metaclass=ABCMeta):
    @abstractmethod
    def say_hello(__tmp2, __tmp4: HelloRequest) :
        raise NotImplementedError('Should implement this method')


class HelloGrainClient():
    def __tmp5(__tmp2, __tmp7: str):
        __tmp2._grain_id = __tmp7

    
    async def say_hello(__tmp2, __tmp4: HelloRequest, ct: CancelToken = None,
                        options: GrainCallOptions = None) -> HelloResponse:
        if options is None:
            options = GrainCallOptions()

        grain_request = GrainRequest(method_index=0,
                                     message_data=__tmp4.SerializeToString())

        async def __tmp0() -> HelloResponse:
            # resolve the grain
            pid, status_code = await Cluster.get_async(__tmp2._grain_id, 'HelloGrain', ct)
            if status_code != ResponseStatusCode.OK:
                raise Exception(f'Get PID failed with StatusCode: {status_code}')

            # request the RPC method to be invoked
            grain_response = await GlobalRootContext.request_future(pid, grain_request, ct)

            # did we get a response
            if isinstance(grain_response, GrainResponse):
                return HelloResponse.ParseFromString(grain_response.message_data)

            # did we get an error response
            if isinstance(grain_response, GrainErrorResponse):
                raise Exception(grain_response.err)
            raise AttributeError()

        for i in range(options.retry_count):
            try:
                return await __tmp0()
            except Exception:
                if options.retry_action is not None:
                    await options.retry_action(i)
        return await __tmp0()
    

class HelloGrainActor(Actor):
    def __tmp5(__tmp2):
        __tmp2._inner = None

    async def __tmp6(__tmp2, context) -> None:
        message = context.message
        if isinstance(message, Started):
            __tmp2._inner = Grains._hello_grain_factory
            context.set_receive_timeout(timedelta(seconds=30))
        elif isinstance(message, ReceiveTimeout):
            await context.my_self.stop()
        elif isinstance(message, GrainRequest):
            if message.method_index == 0:
                __tmp4 = HelloRequest.ParseFromString(message.message_data)
                try:
                    response = await __tmp2._inner.say_hello(__tmp4)
                    grain_response = GrainResponse(message_data=response.SerializeToString())
                    await context.respond(grain_response)
                except Exception as ex:
                    grain_error_response = GrainErrorResponse(err=str(ex))
                    await context.respond(grain_error_response)


class Grains():
    def __tmp5(__tmp2):
        __tmp2._hello_grain_factory = None

    def __tmp3(__tmp2, __tmp1) -> None:
        __tmp2._hello_grain_factory = __tmp1
        Remote().register_known_kind('HelloGrain', Props().from_producer(lambda: HelloGrainActor()))

    def hello_grain_client(__tmp2, __tmp7: <FILL>) :
        return HelloGrainClient(__tmp7)



