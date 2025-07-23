from typing import TypeAlias
__typ0 : TypeAlias = "AbstractContext"
from datetime import timedelta
from typing import Callable, Any

from examples.patterns.saga.messages import OK, Refused, InsufficientFunds, InternalServerError, ServiceUnavailable
from protoactor.actor import PID
from protoactor.actor.actor import Actor
from protoactor.actor.actor_context import AbstractContext
from protoactor.actor.messages import Started, ReceiveTimeout


class __typ1(Actor):
    def __tmp3(__tmp1,__tmp0:<FILL>, __tmp2):
        __tmp1._target = __tmp0
        __tmp1._create_message = __tmp2

    async def __tmp4(__tmp1, context) :
        msg = context.message
        if isinstance(msg, Started):
            # imagine this is some sort of remote call rather than a local actor call
            await __tmp1._target.tell(__tmp1._create_message(context.my_self))
            context.set_receive_timeout(timedelta(milliseconds=100))
        elif isinstance(msg, OK):
            context.cancel_receive_timeout()
            await context.parent.tell(msg)
        elif isinstance(msg, Refused):
            context.cancel_receive_timeout()
            await context.parent.tell(msg)
        # This emulates a failed remote call
        elif isinstance(msg, (InsufficientFunds,
                              InternalServerError,
                              ReceiveTimeout,
                              ServiceUnavailable)):
            raise Exception()