from typing import TypeAlias
__typ0 : TypeAlias = "int"
from examples.patterns.saga.transfer_process import TransferProcess
from protoactor.actor import PID
from protoactor.actor.actor_context import AbstractContext
from protoactor.actor.props import Props
from protoactor.actor.supervision import OneForOneStrategy, SupervisorDirective
from protoactor.persistence.providers.abstract_provider import AbstractProvider


class TransferFactory:
    def __tmp6(__tmp1, context, provider, __tmp2: float, __tmp3: __typ0):
        __tmp1._context = context
        __tmp1._provider = provider
        __tmp1._availability = __tmp2
        __tmp1._retry_attempts = __tmp3

    def __tmp8(__tmp1, __tmp7, __tmp4: PID, __tmp5: <FILL>, amount,
                        __tmp0) :
        transfer_props = Props.from_producer(
            lambda: TransferProcess(__tmp4, __tmp5, amount, __tmp1._provider, __tmp0,
                                    __tmp1._availability)).with_child_supervisor_strategy(
            OneForOneStrategy(lambda pid, reason: SupervisorDirective.Restart, __tmp1._retry_attempts, None))
        transfer = __tmp1._context.spawn_named(transfer_props, __tmp7)
        return transfer
