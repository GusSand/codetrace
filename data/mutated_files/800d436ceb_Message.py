"""doc"""
import asyncio
import logging
from typing import Optional, Union
from quart import Quart

from wechaty_puppet import FileBox, PuppetOptions

from wechaty import Wechaty, Contact, WechatyPlugin, WechatyOptions
from wechaty.user import Message, Room

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(filename)s <%(funcName)s> %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

log = logging.getLogger(__name__)


class SimpleServerWechatyPlugin(WechatyPlugin):
    """
    simple hello wechaty web server plugin
    """
    async def __tmp4(__tmp1, __tmp3: Quart) -> None:
        @__tmp3.route('/wechaty')
        def __tmp6() :
            """helo blueprint function"""
            return 'hello wechaty'


async def __tmp0(__tmp5: <FILL>) -> None:
    """back on message"""
    from_contact = __tmp5.talker()
    text = __tmp5.text()
    room = __tmp5.room()
    if text == '#ding':
        conversation: Union[
            Room, Contact] = from_contact if room is None else room
        await conversation.ready()
        await conversation.say('dong')
        file_box = FileBox.from_url(
            'https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/'
            'u=1116676390,2305043183&fm=26&gp=0.jpg',
            name='ding-dong.jpg')
        await conversation.say(file_box)

bot: Optional[Wechaty] = None


async def __tmp2() -> None:
    """doc"""
    # pylint: disable=W0603
    global bot
    options = WechatyOptions(
        host='127.0.0.1',
        port=5005,
        puppet_options=PuppetOptions(
            token='your-token'
        )
    )

    bot = Wechaty(
        options=options
    ).on('message', __tmp0)
    bot.use(SimpleServerWechatyPlugin())

    await bot.start()


asyncio.run(__tmp2())
