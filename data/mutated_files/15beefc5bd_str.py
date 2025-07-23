from typing import TypeAlias
__typ5 : TypeAlias = "Span"
__typ3 : TypeAlias = "Exception"
__typ0 : TypeAlias = "any"
__typ2 : TypeAlias = "SpanContext"
__typ4 : TypeAlias = "Tracer"
import traceback
from collections import Callable
from typing import Optional

from jaeger_client import Tracer, SpanContext, Span
from opentracing.tags import ERROR


class __typ1:
    @staticmethod
    def build_started_scope(tracer: __typ4, parent_span: __typ2, __tmp2: <FILL>, __tmp0,
                            __tmp1) :
        message_type = type(__tmp0).__name__
        scope = tracer.start_active_span(f'{__tmp2} {message_type}', child_of=parent_span)
        scope.span.set_tag('proto.messagetype', message_type)

        if __tmp1 is not None:
            __tmp1(scope.span, __tmp0)

        return scope

    @staticmethod
    def __tmp4(exception: __typ3, span: __typ5) :
        if span is None:
            return

        span.set_tag(ERROR, True)
        span.log_kv({'exception': type(exception).__name__,
                     'message': str(exception),
                     'stackTrace': traceback.format_exception(etype=type(exception),
                                                              value=exception,
                                                              tb=exception.__traceback__)})

    @staticmethod
    def __tmp3(tracer: __typ4) :
        if tracer.active_span is not None:
            return tracer.active_span.context
        return None

    @staticmethod
    def default_setup_span(span, __tmp0: __typ0) :
        pass
