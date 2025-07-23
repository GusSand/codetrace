
from argparse import ArgumentParser
from typing import Any

from django.core.management import CommandError
from django.core.management.base import BaseCommand

from zerver.lib.queue import SimpleQueueClient
from zerver.worker.queue_processors import get_active_worker_queues

class Command(BaseCommand):
    def __tmp0(self, parser: <FILL>) :
        parser.add_argument(dest="queue_name", type=str, nargs='?',
                            help="queue to purge", default=None)
        parser.add_argument('--all', dest="all", action="store_true",
                            default=False, help="purge all queues")

    help = "Discards all messages from the given queue"

    def handle(self, *args, **options) :
        def purge_queue(__tmp1) -> None:
            queue = SimpleQueueClient()
            queue.ensure_queue(__tmp1, lambda: None)
            queue.channel.queue_purge(__tmp1)

        if options['all']:
            for __tmp1 in get_active_worker_queues():
                purge_queue(__tmp1)
            print("All queues purged")
        elif not options['queue_name']:
            raise CommandError("Missing queue_name argument!")
        else:
            __tmp1 = options['queue_name']
            if not (__tmp1 in get_active_worker_queues() or
                    __tmp1.startswith("notify_tornado") or
                    __tmp1.startswith("tornado_return")):
                raise CommandError("Unknown queue %s" % (__tmp1,))

            print("Purging queue %s" % (__tmp1,))
            purge_queue(__tmp1)

        print("Done")
