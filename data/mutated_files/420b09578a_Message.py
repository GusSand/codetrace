from typing import TypeAlias
__typ0 : TypeAlias = "str"
"""
Python Wechaty - https://github.com/wechaty/python-wechaty

Authors:    Huan LI (李卓桓) <https://github.com/huan>
            Jingjing WU (吴京京) <https://github.com/wj-Mcat>

2020-now @ Copyright Wechaty

Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import annotations

from typing import TYPE_CHECKING
from dataclasses import asdict

from wechaty import Accessory
from wechaty_puppet import MiniProgramPayload, get_logger
from wechaty.utils import default_str

if TYPE_CHECKING:
    from wechaty.user import Message


log = get_logger('MiniProgram')


class MiniProgram(Accessory[MiniProgramPayload]):
    """
    mini_program object which handle the url_link content
    """
    def __init__(__tmp3, payload):
        """
        initialization for mini_program
        :param payload:
        """
        super().__init__()

        log.info('MiniProgram created')
        __tmp3._payload: MiniProgramPayload = payload

    @classmethod
    async def create_from_message(__tmp5, __tmp0: <FILL>) -> MiniProgram:
        """
        static create MiniProgram method
        :return:
        """
        log.info(f'loading the mini-program from message <{__tmp0}>')

        mini_program_payload = await __tmp5.get_puppet().message_mini_program(
            message_id=__tmp0.message_id)

        mini_program = MiniProgram(mini_program_payload)
        return mini_program

    @classmethod
    def __tmp7(__tmp5, __tmp2: dict) -> MiniProgram:
        """
        create the mini_program from json data
        """
        log.info(f'loading the mini-program from json data <{__tmp2}>')

        payload = MiniProgramPayload(**__tmp2)

        mini_program = __tmp5(payload=payload)
        return mini_program

    def __tmp10(__tmp3) -> dict:
        """
        save the mini-program to dict data
        """
        log.info(f'save the mini-program to json data : <{__tmp3.payload}>')
        mini_program_data = asdict(__tmp3.payload)
        return mini_program_data

    @property
    def __tmp8(__tmp3) -> __typ0:
        """
        get mini_program app_id
        :return:
        """
        return default_str(__tmp3._payload.appid)

    @property
    def title(__tmp3) -> __typ0:
        """
        get mini_program title
        :return:
        """
        return default_str(__tmp3._payload.title)

    @property
    def __tmp9(__tmp3) -> __typ0:
        """
        get mini_program icon url
        """
        return default_str(__tmp3._payload.iconUrl)

    @property
    def page_path(__tmp3) -> __typ0:
        """
        get mini_program page_path
        :return:
        """
        return default_str(__tmp3._payload.pagePath)

    @property
    def __tmp1(__tmp3) -> __typ0:
        """
        get mini_program user_name
        :return:
        """
        return default_str(__tmp3._payload.username)

    @property
    def description(__tmp3) -> __typ0:
        """
        get mini_program description
        :return:
        """
        return default_str(__tmp3._payload.description)

    @property
    def __tmp4(__tmp3) -> __typ0:
        """
        get mini_program thumb_url
        :return:
        """
        return default_str(__tmp3._payload.thumbUrl)

    @property
    def __tmp6(__tmp3) -> __typ0:
        """
        get mini_program thumb_key
        :return:
        """
        return default_str(__tmp3._payload.thumbKey)
