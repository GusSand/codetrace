import os
from typing import Any, Iterator

import ujson
from django.core.management.base import BaseCommand, CommandParser
from django.db.models import QuerySet

from zerver.lib.message import render_markdown
from zerver.models import Message

def __tmp5(__tmp2: QuerySet, chunksize: int=5000) :
    __tmp2 = __tmp2.order_by('id')
    while __tmp2.exists():
        for row in __tmp2[:chunksize]:
            msg_id = row.id
            yield row
        __tmp2 = __tmp2.filter(id__gt=msg_id)


class Command(BaseCommand):
    help = """
    Render messages to a file.
    Usage: ./manage.py render_messages <destination> [--amount=10000]
    """

    def __tmp3(__tmp0, __tmp4) -> None:
        __tmp4.add_argument('destination', help='Destination file path')
        __tmp4.add_argument('--amount', default=100000, help='Number of messages to render')
        __tmp4.add_argument('--latest_id', default=0, help="Last message id to render")

    def __tmp1(__tmp0, *args, **options: <FILL>) -> None:
        dest_dir = os.path.realpath(os.path.dirname(options['destination']))
        amount = int(options['amount'])
        latest = int(options['latest_id']) or Message.objects.latest('id').id
        __tmp0.stdout.write('Latest message id: {latest}'.format(latest=latest))
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        with open(options['destination'], 'w') as result:
            result.write('[')
            messages = Message.objects.filter(id__gt=latest - amount, id__lte=latest).order_by('id')
            for message in __tmp5(messages):
                content = message.content
                # In order to ensure that the output of this tool is
                # consistent across the time, even if messages are
                # edited, we always render the original content
                # version, extracting it from the edit history if
                # necessary.
                if message.edit_history:
                    history = ujson.loads(message.edit_history)
                    history = sorted(history, key=lambda i: i['timestamp'])
                    for entry in history:
                        if 'prev_content' in entry:
                            content = entry['prev_content']
                            break
                result.write(ujson.dumps({
                    'id': message.id,
                    'content': render_markdown(message, content)
                }))
                if message.id != latest:
                    result.write(',')
            result.write(']')
