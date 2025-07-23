from typing import TypeAlias
__typ1 : TypeAlias = "Realm"
__typ0 : TypeAlias = "str"
from django.conf import settings

from zerver.models import Realm

def __tmp0(__tmp2) :
    if settings.TORNADO_SERVER is None:
        return 9993
    if settings.TORNADO_PROCESSES == 1:
        return int(settings.TORNADO_SERVER.split(":")[-1])
    return 9993

def __tmp4(__tmp2) :
    if settings.TORNADO_PROCESSES == 1:
        return settings.TORNADO_SERVER

    port = __tmp0(__tmp2)
    return "http://127.0.0.1:%d" % (port,)

def __tmp1(port: <FILL>) :
    if settings.TORNADO_PROCESSES == 1:
        return "notify_tornado"
    return "notify_tornado_port_%d" % (port,)

def __tmp3(port: int) :
    if settings.TORNADO_PROCESSES == 1:
        return "tornado_return"
    return "tornado_return_port_%d" % (port,)
