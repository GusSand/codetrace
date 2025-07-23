from typing import TypeAlias
__typ0 : TypeAlias = "any"
__typ1 : TypeAlias = "Tracer"
import traceback
from collections import Callable
from typing import Optional

from jaeger_client import Tracer, SpanContext, Span
from opentracing.tags import ERROR


class __typ2:
    @staticmethod
    def __tmp2(__tmp0: __typ1, parent_span: SpanContext, __tmp1, __tmp3: __typ0,
                            span_setup: 'Callable[[Span, any], None]') -> None:
        message_type = type(__tmp3).__name__
        scope = __tmp0.start_active_span(f'{__tmp1} {message_type}', child_of=parent_span)
        scope.span.set_tag('proto.messagetype', message_type)

        if span_setup is not None:
            span_setup(scope.span, __tmp3)

        return scope

    @staticmethod
    def setup_span(exception: Exception, span: Span) -> None:
        if span is None:
            return

        span.set_tag(ERROR, True)
        span.log_kv({'exception': type(exception).__name__,
                     'message': str(exception),
                     'stackTrace': traceback.format_exception(etype=type(exception),
                                                              value=exception,
                                                              tb=exception.__traceback__)})

    @staticmethod
    def get_parent_span(__tmp0: __typ1) -> Optional[SpanContext]:
        if __tmp0.active_span is not None:
            return __tmp0.active_span.context
        return None

    @staticmethod
    def default_setup_span(span: <FILL>, __tmp3: __typ0) -> None:
        pass
