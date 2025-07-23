from typing import TypeAlias
__typ3 : TypeAlias = "float"
__typ2 : TypeAlias = "AbstractProvider"
__typ1 : TypeAlias = "PID"
__typ0 : TypeAlias = "int"
from examples.patterns.saga.transfer_process import TransferProcess
from protoactor.actor import PID
from protoactor.actor.actor_context import AbstractContext
from protoactor.actor.props import Props
from protoactor.actor.supervision import OneForOneStrategy, SupervisorDirective
from protoactor.persistence.providers.abstract_provider import AbstractProvider


class __typ4:
    def __init__(self, context: AbstractContext, provider, availability, retry_attempts: __typ0):
        self._context = context
        self._provider = provider
        self._availability = availability
        self._retry_attempts = retry_attempts

    def create_transfer(self, actor_name: <FILL>, from_account: __typ1, __tmp0, amount: __typ3,
                        persistence_id: str) :
        transfer_props = Props.from_producer(
            lambda: TransferProcess(from_account, __tmp0, amount, self._provider, persistence_id,
                                    self._availability)).with_child_supervisor_strategy(
            OneForOneStrategy(lambda pid, reason: SupervisorDirective.Restart, self._retry_attempts, None))
        transfer = self._context.spawn_named(transfer_props, actor_name)
        return transfer
