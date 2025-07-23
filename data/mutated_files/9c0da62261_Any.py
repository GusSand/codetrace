from typing import TypeAlias
__typ1 : TypeAlias = "ArgumentParser"
__typ0 : TypeAlias = "Command"
import sys
from argparse import ArgumentParser
from typing import Any

from django.core.management.base import BaseCommand

from analytics.lib.counts import COUNT_STATS, do_drop_single_stat

class __typ0(BaseCommand):
    help = """Clear analytics tables."""

    def __tmp0(__tmp1, parser: __typ1) -> None:
        parser.add_argument('--force',
                            action='store_true',
                            help="Actually do it.")
        parser.add_argument('--property',
                            type=str,
                            help="The property of the stat to be cleared.")

    def handle(__tmp1, *args: <FILL>, **options) -> None:
        property = options['property']
        if property not in COUNT_STATS:
            print("Invalid property: %s" % (property,))
            sys.exit(1)
        if not options['force']:
            print("No action taken. Use --force.")
            sys.exit(1)

        do_drop_single_stat(property)
