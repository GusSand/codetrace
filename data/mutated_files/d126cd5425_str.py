from typing import TypeAlias
__typ0 : TypeAlias = "Any"

from argparse import ArgumentParser
from typing import Any

from zerver.lib.actions import do_reactivate_realm
from zerver.lib.management import ZulipBaseCommand

class Command(ZulipBaseCommand):
    help = """Script to reactivate a deactivated realm."""

    def add_arguments(__tmp0, __tmp1) :
        __tmp0.add_realm_args(__tmp1, True)

    def __tmp2(__tmp0, *args, **options: <FILL>) :
        realm = __tmp0.get_realm(options)
        assert realm is not None  # Should be ensured by parser
        if not realm.deactivated:
            print("Realm", options["realm_id"], "is already active.")
            exit(0)
        print("Reactivating", options["realm_id"])
        do_reactivate_realm(realm)
        print("Done!")
