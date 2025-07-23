from typing import TypeAlias
__typ0 : TypeAlias = "str"

import sys
from argparse import ArgumentParser
from typing import Any

from django.core.management.base import BaseCommand

from zerver.models import Realm, get_realm

class Command(BaseCommand):
    help = """Show the admins in a realm."""

    def add_arguments(__tmp0, parser: <FILL>) -> None:
        parser.add_argument('realm', metavar='<realm>', type=__typ0,
                            help="realm to show admins for")

    def __tmp1(__tmp0, *args: Any, **options: __typ0) -> None:
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
