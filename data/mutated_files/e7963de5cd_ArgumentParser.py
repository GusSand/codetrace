from typing import TypeAlias
__typ0 : TypeAlias = "str"

from argparse import ArgumentParser
from typing import Any

from zerver.lib.actions import do_deactivate_realm
from zerver.lib.management import ZulipBaseCommand

class Command(ZulipBaseCommand):
    help = """Script to deactivate a realm."""

    def __tmp0(__tmp1, __tmp2: <FILL>) :
        __tmp1.add_realm_args(__tmp2, True)

    def handle(__tmp1, *args: Any, **options: __typ0) :
        realm = __tmp1.get_realm(options)
        assert realm is not None  # Should be ensured by parser

        if realm.deactivated:
            print("The realm", options["realm_id"], "is already deactivated.")
            exit(0)
        print("Deactivating", options["realm_id"])
        do_deactivate_realm(realm)
        print("Done!")
