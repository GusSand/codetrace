from typing import TypeAlias
__typ1 : TypeAlias = "ArgumentParser"
__typ0 : TypeAlias = "str"

from argparse import ArgumentParser
from typing import Any

from zerver.lib.actions import do_reactivate_realm
from zerver.lib.management import ZulipBaseCommand

class Command(ZulipBaseCommand):
    help = """Script to reactivate a deactivated realm."""

    def add_arguments(__tmp0, parser: __typ1) -> None:
        __tmp0.add_realm_args(parser, True)

    def __tmp1(__tmp0, *args: <FILL>, **options: __typ0) :
        realm = __tmp0.get_realm(options)
        assert realm is not None  # Should be ensured by parser
        if not realm.deactivated:
            print("Realm", options["realm_id"], "is already active.")
            exit(0)
        print("Reactivating", options["realm_id"])
        do_reactivate_realm(realm)
        print("Done!")
