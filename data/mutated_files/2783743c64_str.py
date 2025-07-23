from typing import TypeAlias
__typ0 : TypeAlias = "Any"

import sys
from argparse import ArgumentParser, RawTextHelpFormatter
from typing import Any, Dict

from zerver.lib.actions import set_default_streams
from zerver.lib.management import ZulipBaseCommand

class Command(ZulipBaseCommand):
    help = """Set default streams for a realm

Users created under this realm will start out with these streams. This
command is not additive: if you re-run it on a realm with a different
set of default streams, those will be the new complete set of default
streams.

For example:

./manage.py set_default_streams --realm=foo --streams=foo,bar,baz
./manage.py set_default_streams --realm=foo --streams="foo,bar,baz with space"
./manage.py set_default_streams --realm=foo --streams=
"""

    # Fix support for multi-line usage
    def create_parser(__tmp1, *args: __typ0, **kwargs) :
        __tmp2 = super().create_parser(*args, **kwargs)
        __tmp2.formatter_class = RawTextHelpFormatter
        return __tmp2

    def __tmp0(__tmp1, __tmp2) :
        __tmp2.add_argument('-s', '--streams',
                            dest='streams',
                            type=str,
                            help='A comma-separated list of stream names.')
        __tmp1.add_realm_args(__tmp2, True)

    def __tmp3(__tmp1, **options: <FILL>) -> None:
        realm = __tmp1.get_realm(options)
        if options["streams"] is None:
            print("Please provide a default set of streams (which can be empty,\
with `--streams=`).", file=sys.stderr)
            exit(1)
        realm = __tmp1.get_realm(options)
        assert realm is not None  # Should be ensured by parser

        stream_dict = {
            stream.strip(): {"description": stream.strip(), "invite_only": False}
            for stream in options["streams"].split(",")
        }  # type: Dict[str, Dict[str, Any]]

        set_default_streams(realm, stream_dict)
