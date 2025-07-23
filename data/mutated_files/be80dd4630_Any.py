from typing import TypeAlias
__typ0 : TypeAlias = "Command"

import sys
from argparse import ArgumentParser
from typing import Any

from zerver.lib.actions import do_rename_stream
from zerver.lib.management import ZulipBaseCommand
from zerver.lib.str_utils import force_text
from zerver.models import get_stream

class __typ0(ZulipBaseCommand):
    help = """Change the stream name for a realm."""

    def __tmp0(self, parser) -> None:
        parser.add_argument('old_name', metavar='<old name>', type=str,
                            help='name of stream to be renamed')
        parser.add_argument('new_name', metavar='<new name>', type=str,
                            help='new name to rename the stream to')
        self.add_realm_args(parser, True)

    def __tmp1(self, *args: <FILL>, **options) :
        realm = self.get_realm(options)
        assert realm is not None  # Should be ensured by parser
        old_name = options['old_name']
        new_name = options['new_name']
        encoding = sys.getfilesystemencoding()

        stream = get_stream(force_text(old_name, encoding), realm)
        do_rename_stream(stream, force_text(new_name, encoding))
