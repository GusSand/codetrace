from typing import TypeAlias
__typ0 : TypeAlias = "Command"
__typ1 : TypeAlias = "str"

import sys
from argparse import ArgumentParser
from typing import Any

from zerver.lib.actions import create_stream_if_needed
from zerver.lib.management import ZulipBaseCommand
from zerver.lib.str_utils import force_text

class __typ0(ZulipBaseCommand):
    help = """Create a stream, and subscribe all active users (excluding bots).

This should be used for TESTING only, unless you understand the limitations of
the command."""

    def __tmp0(__tmp1, __tmp2: ArgumentParser) :
        __tmp1.add_realm_args(__tmp2, True, "realm in which to create the stream")
        __tmp2.add_argument('stream_name', metavar='<stream name>', type=__typ1,
                            help='name of stream to create')

    def __tmp3(__tmp1, *args: <FILL>, **options) :
        realm = __tmp1.get_realm(options)
        assert realm is not None  # Should be ensured by parser

        encoding = sys.getfilesystemencoding()
        stream_name = options['stream_name']
        create_stream_if_needed(realm, force_text(stream_name, encoding))
