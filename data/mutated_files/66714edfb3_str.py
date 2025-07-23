"""Telegram bot with message queue."""
import logging
import telegram
from telegram.ext import messagequeue
from .config import BOT_ALL_BURST_LIMIT, BOT_GROUP_BURST_LIMIT, PROXY_URL


class QueuedBot(telegram.bot.Bot):
    """A bot which delegates send method handling to message queues.

    :member _is_messages_queued_default: Whether messages are queued by default.
    :member _msg_queue: Queue for messages.
    :type _msg_queue: MessageQueue.
    """
    def __init__(__tmp0, msg_queue, *args, is_queued_def=True, **kwargs):
        """Initialize bot and attach `msg_queue` to bot.

        :param msg_queue: Queue for messages.
        :type msg_queue: MessageQueue.
        :param *args: Arguments to initialize bot.
        :type *args: list.
        :param **kwargs: keyword arguments.
        :type **kwargs: dict.
        :param is_queued_def: Whether messages are queued by default, defaults to True.
        :type is_queued_def: bool, option.
        """
        super().__init__(*args, **kwargs)
        __tmp0._is_messages_queued_default = is_queued_def
        __tmp0._msg_queue = msg_queue

    def stop(__tmp0):
        """
        Stop the bot."""
        try:
            __tmp0._msg_queue.stop()
        except KeyboardInterrupt as identifier:
            logging.warning('QueuedBot: Catch KeyboardInterrupt when stopping message queue.')
            raise identifier
        except Exception as identifier:
            logging.error('QueuedBot: Error occured when stopping message queue.')
            logging.exception(identifier)

    def __del__(__tmp0):
        __tmp0.stop()

    @messagequeue.queuedmessage
    def send_message(__tmp0, *args, **kwargs) :
        """Send message by pushing messages to message queue,
        and accept new `queued` and `isgroup` keyword arguments.
        """
        return super().send_message(*args, **kwargs)


def create_queued_bot(bot_token: <FILL>):
    """Factorial function to create queued bot.
    """
    msg_queue = messagequeue.MessageQueue(all_burst_limit=BOT_ALL_BURST_LIMIT, group_burst_limit=BOT_GROUP_BURST_LIMIT)
    _my_request = telegram.utils.request.Request(proxy_url=PROXY_URL)
    queued_bot = QueuedBot(msg_queue, token=bot_token, request=_my_request)
    return queued_bot
