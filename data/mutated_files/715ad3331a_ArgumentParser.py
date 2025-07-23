from typing import TypeAlias
__typ2 : TypeAlias = "Any"
__typ0 : TypeAlias = "Command"
__typ1 : TypeAlias = "str"

from argparse import ArgumentParser
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand

class __typ0(BaseCommand):
    help = """Send some stats to statsd."""

    def __tmp0(__tmp1, __tmp2: <FILL>) :
        __tmp2.add_argument('operation', metavar='<operation>', type=__typ1,
                            choices=['incr', 'decr', 'timing', 'timer', 'gauge'],
                            help="incr|decr|timing|timer|gauge")
        __tmp2.add_argument('name', metavar='<name>', type=__typ1)
        __tmp2.add_argument('val', metavar='<val>', type=__typ1)

    def __tmp3(__tmp1, *args: __typ2, **options) -> None:
        operation = options['operation']
        name = options['name']
        val = options['val']

        if settings.STATSD_HOST != '':
            from statsd import statsd

            func = getattr(statsd, operation)
            func(name, val)
