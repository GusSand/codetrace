from typing import TypeAlias
__typ2 : TypeAlias = "Any"
__typ0 : TypeAlias = "Command"
__typ1 : TypeAlias = "str"

from argparse import ArgumentParser
from typing import Any

from zerver.lib.actions import do_change_user_email
from zerver.lib.management import ZulipBaseCommand

class __typ0(ZulipBaseCommand):
    help = """Change the email address for a user."""

    def __tmp0(__tmp1, parser: <FILL>) :
        __tmp1.add_realm_args(parser)
        parser.add_argument('old_email', metavar='<old email>', type=__typ1,
                            help='email address to change')
        parser.add_argument('new_email', metavar='<new email>', type=__typ1,
                            help='new email address')

    def __tmp2(__tmp1, *args, **options: __typ1) :
        old_email = options['old_email']
        new_email = options['new_email']

        realm = __tmp1.get_realm(options)
        user_profile = __tmp1.get_user(old_email, realm)

        do_change_user_email(user_profile, new_email)
