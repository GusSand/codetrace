from typing import TypeAlias
__typ3 : TypeAlias = "str"
__typ1 : TypeAlias = "FileBox"
__typ4 : TypeAlias = "bool"
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
import os
import re
from typing import (
    Optional,
    Any
)

from wechaty_puppet import (
    FileBox,
    get_logger
)


log = get_logger('Config')

# log.debug('test logging debug')
# log.info('test logging info')


# TODO(wj-Mcat): there is no reference usage, so need to be removed
_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.realpath(
    os.path.join(
        _FILE_PATH,
        '../data',
    ),
)

# http://jkorpela.fi/chars/spaces.html
# String.fromCharCode(8197)
AT_SEPARATOR = chr(0x2005)

# refer to:https://github.com/wechaty/python-wechaty/issues/285#issuecomment-997441596
PARALLEL_TASK_NUM = 100


def __tmp4(__tmp8: <FILL>) :
    """
    handle the global exception
    :param exception: exception message
    :return:
    """
    log.error('occur %s %s', __tmp8.__class__.__name__, __typ3(__tmp8.args))
    print(__tmp8)


class __typ0(dict):
    """
    store global default setting
    """
    default_api_host: Optional[__typ3] = None
    default_port: Optional[int] = None
    default_protocol: Optional[__typ3] = None


# pylint: disable=R0903
def __tmp3(__tmp5) :
    """
    test the validation of the api_host
    :param api_host:
    :return:
    """
    pattern = re.compile(
        r'^(([a-zA-Z]{1})|([a-zA-Z]{1}[a-zA-Z]{1})|:?[0-9]*'
        r'([a-zA-Z]{1}[0-9]{1})|([0-9]{1}[a-zA-Z]{1})|:?[0-9]*'
        r'([a-zA-Z0-9][-_.a-zA-Z0-9]{0,61}[a-zA-Z0-9]))\.:?[0-9]*'
        r'([a-zA-Z]{2,13}|[a-zA-Z0-9-]{2,30}.[a-zA-Z]{2,3}):?[0-9]*$'
    )
    return __typ4(pattern.match(__tmp5))


class __typ2:
    """
    get the configuration from the environment variables
    """
    @property
    def cache_dir(__tmp1) :
        """get the cache dir in the lazy loading mode

        Returns:
            str: the path of cache dir
        """
        path = os.environ.get("CACHE_DIR", '.wechaty')
        os.makedirs(path, exist_ok=True)
        return path

    @property
    def __tmp0(__tmp1) -> __typ3:
        """get the ui directory

        Returns:
            str: the path of the ui dir
        """
        default_ui_dir = os.path.join(
            os.path.dirname(__file__),
            'ui'
        )
        return os.environ.get("UI_DIR", default_ui_dir)

    def get_environment_variable(
        __tmp1,
        name,
        default_value: Optional[Any] = None
    ) -> Optional[Any]:
        """get environment variable

        Args:
            name (str): the name of environment
            default_value (Optional[Any], optional): default Value. Defaults to None.
        """
        if name not in os.environ:
            return default_value
        return os.environ[name]
    
    @property
    def __tmp9(__tmp1) :
        """whether cache all of payloads of rooms

        Returns:
            bool: whether cache the paylaod of rooms
        """
        env_key = 'CACHE_ROOMS'
        true_strings = ['true', '1']
        if env_key not in os.environ:
            return True
        value = os.environ[env_key]
        return value in true_strings

    @property
    def __tmp2(__tmp1) :
        """get the room pickle path"""
        env_key = "CACHE_ROOMS_PATH"
        if env_key in os.environ:
            return os.environ[env_key]

        default_path = os.path.join(
            __tmp1.cache_dir,
            "room_payloads.pkl"
        )
        return default_path

    @property
    def __tmp7(__tmp1) :
        """whether cache all of payloads of contact

        Returns:
            bool: whether cache the paylaod of contact
        """

        env_key = 'CACHE_CONTACTS'
        true_strings = ['true', '1']
        if env_key not in os.environ:
            return True
        value = os.environ[env_key]
        return value in true_strings

    @property
    def __tmp6(__tmp1) -> __typ3:
        """get the contact pickle path"""
        env_key = "CACHE_CONTACTS_PATH"
        if env_key in os.environ:
            return os.environ[env_key]

        default_path = os.path.join(
            __tmp1.cache_dir,
            "contact_payloads.pkl"
        )
        return default_path

# export const CHATIE_OFFICIAL_ACCOUNT_ID = 'gh_051c89260e5d'
# chatie_official_account_id = 'gh_051c89260e5d'
# CHATIE_OFFICIAL_ACCOUNT_ID = 'gh_051c89260e5d'


def __tmp10() -> __typ1:
    """
    create QRcode for chatie
    :return:
    """
    # const CHATIE_OFFICIAL_ACCOUNT_QRCODE =
    # 'http://weixin.qq.com/r/qymXj7DEO_1ErfTs93y5'
    chatie_official_account_qr_code: __typ3 = \
        'http://weixin.qq.com/r/qymXj7DEO_1ErfTs93y5'
    return __typ1.from_qr_code(chatie_official_account_qr_code)


config = __typ2()
