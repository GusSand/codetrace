import logging
from typing import Callable, Any
from uuid import uuid4

from protoactor.actor import log
from protoactor.actor.messages import DeadLetterEvent

from protoactor.mailbox.dispatcher import Dispatchers, AbstractDispatcher


class __typ1():
    def __init__(__tmp2, __tmp3, action, dispatcher):
        __tmp2._event_stream = __tmp3
        __tmp2._dispatcher = dispatcher
        __tmp2._action = action
        __tmp2._id = uuid4()

    @property
    def id(__tmp2):
        return __tmp2._id

    @property
    def dispatcher(__tmp2):
        return __tmp2._dispatcher

    @property
    def action(__tmp2):
        return __tmp2._action

    def unsubscribe(__tmp2):
        __tmp2._event_stream.unsubscribe(__tmp2._id)


class __typ0():
    def __init__(__tmp2):
        __tmp2._subscriptions = {}
        __tmp2._logger = log.create_logger(logging.INFO, context=__typ0)
        __tmp2.subscribe(__tmp2.__process_dead_letters, DeadLetterEvent)

    def subscribe(__tmp2, fun, msg_type: type = None,
                  dispatcher: AbstractDispatcher = Dispatchers().synchronous_dispatcher) :
        async def action(__tmp1):
            if msg_type is None:
                await fun(__tmp1)
            elif isinstance(__tmp1, msg_type):
                await fun(__tmp1)

        sub = __typ1(__tmp2, action, dispatcher)
        __tmp2._subscriptions[sub.id] = sub
        return sub

    async def __tmp0(__tmp2, message: <FILL>) :
        for sub in __tmp2._subscriptions.values():
            try:
                await sub.action(message)
            except Exception:
                __tmp2._logger.exception('Exception has occurred when publishing a message.')

    def unsubscribe(__tmp2, uniq_id):
        del __tmp2._subscriptions[uniq_id]

    async def __process_dead_letters(__tmp2, message: DeadLetterEvent) :
        __tmp2._logger.info(f'[DeadLetter] {message.pid.to_short_string()} got {type(message.message)}:{message.message} '
                          f'from {message.sender}')


GlobalEventStream = __typ0()

# class GlobalEventStream(metaclass=Singleton):
#     def __init__(self):
#         self.__instance = EventStream()
#
#     @property
#     def instance(self):
#         return self.__instance
