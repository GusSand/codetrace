from typing import TypeAlias
__typ0 : TypeAlias = "Tracer"
import traceback
from collections import Callable
from typing import Optional

from jaeger_client import Tracer, SpanContext, Span
from opentracing.tags import ERROR


class OpenTracingHelper:
    @staticmethod
    def build_started_scope(__tmp2, __tmp4, __tmp3, __tmp0: any,
                            __tmp1) :
        message_type = type(__tmp0).__name__
        scope = __tmp2.start_active_span(f'{__tmp3} {message_type}', child_of=__tmp4)
        scope.span.set_tag('proto.messagetype', message_type)

        if __tmp1 is not None:
            __tmp1(scope.span, __tmp0)

        return scope

    @staticmethod
    def setup_span(exception: Exception, span) :
        if span is None:
            return

        span.set_tag(ERROR, True)
        span.log_kv({'exception': type(exception).__name__,
                     'message': str(exception),
                     'stackTrace': traceback.format_exception(etype=type(exception),
                                                              value=exception,
                                                              tb=exception.__traceback__)})

    @staticmethod
    def get_parent_span(__tmp2: __typ0) -> Optional[SpanContext]:
        if __tmp2.active_span is not None:
            return __tmp2.active_span.context
        return None

    @staticmethod
    def default_setup_span(span: Span, __tmp0: <FILL>) :
        pass
