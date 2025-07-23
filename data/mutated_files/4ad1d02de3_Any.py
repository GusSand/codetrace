from typing import TypeAlias
__typ2 : TypeAlias = "ArgumentParser"
__typ1 : TypeAlias = "Command"
__typ0 : TypeAlias = "str"

from argparse import ArgumentParser
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand

class __typ1(BaseCommand):
    help = """Send some stats to statsd."""

    def __tmp0(__tmp1, parser) :
        parser.add_argument('operation', metavar='<operation>', type=__typ0,
                            choices=['incr', 'decr', 'timing', 'timer', 'gauge'],
                            help="incr|decr|timing|timer|gauge")
        parser.add_argument('name', metavar='<name>', type=__typ0)
        parser.add_argument('val', metavar='<val>', type=__typ0)

    def handle(__tmp1, *args: <FILL>, **options) :
        operation = options['operation']
        name = options['name']
        val = options['val']

        if settings.STATSD_HOST != '':
            from statsd import statsd

            func = getattr(statsd, operation)
            func(name, val)
