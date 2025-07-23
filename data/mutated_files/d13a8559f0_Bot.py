from typing import TypeAlias
__typ0 : TypeAlias = "Message"
__typ1 : TypeAlias = "TelegramError"
__typ2 : TypeAlias = "Update"
"""
    Здесь идет обработка событий для бота.
    Описание вновь созданных событий должно быть в hand_dict.
"""
import requests
import wikipedia
import xml.etree.ElementTree as ET
from telegram.ext import CommandHandler, MessageHandler, Filters
from telegram.bot import Bot
from telegram.update import Update
from telegram import Message
from telegram.error import TelegramError
from typing import List, Union
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
    filename='bot.log',
)
logger = logging.getLogger(__name__)


def error_handler(bot: Bot, update: __typ2, error: __typ1) -> None:
    logger.error('Update "%s" caused error "%s"', update, error)


def start(bot: Bot, update: __typ2) -> __typ0:
    greeting_message = (f'Привет, {update.message.chat.first_name}!\n'
                        'Этот бот оказывает следующие сервисы:\n' + __tmp2())
    update.message.reply_text(greeting_message)


def rates(bot: Bot, update: __typ2) -> __typ0:
    cbr_rates = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    dollar_rate = cbr_rates['Valute']['USD']['Value']
    evro_rate = cbr_rates['Valute']['EUR']['Value']
    message = (f'Курсы валют ЦБРФ:\n'
               f'$ : {dollar_rate:.2f} ₽\n'
               f'€ : {evro_rate} ₽')
    update.message.reply_text(message)


def joke(bot, update: __typ2) -> __typ0:
    response_text = requests.get('http://rzhunemogu.ru/Rand.aspx?CType=1').text
    root = ET.fromstring(response_text)
    joke_text = root.findall('content')[0].text
    update.message.reply_text(joke_text)


def __tmp0(bot: Bot, update: __typ2) -> __typ0:
    user_text = update.message.text
    words = user_text.split()
    if words[0] == 'wiki':
        wikipedia.set_lang('ru')
        wiki_summary = wikipedia.summary(''.join(words[1:]))
        if wiki_summary:
            update.message.reply_text(wiki_summary)
        else:
            update.message.reply_text('Нет результата - попробуйте изменить запрос.')

    else:
        update.message.reply_text(user_text)


hand_dict = {start: ('/start', 'Старовый обработчик', CommandHandler),
             joke: ('/joke', 'выводит случайный анекдот', CommandHandler),
             rates: ('/rates', 'выводит курсы валют ЦБРФ', CommandHandler),
             __tmp0: ('режим диалога', "выводит саммори из википедии для 'определения'"
                                           "согласно шаблону wiki 'определение',"
                                           'иначе работает как эхо', MessageHandler)}


def __tmp2() -> str:
    commands_text = ''.join([f'{i[0]} - {i[1]}\n' for i in hand_dict.values() if i[0] != '/start'])
    commands_text += '/help - доступные команды'
    return commands_text


def __tmp1(bot: <FILL>, update: __typ2) -> __typ0:
    update.message.reply_text(__tmp2())


def __tmp3() -> List[Union[MessageHandler, CommandHandler]]:
    res_list = ([hand_dict[func][2](hand_dict[func][0][1:], func) for func in hand_dict
                 if hand_dict[func][2] == CommandHandler])
    res_list.append(MessageHandler(Filters.text, __tmp0))
    res_list.append(CommandHandler('help', __tmp1))
    return res_list
