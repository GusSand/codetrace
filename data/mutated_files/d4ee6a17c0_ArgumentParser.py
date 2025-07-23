from typing import TypeAlias
__typ2 : TypeAlias = "Any"
__typ0 : TypeAlias = "Command"
__typ1 : TypeAlias = "str"

from argparse import ArgumentParser
from typing import Any

from zerver.lib.actions import do_scrub_realm
from zerver.lib.management import ZulipBaseCommand

class __typ0(ZulipBaseCommand):
    help = """Script to scrub a deactivated realm."""

    def __tmp0(__tmp1, __tmp2: <FILL>) :
        __tmp1.add_realm_args(__tmp2, True)

    def __tmp3(__tmp1, *args: __typ2, **options) :
        realm = __tmp1.get_realm(options)
        assert realm is not None  # Should be ensured by parser
        if not realm.deactivated:
            print("Realm", options["realm_id"], "is active. Please deactivate the Realm the first.")
            exit(0)
        print("Scrubbing", options["realm_id"])
        do_scrub_realm(realm)
        print("Done!")
