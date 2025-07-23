from typing import TypeAlias
__typ2 : TypeAlias = "ArgumentParser"
__typ1 : TypeAlias = "Command"
__typ0 : TypeAlias = "str"

from argparse import ArgumentParser
from typing import Any

from zerver.lib.actions import do_change_user_email
from zerver.lib.management import ZulipBaseCommand

class __typ1(ZulipBaseCommand):
    help = """Change the email address for a user."""

    def __tmp0(self, parser: __typ2) :
        self.add_realm_args(parser)
        parser.add_argument('old_email', metavar='<old email>', type=__typ0,
                            help='email address to change')
        parser.add_argument('new_email', metavar='<new email>', type=__typ0,
                            help='new email address')

    def handle(self, *args: <FILL>, **options) :
        old_email = options['old_email']
        new_email = options['new_email']

        realm = self.get_realm(options)
        user_profile = self.get_user(old_email, realm)

        do_change_user_email(user_profile, new_email)
