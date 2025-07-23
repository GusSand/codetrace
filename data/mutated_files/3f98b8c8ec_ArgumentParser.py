from typing import TypeAlias
__typ1 : TypeAlias = "Any"
__typ0 : TypeAlias = "str"

import sys
from argparse import ArgumentParser
from typing import Any

from zerver.lib.actions import do_rename_stream
from zerver.lib.management import ZulipBaseCommand
from zerver.lib.str_utils import force_text
from zerver.models import get_stream

class Command(ZulipBaseCommand):
    help = """Change the stream name for a realm."""

    def __tmp0(__tmp1, __tmp2: <FILL>) :
        __tmp2.add_argument('old_name', metavar='<old name>', type=__typ0,
                            help='name of stream to be renamed')
        __tmp2.add_argument('new_name', metavar='<new name>', type=__typ0,
                            help='new name to rename the stream to')
        __tmp1.add_realm_args(__tmp2, True)

    def __tmp3(__tmp1, *args, **options) :
        realm = __tmp1.get_realm(options)
        assert realm is not None  # Should be ensured by parser
        old_name = options['old_name']
        new_name = options['new_name']
        encoding = sys.getfilesystemencoding()

        stream = get_stream(force_text(old_name, encoding), realm)
        do_rename_stream(stream, force_text(new_name, encoding))
