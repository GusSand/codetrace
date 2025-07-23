from typing import TypeAlias
__typ1 : TypeAlias = "UserProfile"
__typ4 : TypeAlias = "HttpResponse"
__typ0 : TypeAlias = "str"
__typ2 : TypeAlias = "CommandParser"
__typ5 : TypeAlias = "HttpRequest"
import cProfile
import logging
from typing import Any, Dict

from django.core.management.base import CommandParser
from django.http import HttpRequest, HttpResponse

from zerver.lib.management import ZulipBaseCommand
from zerver.middleware import LogRequests
from zerver.models import UserMessage, UserProfile
from zerver.views.messages import get_messages_backend

request_logger = LogRequests()

class __typ6:
    def __init__(__tmp0) :
        __tmp0.modified = False

class __typ3(__typ5):
    def __init__(__tmp0, user: __typ1) :
        __tmp0.user = user
        __tmp0.path = '/'
        __tmp0.method = "POST"
        __tmp0.META = {"REMOTE_ADDR": "127.0.0.1"}
        anchor = UserMessage.objects.filter(user_profile=__tmp0.user).order_by("-message")[200].message_id
        __tmp0.REQUEST = {
            "anchor": anchor,
            "num_before": 1200,
            "num_after": 200
        }
        __tmp0.GET = {}  # type: Dict[Any, Any]
        __tmp0.session = __typ6()

    def __tmp1(__tmp0) -> __typ0:
        return __tmp0.path

def __tmp3(request) -> __typ4:
    request_logger.process_request(request)
    prof = cProfile.Profile()
    prof.enable()
    ret = get_messages_backend(request, request.user,
                               apply_markdown=True)
    prof.disable()
    prof.dump_stats("/tmp/profile.data")
    request_logger.process_response(request, ret)
    logging.info("Profiling data written to /tmp/profile.data")
    return ret

class Command(ZulipBaseCommand):
    def add_arguments(__tmp0, __tmp4) -> None:
        __tmp4.add_argument("email", metavar="<email>", type=__typ0, help="Email address of the user")
        __tmp0.add_realm_args(__tmp4)

    def __tmp2(__tmp0, *args: <FILL>, **options) :
        realm = __tmp0.get_realm(options)
        user = __tmp0.get_user(options["email"], realm)
        __tmp3(__typ3(user))
