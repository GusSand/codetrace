from telegram.ext import Updater, MessageHandler, CommandHandler
from telegram.bot import Bot
from typing import List, Union, Callable
import config
from handlers import get_handlers_list, error_handler


def setup_bot(handlers) :
    bot = Updater(config.TELEGRAM_BOT_TOKEN, request_kwargs=config.TELEGRAM_PROXY_CONFIG)
    dp = bot.dispatcher
    for handler in handlers:
        dp.add_handler(handler)
    return bot


def start_bot(bot: <FILL>, err_handler: Callable) :
    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    bot = setup_bot(handlers=get_handlers_list())
    start_bot(bot, error_handler)
