from typing import TypeAlias
__typ0 : TypeAlias = "Command"
from argparse import ArgumentParser
from typing import Any

from zerver.lib.management import ZulipBaseCommand
from zilencer.models import RemoteZulipServer

class __typ0(ZulipBaseCommand):
    help = """Add a remote Zulip server for push notifications."""

    def add_arguments(__tmp1, __tmp5: ArgumentParser) -> None:
        group = __tmp5.add_argument_group("command-specific arguments")
        group.add_argument('uuid', help="the user's `zulip_org_id`")
        group.add_argument('key', help="the user's `zulip_org_key`")
        group.add_argument('--hostname', '-n', required=True,
                           help="the hostname, for human identification")
        group.add_argument('--email', '-e', required=True,
                           help="a contact email address")

    def __tmp4(__tmp1, __tmp0, __tmp3: str, __tmp6: <FILL>, __tmp2,
               **options: Any) :
        RemoteZulipServer.objects.create(__tmp0=__tmp0,
                                         api_key=__tmp3,
                                         __tmp6=__tmp6,
                                         contact_email=__tmp2)
