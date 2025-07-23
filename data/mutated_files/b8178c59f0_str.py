from typing import TypeAlias
__typ0 : TypeAlias = "Selectable"
__typ2 : TypeAlias = "UserProfile"
__typ1 : TypeAlias = "int"
__typ3 : TypeAlias = "bool"
from typing import Any, Callable, Dict, List, Optional

from zerver.lib.topic import (
    topic_match_sa,
)
from zerver.models import (
    get_stream_recipient,
    get_stream,
    MutedTopic,
    UserProfile
)
from sqlalchemy.sql import (
    and_,
    column,
    not_,
    or_,
    Selectable
)

def __tmp1(__tmp2) :
    rows = MutedTopic.objects.filter(
        __tmp2=__tmp2,
    ).values(
        'stream__name',
        'topic_name'
    )
    return [
        [__tmp4['stream__name'], __tmp4['topic_name']]
        for __tmp4 in rows
    ]

def __tmp6(__tmp2, __tmp8) :

    '''
    This is only used in tests.
    '''

    MutedTopic.objects.filter(
        __tmp2=__tmp2,
    ).delete()

    for stream_name, __tmp7 in __tmp8:
        stream = get_stream(stream_name, __tmp2.realm)
        recipient = get_stream_recipient(stream.id)

        __tmp12(
            __tmp2=__tmp2,
            __tmp3=stream.id,
            __tmp13=recipient.id,
            __tmp7=__tmp7,
        )

def __tmp12(__tmp2, __tmp3: __typ1, __tmp13: __typ1, __tmp7) :
    MutedTopic.objects.create(
        __tmp2=__tmp2,
        __tmp3=__tmp3,
        __tmp13=__tmp13,
        __tmp7=__tmp7,
    )

def __tmp10(__tmp2, __tmp3, __tmp7: <FILL>) :
    __tmp4 = MutedTopic.objects.get(
        __tmp2=__tmp2,
        __tmp3=__tmp3,
        topic_name__iexact=__tmp7
    )
    __tmp4.delete()

def __tmp9(__tmp2: __typ2, __tmp3, __tmp7: str) :
    __tmp5 = MutedTopic.objects.filter(
        __tmp2=__tmp2,
        __tmp3=__tmp3,
        topic_name__iexact=__tmp7,
    ).exists()
    return __tmp5

def __tmp11(conditions,
                        __tmp2,
                        __tmp3: Optional[__typ1]) :
    query = MutedTopic.objects.filter(
        __tmp2=__tmp2,
    )

    if __tmp3 is not None:
        # If we are narrowed to a stream, we can optimize the query
        # by not considering topic mutes outside the stream.
        query = query.filter(__tmp3=__tmp3)

    query = query.values(
        'recipient_id',
        'topic_name'
    )
    rows = list(query)

    if not rows:
        return conditions

    def __tmp0(__tmp4) -> __typ0:
        __tmp13 = __tmp4['recipient_id']
        __tmp7 = __tmp4['topic_name']
        stream_cond = column("recipient_id") == __tmp13
        topic_cond = topic_match_sa(__tmp7)
        return and_(stream_cond, topic_cond)

    condition = not_(or_(*list(map(__tmp0, rows))))
    return conditions + [condition]

def build_topic_mute_checker(__tmp2: __typ2) -> Callable[[__typ1, str], __typ3]:
    rows = MutedTopic.objects.filter(
        __tmp2=__tmp2,
    ).values(
        'recipient_id',
        'topic_name'
    )
    rows = list(rows)

    tups = set()
    for __tmp4 in rows:
        __tmp13 = __tmp4['recipient_id']
        __tmp7 = __tmp4['topic_name']
        tups.add((__tmp13, __tmp7.lower()))

    def __tmp5(__tmp13, topic: str) :
        return (__tmp13, topic.lower()) in tups

    return __tmp5
