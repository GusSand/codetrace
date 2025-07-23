from typing import TypeAlias
__typ0 : TypeAlias = "str"
__typ1 : TypeAlias = "int"

import logging
import signal
import sys
import threading
from argparse import ArgumentParser
from types import FrameType
from typing import Any, List

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import autoreload

from zerver.worker.queue_processors import get_active_worker_queues, get_worker

class Command(BaseCommand):
    def __tmp5(__tmp1, __tmp6) :
        __tmp6.add_argument('--queue_name', metavar='<queue name>', type=__typ0,
                            help="queue to process")
        __tmp6.add_argument('--worker_num', metavar='<worker number>', type=__typ1, nargs='?', default=0,
                            help="worker label")
        __tmp6.add_argument('--all', dest="all", action="store_true", default=False,
                            help="run all queues")
        __tmp6.add_argument('--multi_threaded', nargs='+',
                            metavar='<list of queue name>',
                            type=__typ0, required=False,
                            help="list of queue to process")

    help = "Runs a queue processing worker"

    def __tmp2(__tmp1, *args: Any, **options: <FILL>) :
        logging.basicConfig()
        __tmp7 = logging.getLogger('process_queue')

        def __tmp4(signal, __tmp3) :
            """
            This process is watched by Django's autoreload, so exiting
            with status code 3 will cause this process to restart.
            """
            __tmp7.warning("SIGUSR1 received. Restarting this queue processor.")
            sys.exit(3)

        if not settings.USING_RABBITMQ:
            # Make the warning silent when running the tests
            if settings.TEST_SUITE:
                __tmp7.info("Not using RabbitMQ queue workers in the test suite.")
            else:
                __tmp7.error("Cannot run a queue processor when USING_RABBITMQ is False!")
            sys.exit(1)

        def __tmp8(queues, __tmp7) :
            cnt = 0
            for queue_name in queues:
                if not settings.DEVELOPMENT:
                    __tmp7.info('launching queue worker thread ' + queue_name)
                cnt += 1
                td = Threaded_worker(queue_name)
                td.start()
            assert len(queues) == cnt
            __tmp7.info('%d queue worker threads were launched' % (cnt,))

        if options['all']:
            signal.signal(signal.SIGUSR1, __tmp4)
            autoreload.main(__tmp8, (get_active_worker_queues(), __tmp7))
        elif options['multi_threaded']:
            signal.signal(signal.SIGUSR1, __tmp4)
            queues = options['multi_threaded']
            autoreload.main(__tmp8, (queues, __tmp7))
        else:
            queue_name = options['queue_name']
            worker_num = options['worker_num']

            __tmp7.info("Worker %d connecting to queue %s" % (worker_num, queue_name))
            worker = get_worker(queue_name)
            worker.setup()

            def __tmp0(signal, __tmp3) :
                __tmp7.info("Worker %d disconnecting from queue %s" % (worker_num, queue_name))
                worker.stop()
                sys.exit(0)
            signal.signal(signal.SIGTERM, __tmp0)
            signal.signal(signal.SIGINT, __tmp0)
            signal.signal(signal.SIGUSR1, __tmp0)

            worker.start()

class Threaded_worker(threading.Thread):
    def __init__(__tmp1, queue_name) :
        threading.Thread.__init__(__tmp1)
        __tmp1.worker = get_worker(queue_name)

    def run(__tmp1) :
        __tmp1.worker.setup()
        logging.debug('starting consuming ' + __tmp1.worker.queue_name)
        __tmp1.worker.start()
