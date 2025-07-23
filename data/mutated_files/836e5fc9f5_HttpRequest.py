from typing import TypeAlias
__typ2 : TypeAlias = "UserProfile"
__typ0 : TypeAlias = "Command"
__typ3 : TypeAlias = "Any"
__typ1 : TypeAlias = "str"
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
    def __init__(__tmp1) -> None:
        __tmp1.modified = False

class MockRequest(HttpRequest):
    def __init__(__tmp1, user) :
        __tmp1.user = user
        __tmp1.path = '/'
        __tmp1.method = "POST"
        __tmp1.META = {"REMOTE_ADDR": "127.0.0.1"}
        anchor = UserMessage.objects.filter(user_profile=__tmp1.user).order_by("-message")[200].message_id
        __tmp1.REQUEST = {
            "anchor": anchor,
            "num_before": 1200,
            "num_after": 200
        }
        __tmp1.GET = {}  # type: Dict[Any, Any]
        __tmp1.session = MockSession()

    def __tmp0(__tmp1) -> __typ1:
        return __tmp1.path

def __tmp2(__tmp3: <FILL>) -> HttpResponse:
    request_logger.process_request(__tmp3)
    prof = cProfile.Profile()
    prof.enable()
    ret = get_messages_backend(__tmp3, __tmp3.user,
                               apply_markdown=True)
    prof.disable()
    prof.dump_stats("/tmp/profile.data")
    request_logger.process_response(__tmp3, ret)
    logging.info("Profiling data written to /tmp/profile.data")
    return ret

class __typ0(ZulipBaseCommand):
    def __tmp4(__tmp1, parser: CommandParser) -> None:
        parser.add_argument("email", metavar="<email>", type=__typ1, help="Email address of the user")
        __tmp1.add_realm_args(parser)

    def handle(__tmp1, *args: __typ3, **options: __typ3) -> None:
        realm = __tmp1.get_realm(options)
        user = __tmp1.get_user(options["email"], realm)
        __tmp2(MockRequest(user))
