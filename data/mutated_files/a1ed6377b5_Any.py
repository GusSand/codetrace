from typing import TypeAlias
__typ0 : TypeAlias = "Command"
from typing import Any

import ijson
from django.core.management.base import BaseCommand, CommandParser

class __typ0(BaseCommand):
    help = """
    Render messages to a file.
    Usage: ./manage.py render_messages <destination> <--amount>
    """

    def __tmp0(__tmp1, __tmp2: CommandParser) :
        __tmp2.add_argument('dump1', help='First file to compare')
        __tmp2.add_argument('dump2', help='Second file to compare')

    def handle(__tmp1, *args, **options: <FILL>) -> None:
        total_count = 0
        changed_count = 0
        with open(options['dump1'], 'r') as dump1, open(options['dump2'], 'r') as dump2:
            for m1, m2 in zip(ijson.items(dump1, 'item'), ijson.items(dump2, 'item')):
                total_count += 1
                if m1['id'] != m2['id']:
                    __tmp1.stderr.write('Inconsistent messages dump')
                    break
                if m1['content'] != m2['content']:
                    changed_count += 1
                    __tmp1.stdout.write('Changed message id: {id}'.format(id=m1['id']))
        __tmp1.stdout.write('Total messages: {count}'.format(count=total_count))
        __tmp1.stdout.write('Changed messages: {count}'.format(count=changed_count))
