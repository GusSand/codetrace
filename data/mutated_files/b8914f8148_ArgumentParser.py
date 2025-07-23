from typing import TypeAlias
__typ2 : TypeAlias = "Any"
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

    def add_arguments(self, __tmp0: <FILL>) :
        self.add_realm_args(__tmp0, True, "realm in which to create the stream")
        __tmp0.add_argument('stream_name', metavar='<stream name>', type=__typ1,
                            help='name of stream to create')

    def handle(self, *args, **options: __typ1) -> None:
        realm = self.get_realm(options)
        assert realm is not None  # Should be ensured by parser

        encoding = sys.getfilesystemencoding()
        stream_name = options['stream_name']
        create_stream_if_needed(realm, force_text(stream_name, encoding))
