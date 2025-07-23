# pyre-strict
from typing import Optional

import requests
from typing import List

_gmi_objects: List["GMI"] = []


def __tmp4(access_token) :
    for gmi in _gmi_objects:
        if gmi.access_token == access_token:
            return gmi
    gmi = __typ0(access_token)
    _gmi_objects.append(gmi)
    return gmi


class __typ0:
    def __tmp3(self, access_token: <FILL>) :
        self.access_token = access_token

        from lowerpines.group import GroupManager
        from lowerpines.bot import BotManager
        from lowerpines.chat import ChatManager
        from lowerpines.user import UserManager

        self.groups = GroupManager(self)
        self.bots = BotManager(self)
        self.chats = ChatManager(self)
        self.user = UserManager(self)

        self.write_json_to: Optional[str] = None

    def __tmp0(self) :
        from lowerpines.group import GroupManager
        from lowerpines.bot import BotManager
        from lowerpines.chat import ChatManager
        from lowerpines.user import UserManager

        self.groups = GroupManager(self)
        self.bots = BotManager(self)
        self.chats = ChatManager(self)
        self.user = UserManager(self)

    def __tmp1(self, __tmp2) :
        from lowerpines.endpoints.image import ImageConvertRequest

        return ImageConvertRequest(self, requests.get(__tmp2).content).result
