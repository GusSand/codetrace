from typing import TypeAlias
__typ0 : TypeAlias = "AbstractContext"
__typ4 : TypeAlias = "OpenTracingRootContextDecorator"
__typ3 : TypeAlias = "OpenTracingActorContextDecorator"
__typ1 : TypeAlias = "AbstractRootContext"
__typ2 : TypeAlias = "Tracer"
from typing import Callable

import opentracing
from jaeger_client import Span, Tracer

from protoactor.actor.actor_context import AbstractContext, AbstractRootContext
from protoactor.actor.props import Props
from protoactor.tracing.opentracing.open_tracing_decorator import OpenTracingRootContextDecorator, \
    OpenTracingActorContextDecorator
from protoactor.tracing.opentracing.open_tracing_helper import OpenTracingHelper
from protoactor.tracing.opentracing.open_tracing_middleware import open_tracing_sender_middleware


class __typ5:
    @staticmethod
    def get_props_with_open_tracing(props: <FILL>, send_span_setup: Callable[[Span, any], None] = None,
                                    receive_span_setup: Callable[[Span, any], None] = None,
                                    __tmp0: __typ2 = None) -> Props:
        def fn(ctx):
            return __typ5.get_context_with_open_tracing(ctx, send_span_setup, receive_span_setup)

        new_props = props.with_context_decorator([fn])
        return __typ5.get_props_with_open_tracing_sender(new_props, __tmp0)

    @staticmethod
    def get_props_with_open_tracing_sender(props, __tmp0: __typ2) -> Props:
        return props.with_sender_middleware([open_tracing_sender_middleware(__tmp0)])

    @staticmethod
    def get_context_with_open_tracing(context: __typ0, send_span_setup: Callable[[Span, any], None] = None,
                                      receive_span_setup: Callable[[Span, any], None] = None,
                                      __tmp0: __typ2 = None) :
        if send_span_setup is None:
            send_span_setup = OpenTracingHelper.default_setup_span

        if receive_span_setup is None:
            receive_span_setup = OpenTracingHelper.default_setup_span

        if __tmp0 is None:
            __tmp0 = opentracing.global_tracer()

        return __typ3(context, send_span_setup, receive_span_setup, __tmp0)

    @staticmethod
    def get_root_context_with_open_tracing(context,
                                           send_span_setup: Callable[[Span, any], None] = None,
                                           __tmp0: __typ2 = None) -> __typ4:
        if send_span_setup is None:
            send_span_setup = OpenTracingHelper.default_setup_span

        if __tmp0 is None:
            __tmp0 = opentracing.global_tracer()

        return __typ4(context, send_span_setup, __tmp0)
