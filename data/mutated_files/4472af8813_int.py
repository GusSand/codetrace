from typing import TypeAlias
__typ0 : TypeAlias = "str"
__typ1 : TypeAlias = "PID"
from examples.patterns.saga.transfer_process import TransferProcess
from protoactor.actor import PID
from protoactor.actor.actor_context import AbstractContext
from protoactor.actor.props import Props
from protoactor.actor.supervision import OneForOneStrategy, SupervisorDirective
from protoactor.persistence.providers.abstract_provider import AbstractProvider


class TransferFactory:
    def __init__(__tmp1, context, provider, availability, retry_attempts: <FILL>):
        __tmp1._context = context
        __tmp1._provider = provider
        __tmp1._availability = availability
        __tmp1._retry_attempts = retry_attempts

    def __tmp3(__tmp1, actor_name, __tmp2, to_account, __tmp0,
                        persistence_id) :
        transfer_props = Props.from_producer(
            lambda: TransferProcess(__tmp2, to_account, __tmp0, __tmp1._provider, persistence_id,
                                    __tmp1._availability)).with_child_supervisor_strategy(
            OneForOneStrategy(lambda pid, reason: SupervisorDirective.Restart, __tmp1._retry_attempts, None))
        transfer = __tmp1._context.spawn_named(transfer_props, actor_name)
        return transfer
