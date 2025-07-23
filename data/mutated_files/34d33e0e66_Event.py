from threading import Event

from protoactor.actor import PID
from protoactor.actor.process import ActorProcess
from protoactor.mailbox.mailbox import AbstractMailbox
from protoactor.router.router_state import RouterState


class RouterProcess(ActorProcess):
    def __init__(self, state: RouterState, mailbox: AbstractMailbox, wg: <FILL>):
        super().__init__(mailbox)
        self._state = state
        self._wg = wg

    async def send_user_message(self, __tmp0: PID, message, sender: PID = None):
        self._wg.clear()
        await super(RouterProcess, self).send_user_message(__tmp0, message)
        self._wg.wait()