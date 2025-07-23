from typing import TypeAlias
__typ1 : TypeAlias = "Any"
__typ0 : TypeAlias = "Command"

from argparse import ArgumentParser
from typing import Any

from django.core.management.base import CommandError

from zerver.lib.actions import do_change_full_name
from zerver.lib.management import ZulipBaseCommand

class __typ0(ZulipBaseCommand):
    help = """Change the names for many users."""

    def __tmp0(__tmp1, parser) :
        parser.add_argument('data_file', metavar='<data file>', type=str,
                            help="file containing rows of the form <email>,<desired name>")
        __tmp1.add_realm_args(parser, True)

    def handle(__tmp1, *args, **options: <FILL>) -> None:
        data_file = options['data_file']
        realm = __tmp1.get_realm(options)
        with open(data_file, "r") as f:
            for line in f:
                email, new_name = line.strip().split(",", 1)

                try:
                    user_profile = __tmp1.get_user(email, realm)
                    old_name = user_profile.full_name
                    print("%s: %s -> %s" % (email, old_name, new_name))
                    do_change_full_name(user_profile, new_name, None)
                except CommandError:
                    print("e-mail %s doesn't exist in the realm %s, skipping" % (email, realm))
