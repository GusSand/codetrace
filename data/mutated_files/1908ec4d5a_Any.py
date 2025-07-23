from typing import TypeAlias
__typ0 : TypeAlias = "Realm"

import logging
import sys
from argparse import ArgumentParser
from typing import Any, List, Optional

from django.core.management.base import CommandError
from django.db import connection

from zerver.lib.fix_unreads import fix
from zerver.lib.management import ZulipBaseCommand
from zerver.models import Realm, UserProfile

logging.getLogger('zulip.fix_unreads').setLevel(logging.INFO)

class Command(ZulipBaseCommand):
    help = """Fix problems related to unread counts."""

    def __tmp1(__tmp2, parser: ArgumentParser) :
        parser.add_argument('emails',
                            metavar='<emails>',
                            type=str,
                            nargs='*',
                            help='email address to spelunk')
        parser.add_argument('--all',
                            action='store_true',
                            dest='all',
                            default=False,
                            help='fix all users in specified realm')
        __tmp2.add_realm_args(parser)

    def fix_all_users(__tmp2, __tmp0: __typ0) :
        user_profiles = list(UserProfile.objects.filter(
            __tmp0=__tmp0,
            is_bot=False
        ))
        for user_profile in user_profiles:
            fix(user_profile)
            connection.commit()

    def fix_emails(__tmp2, __tmp0, emails: List[str]) :

        for email in emails:
            try:
                user_profile = __tmp2.get_user(email, __tmp0)
            except CommandError:
                print("e-mail %s doesn't exist in the realm %s, skipping" % (email, __tmp0))
                return

            fix(user_profile)
            connection.commit()

    def handle(__tmp2, *args: <FILL>, **options: Any) -> None:
        __tmp0 = __tmp2.get_realm(options)

        if options['all']:
            if __tmp0 is None:
                print('You must specify a realm if you choose the --all option.')
                sys.exit(1)

            __tmp2.fix_all_users(__tmp0)
            return

        __tmp2.fix_emails(__tmp0, options['emails'])
