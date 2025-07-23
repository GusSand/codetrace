from typing import TypeAlias
__typ0 : TypeAlias = "Span"
import traceback
from collections import Callable
from typing import Optional

from jaeger_client import Tracer, SpanContext, Span
from opentracing.tags import ERROR


class OpenTracingHelper:
    @staticmethod
    def __tmp4(tracer, __tmp5: SpanContext, __tmp1: str, __tmp0,
                            span_setup: 'Callable[[Span, any], None]') -> None:
        message_type = type(__tmp0).__name__
        scope = tracer.start_active_span(f'{__tmp1} {message_type}', child_of=__tmp5)
        scope.span.set_tag('proto.messagetype', message_type)

        if span_setup is not None:
            span_setup(scope.span, __tmp0)

        return scope

    @staticmethod
    def __tmp3(exception: <FILL>, span: __typ0) :
        if span is None:
            return

        span.set_tag(ERROR, True)
        span.log_kv({'exception': type(exception).__name__,
                     'message': str(exception),
                     'stackTrace': traceback.format_exception(etype=type(exception),
                                                              value=exception,
                                                              tb=exception.__traceback__)})

    @staticmethod
    def get_parent_span(tracer) :
        if tracer.active_span is not None:
            return tracer.active_span.context
        return None

    @staticmethod
    def __tmp2(span, __tmp0: any) -> None:
        pass
