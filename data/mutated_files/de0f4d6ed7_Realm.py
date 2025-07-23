from typing import TypeAlias
__typ0 : TypeAlias = "ArgumentParser"

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

    def __tmp3(__tmp0, __tmp4: __typ0) -> None:
        __tmp4.add_argument('emails',
                            metavar='<emails>',
                            type=str,
                            nargs='*',
                            help='email address to spelunk')
        __tmp4.add_argument('--all',
                            action='store_true',
                            dest='all',
                            default=False,
                            help='fix all users in specified realm')
        __tmp0.add_realm_args(__tmp4)

    def fix_all_users(__tmp0, __tmp2: <FILL>) :
        user_profiles = list(UserProfile.objects.filter(
            __tmp2=__tmp2,
            is_bot=False
        ))
        for user_profile in user_profiles:
            fix(user_profile)
            connection.commit()

    def fix_emails(__tmp0, __tmp2: Optional[Realm], __tmp1: List[str]) -> None:

        for email in __tmp1:
            try:
                user_profile = __tmp0.get_user(email, __tmp2)
            except CommandError:
                print("e-mail %s doesn't exist in the realm %s, skipping" % (email, __tmp2))
                return

            fix(user_profile)
            connection.commit()

    def handle(__tmp0, *args: Any, **options: Any) -> None:
        __tmp2 = __tmp0.get_realm(options)

        if options['all']:
            if __tmp2 is None:
                print('You must specify a realm if you choose the --all option.')
                sys.exit(1)

            __tmp0.fix_all_users(__tmp2)
            return

        __tmp0.fix_emails(__tmp2, options['emails'])
