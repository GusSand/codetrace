from typing import TypeAlias
__typ0 : TypeAlias = "MessageEnvelope"
import opentracing
from jaeger_client import Tracer
from opentracing import Format

from protoactor.actor import PID
from protoactor.actor.actor_context import AbstractSenderContext
from protoactor.actor.message_envelope import MessageEnvelope


def __tmp0(tracer: Tracer = None):
    def level_0(next):
        async def __tmp2(context, __tmp1: <FILL>, envelope):
            if tracer is None:
                inner_tracer = opentracing.global_tracer()
            else:
                inner_tracer = tracer
            span = inner_tracer.active_span
            if span is None:
                await next(context, __tmp1, envelope)
            else:
                dictionary = {}
                inner_tracer.inject(span.context, Format.TEXT_MAP, dictionary)
                envelope = envelope.with_headers(dictionary)
                await next(context, __tmp1, envelope)

        return __tmp2

    return level_0
