from typing import TypeAlias
__typ1 : TypeAlias = "RouterState"
__typ0 : TypeAlias = "AbstractContext"
import threading
from abc import abstractmethod, ABC

from protoactor.actor import PID, ProcessRegistry
from protoactor.actor.actor_context import AbstractContext, ActorContext
from protoactor.actor.exceptions import ProcessNameExistException
from protoactor.actor.messages import Started
from protoactor.actor.props import Props
from protoactor.router.router_actor import RouterActor
from protoactor.router.router_process import RouterProcess
from protoactor.router.router_state import RouterState


class RouterConfig:
    @abstractmethod
    async def on_started(__tmp0, context: __typ0, router: __typ1) -> None:
        pass

    @abstractmethod
    def create_router_state(__tmp0) -> __typ1:
        pass

    def props(__tmp0) -> Props:
        def spawn_router_process(__tmp1, props: Props, parent: PID) -> PID:
            wg = threading.Event()
            router_state = __tmp0.create_router_state()
            p = props.with_producer(lambda: RouterActor(__tmp0, router_state, wg))

            ctx = ActorContext(p, parent)
            mailbox = props.mailbox_producer()
            dispatcher = props.dispatcher
            process = RouterProcess(router_state, mailbox, wg)
            pid, absent = ProcessRegistry().try_add(__tmp1, process)
            if not absent:
                raise ProcessNameExistException(__tmp1, pid)

            ctx.my_self = pid
            mailbox.register_handlers(ctx, dispatcher)
            mailbox.post_system_message(Started())
            mailbox.start()
            wg.wait()

            return pid

        return Props().with_spawner(spawn_router_process)


class GroupRouterConfig(RouterConfig, ABC):
    def __init__(__tmp0):
        __tmp0._routees = None

    async def on_started(__tmp0, context, router: __typ1) :
        for pid in __tmp0._routees:
            await context.watch(pid)
        router.set_routees(__tmp0._routees)


class PoolRouterConfig(RouterConfig, ABC):
    def __init__(__tmp0, pool_size: <FILL>, routee_props: Props):
        __tmp0._pool_size = pool_size
        __tmp0._routee_props = routee_props

    async def on_started(__tmp0, context: __typ0, router) -> None:
        routees = map(lambda x: context.spawn(__tmp0._routee_props), range(__tmp0._pool_size))
        router.set_routees(list(routees))
