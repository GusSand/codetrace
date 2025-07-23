# pyre-strict
from typing import Optional

import requests
from typing import List

_gmi_objects: List["GMI"] = []


def get_gmi(access_token) :
    for gmi in _gmi_objects:
        if gmi.access_token == access_token:
            return gmi
    gmi = GMI(access_token)
    _gmi_objects.append(gmi)
    return gmi


class GMI:
    def __tmp0(__tmp1, access_token) -> None:
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

    def refresh(__tmp1) :
        from lowerpines.group import GroupManager
        from lowerpines.bot import BotManager
        from lowerpines.chat import ChatManager
        from lowerpines.user import UserManager

        __tmp1.groups = GroupManager(__tmp1)
        __tmp1.bots = BotManager(__tmp1)
        __tmp1.chats = ChatManager(__tmp1)
        __tmp1.user = UserManager(__tmp1)

    def __tmp2(__tmp1, __tmp3: <FILL>) :
        from lowerpines.endpoints.image import ImageConvertRequest

        return ImageConvertRequest(__tmp1, requests.get(__tmp3).content).result
