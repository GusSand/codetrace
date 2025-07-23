from typing import TypeAlias
__typ1 : TypeAlias = "Any"
__typ0 : TypeAlias = "Command"

import logging
from argparse import ArgumentParser
from typing import Any, Dict, List, Optional

from django.contrib.auth.tokens import default_token_generator

from zerver.forms import generate_password_reset_url
from zerver.lib.management import CommandError, ZulipBaseCommand
from zerver.lib.send_email import FromAddress, send_email
from zerver.models import UserProfile

class __typ0(ZulipBaseCommand):
    help = """Send email to specified email address."""

    def __tmp3(__tmp0, __tmp4: <FILL>) :
        __tmp4.add_argument('--entire-server', action="store_true", default=False,
                            help="Send to every user on the server. ")
        __tmp0.add_user_list_args(__tmp4,
                                help="Email addresses of user(s) to send password reset emails to.",
                                all_users_help="Send to every user on the realm.")
        __tmp0.add_realm_args(__tmp4)

    def __tmp1(__tmp0, *args: __typ1, **options: str) -> None:
        if options["entire_server"]:
            __tmp2 = UserProfile.objects.filter(is_active=True, is_bot=False,
                                               is_mirror_dummy=False)
        else:
            realm = __tmp0.get_realm(options)
            try:
                __tmp2 = __tmp0.get_users(options, realm)
            except CommandError as error:
                if str(error) == "You have to pass either -u/--users or -a/--all-users.":
                    raise CommandError("You have to pass -u/--users or -a/--all-users or --entire-server.")
                raise error

        __tmp0.send(__tmp2)

    def send(__tmp0, __tmp2: List[UserProfile]) -> None:
        """Sends one-use only links for resetting password to target users

        """
        for user_profile in __tmp2:
            context = {
                'email': user_profile.email,
                'reset_url': generate_password_reset_url(user_profile, default_token_generator),
                'realm_uri': user_profile.realm.uri,
                'active_account_in_realm': True,
            }
            send_email('zerver/emails/password_reset', to_user_id=user_profile.id,
                       from_address=FromAddress.tokenized_no_reply_address(),
                       from_name="Zulip Account Security", context=context)
