from typing import TypeAlias
__typ5 : TypeAlias = "Span"
__typ3 : TypeAlias = "Exception"
__typ2 : TypeAlias = "SpanContext"
__typ1 : TypeAlias = "str"
__typ4 : TypeAlias = "Tracer"
import traceback
from collections import Callable
from typing import Optional

from jaeger_client import Tracer, SpanContext, Span
from opentracing.tags import ERROR


class __typ0:
    @staticmethod
    def build_started_scope(__tmp2: __typ4, parent_span: __typ2, __tmp3, __tmp0: <FILL>,
                            __tmp1) :
        message_type = type(__tmp0).__name__
        scope = __tmp2.start_active_span(f'{__tmp3} {message_type}', child_of=parent_span)
        scope.span.set_tag('proto.messagetype', message_type)

        if __tmp1 is not None:
            __tmp1(scope.span, __tmp0)

        return scope

    @staticmethod
    def setup_span(__tmp4, span: __typ5) :
        if span is None:
            return

        span.set_tag(ERROR, True)
        span.log_kv({'exception': type(__tmp4).__name__,
                     'message': __typ1(__tmp4),
                     'stackTrace': traceback.format_exception(etype=type(__tmp4),
                                                              value=__tmp4,
                                                              tb=__tmp4.__traceback__)})

    @staticmethod
    def get_parent_span(__tmp2) :
        if __tmp2.active_span is not None:
            return __tmp2.active_span.context
        return None

    @staticmethod
    def default_setup_span(span: __typ5, __tmp0) :
        pass
