from typing import TypeAlias
__typ0 : TypeAlias = "int"
from django.conf import settings

from zerver.models import Realm

def __tmp3(__tmp0: Realm) -> __typ0:
    if settings.TORNADO_SERVER is None:
        return 9993
    if settings.TORNADO_PROCESSES == 1:
        return __typ0(settings.TORNADO_SERVER.split(":")[-1])
    return 9993

def __tmp2(__tmp0: <FILL>) -> str:
    if settings.TORNADO_PROCESSES == 1:
        return settings.TORNADO_SERVER

    port = __tmp3(__tmp0)
    return "http://127.0.0.1:%d" % (port,)

def __tmp1(port) -> str:
    if settings.TORNADO_PROCESSES == 1:
        return "notify_tornado"
    return "notify_tornado_port_%d" % (port,)

def tornado_return_queue_name(port: __typ0) -> str:
    if settings.TORNADO_PROCESSES == 1:
        return "tornado_return"
    return "tornado_return_port_%d" % (port,)
