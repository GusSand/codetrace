from typing import TypeAlias
__typ0 : TypeAlias = "int"
__typ1 : TypeAlias = "bool"
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

def get_topic_mutes(__tmp0) :
    rows = MutedTopic.objects.filter(
        __tmp0=__tmp0,
    ).values(
        'stream__name',
        'topic_name'
    )
    return [
        [__tmp2['stream__name'], __tmp2['topic_name']]
        for __tmp2 in rows
    ]

def set_topic_mutes(__tmp0, muted_topics) :

    '''
    This is only used in tests.
    '''

    MutedTopic.objects.filter(
        __tmp0=__tmp0,
    ).delete()

    for stream_name, __tmp3 in muted_topics:
        stream = get_stream(stream_name, __tmp0.realm)
        recipient = get_stream_recipient(stream.id)

        add_topic_mute(
            __tmp0=__tmp0,
            __tmp1=stream.id,
            __tmp6=recipient.id,
            __tmp3=__tmp3,
        )

def add_topic_mute(__tmp0: <FILL>, __tmp1, __tmp6, __tmp3) :
    MutedTopic.objects.create(
        __tmp0=__tmp0,
        __tmp1=__tmp1,
        __tmp6=__tmp6,
        __tmp3=__tmp3,
    )

def remove_topic_mute(__tmp0, __tmp1, __tmp3: str) :
    __tmp2 = MutedTopic.objects.get(
        __tmp0=__tmp0,
        __tmp1=__tmp1,
        topic_name__iexact=__tmp3
    )
    __tmp2.delete()

def __tmp4(__tmp0: UserProfile, __tmp1, __tmp3) :
    is_muted = MutedTopic.objects.filter(
        __tmp0=__tmp0,
        __tmp1=__tmp1,
        topic_name__iexact=__tmp3,
    ).exists()
    return is_muted

def __tmp5(conditions,
                        __tmp0,
                        __tmp1) :
    query = MutedTopic.objects.filter(
        __tmp0=__tmp0,
    )

    if __tmp1 is not None:
        # If we are narrowed to a stream, we can optimize the query
        # by not considering topic mutes outside the stream.
        query = query.filter(__tmp1=__tmp1)

    query = query.values(
        'recipient_id',
        'topic_name'
    )
    rows = list(query)

    if not rows:
        return conditions

    def mute_cond(__tmp2) :
        __tmp6 = __tmp2['recipient_id']
        __tmp3 = __tmp2['topic_name']
        stream_cond = column("recipient_id") == __tmp6
        topic_cond = topic_match_sa(__tmp3)
        return and_(stream_cond, topic_cond)

    condition = not_(or_(*list(map(mute_cond, rows))))
    return conditions + [condition]

def build_topic_mute_checker(__tmp0) :
    rows = MutedTopic.objects.filter(
        __tmp0=__tmp0,
    ).values(
        'recipient_id',
        'topic_name'
    )
    rows = list(rows)

    tups = set()
    for __tmp2 in rows:
        __tmp6 = __tmp2['recipient_id']
        __tmp3 = __tmp2['topic_name']
        tups.add((__tmp6, __tmp3.lower()))

    def is_muted(__tmp6, topic) :
        return (__tmp6, topic.lower()) in tups

    return is_muted
