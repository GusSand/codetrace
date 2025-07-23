from typing import MutableMapping, Any, Optional, List, Tuple
from django.conf import settings

import re
import json

from zerver.models import SubMessage


def get_widget_data(content: <FILL>) :
    valid_widget_types = ['tictactoe', 'poll', 'todo']
    tokens = content.split(' ')

    # tokens[0] will always exist
    if tokens[0].startswith('/'):
        __tmp0 = tokens[0][1:]
        if __tmp0 in valid_widget_types:
            extra_data = get_extra_data_from_widget_type(tokens, __tmp0)
            return __tmp0, extra_data

    return None, None

def get_extra_data_from_widget_type(tokens,
                                    __tmp0: Optional[str]) -> Any:
    if __tmp0 == 'poll':
        # This is used to extract the question from the poll command.
        # The command '/poll question' will pre-set the question in the poll
        question = ' '.join(tokens[1:])
        if not question:
            question = ''
        extra_data = {'question': question}
        return extra_data
    return None

def do_widget_post_save_actions(message) -> None:
    '''
    This is experimental code that only works with the
    webapp for now.
    '''
    if not settings.ALLOW_SUB_MESSAGES:
        return
    content = message['message'].content
    sender_id = message['message'].sender_id
    message_id = message['message'].id

    __tmp0 = None
    extra_data = None

    __tmp0, extra_data = get_widget_data(content)
    widget_content = message.get('widget_content')
    if widget_content is not None:
        # Note that we validate this data in check_message,
        # so we can trust it here.
        __tmp0 = widget_content['widget_type']
        extra_data = widget_content['extra_data']

    if __tmp0:
        content = dict(
            __tmp0=__tmp0,
            extra_data=extra_data
        )
        submessage = SubMessage(
            sender_id=sender_id,
            message_id=message_id,
            msg_type='widget',
            content=json.dumps(content),
        )
        submessage.save()
        message['submessages'] = SubMessage.get_raw_db_rows([message_id])
