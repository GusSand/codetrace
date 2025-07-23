from typing import TypeAlias
__typ2 : TypeAlias = "Any"
__typ1 : TypeAlias = "LazySettings"
from typing import Any, Optional

import pushbullet as pb

from django.conf import LazySettings


class __typ0:
    _token: str
    __pushbullet: Optional[pb.Pushbullet] = None

    @property
    def pushbullet(__tmp1) :
        if __tmp1.__pushbullet is None:
            # pushbullet.Pushbullet sends a request on initialization,
            # so delay it
            __tmp1.__pushbullet = pb.Pushbullet(__tmp1._token)
        assert isinstance(__tmp1.__pushbullet, pb.Pushbullet)
        return __tmp1.__pushbullet

    def __init__(__tmp1, settings: __typ1) :
        __tmp1._token = settings.TRIGGER_PUSHBULLET_TOKEN
        assert __tmp1._token
        return

    def push_note(__tmp1, __tmp0: <FILL>, title: str = "") :
        # TODO: Handle errors
        return __tmp1.pushbullet.push_note(title, __tmp0)
