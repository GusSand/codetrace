#!/usr/bin/env python3

from faceanalysis.api import app as application
from faceanalysis.log import get_logger
from faceanalysis.models import delete_models
from faceanalysis.models import init_models
from faceanalysis.settings import FACE_VECTORIZE_ALGORITHM
from faceanalysis.settings import IMAGE_PROCESSOR_CONCURRENCY
from faceanalysis.settings import IMAGE_PROCESSOR_QUEUE
from faceanalysis.settings import LOGGING_LEVEL
from faceanalysis.tasks import celery

logger = get_logger(__name__)


class __typ0:
    @classmethod
    def __tmp4(__tmp0):
        if FACE_VECTORIZE_ALGORITHM == 'FaceApi':
            logger.warning('FaceApi backend detected: not starting worker')
            return

        celery.worker_main([
            '--queues={}'.format(IMAGE_PROCESSOR_QUEUE),
            '--concurrency={}'.format(IMAGE_PROCESSOR_CONCURRENCY),
            '--loglevel={}'.format(LOGGING_LEVEL),
            '-Ofair',
        ])

    @classmethod
    def runserver(__tmp0):
        application.run()

    @classmethod
    def __tmp5(__tmp0):
        init_models()

    @classmethod
    def __tmp2(__tmp0):
        delete_models()


def __tmp1(command: <FILL>):
    command = getattr(__typ0, command)
    command()


def __tmp3():
    from argparse import ArgumentParser
    from inspect import getmembers
    from inspect import ismethod

    all_commands = [name for name, _ in
                    getmembers(__typ0, predicate=ismethod)]

    parser = ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=all_commands)
    args = parser.parse_args()

    __tmp1(args.command)


if __name__ == '__main__':
    __tmp3()
