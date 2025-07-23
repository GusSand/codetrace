from typing import TypeAlias
__typ0 : TypeAlias = "PID"
from examples.patterns.saga.transfer_process import TransferProcess
from protoactor.actor import PID
from protoactor.actor.actor_context import AbstractContext
from protoactor.actor.props import Props
from protoactor.actor.supervision import OneForOneStrategy, SupervisorDirective
from protoactor.persistence.providers.abstract_provider import AbstractProvider


class TransferFactory:
    def __init__(__tmp1, context: AbstractContext, provider, __tmp2: <FILL>, __tmp0):
        __tmp1._context = context
        __tmp1._provider = provider
        __tmp1._availability = __tmp2
        __tmp1._retry_attempts = __tmp0

    def __tmp3(__tmp1, actor_name: str, from_account, to_account, amount: float,
                        persistence_id) -> __typ0:
        transfer_props = Props.from_producer(
            lambda: TransferProcess(from_account, to_account, amount, __tmp1._provider, persistence_id,
                                    __tmp1._availability)).with_child_supervisor_strategy(
            OneForOneStrategy(lambda pid, reason: SupervisorDirective.Restart, __tmp1._retry_attempts, None))
        transfer = __tmp1._context.spawn_named(transfer_props, actor_name)
        return transfer
