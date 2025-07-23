from typing import TypeAlias
__typ0 : TypeAlias = "Command"
__typ1 : TypeAlias = "str"

import sys
from argparse import ArgumentParser
from typing import IO, Any

import ujson
from django.core.management.base import BaseCommand

from zerver.lib.queue import queue_json_publish

def __tmp0(*args: Any) -> None:
    raise Exception('We cannot enqueue because settings.USING_RABBITMQ is False.')

class __typ0(BaseCommand):
    help = """Read JSON lines from a file and enqueue them to a worker queue.

Each line in the file should either be a JSON payload or two tab-separated
fields, the second of which is a JSON payload.  (The latter is to accommodate
the format of error files written by queue workers that catch exceptions--their
first field is a timestamp that we ignore.)

You can use "-" to represent stdin.
"""

    def __tmp1(self, parser: ArgumentParser) :
        parser.add_argument('queue_name', metavar='<queue>', type=__typ1,
                            help="name of worker queue to enqueue to")
        parser.add_argument('file_name', metavar='<file>', type=__typ1,
                            help="name of file containing JSON lines")

    def handle(self, *args: <FILL>, **options: __typ1) :
        queue_name = options['queue_name']
        file_name = options['file_name']

        if file_name == '-':
            f = sys.stdin  # type: IO[str]
        else:
            f = open(file_name)

        while True:
            line = f.readline()
            if not line:
                break

            line = line.strip()
            try:
                payload = line.split('\t')[1]
            except IndexError:
                payload = line

            print('Queueing to queue %s: %s' % (queue_name, payload))

            # Verify that payload is valid json.
            data = ujson.loads(payload)

            # This is designed to use the `error` method rather than
            # the call_consume_in_tests flow.
            queue_json_publish(queue_name, data, __tmp0)
