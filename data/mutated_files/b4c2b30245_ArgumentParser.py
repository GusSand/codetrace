from typing import TypeAlias
__typ1 : TypeAlias = "Any"
__typ0 : TypeAlias = "Command"
import sys
from argparse import ArgumentParser
from typing import Any

from django.core.management.base import BaseCommand

from analytics.lib.counts import do_drop_all_analytics_tables

class __typ0(BaseCommand):
    help = """Clear analytics tables."""

    def add_arguments(__tmp0, parser: <FILL>) :
        parser.add_argument('--force',
                            action='store_true',
                            help="Clear analytics tables.")

    def handle(__tmp0, *args: __typ1, **options: __typ1) :
        if options['force']:
            do_drop_all_analytics_tables()
        else:
            print("Would delete all data from analytics tables (!); use --force to do so.")
            sys.exit(1)
