from typing import TypeAlias
__typ2 : TypeAlias = "Any"
__typ1 : TypeAlias = "ArgumentParser"
__typ0 : TypeAlias = "Command"

import sys
from argparse import ArgumentParser
from typing import Any

from django.core.management.base import BaseCommand

from zerver.models import Realm, get_realm

class __typ0(BaseCommand):
    help = """Show the admins in a realm."""

    def __tmp0(__tmp1, __tmp2: __typ1) :
        __tmp2.add_argument('realm', metavar='<realm>', type=str,
                            help="realm to show admins for")

    def __tmp3(__tmp1, *args, **options: <FILL>) -> None:
        realm_name = options['realm']

        try:
            realm = get_realm(realm_name)
        except Realm.DoesNotExist:
            print('There is no realm called %s.' % (realm_name,))
            sys.exit(1)

        users = realm.get_admin_users()

        if users:
            print('Admins:\n')
            for user in users:
                print('  %s (%s)' % (user.email, user.full_name))
        else:
            print('There are no admins for this realm!')

        print('\nYou can use the "knight" management command to knight admins.')
