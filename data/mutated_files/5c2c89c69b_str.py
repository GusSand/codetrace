from typing import TypeAlias
__typ2 : TypeAlias = "Any"
__typ1 : TypeAlias = "ArgumentParser"
__typ0 : TypeAlias = "Command"

from argparse import ArgumentParser
from typing import Any

from zerver.lib.actions import do_change_user_email
from zerver.lib.management import ZulipBaseCommand

class __typ0(ZulipBaseCommand):
    help = """Change the email address for a user."""

    def add_arguments(__tmp0, __tmp1: __typ1) -> None:
        __tmp0.add_realm_args(__tmp1)
        __tmp1.add_argument('old_email', metavar='<old email>', type=str,
                            help='email address to change')
        __tmp1.add_argument('new_email', metavar='<new email>', type=str,
                            help='new email address')

    def __tmp2(__tmp0, *args, **options: <FILL>) -> None:
        old_email = options['old_email']
        new_email = options['new_email']

        realm = __tmp0.get_realm(options)
        user_profile = __tmp0.get_user(old_email, realm)

        do_change_user_email(user_profile, new_email)
