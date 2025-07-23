from typing import TypeAlias
__typ0 : TypeAlias = "UserProfile"
__typ2 : TypeAlias = "HttpResponse"
__typ1 : TypeAlias = "bool"

from django.http import HttpRequest, HttpResponse
from typing import Iterable, Optional, Sequence

from zerver.lib.events import do_events_register
from zerver.lib.request import REQ, has_request_variables
from zerver.lib.response import json_success
from zerver.lib.validator import check_string, check_list, check_bool
from zerver.models import Stream, UserProfile

def __tmp4(__tmp1: __typ0,
                                __tmp0: Optional[__typ1]) -> __typ1:
    if __tmp0 is not None:
        return __tmp0
    else:
        return __tmp1.default_all_public_streams

def __tmp3(__tmp1: __typ0,
                    narrow: Iterable[Sequence[str]]) -> Iterable[Sequence[str]]:
    default_stream = __tmp1.default_events_register_stream  # type: Optional[Stream]
    if not narrow and default_stream is not None:
        narrow = [['stream', default_stream.name]]
    return narrow

NarrowT = Iterable[Sequence[str]]
@has_request_variables
def __tmp2(
        request: <FILL>, __tmp1: __typ0,
        apply_markdown: __typ1=REQ(default=False, validator=check_bool),
        client_gravatar: __typ1=REQ(default=False, validator=check_bool),
        __tmp0: Optional[__typ1]=REQ(default=None, validator=check_bool),
        include_subscribers: __typ1=REQ(default=False, validator=check_bool),
        event_types: Optional[Iterable[str]]=REQ(validator=check_list(check_string), default=None),
        fetch_event_types: Optional[Iterable[str]]=REQ(validator=check_list(check_string), default=None),
        narrow: NarrowT=REQ(validator=check_list(check_list(check_string, length=2)), default=[]),
        queue_lifespan_secs: int=REQ(converter=int, default=0)
) :
    __tmp0 = __tmp4(__tmp1, __tmp0)
    narrow = __tmp3(__tmp1, narrow)

    ret = do_events_register(__tmp1, request.client, apply_markdown, client_gravatar,
                             event_types, queue_lifespan_secs, __tmp0,
                             narrow=narrow, include_subscribers=include_subscribers,
                             fetch_event_types=fetch_event_types)
    return json_success(ret)
