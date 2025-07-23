from typing import TypeAlias
__typ1 : TypeAlias = "Span"
import traceback
from collections import Callable
from typing import Optional

from jaeger_client import Tracer, SpanContext, Span
from opentracing.tags import ERROR


class __typ0:
    @staticmethod
    def build_started_scope(__tmp0: <FILL>, parent_span: SpanContext, verb: str, message: any,
                            span_setup: 'Callable[[Span, any], None]') -> None:
        message_type = type(message).__name__
        scope = __tmp0.start_active_span(f'{verb} {message_type}', child_of=parent_span)
        scope.span.set_tag('proto.messagetype', message_type)

        if span_setup is not None:
            span_setup(scope.span, message)

        return scope

    @staticmethod
    def __tmp2(__tmp3: Exception, span: __typ1) -> None:
        if span is None:
            return

        span.set_tag(ERROR, True)
        span.log_kv({'exception': type(__tmp3).__name__,
                     'message': str(__tmp3),
                     'stackTrace': traceback.format_exception(etype=type(__tmp3),
                                                              value=__tmp3,
                                                              tb=__tmp3.__traceback__)})

    @staticmethod
    def get_parent_span(__tmp0: Tracer) -> Optional[SpanContext]:
        if __tmp0.active_span is not None:
            return __tmp0.active_span.context
        return None

    @staticmethod
    def __tmp1(span, message: any) -> None:
        pass
