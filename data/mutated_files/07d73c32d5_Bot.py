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


def __tmp2(bot, update, error) :
    logger.error('Update "%s" caused error "%s"', update, error)


def start(bot, update) :
    greeting_message = (f'Привет, {update.message.chat.first_name}!\n'
                        'Этот бот оказывает следующие сервисы:\n' + __tmp4())
    update.message.reply_text(greeting_message)


def __tmp0(bot, update) :
    cbr_rates = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    dollar_rate = cbr_rates['Valute']['USD']['Value']
    evro_rate = cbr_rates['Valute']['EUR']['Value']
    message = (f'Курсы валют ЦБРФ:\n'
               f'$ : {dollar_rate:.2f} ₽\n'
               f'€ : {evro_rate} ₽')
    update.message.reply_text(message)


def __tmp1(bot: Bot, update) -> __typ0:
    response_text = requests.get('http://rzhunemogu.ru/Rand.aspx?CType=1').text
    root = ET.fromstring(response_text)
    joke_text = root.findall('content')[0].text
    update.message.reply_text(joke_text)


def talk_to_me(bot: <FILL>, update) :
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
             __tmp1: ('/joke', 'выводит случайный анекдот', CommandHandler),
             __tmp0: ('/rates', 'выводит курсы валют ЦБРФ', CommandHandler),
             talk_to_me: ('режим диалога', "выводит саммори из википедии для 'определения'"
                                           "согласно шаблону wiki 'определение',"
                                           'иначе работает как эхо', MessageHandler)}


def __tmp4() -> str:
    commands_text = ''.join([f'{i[0]} - {i[1]}\n' for i in hand_dict.values() if i[0] != '/start'])
    commands_text += '/help - доступные команды'
    return commands_text


def __tmp3(bot, update) :
    update.message.reply_text(__tmp4())


def __tmp5() :
    res_list = ([hand_dict[func][2](hand_dict[func][0][1:], func) for func in hand_dict
                 if hand_dict[func][2] == CommandHandler])
    res_list.append(MessageHandler(Filters.text, talk_to_me))
    res_list.append(CommandHandler('help', __tmp3))
    return res_list
