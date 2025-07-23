from typing import TypeAlias
__typ2 : TypeAlias = "str"
__typ3 : TypeAlias = "UserProfile"
__typ0 : TypeAlias = "CommandParser"
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

class MockSession:
    def __tmp5(__tmp0) :
        __tmp0.modified = False

class __typ1(HttpRequest):
    def __tmp5(__tmp0, user) :
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
        __tmp0.session = MockSession()

    def __tmp1(__tmp0) -> __typ2:
        return __tmp0.path

def __tmp3(__tmp4: HttpRequest) :
    request_logger.process_request(__tmp4)
    prof = cProfile.Profile()
    prof.enable()
    ret = get_messages_backend(__tmp4, __tmp4.user,
                               apply_markdown=True)
    prof.disable()
    prof.dump_stats("/tmp/profile.data")
    request_logger.process_response(__tmp4, ret)
    logging.info("Profiling data written to /tmp/profile.data")
    return ret

class Command(ZulipBaseCommand):
    def add_arguments(__tmp0, __tmp6) :
        __tmp6.add_argument("email", metavar="<email>", type=__typ2, help="Email address of the user")
        __tmp0.add_realm_args(__tmp6)

    def __tmp2(__tmp0, *args: Any, **options: <FILL>) :
        realm = __tmp0.get_realm(options)
        user = __tmp0.get_user(options["email"], realm)
        __tmp3(__typ1(user))
