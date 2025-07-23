from typing import TypeAlias
__typ2 : TypeAlias = "Realm"
__typ1 : TypeAlias = "ArgumentParser"
__typ0 : TypeAlias = "Command"

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

class __typ0(ZulipBaseCommand):
    help = """Fix problems related to unread counts."""

    def __tmp0(__tmp1, parser: __typ1) -> None:
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
        __tmp1.add_realm_args(parser)

    def fix_all_users(__tmp1, realm) -> None:
        user_profiles = list(UserProfile.objects.filter(
            realm=realm,
            is_bot=False
        ))
        for user_profile in user_profiles:
            fix(user_profile)
            connection.commit()

    def fix_emails(__tmp1, realm: Optional[__typ2], emails: List[str]) :

        for email in emails:
            try:
                user_profile = __tmp1.get_user(email, realm)
            except CommandError:
                print("e-mail %s doesn't exist in the realm %s, skipping" % (email, realm))
                return

            fix(user_profile)
            connection.commit()

    def handle(__tmp1, *args: Any, **options: <FILL>) -> None:
        realm = __tmp1.get_realm(options)

        if options['all']:
            if realm is None:
                print('You must specify a realm if you choose the --all option.')
                sys.exit(1)

            __tmp1.fix_all_users(realm)
            return

        __tmp1.fix_emails(realm, options['emails'])
