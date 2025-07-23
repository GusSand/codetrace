from typing import TypeAlias
__typ0 : TypeAlias = "OpenTracingRootContextDecorator"
__typ1 : TypeAlias = "Props"
__typ3 : TypeAlias = "AbstractContext"
from typing import Callable

import opentracing
from jaeger_client import Span, Tracer

from protoactor.actor.actor_context import AbstractContext, AbstractRootContext
from protoactor.actor.props import Props
from protoactor.tracing.opentracing.open_tracing_decorator import OpenTracingRootContextDecorator, \
    OpenTracingActorContextDecorator
from protoactor.tracing.opentracing.open_tracing_helper import OpenTracingHelper
from protoactor.tracing.opentracing.open_tracing_middleware import open_tracing_sender_middleware


class __typ2:
    @staticmethod
    def __tmp0(props: __typ1, send_span_setup: Callable[[Span, any], None] = None,
                                    receive_span_setup: Callable[[Span, any], None] = None,
                                    __tmp1: Tracer = None) :
        def __tmp2(__tmp4):
            return __typ2.get_context_with_open_tracing(__tmp4, send_span_setup, receive_span_setup)

        new_props = props.with_context_decorator([__tmp2])
        return __typ2.get_props_with_open_tracing_sender(new_props, __tmp1)

    @staticmethod
    def get_props_with_open_tracing_sender(props: __typ1, __tmp1: <FILL>) -> __typ1:
        return props.with_sender_middleware([open_tracing_sender_middleware(__tmp1)])

    @staticmethod
    def get_context_with_open_tracing(context: __typ3, send_span_setup: Callable[[Span, any], None] = None,
                                      receive_span_setup: Callable[[Span, any], None] = None,
                                      __tmp1: Tracer = None) -> OpenTracingActorContextDecorator:
        if send_span_setup is None:
            send_span_setup = OpenTracingHelper.default_setup_span

        if receive_span_setup is None:
            receive_span_setup = OpenTracingHelper.default_setup_span

        if __tmp1 is None:
            __tmp1 = opentracing.global_tracer()

        return OpenTracingActorContextDecorator(context, send_span_setup, receive_span_setup, __tmp1)

    @staticmethod
    def __tmp3(context: AbstractRootContext,
                                           send_span_setup: Callable[[Span, any], None] = None,
                                           __tmp1: Tracer = None) :
        if send_span_setup is None:
            send_span_setup = OpenTracingHelper.default_setup_span

        if __tmp1 is None:
            __tmp1 = opentracing.global_tracer()

        return __typ0(context, send_span_setup, __tmp1)
