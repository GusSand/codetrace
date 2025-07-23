from typing import TypeAlias
__typ1 : TypeAlias = "Any"
__typ0 : TypeAlias = "str"

from argparse import ArgumentParser
from typing import Any

from django.core.management.base import CommandError

from zerver.lib.actions import do_change_full_name
from zerver.lib.management import ZulipBaseCommand

class Command(ZulipBaseCommand):
    help = """Change the names for many users."""

    def __tmp0(__tmp1, __tmp2: <FILL>) -> None:
        __tmp2.add_argument('data_file', metavar='<data file>', type=__typ0,
                            help="file containing rows of the form <email>,<desired name>")
        __tmp1.add_realm_args(__tmp2, True)

    def __tmp3(__tmp1, *args, **options: __typ0) :
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
