from typing import TypeAlias
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
    async def on_started(self, context, router) :
        pass

    @abstractmethod
    def create_router_state(self) :
        pass

    def props(self) :
        def __tmp1(__tmp2: str, props, __tmp0: <FILL>) :
            wg = threading.Event()
            router_state = self.create_router_state()
            p = props.with_producer(lambda: RouterActor(self, router_state, wg))

            ctx = ActorContext(p, __tmp0)
            mailbox = props.mailbox_producer()
            dispatcher = props.dispatcher
            process = RouterProcess(router_state, mailbox, wg)
            pid, absent = ProcessRegistry().try_add(__tmp2, process)
            if not absent:
                raise ProcessNameExistException(__tmp2, pid)

            ctx.my_self = pid
            mailbox.register_handlers(ctx, dispatcher)
            mailbox.post_system_message(Started())
            mailbox.start()
            wg.wait()

            return pid

        return Props().with_spawner(__tmp1)


class GroupRouterConfig(RouterConfig, ABC):
    def __init__(self):
        self._routees = None

    async def on_started(self, context, router) :
        for pid in self._routees:
            await context.watch(pid)
        router.set_routees(self._routees)


class PoolRouterConfig(RouterConfig, ABC):
    def __init__(self, pool_size, routee_props):
        self._pool_size = pool_size
        self._routee_props = routee_props

    async def on_started(self, context, router) :
        routees = map(lambda x: context.spawn(self._routee_props), range(self._pool_size))
        router.set_routees(list(routees))
