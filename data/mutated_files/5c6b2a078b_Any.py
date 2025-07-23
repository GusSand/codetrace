from typing import TypeAlias
__typ1 : TypeAlias = "Command"
__typ0 : TypeAlias = "CommandParser"
from typing import Any

from django.core.management.base import CommandParser

from zerver.lib.actions import do_create_user
from zerver.lib.management import ZulipBaseCommand
from zerver.models import Realm, UserProfile

class __typ1(ZulipBaseCommand):
    help = """Add a new user for manual testing of the onboarding process.
If realm is unspecified, will try to use a realm created by add_new_realm,
and will otherwise fall back to the zulip realm."""

    def __tmp0(__tmp1, __tmp2) :
        __tmp1.add_realm_args(__tmp2)

    def __tmp3(__tmp1, **options: <FILL>) :
        realm = __tmp1.get_realm(options)
        if realm is None:
            realm = Realm.objects.filter(string_id__startswith='realm') \
                                 .order_by('-string_id').first()
        if realm is None:
            print('Warning: Using default zulip realm, which has an unusual configuration.\n'
                  'Try running `manage.py add_new_realm`, and then running this again.')
            valid_realm = Realm.objects.get(string_id='zulip')
            domain = 'zulip.com'
        else:
            valid_realm = realm
            domain = realm.string_id + '.zulip.com'

        name = '%02d-user' % (UserProfile.objects.filter(email__contains='user@').count(),)
        do_create_user('%s@%s' % (name, domain), 'password', valid_realm, name, name)
