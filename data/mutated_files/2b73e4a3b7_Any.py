from typing import TypeAlias
__typ1 : TypeAlias = "ArgumentParser"
__typ0 : TypeAlias = "Command"

from argparse import ArgumentParser
from typing import Any

from django.core.management.base import CommandError

from zerver.lib.actions import do_change_is_admin
from zerver.lib.management import ZulipBaseCommand

class __typ0(ZulipBaseCommand):
    help = """Give an existing user administrative permissions over their (own) Realm.

ONLY perform this on customer request from an authorized person.
"""

    def __tmp0(__tmp1, __tmp2: __typ1) :
        __tmp2.add_argument('-f', '--for-real',
                            dest='ack',
                            action="store_true",
                            default=False,
                            help='Acknowledgement that this is done according to policy.')
        __tmp2.add_argument('--revoke',
                            dest='grant',
                            action="store_false",
                            default=True,
                            help='Remove an administrator\'s rights.')
        __tmp2.add_argument('--permission',
                            dest='permission',
                            action="store",
                            default='administer',
                            choices=['administer', 'api_super_user', ],
                            help='Permission to grant/remove.')
        __tmp2.add_argument('email', metavar='<email>', type=str,
                            help="email of user to knight")
        __tmp1.add_realm_args(__tmp2, True)

    def __tmp3(__tmp1, *args: <FILL>, **options) -> None:
        email = options['email']
        realm = __tmp1.get_realm(options)

        profile = __tmp1.get_user(email, realm)

        if options['grant']:
            if profile.has_perm(options['permission'], profile.realm):
                raise CommandError("User already has permission for this realm.")
            else:
                if options['ack']:
                    do_change_is_admin(profile, True, permission=options['permission'])
                    print("Done!")
                else:
                    print("Would have granted %s %s rights for %s" % (
                          email, options['permission'], profile.realm.string_id))
        else:
            if profile.has_perm(options['permission'], profile.realm):
                if options['ack']:
                    do_change_is_admin(profile, False, permission=options['permission'])
                    print("Done!")
                else:
                    print("Would have removed %s's %s rights on %s" % (email, options['permission'],
                                                                       profile.realm.string_id))
            else:
                raise CommandError("User did not have permission for this realm!")
