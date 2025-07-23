from typing import TypeAlias
__typ2 : TypeAlias = "Any"
__typ0 : TypeAlias = "Command"
__typ1 : TypeAlias = "str"

import sys
from argparse import ArgumentParser
from typing import Any, Dict, List

from django.conf import settings

from zerver.lib.management import ZulipBaseCommand
from zerver.lib.soft_deactivation import do_soft_activate_users, \
    do_soft_deactivate_users, get_users_for_soft_deactivation, logger
from zerver.models import Realm, UserProfile

class __typ0(ZulipBaseCommand):
    help = """Soft activate/deactivate users. Users are recognised by there emails here."""

    def __tmp0(__tmp1, parser: <FILL>) :
        __tmp1.add_realm_args(parser)
        parser.add_argument('-d', '--deactivate',
                            dest='deactivate',
                            action='store_true',
                            default=False,
                            help='Used to deactivate user/users.')
        parser.add_argument('-a', '--activate',
                            dest='activate',
                            action='store_true',
                            default=False,
                            help='Used to activate user/users.')
        parser.add_argument('--inactive-for',
                            type=int,
                            default=28,
                            help='Number of days of inactivity before soft-deactivation')
        parser.add_argument('users', metavar='<users>', type=__typ1, nargs='*', default=[],
                            help="A list of user emails to soft activate/deactivate.")

    def handle(__tmp1, *args: __typ2, **options) :
        if settings.STAGING:
            print('This is a Staging server. Suppressing management command.')
            sys.exit(0)

        realm = __tmp1.get_realm(options)
        user_emails = options['users']
        activate = options['activate']
        deactivate = options['deactivate']

        filter_kwargs = {}  # type: Dict[str, Realm]
        if realm is not None:
            filter_kwargs = dict(realm=realm)

        if activate:
            if not user_emails:
                print('You need to specify at least one user to use the activate option.')
                __tmp1.print_help("./manage.py", "soft_deactivate_users")
                sys.exit(1)

            users_to_activate = UserProfile.objects.filter(
                email__in=user_emails,
                **filter_kwargs
            )
            users_to_activate = list(users_to_activate)

            if len(users_to_activate) != len(user_emails):
                user_emails_found = [user.email for user in users_to_activate]
                for user in user_emails:
                    if user not in user_emails_found:
                        raise Exception('User with email %s was not found. '
                                        'Check if the email is correct.' % (user))

            users_activated = do_soft_activate_users(users_to_activate)
            logger.info('Soft Reactivated %d user(s)' % (len(users_activated)))
        elif deactivate:
            if user_emails:
                users_to_deactivate = UserProfile.objects.filter(
                    email__in=user_emails,
                    **filter_kwargs
                )
                users_to_deactivate = list(users_to_deactivate)

                if len(users_to_deactivate) != len(user_emails):
                    user_emails_found = [user.email for user in users_to_deactivate]
                    for user in user_emails:
                        if user not in user_emails_found:
                            raise Exception('User with email %s was not found. '
                                            'Check if the email is correct.' % (user,))
                print('Soft deactivating forcefully...')
            else:
                if realm is not None:
                    filter_kwargs = dict(user_profile__realm=realm)
                users_to_deactivate = get_users_for_soft_deactivation(int(options['inactive_for']),
                                                                      filter_kwargs)

            if users_to_deactivate:
                users_deactivated = do_soft_deactivate_users(users_to_deactivate)
                logger.info('Soft Deactivated %d user(s)' % (len(users_deactivated)))
        else:
            __tmp1.print_help("./manage.py", "soft_deactivate_users")
            sys.exit(1)
