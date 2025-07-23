from typing import TypeAlias
__typ0 : TypeAlias = "HttpRequest"
__typ1 : TypeAlias = "bool"

from django.http import HttpRequest, HttpResponse
from typing import Iterable, Optional, Sequence

from zerver.lib.events import do_events_register
from zerver.lib.request import REQ, has_request_variables
from zerver.lib.response import json_success
from zerver.lib.validator import check_string, check_list, check_bool
from zerver.models import Stream, UserProfile

def _default_all_public_streams(__tmp0: <FILL>,
                                all_public_streams: Optional[__typ1]) -> __typ1:
    if all_public_streams is not None:
        return all_public_streams
    else:
        return __tmp0.default_all_public_streams

def __tmp2(__tmp0: UserProfile,
                    narrow: Iterable[Sequence[str]]) -> Iterable[Sequence[str]]:
    default_stream = __tmp0.default_events_register_stream  # type: Optional[Stream]
    if not narrow and default_stream is not None:
        narrow = [['stream', default_stream.name]]
    return narrow

NarrowT = Iterable[Sequence[str]]
@has_request_variables
def __tmp1(
        request: __typ0, __tmp0: UserProfile,
        apply_markdown: __typ1=REQ(default=False, validator=check_bool),
        client_gravatar: __typ1=REQ(default=False, validator=check_bool),
        all_public_streams: Optional[__typ1]=REQ(default=None, validator=check_bool),
        include_subscribers: __typ1=REQ(default=False, validator=check_bool),
        event_types: Optional[Iterable[str]]=REQ(validator=check_list(check_string), default=None),
        fetch_event_types: Optional[Iterable[str]]=REQ(validator=check_list(check_string), default=None),
        narrow: NarrowT=REQ(validator=check_list(check_list(check_string, length=2)), default=[]),
        queue_lifespan_secs: int=REQ(converter=int, default=0)
) :
    all_public_streams = _default_all_public_streams(__tmp0, all_public_streams)
    narrow = __tmp2(__tmp0, narrow)

    ret = do_events_register(__tmp0, request.client, apply_markdown, client_gravatar,
                             event_types, queue_lifespan_secs, all_public_streams,
                             narrow=narrow, include_subscribers=include_subscribers,
                             fetch_event_types=fetch_event_types)
    return json_success(ret)
