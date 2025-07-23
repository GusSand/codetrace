from typing import TypeAlias
__typ0 : TypeAlias = "ArgumentParser"
import sys
from argparse import ArgumentParser
from typing import Any

from django.core.management.base import BaseCommand

from analytics.lib.counts import do_drop_all_analytics_tables

class Command(BaseCommand):
    help = """Clear analytics tables."""

    def add_arguments(__tmp0, parser: __typ0) :
        parser.add_argument('--force',
                            action='store_true',
                            help="Clear analytics tables.")

    def handle(__tmp0, *args: <FILL>, **options: Any) -> None:
        if options['force']:
            do_drop_all_analytics_tables()
        else:
            print("Would delete all data from analytics tables (!); use --force to do so.")
            sys.exit(1)
