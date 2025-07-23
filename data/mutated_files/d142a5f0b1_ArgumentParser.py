from typing import TypeAlias
__typ0 : TypeAlias = "Command"

from argparse import ArgumentParser
from typing import Any

from django.core.management.base import CommandError

from confirmation.models import Confirmation, create_confirmation_link
from zerver.lib.management import ZulipBaseCommand
from zerver.models import PreregistrationUser, email_allowed_for_realm, \
    email_allowed_for_realm, DomainNotAllowedForRealmError

class __typ0(ZulipBaseCommand):
    help = "Generate activation links for users and print them to stdout."

    def __tmp0(__tmp1, __tmp2: <FILL>) -> None:
        __tmp2.add_argument('--force',
                            dest='force',
                            action="store_true",
                            default=False,
                            help='Override that the domain is restricted to external users.')
        __tmp2.add_argument('emails', metavar='<email>', type=str, nargs='*',
                            help='email of users to generate an activation link for')
        __tmp1.add_realm_args(__tmp2, True)

    def __tmp3(__tmp1, *args: Any, **options) :
        duplicates = False
        realm = __tmp1.get_realm(options)
        assert realm is not None  # Should be ensured by parser

        if not options['emails']:
            __tmp1.print_help("./manage.py", "generate_invite_links")
            exit(1)

        for email in options['emails']:
            try:
                __tmp1.get_user(email, realm)
                print(email + ": There is already a user registered with that address.")
                duplicates = True
                continue
            except CommandError:
                pass

        if duplicates:
            return

        for email in options['emails']:
            try:
                email_allowed_for_realm(email, realm)
            except DomainNotAllowedForRealmError:
                if not options["force"]:
                    print("You've asked to add an external user '%s' to a closed realm '%s'." % (
                        email, realm.string_id))
                    print("Are you sure? To do this, pass --force.")
                    exit(1)

            prereg_user = PreregistrationUser(email=email, realm=realm)
            prereg_user.save()
            print(email + ": " + create_confirmation_link(prereg_user, realm.host,
                                                          Confirmation.INVITATION))
