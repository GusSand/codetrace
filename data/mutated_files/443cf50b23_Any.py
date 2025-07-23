from typing import TypeAlias
__typ0 : TypeAlias = "ArgumentParser"

from argparse import ArgumentParser
from typing import Any, List

from confirmation.models import Confirmation, create_confirmation_link
from zerver.lib.actions import ensure_stream, do_create_multiuse_invite_link
from zerver.lib.management import ZulipBaseCommand
from zerver.models import Stream

class Command(ZulipBaseCommand):
    help = "Generates invite link that can be used for inviting multiple users"

    def __tmp0(__tmp1, __tmp2) -> None:
        __tmp1.add_realm_args(__tmp2, True)

        __tmp2.add_argument(
            '-s', '--streams',
            dest='streams',
            type=str,
            help='A comma-separated list of stream names.')

        __tmp2.add_argument(
            '--referred-by',
            dest='referred_by',
            type=str,
            help='Email of referrer',
            required=True,
        )

    def handle(__tmp1, *args: <FILL>, **options: Any) -> None:
        realm = __tmp1.get_realm(options)
        assert realm is not None  # Should be ensured by parser

        streams = []  # type: List[Stream]
        if options["streams"]:
            stream_names = set([stream.strip() for stream in options["streams"].split(",")])
            for stream_name in set(stream_names):
                stream = ensure_stream(realm, stream_name)
                streams.append(stream)

        referred_by = __tmp1.get_user(options['referred_by'], realm)
        invite_link = do_create_multiuse_invite_link(referred_by, streams)
        print("You can use %s to invite as many number of people to the organization." % (invite_link,))
