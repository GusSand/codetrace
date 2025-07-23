from typing import TypeAlias
__typ2 : TypeAlias = "Any"
__typ1 : TypeAlias = "ArgumentParser"
__typ0 : TypeAlias = "Command"

from argparse import ArgumentParser
from typing import Any

from django.core.management import CommandError
from django.core.management.base import BaseCommand

from zerver.lib.queue import SimpleQueueClient
from zerver.worker.queue_processors import get_active_worker_queues

class __typ0(BaseCommand):
    def add_arguments(__tmp0, parser: __typ1) -> None:
        parser.add_argument(dest="queue_name", type=str, nargs='?',
                            help="queue to purge", default=None)
        parser.add_argument('--all', dest="all", action="store_true",
                            default=False, help="purge all queues")

    help = "Discards all messages from the given queue"

    def __tmp1(__tmp0, *args, **options: <FILL>) :
        def purge_queue(queue_name: str) :
            queue = SimpleQueueClient()
            queue.ensure_queue(queue_name, lambda: None)
            queue.channel.queue_purge(queue_name)

        if options['all']:
            for queue_name in get_active_worker_queues():
                purge_queue(queue_name)
            print("All queues purged")
        elif not options['queue_name']:
            raise CommandError("Missing queue_name argument!")
        else:
            queue_name = options['queue_name']
            if not (queue_name in get_active_worker_queues() or
                    queue_name.startswith("notify_tornado") or
                    queue_name.startswith("tornado_return")):
                raise CommandError("Unknown queue %s" % (queue_name,))

            print("Purging queue %s" % (queue_name,))
            purge_queue(queue_name)

        print("Done")
