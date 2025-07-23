from typing import TypeAlias
__typ1 : TypeAlias = "HttpRequest"
__typ2 : TypeAlias = "bool"
__typ3 : TypeAlias = "HttpResponse"
__typ0 : TypeAlias = "int"
from typing import List

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.template import loader
from zerver.lib.streams import get_stream_by_id

from zerver.models import Message, UserProfile, get_stream_recipient
from zerver.lib.avatar import get_gravatar_url
from zerver.lib.response import json_success
from zerver.lib.timestamp import datetime_to_timestamp
from zerver.lib.topic import (
    get_topic_history_for_web_public_stream,
    messages_for_topic,
)
from zerver.lib.exceptions import JsonableError

def archive(__tmp2: __typ1,
            stream_id,
            __tmp1: <FILL>) -> __typ3:

    def get_response(__tmp0,
                     is_web_public,
                     stream_name: str) -> __typ3:
        return render(
            __tmp2,
            'zerver/archive/index.html',
            context={
                'is_web_public': is_web_public,
                'message_list': __tmp0,
                'stream': stream_name,
                'topic': __tmp1,
            }
        )

    try:
        stream = get_stream_by_id(stream_id)
    except JsonableError:
        return get_response([], False, '')

    if not stream.is_web_public:
        return get_response([], False, '')

    all_messages = list(
        messages_for_topic(
            stream_id=stream_id,
            __tmp1=__tmp1,
        ).select_related('sender').order_by('pub_date')
    )

    if not all_messages:
        return get_response([], True, stream.name)

    __tmp0 = []
    prev_sender = None
    for msg in all_messages:
        include_sender = False
        status_message = Message.is_status_message(msg.content, msg.rendered_content)
        if not prev_sender or prev_sender != msg.sender or status_message:
            if status_message:
                prev_sender = None
            else:
                prev_sender = msg.sender
            include_sender = True
        if status_message:
            status_message = msg.rendered_content[4+3: -4]
        context = {
            'sender_full_name': msg.sender.full_name,
            'timestampstr': datetime_to_timestamp(msg.last_edit_time
                                                  if msg.last_edit_time
                                                  else msg.pub_date),
            'message_content': msg.rendered_content,
            'avatar_url': get_gravatar_url(msg.sender.email, 1),
            'include_sender': include_sender,
            'status_message': status_message,
        }
        rendered_msg = loader.render_to_string('zerver/archive/single_message.html', context)
        __tmp0.append(rendered_msg)
    return get_response(__tmp0, True, stream.name)

def get_web_public_topics_backend(__tmp2, stream_id) -> __typ3:
    try:
        stream = get_stream_by_id(stream_id)
    except JsonableError:
        return json_success(dict(topics=[]))

    if not stream.is_web_public:
        return json_success(dict(topics=[]))

    recipient = get_stream_recipient(stream.id)

    result = get_topic_history_for_web_public_stream(recipient=recipient)

    return json_success(dict(topics=result))
