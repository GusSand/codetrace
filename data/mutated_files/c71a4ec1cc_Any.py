from typing import TypeAlias
__typ1 : TypeAlias = "ArgumentParser"
__typ0 : TypeAlias = "Command"

from argparse import ArgumentParser
from typing import Any

from zerver.lib.management import ZulipBaseCommand
from zerver.lib.sessions import delete_all_deactivated_user_sessions, \
    delete_all_user_sessions, delete_realm_user_sessions

class __typ0(ZulipBaseCommand):
    help = "Log out all users."

    def __tmp0(__tmp1, __tmp2) :
        __tmp2.add_argument('--deactivated-only',
                            action='store_true',
                            default=False,
                            help="Only logout all users who are deactivated")
        __tmp1.add_realm_args(__tmp2, help="Only logout all users in a particular realm")

    def handle(__tmp1, *args: <FILL>, **options) :
        realm = __tmp1.get_realm(options)
        if realm:
            delete_realm_user_sessions(realm)
        elif options["deactivated_only"]:
            delete_all_deactivated_user_sessions()
        else:
            delete_all_user_sessions()
