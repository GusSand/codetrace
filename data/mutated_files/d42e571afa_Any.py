from typing import TypeAlias
__typ1 : TypeAlias = "Command"
__typ0 : TypeAlias = "CommandParser"

import datetime
import time
from typing import Any

from django.core.management.base import CommandParser
from django.utils.timezone import utc as timezone_utc

from zerver.lib.management import ZulipBaseCommand
from zerver.models import Message, Recipient, Stream

class __typ1(ZulipBaseCommand):
    help = "Dump messages from public streams of a realm"

    def add_arguments(__tmp0, parser) -> None:
        default_cutoff = time.time() - 60 * 60 * 24 * 30  # 30 days.
        __tmp0.add_realm_args(parser, True)
        parser.add_argument('--since',
                            dest='since',
                            type=int,
                            default=default_cutoff,
                            help='The time in epoch since from which to start the dump.')

    def handle(__tmp0, *args: Any, **options: <FILL>) -> None:
        realm = __tmp0.get_realm(options)
        streams = Stream.objects.filter(realm=realm, invite_only=False)
        recipients = Recipient.objects.filter(
            type=Recipient.STREAM, type_id__in=[stream.id for stream in streams])
        cutoff = datetime.datetime.fromtimestamp(options["since"], tz=timezone_utc)
        messages = Message.objects.filter(pub_date__gt=cutoff, recipient__in=recipients)

        for message in messages:
            print(message.to_dict(False))
