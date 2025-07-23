from typing import TypeAlias
__typ0 : TypeAlias = "AbstractContext"
from threading import Event

from protoactor.actor.actor import Actor
from protoactor.actor.actor_context import AbstractContext
from protoactor.actor.messages import Started
from protoactor.actor.protos_pb2 import Terminated
from protoactor.router.messages import AddRoutee, RemoveRoutee, BroadcastMessage, GetRoutees, Routees, \
    RouterManagementMessage
from protoactor.router.router_state import RouterState

is_import = False
if is_import:
    from protoactor.router.router_config import RouterConfig


class __typ1(Actor):
    def __init__(__tmp0, config, router_state: RouterState, wg: <FILL>):
        __tmp0._config = config
        __tmp0._router_state = router_state
        __tmp0._wg = wg

    async def receive(__tmp0, context) :
        msg = context.message
        if isinstance(msg, Started):
            await __tmp0.process_started_message(context)
        elif isinstance(msg, Terminated):
            await __tmp0.process_terminated_message(context)
        elif isinstance(msg, RouterManagementMessage):
            await __tmp0.process_router_management_message(context)
        else:
            await __tmp0.process_message(context)

    async def process_started_message(__tmp0, context):
        await __tmp0._config.on_started(context, __tmp0._router_state)
        __tmp0._wg.set()

    async def process_terminated_message(__tmp0, context):
        pass

    async def process_router_management_message(__tmp0, context):
        msg = context.message
        if isinstance(msg, AddRoutee):
            routees = __tmp0._router_state.get_routees()
            if msg.pid not in routees:
                await context.watch(msg.pid)
                routees.append(msg.pid)
                __tmp0._router_state.set_routees(routees)
            __tmp0._wg.set()
        elif isinstance(msg, RemoveRoutee):
            routees = __tmp0._router_state.get_routees()
            if msg.pid in routees:
                await context.unwatch(msg.pid)
                routees.remove(msg.pid)
                __tmp0._router_state.set_routees(routees)
            __tmp0._wg.set()
        elif isinstance(msg, BroadcastMessage):
            for routee in __tmp0._router_state.get_routees():
                await context.request(routee, msg.message)
            __tmp0._wg.set()
        elif isinstance(msg, GetRoutees):
            __tmp0._wg.set()
            routees = __tmp0._router_state.get_routees()
            await context.respond(Routees(routees))

    async def process_message(__tmp0, context):
        await __tmp0._router_state.route_message(context.message)
        __tmp0._wg.set()
