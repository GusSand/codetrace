
from django.http import HttpRequest, HttpResponse
from typing import Iterable, Optional, Sequence

from zerver.lib.events import do_events_register
from zerver.lib.request import REQ, has_request_variables
from zerver.lib.response import json_success
from zerver.lib.validator import check_string, check_list, check_bool
from zerver.models import Stream, UserProfile

def _default_all_public_streams(__tmp1: UserProfile,
                                __tmp0) :
    if __tmp0 is not None:
        return __tmp0
    else:
        return __tmp1.default_all_public_streams

def __tmp3(__tmp1: <FILL>,
                    __tmp4) :
    default_stream = __tmp1.default_events_register_stream  # type: Optional[Stream]
    if not __tmp4 and default_stream is not None:
        __tmp4 = [['stream', default_stream.name]]
    return __tmp4

NarrowT = Iterable[Sequence[str]]
@has_request_variables
def __tmp2(
        request, __tmp1,
        apply_markdown: bool=REQ(default=False, validator=check_bool),
        client_gravatar: bool=REQ(default=False, validator=check_bool),
        __tmp0: Optional[bool]=REQ(default=None, validator=check_bool),
        include_subscribers: bool=REQ(default=False, validator=check_bool),
        event_types: Optional[Iterable[str]]=REQ(validator=check_list(check_string), default=None),
        fetch_event_types: Optional[Iterable[str]]=REQ(validator=check_list(check_string), default=None),
        __tmp4: NarrowT=REQ(validator=check_list(check_list(check_string, length=2)), default=[]),
        queue_lifespan_secs: int=REQ(converter=int, default=0)
) :
    __tmp0 = _default_all_public_streams(__tmp1, __tmp0)
    __tmp4 = __tmp3(__tmp1, __tmp4)

    ret = do_events_register(__tmp1, request.client, apply_markdown, client_gravatar,
                             event_types, queue_lifespan_secs, __tmp0,
                             __tmp4=__tmp4, include_subscribers=include_subscribers,
                             fetch_event_types=fetch_event_types)
    return json_success(ret)
