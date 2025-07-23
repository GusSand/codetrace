from typing import TypeAlias
__typ0 : TypeAlias = "CommandParser"

import datetime
import time
from typing import Any

from django.core.management.base import CommandParser
from django.utils.timezone import utc as timezone_utc

from zerver.lib.management import ZulipBaseCommand
from zerver.models import Message, Recipient, Stream

class Command(ZulipBaseCommand):
    help = "Dump messages from public streams of a realm"

    def __tmp0(__tmp1, __tmp2: __typ0) -> None:
        default_cutoff = time.time() - 60 * 60 * 24 * 30  # 30 days.
        __tmp1.add_realm_args(__tmp2, True)
        __tmp2.add_argument('--since',
                            dest='since',
                            type=int,
                            default=default_cutoff,
                            help='The time in epoch since from which to start the dump.')

    def __tmp3(__tmp1, *args: <FILL>, **options) -> None:
        realm = __tmp1.get_realm(options)
        streams = Stream.objects.filter(realm=realm, invite_only=False)
        recipients = Recipient.objects.filter(
            type=Recipient.STREAM, type_id__in=[stream.id for stream in streams])
        cutoff = datetime.datetime.fromtimestamp(options["since"], tz=timezone_utc)
        messages = Message.objects.filter(pub_date__gt=cutoff, recipient__in=recipients)

        for message in messages:
            print(message.to_dict(False))
