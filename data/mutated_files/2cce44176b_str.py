from typing import TypeAlias
__typ0 : TypeAlias = "ArgumentParser"
__typ1 : TypeAlias = "Any"

from argparse import ArgumentParser
from typing import Any

from django.core.management import CommandError
from django.core.management.base import BaseCommand

from zerver.lib.queue import SimpleQueueClient
from zerver.worker.queue_processors import get_active_worker_queues

class Command(BaseCommand):
    def __tmp2(__tmp0, __tmp5: __typ0) -> None:
        __tmp5.add_argument(dest="queue_name", type=str, nargs='?',
                            help="queue to purge", default=None)
        __tmp5.add_argument('--all', dest="all", action="store_true",
                            default=False, help="purge all queues")

    help = "Discards all messages from the given queue"

    def __tmp1(__tmp0, *args, **options: str) -> None:
        def __tmp4(__tmp3: <FILL>) :
            queue = SimpleQueueClient()
            queue.ensure_queue(__tmp3, lambda: None)
            queue.channel.queue_purge(__tmp3)

        if options['all']:
            for __tmp3 in get_active_worker_queues():
                __tmp4(__tmp3)
            print("All queues purged")
        elif not options['queue_name']:
            raise CommandError("Missing queue_name argument!")
        else:
            __tmp3 = options['queue_name']
            if not (__tmp3 in get_active_worker_queues() or
                    __tmp3.startswith("notify_tornado") or
                    __tmp3.startswith("tornado_return")):
                raise CommandError("Unknown queue %s" % (__tmp3,))

            print("Purging queue %s" % (__tmp3,))
            __tmp4(__tmp3)

        print("Done")
