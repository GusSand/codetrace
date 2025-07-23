from typing import TypeAlias
__typ0 : TypeAlias = "ArgumentParser"
__typ1 : TypeAlias = "Any"
from argparse import ArgumentParser
from typing import Any

from zerver.lib.management import ZulipBaseCommand
from zilencer.models import RemoteZulipServer

class Command(ZulipBaseCommand):
    help = """Add a remote Zulip server for push notifications."""

    def __tmp4(__tmp2, __tmp5) :
        group = __tmp5.add_argument_group("command-specific arguments")
        group.add_argument('uuid', help="the user's `zulip_org_id`")
        group.add_argument('key', help="the user's `zulip_org_key`")
        group.add_argument('--hostname', '-n', required=True,
                           help="the hostname, for human identification")
        group.add_argument('--email', '-e', required=True,
                           help="a contact email address")

    def __tmp3(__tmp2, __tmp1, __tmp6: <FILL>, __tmp0, email,
               **options: __typ1) :
        RemoteZulipServer.objects.create(__tmp1=__tmp1,
                                         api_key=__tmp6,
                                         __tmp0=__tmp0,
                                         contact_email=email)
