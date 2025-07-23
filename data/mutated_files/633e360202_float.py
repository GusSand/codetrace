from typing import TypeAlias
__typ1 : TypeAlias = "PID"
__typ0 : TypeAlias = "int"
import asyncio

from examples.patterns.saga.account import Account
from examples.patterns.saga.factories.transfer_factory import TransferFactory
from examples.patterns.saga.in_memory_provider import InMemoryProvider
from examples.patterns.saga.internal.for_with_progress import ForWithProgress
from examples.patterns.saga.messages import SuccessResult, UnknownResult, FailedAndInconsistent, \
    FailedButConsistentResult
from protoactor.actor import PID
from protoactor.actor.actor import Actor
from protoactor.actor.actor_context import RootContext, AbstractContext
from protoactor.actor.messages import Started
from protoactor.actor.props import Props


class Runner(Actor):
    def __init__(__tmp0, number_of_iterations: __typ0, interval_between_console_updates, uptime: float,
                 refusal_probability: float, busy_probability: <FILL>, retry_attempts, verbose: bool):
        __tmp0._context = RootContext()
        __tmp0._number_of_iterations = number_of_iterations
        __tmp0._interval_between_console_updates = interval_between_console_updates
        __tmp0._uptime = uptime
        __tmp0._refusal_probability = refusal_probability
        __tmp0._busy_probability = busy_probability
        __tmp0._retry_attempts = retry_attempts
        __tmp0._verbose = verbose

        __tmp0._transfers = []
        __tmp0._success_results = 0
        __tmp0._failed_and_inconsistent_results = 0
        __tmp0._failed_but_consistent_results = 0
        __tmp0._unknown_results = 0
        __tmp0._in_memory_provider = None

    def __create_account(__tmp0, name) -> __typ1:
        account_props = Props.from_producer(lambda: Account(name,
                                                            __tmp0._uptime,
                                                            __tmp0._refusal_probability,
                                                            __tmp0._busy_probability))
        return __tmp0._context.spawn_named(account_props, name)

    async def receive(__tmp0, context: AbstractContext) :
        msg = context.message
        if isinstance(msg, SuccessResult):
            __tmp0._success_results += 1
            await __tmp0.__check_for_completion(msg.pid)
        elif isinstance(msg, UnknownResult):
            __tmp0._unknown_results += 1
            await __tmp0.__check_for_completion(msg.pid)
        elif isinstance(msg, FailedAndInconsistent):
            __tmp0._failed_and_inconsistent_results += 1
            await __tmp0.__check_for_completion(msg.pid)
        elif isinstance(msg, FailedButConsistentResult):
            __tmp0._failed_but_consistent_results += 1
            await __tmp0.__check_for_completion(msg.pid)
        elif isinstance(msg, Started):
            __tmp0._in_memory_provider = InMemoryProvider()

            def every_nth_action(i: __typ0):
                print(f'Started {i}/{__tmp0._number_of_iterations} processes')

            def every_action(i: __typ0, nth: bool):
                j = i
                from_account = __tmp0.__create_account(f'FromAccount{j}')
                to_account = __tmp0.__create_account(f'ToAccount{j}')
                actor_name = f'Transfer Process {j}'
                persistance_id = f'Transfer Process {j}'
                factory = TransferFactory(context, __tmp0._in_memory_provider, __tmp0._uptime, __tmp0._retry_attempts)
                transfer = factory.create_transfer(actor_name, from_account, to_account, 10, persistance_id)
                __tmp0._transfers.append(transfer)
                if i == __tmp0._number_of_iterations and not nth:
                    print(f'Started {j}/{__tmp0._number_of_iterations} proesses')

            ForWithProgress(__tmp0._number_of_iterations, __tmp0._interval_between_console_updates, True, False).every_nth(
                every_nth_action, every_action)

    async def __check_for_completion(__tmp0, pid: __typ1):
        __tmp0._transfers.remove(pid)
        remaining = len(__tmp0._transfers)
        if __tmp0._number_of_iterations >= __tmp0._interval_between_console_updates:
            print('.')
            if remaining % (__tmp0._number_of_iterations / __tmp0._interval_between_console_updates) == 0:
                print()
                print(f'{remaining} processes remaining')
            else:
                print(f'{remaining} processes remaining')
            if remaining == 0:
                await asyncio.sleep(0.25)
                print()
                print(f'RESULTS for {__tmp0._uptime}% uptime, {__tmp0._refusal_probability}% chance of refusal, '
                      f'{__tmp0._busy_probability}% of being busy and {__tmp0._retry_attempts} retry attempts:')

                print(f'{__tmp0.__as_percentage(__tmp0._number_of_iterations, __tmp0._success_results)}% '
                      f'({__tmp0._success_results}/{__tmp0._number_of_iterations}) successful transfers')

                print(f'{__tmp0.__as_percentage(__tmp0._number_of_iterations, __tmp0._failed_but_consistent_results)}% '
                      f'({__tmp0._failed_but_consistent_results}/{__tmp0._number_of_iterations}) '
                      f'failures leaving a consistent system')

                print(f'{__tmp0.__as_percentage(__tmp0._number_of_iterations, __tmp0._failed_and_inconsistent_results)}% '
                      f'({__tmp0._failed_and_inconsistent_results}/{__tmp0._number_of_iterations}) '
                      f'failures leaving an inconsistent system')

                print(f'{__tmp0.__as_percentage(__tmp0._number_of_iterations, __tmp0._unknown_results)}% '
                      f'({__tmp0._unknown_results}/{__tmp0._number_of_iterations}) unknown results')

                if __tmp0._verbose:
                    for stream in __tmp0._in_memory_provider.events:
                        print()
                        print(f'Event log for {stream.key}')
                        for event in stream.value:
                            print(event.value)

    def __as_percentage(__tmp0, number_of_iterations, results: float):
        return (results / number_of_iterations) * 100
