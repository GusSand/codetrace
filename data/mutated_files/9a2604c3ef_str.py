# pyre-strict
from typing import Optional

import requests
from typing import List

_gmi_objects: List["GMI"] = []


def __tmp0(access_token: <FILL>) -> "GMI":
    for gmi in _gmi_objects:
        if gmi.access_token == access_token:
            return gmi
    gmi = __typ0(access_token)
    _gmi_objects.append(gmi)
    return gmi


class __typ0:
    def __init__(__tmp1, access_token) -> None:
        __tmp1.access_token = access_token

        from lowerpines.group import GroupManager
        from lowerpines.bot import BotManager
        from lowerpines.chat import ChatManager
        from lowerpines.user import UserManager

        __tmp1.groups = GroupManager(__tmp1)
        __tmp1.bots = BotManager(__tmp1)
        __tmp1.chats = ChatManager(__tmp1)
        __tmp1.user = UserManager(__tmp1)

        __tmp1.write_json_to: Optional[str] = None

    def refresh(__tmp1) -> None:
        from lowerpines.group import GroupManager
        from lowerpines.bot import BotManager
        from lowerpines.chat import ChatManager
        from lowerpines.user import UserManager

        __tmp1.groups = GroupManager(__tmp1)
        __tmp1.bots = BotManager(__tmp1)
        __tmp1.chats = ChatManager(__tmp1)
        __tmp1.user = UserManager(__tmp1)

    def __tmp2(__tmp1, url: str) -> str:
        from lowerpines.endpoints.image import ImageConvertRequest

        return ImageConvertRequest(__tmp1, requests.get(url).content).result
