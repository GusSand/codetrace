from typing import TypeAlias
__typ1 : TypeAlias = "AbstractProvider"
__typ0 : TypeAlias = "float"
from examples.patterns.saga.transfer_process import TransferProcess
from protoactor.actor import PID
from protoactor.actor.actor_context import AbstractContext
from protoactor.actor.props import Props
from protoactor.actor.supervision import OneForOneStrategy, SupervisorDirective
from protoactor.persistence.providers.abstract_provider import AbstractProvider


class TransferFactory:
    def __init__(__tmp0, context, provider: __typ1, __tmp1, __tmp2):
        __tmp0._context = context
        __tmp0._provider = provider
        __tmp0._availability = __tmp1
        __tmp0._retry_attempts = __tmp2

    def __tmp6(__tmp0, __tmp5: str, __tmp3: PID, __tmp4: PID, amount: __typ0,
                        persistence_id: <FILL>) -> PID:
        transfer_props = Props.from_producer(
            lambda: TransferProcess(__tmp3, __tmp4, amount, __tmp0._provider, persistence_id,
                                    __tmp0._availability)).with_child_supervisor_strategy(
            OneForOneStrategy(lambda pid, reason: SupervisorDirective.Restart, __tmp0._retry_attempts, None))
        transfer = __tmp0._context.spawn_named(transfer_props, __tmp5)
        return transfer
