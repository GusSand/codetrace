from typing import TypeAlias
__typ0 : TypeAlias = "CommandParser"

import os

import ujson
from django.conf import settings
from django.core.management.base import CommandParser
from django.test import Client

from zerver.lib.management import ZulipBaseCommand
from zerver.models import get_realm

class Command(ZulipBaseCommand):
    help = """
Create webhook message based on given fixture
Example:
./manage.py send_webhook_fixture_message \
    [--realm=zulip] \
    --fixture=zerver/webhooks/integration/fixtures/name.json \
    '--url=/api/v1/external/integration?stream=stream_name&api_key=api_key'

"""

    def add_arguments(__tmp0, __tmp2) -> None:
        __tmp2.add_argument('-f', '--fixture',
                            dest='fixture',
                            type=str,
                            help='The path to the fixture you\'d like to send '
                                 'into Zulip')

        __tmp2.add_argument('-u', '--url',
                            dest='url',
                            type=str,
                            help='The url on your Zulip server that you want '
                                 'to post the fixture to')

        __tmp0.add_realm_args(__tmp2, help="Specify which realm/subdomain to connect to; default is zulip")

    def __tmp3(__tmp0, **options) :
        if options['fixture'] is None or options['url'] is None:
            __tmp0.print_help('./manage.py', 'send_webhook_fixture_message')
            exit(1)

        full_fixture_path = os.path.join(settings.DEPLOY_ROOT, options['fixture'])

        if not __tmp0._does_fixture_path_exist(full_fixture_path):
            print('Fixture {} does not exist'.format(options['fixture']))
            exit(1)

        json = __tmp0._get_fixture_as_json(full_fixture_path)
        realm = __tmp0.get_realm(options)
        if realm is None:
            realm = get_realm("zulip")

        client = Client()
        result = client.post(options['url'], json, content_type="application/json",
                             HTTP_HOST=realm.host)
        if result.status_code != 200:
            print('Error status %s: %s' % (result.status_code, result.content))
            exit(1)

    def _does_fixture_path_exist(__tmp0, __tmp1: <FILL>) :
        return os.path.exists(__tmp1)

    def _get_fixture_as_json(__tmp0, __tmp1) :
        return ujson.dumps(ujson.loads(open(__tmp1).read()))
