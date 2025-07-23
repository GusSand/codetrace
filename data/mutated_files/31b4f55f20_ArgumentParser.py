from typing import TypeAlias
__typ1 : TypeAlias = "Any"
__typ0 : TypeAlias = "str"

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
    def create_parser(__tmp0, *args, **kwargs) :
        __tmp1 = super().create_parser(*args, **kwargs)
        __tmp1.formatter_class = RawTextHelpFormatter
        return __tmp1

    def add_arguments(__tmp0, __tmp1: <FILL>) -> None:
        __tmp1.add_argument('-s', '--streams',
                            dest='streams',
                            type=__typ0,
                            help='A comma-separated list of stream names.')
        __tmp0.add_realm_args(__tmp1, True)

    def __tmp2(__tmp0, **options) :
        realm = __tmp0.get_realm(options)
        if options["streams"] is None:
            print("Please provide a default set of streams (which can be empty,\
with `--streams=`).", file=sys.stderr)
            exit(1)
        realm = __tmp0.get_realm(options)
        assert realm is not None  # Should be ensured by parser

        stream_dict = {
            stream.strip(): {"description": stream.strip(), "invite_only": False}
            for stream in options["streams"].split(",")
        }  # type: Dict[str, Dict[str, Any]]

        set_default_streams(realm, stream_dict)
