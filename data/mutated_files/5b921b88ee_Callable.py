from telegram.ext import Updater, MessageHandler, CommandHandler
from telegram.bot import Bot
from typing import List, Union, Callable
import config
from handlers import get_handlers_list, error_handler


def __tmp0(handlers: List[Union[MessageHandler, CommandHandler]]) -> Bot:
    bot = Updater(config.TELEGRAM_BOT_TOKEN, request_kwargs=config.TELEGRAM_PROXY_CONFIG)
    dp = bot.dispatcher
    for handler in handlers:
        dp.add_handler(handler)
    return bot


def __tmp1(bot, err_handler: <FILL>) :
    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    bot = __tmp0(handlers=get_handlers_list())
    __tmp1(bot, error_handler)
