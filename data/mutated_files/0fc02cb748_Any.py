
import logging
import sys
from typing import Any, Iterable

from django.core.management.base import CommandParser
from django.db import models

from zerver.lib import utils
from zerver.lib.management import ZulipBaseCommand
from zerver.models import UserMessage

class Command(ZulipBaseCommand):
    help = """Sets user message flags. Used internally by actions.py. Marks all
    Expects a comma-delimited list of user message ids via stdin, and an EOF to terminate."""

    def __tmp3(__tmp0, __tmp4) -> None:
        __tmp4.add_argument('-l', '--for-real',
                            dest='for_real',
                            action='store_true',
                            default=False,
                            help="Actually change message flags. Default is a dry run.")

        __tmp4.add_argument('-f', '--flag',
                            dest='flag',
                            type=str,
                            help="The flag to add of remove")

        __tmp4.add_argument('-o', '--op',
                            dest='op',
                            type=str,
                            help="The operation to do: 'add' or 'remove'")

        __tmp4.add_argument('-u', '--until',
                            dest='all_until',
                            type=str,
                            help="Mark all messages <= specific usermessage id")

        __tmp4.add_argument('-m', '--email',
                            dest='email',
                            type=str,
                            help="Email to set messages for")
        __tmp0.add_realm_args(__tmp4)

    def __tmp2(__tmp0, *args, **options: <FILL>) -> None:
        if not options["flag"] or not options["op"] or not options["email"]:
            print("Please specify an operation, a flag and an email")
            exit(1)

        op = options['op']
        flag = getattr(UserMessage.flags, options['flag'])
        all_until = options['all_until']
        email = options['email']

        realm = __tmp0.get_realm(options)
        user_profile = __tmp0.get_user(email, realm)

        if all_until:
            filt = models.Q(id__lte=all_until)
        else:
            filt = models.Q(message__id__in=[mid.strip() for mid in sys.stdin.read().split(',')])
        mids = [m.id for m in
                UserMessage.objects.filter(filt, user_profile=user_profile).order_by('-id')]

        if options["for_real"]:
            sys.stdin.close()
            sys.stdout.close()
            sys.stderr.close()

        def __tmp5(__tmp1) -> None:
            msgs = UserMessage.objects.filter(id__in=__tmp1)
            if op == 'add':
                msgs.update(flags=models.F('flags').bitor(flag))
            elif op == 'remove':
                msgs.update(flags=models.F('flags').bitand(~flag))

        if not options["for_real"]:
            logging.info("Updating %s by %s %s" % (mids, op, flag))
            logging.info("Dry run completed. Run with --for-real to change message flags.")
            exit(1)

        utils.run_in_batches(mids, 400, __tmp5, sleep_time=3)
        exit(0)
