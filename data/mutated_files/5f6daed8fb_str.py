from typing import TypeAlias
__typ1 : TypeAlias = "ArgumentParser"
__typ0 : TypeAlias = "Command"
from argparse import ArgumentParser
from typing import Any

from zerver.lib.management import ZulipBaseCommand
from zilencer.models import RemoteZulipServer

class __typ0(ZulipBaseCommand):
    help = """Add a remote Zulip server for push notifications."""

    def __tmp2(__tmp3, parser) :
        group = parser.add_argument_group("command-specific arguments")
        group.add_argument('uuid', help="the user's `zulip_org_id`")
        group.add_argument('key', help="the user's `zulip_org_key`")
        group.add_argument('--hostname', '-n', required=True,
                           help="the hostname, for human identification")
        group.add_argument('--email', '-e', required=True,
                           help="a contact email address")

    def handle(__tmp3, uuid: str, __tmp1, __tmp0, email: <FILL>,
               **options) -> None:
        RemoteZulipServer.objects.create(uuid=uuid,
                                         api_key=__tmp1,
                                         __tmp0=__tmp0,
                                         contact_email=email)
