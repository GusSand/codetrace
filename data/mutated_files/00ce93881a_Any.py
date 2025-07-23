from typing import TypeAlias
__typ1 : TypeAlias = "ArgumentParser"
__typ0 : TypeAlias = "Command"

from argparse import ArgumentParser
from typing import Any

from zerver.lib.actions import ensure_stream
from zerver.lib.management import ZulipBaseCommand
from zerver.models import DefaultStreamGroup

class __typ0(ZulipBaseCommand):
    help = """
Create default stream groups which the users can choose during sign up.

./manage.py create_default_stream_groups -s gsoc-1,gsoc-2,gsoc-3 -d "Google summer of code"  -r zulip
"""

    def __tmp0(__tmp1, __tmp2) :
        __tmp1.add_realm_args(__tmp2, True)

        __tmp2.add_argument(
            '-n', '--name',
            dest='name',
            type=str,
            required=True,
            help='Name of the group you want to create.'
        )

        __tmp2.add_argument(
            '-d', '--description',
            dest='description',
            type=str,
            required=True,
            help='Description of the group.'
        )

        __tmp2.add_argument(
            '-s', '--streams',
            dest='streams',
            type=str,
            required=True,
            help='A comma-separated list of stream names.')

    def __tmp3(__tmp1, *args, **options: <FILL>) :
        realm = __tmp1.get_realm(options)
        assert realm is not None  # Should be ensured by parser

        streams = []
        stream_names = set([stream.strip() for stream in options["streams"].split(",")])
        for stream_name in set(stream_names):
            stream = ensure_stream(realm, stream_name)
            streams.append(stream)

        try:
            default_stream_group = DefaultStreamGroup.objects.get(
                name=options["name"], realm=realm, description=options["description"])
        except DefaultStreamGroup.DoesNotExist:
            default_stream_group = DefaultStreamGroup.objects.create(
                name=options["name"], realm=realm, description=options["description"])
        default_stream_group.streams.set(streams)

        default_stream_groups = DefaultStreamGroup.objects.all()
        for default_stream_group in default_stream_groups:
            print(default_stream_group.name)
            print(default_stream_group.description)
            for stream in default_stream_group.streams.all():
                print(stream.name)
            print("")
