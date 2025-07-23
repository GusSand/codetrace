import asyncio

from protoactor.actor.actor_context import Actor, AbstractContext, RootContext
from protoactor.actor.props import Props
from protoactor.router.messages import AbstractHashable
from protoactor.router.router import Router

my_actor_props = Props.from_producer(lambda: MyTestActor())


class Message(AbstractHashable):
    def __tmp8(__tmp1, text: <FILL>):
        __tmp1.text = text

    def __tmp4(__tmp1) -> str:
        return __tmp1.text

    def __tmp12(__tmp1):
        return __tmp1.text


class MyTestActor(Actor):
    def __tmp8(__tmp1):
        __tmp1._received_messages = []

    async def __tmp10(__tmp1, context: AbstractContext) :
        msg = context.message
        if isinstance(msg, Message):
            print('actor %s got message %s' % (str(context.my_self.id), msg.text))


async def __tmp13():
    context = RootContext()
    props = Router.new_broadcast_pool(my_actor_props, 5)

    for i in range(10):
        pid = context.spawn(props)
        await context.send(pid, Message('%s' % (i % 4)))


async def __tmp11():
    context = RootContext()
    props = Router.new_broadcast_group([context.spawn(my_actor_props),
                                        context.spawn(my_actor_props),
                                        context.spawn(my_actor_props),
                                        context.spawn(my_actor_props)])

    for i in range(10):
        pid = context.spawn(props)
        await context.send(pid, Message('%s' % (i % 4)))


async def __tmp9():
    context = RootContext()
    props = Router.new_random_pool(my_actor_props, 5)
    pid = context.spawn(props)

    for i in range(10):
        await context.send(pid, Message('%s' % (i % 4)))


async def __tmp6():
    context = RootContext()
    props = Router.new_random_group([context.spawn(my_actor_props),
                                     context.spawn(my_actor_props),
                                     context.spawn(my_actor_props),
                                     context.spawn(my_actor_props)])

    pid = context.spawn(props)
    for i in range(10):
        await context.send(pid, Message('%s' % (i % 4)))


async def __tmp0():
    context = RootContext()
    props = Router.new_round_robin_pool(my_actor_props, 5)
    pid = context.spawn(props)

    for i in range(10):
        await context.send(pid, Message('%s' % (i % 4)))


async def __tmp3():
    context = RootContext()
    props = Router.new_round_robin_group([context.spawn(my_actor_props),
                                          context.spawn(my_actor_props),
                                          context.spawn(my_actor_props),
                                          context.spawn(my_actor_props)])

    pid = context.spawn(props)
    for i in range(10):
        await context.send(pid, Message('%s' % (i % 4)))


async def __tmp5():
    context = RootContext()
    props = Router.new_consistent_hash_pool(my_actor_props, 5)
    pid = context.spawn(props)

    for i in range(10):
        await context.send(pid, Message('%s' % (i % 4)))


async def __tmp7():
    context = RootContext()
    props = Router.new_consistent_hash_group([context.spawn(my_actor_props),
                                              context.spawn(my_actor_props),
                                              context.spawn(my_actor_props),
                                              context.spawn(my_actor_props)])

    pid = context.spawn(props)
    for i in range(10):
        await context.send(pid, Message('%s' % (i % 4)))


async def __tmp2():
    await __tmp13()
    # await run_broadcast_group_test()

    #await run_random_pool_test()
    # await run_random_group_test()

    # await run_round_robin_pool_test()
    # await run_round_robin_group_test()

    # await run_consistent_hash_pool_test()
    # await run_consistent_hash_group_test()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(__tmp2())
