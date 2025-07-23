from examples.patterns.saga.transfer_process import TransferProcess
from protoactor.actor import PID
from protoactor.actor.actor_context import AbstractContext
from protoactor.actor.props import Props
from protoactor.actor.supervision import OneForOneStrategy, SupervisorDirective
from protoactor.persistence.providers.abstract_provider import AbstractProvider


class TransferFactory:
    def __tmp1(self, context: AbstractContext, provider: AbstractProvider, __tmp0: float, retry_attempts: int):
        self._context = context
        self._provider = provider
        self._availability = __tmp0
        self._retry_attempts = retry_attempts

    def create_transfer(self, actor_name: str, __tmp2: <FILL>, __tmp3: PID, amount: float,
                        persistence_id) :
        transfer_props = Props.from_producer(
            lambda: TransferProcess(__tmp2, __tmp3, amount, self._provider, persistence_id,
                                    self._availability)).with_child_supervisor_strategy(
            OneForOneStrategy(lambda pid, reason: SupervisorDirective.Restart, self._retry_attempts, None))
        transfer = self._context.spawn_named(transfer_props, actor_name)
        return transfer
