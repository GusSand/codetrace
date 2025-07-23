import asyncio
from random import Random, randint

from examples.persistence.messages.protos_pb2 import RenameCommand, State, RenameEvent
from protoactor.actor.actor import Actor
from protoactor.actor.actor_context import AbstractContext, RootContext
from protoactor.actor.messages import Started
from protoactor.actor.props import Props
from protoactor.persistence.messages import ReplayEvent, PersistedEvent, RecoverSnapshot, RecoverEvent, Snapshot, Event
from protoactor.persistence.persistence import Persistence
from protoactor.persistence.providers.abstract_provider import AbstractProvider
from protoactor.persistence.providers.in_memory_provider import InMemoryProvider
from protoactor.persistence.snapshot_strategies.interval_strategy import IntervalStrategy


class StartLoopActor:
    pass


class LoopParentMessage:
    pass


class LoopActor(Actor):
    def __tmp2(__tmp1):
        pass

    async def receive(__tmp1, context) -> None:
        message = context.message
        if isinstance(message, Started):
            print('LoopActor - Started')
            await context.send(context.my_self, LoopParentMessage())
        elif isinstance(message, LoopParentMessage):
            async def fn():
                await context.send(context.parent, RenameCommand(name=__tmp1.generate_pronounceable_name(5)))
                await asyncio.sleep(0.5)
                await context.send(context.my_self, LoopParentMessage())

            asyncio.create_task(fn())

    @staticmethod
    def generate_pronounceable_name(__tmp0: int) -> str:
        name = ''
        vowels = 'aeiou'
        consonants = 'bcdfghjklmnpqrstvwxyz'

        if __tmp0 % 2 != 0:
            __tmp0 += 1

        for i in range((__tmp0 // 2)):
            name = f'{name}{vowels[randint(0, len(vowels) - 1)]}{consonants[randint(0, len(consonants) - 1)]}'

        return name


class __typ0(Actor):
    def __tmp2(__tmp1, provider: AbstractProvider):
        __tmp1._state = State()
        __tmp1._loop_actor = None
        __tmp1._timer_started = False
        __tmp1._persistence = Persistence.with_event_sourcing_and_snapshotting(provider,
                                                                             provider,
                                                                             'demo-app-id',
                                                                             __tmp1.__apply_event,
                                                                             __tmp1.__apply_snapshot,
                                                                             IntervalStrategy(20),
                                                                             lambda: __tmp1._state)

    def __apply_event(__tmp1, __tmp3: <FILL>) -> None:
        if isinstance(__tmp3, RecoverEvent):
            if isinstance(__tmp3.data, RenameEvent):
                __tmp1._state.name = __tmp3.name
                print(f'MyPersistenceActor - RecoverEvent = Event.Index = {__tmp3.index}, Event.Data = {__tmp3.data}')
        elif isinstance(__tmp3, ReplayEvent):
            if isinstance(__tmp3.data, RenameEvent):
                __tmp1._state.name = __tmp3.name
                print(f'MyPersistenceActor - ReplayEvent = Event.Index = {__tmp3.index}, Event.Data = {__tmp3.data}')
        elif isinstance(__tmp3, PersistedEvent):
            print(f'MyPersistenceActor - PersistedEvent = Event.Index = {__tmp3.index}, Event.Data = {__tmp3.data}')

    def __apply_snapshot(__tmp1, snapshot) :
        if isinstance(snapshot, RecoverSnapshot):
            if isinstance(snapshot.state, State):
                __tmp1._state = snapshot.state
                print(f'MyPersistenceActor - RecoverSnapshot = Snapshot.Index = {__tmp1._persistence.index}, '
                      f'Snapshot.State = {snapshot.state.name}')

    async def receive(__tmp1, context) -> None:
        message = context.message
        if isinstance(message, Started):
            print('MyPersistenceActor - Started')
            print(f'MyPersistenceActor - Current State: {__tmp1._state}')
            await __tmp1._persistence.recover_state()
            await context.send(context.my_self, StartLoopActor())
        elif isinstance(message, StartLoopActor):
            await __tmp1.__process_start_loop_actor_message(context, message)
        elif isinstance(message, RenameCommand):
            await __tmp1.__process_rename_command_message(message)

    async def __process_start_loop_actor_message(__tmp1, context, message):
        if __tmp1._timer_started:
            return
        __tmp1._timer_started = True
        print('MyPersistenceActor - StartLoopActor')
        props = Props.from_producer(lambda: LoopActor())
        __tmp1._loop_actor = context.spawn(props)

    async def __process_rename_command_message(__tmp1, message):
        print('MyPersistenceActor - RenameCommand')
        __tmp1._state.Name = message.name
        await __tmp1._persistence.persist_event(RenameEvent(name=message.name))


async def main():
    context = RootContext()
    provider = InMemoryProvider()

    props = Props.from_producer(lambda: __typ0(provider))
    pid = context.spawn(props)

    input()


if __name__ == "__main__":
    asyncio.run(main())
