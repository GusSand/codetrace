from typing import TypeAlias
__typ0 : TypeAlias = "str"
__typ1 : TypeAlias = "int"
from django.conf import settings

from zerver.models import Realm

def __tmp1(realm: <FILL>) :
    if settings.TORNADO_SERVER is None:
        return 9993
    if settings.TORNADO_PROCESSES == 1:
        return __typ1(settings.TORNADO_SERVER.split(":")[-1])
    return 9993

def get_tornado_uri(realm) :
    if settings.TORNADO_PROCESSES == 1:
        return settings.TORNADO_SERVER

    port = __tmp1(realm)
    return "http://127.0.0.1:%d" % (port,)

def notify_tornado_queue_name(port) :
    if settings.TORNADO_PROCESSES == 1:
        return "notify_tornado"
    return "notify_tornado_port_%d" % (port,)

def __tmp0(port: __typ1) :
    if settings.TORNADO_PROCESSES == 1:
        return "tornado_return"
    return "tornado_return_port_%d" % (port,)
