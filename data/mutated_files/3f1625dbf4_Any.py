from typing import TypeAlias
__typ1 : TypeAlias = "ArgumentParser"
__typ0 : TypeAlias = "Command"
import os
import time
from argparse import ArgumentParser
from typing import Any, Dict

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from django.utils.timezone import now as timezone_now
from django.utils.timezone import utc as timezone_utc

from analytics.lib.counts import COUNT_STATS, logger, process_count_stat
from scripts.lib.zulip_tools import ENDC, WARNING
from zerver.lib.timestamp import floor_to_hour
from zerver.models import Realm

class __typ0(BaseCommand):
    help = """Fills Analytics tables.

    Run as a cron job that runs every hour."""

    def add_arguments(__tmp0, __tmp1: __typ1) -> None:
        __tmp1.add_argument('--time', '-t',
                            type=str,
                            help='Update stat tables from current state to'
                                 '--time. Defaults to the current time.',
                            default=timezone_now().isoformat())
        __tmp1.add_argument('--utc',
                            action='store_true',
                            help="Interpret --time in UTC.",
                            default=False)
        __tmp1.add_argument('--stat', '-s',
                            type=str,
                            help="CountStat to process. If omitted, all stats are processed.")
        __tmp1.add_argument('--verbose',
                            action='store_true',
                            help="Print timing information to stdout.",
                            default=False)

    def handle(__tmp0, *args: <FILL>, **options: Any) :
        try:
            os.mkdir(settings.ANALYTICS_LOCK_DIR)
        except OSError:
            print(WARNING + "Analytics lock %s is unavailable; exiting... " + ENDC)
            return

        try:
            __tmp0.run_update_analytics_counts(options)
        finally:
            os.rmdir(settings.ANALYTICS_LOCK_DIR)

    def run_update_analytics_counts(__tmp0, options) -> None:
        # installation_epoch relies on there being at least one realm; we
        # shouldn't run the analytics code if that condition isn't satisfied
        if not Realm.objects.exists():
            logger.info("No realms, stopping update_analytics_counts")
            return

        fill_to_time = parse_datetime(options['time'])
        if options['utc']:
            fill_to_time = fill_to_time.replace(tzinfo=timezone_utc)
        if fill_to_time.tzinfo is None:
            raise ValueError("--time must be timezone aware. Maybe you meant to use the --utc option?")

        fill_to_time = floor_to_hour(fill_to_time.astimezone(timezone_utc))

        if options['stat'] is not None:
            stats = [COUNT_STATS[options['stat']]]
        else:
            stats = list(COUNT_STATS.values())

        logger.info("Starting updating analytics counts through %s" % (fill_to_time,))
        if options['verbose']:
            start = time.time()
            last = start

        for stat in stats:
            process_count_stat(stat, fill_to_time)
            if options['verbose']:
                print("Updated %s in %.3fs" % (stat.property, time.time() - last))
                last = time.time()

        if options['verbose']:
            print("Finished updating analytics counts through %s in %.3fs" %
                  (fill_to_time, time.time() - start))
        logger.info("Finished updating analytics counts through %s" % (fill_to_time,))
