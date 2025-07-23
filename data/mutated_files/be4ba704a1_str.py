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

def get_topic_mutes(__tmp1) -> List[List[str]]:
    rows = MutedTopic.objects.filter(
        __tmp1=__tmp1,
    ).values(
        'stream__name',
        'topic_name'
    )
    return [
        [__tmp3['stream__name'], __tmp3['topic_name']]
        for __tmp3 in rows
    ]

def __tmp8(__tmp1, __tmp7) :

    '''
    This is only used in tests.
    '''

    MutedTopic.objects.filter(
        __tmp1=__tmp1,
    ).delete()

    for stream_name, __tmp6 in __tmp7:
        stream = get_stream(stream_name, __tmp1.realm)
        recipient = get_stream_recipient(stream.id)

        __tmp11(
            __tmp1=__tmp1,
            __tmp2=stream.id,
            __tmp12=recipient.id,
            __tmp6=__tmp6,
        )

def __tmp11(__tmp1, __tmp2, __tmp12, __tmp6) :
    MutedTopic.objects.create(
        __tmp1=__tmp1,
        __tmp2=__tmp2,
        __tmp12=__tmp12,
        __tmp6=__tmp6,
    )

def __tmp9(__tmp1, __tmp2: __typ1, __tmp6) :
    __tmp3 = MutedTopic.objects.get(
        __tmp1=__tmp1,
        __tmp2=__tmp2,
        topic_name__iexact=__tmp6
    )
    __tmp3.delete()

def topic_is_muted(__tmp1, __tmp2, __tmp6: str) -> __typ3:
    __tmp5 = MutedTopic.objects.filter(
        __tmp1=__tmp1,
        __tmp2=__tmp2,
        topic_name__iexact=__tmp6,
    ).exists()
    return __tmp5

def exclude_topic_mutes(__tmp10,
                        __tmp1,
                        __tmp2) :
    query = MutedTopic.objects.filter(
        __tmp1=__tmp1,
    )

    if __tmp2 is not None:
        # If we are narrowed to a stream, we can optimize the query
        # by not considering topic mutes outside the stream.
        query = query.filter(__tmp2=__tmp2)

    query = query.values(
        'recipient_id',
        'topic_name'
    )
    rows = list(query)

    if not rows:
        return __tmp10

    def __tmp0(__tmp3) :
        __tmp12 = __tmp3['recipient_id']
        __tmp6 = __tmp3['topic_name']
        stream_cond = column("recipient_id") == __tmp12
        topic_cond = topic_match_sa(__tmp6)
        return and_(stream_cond, topic_cond)

    condition = not_(or_(*list(map(__tmp0, rows))))
    return __tmp10 + [condition]

def __tmp4(__tmp1) :
    rows = MutedTopic.objects.filter(
        __tmp1=__tmp1,
    ).values(
        'recipient_id',
        'topic_name'
    )
    rows = list(rows)

    tups = set()
    for __tmp3 in rows:
        __tmp12 = __tmp3['recipient_id']
        __tmp6 = __tmp3['topic_name']
        tups.add((__tmp12, __tmp6.lower()))

    def __tmp5(__tmp12, topic: <FILL>) :
        return (__tmp12, topic.lower()) in tups

    return __tmp5
