from typing import TypeAlias
__typ0 : TypeAlias = "RouterState"
from threading import Event

from protoactor.actor import PID
from protoactor.actor.process import ActorProcess
from protoactor.mailbox.mailbox import AbstractMailbox
from protoactor.router.router_state import RouterState


class __typ1(ActorProcess):
    def __init__(__tmp0, state, mailbox: AbstractMailbox, wg: Event):
        super().__init__(mailbox)
        __tmp0._state = state
        __tmp0._wg = wg

    async def send_user_message(__tmp0, pid: PID, message: <FILL>, sender: PID = None):
        __tmp0._wg.clear()
        await super(__typ1, __tmp0).send_user_message(pid, message)
        __tmp0._wg.wait()