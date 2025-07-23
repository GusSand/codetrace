from typing import TypeAlias
__typ0 : TypeAlias = "str"

import logging
from argparse import ArgumentParser
from typing import Any, Dict, List, Optional

from django.contrib.auth.tokens import default_token_generator

from zerver.forms import generate_password_reset_url
from zerver.lib.management import CommandError, ZulipBaseCommand
from zerver.lib.send_email import FromAddress, send_email
from zerver.models import UserProfile

class Command(ZulipBaseCommand):
    help = """Send email to specified email address."""

    def add_arguments(__tmp0, parser: ArgumentParser) :
        parser.add_argument('--entire-server', action="store_true", default=False,
                            help="Send to every user on the server. ")
        __tmp0.add_user_list_args(parser,
                                help="Email addresses of user(s) to send password reset emails to.",
                                all_users_help="Send to every user on the realm.")
        __tmp0.add_realm_args(parser)

    def handle(__tmp0, *args: <FILL>, **options: __typ0) :
        if options["entire_server"]:
            users = UserProfile.objects.filter(is_active=True, is_bot=False,
                                               is_mirror_dummy=False)
        else:
            realm = __tmp0.get_realm(options)
            try:
                users = __tmp0.get_users(options, realm)
            except CommandError as error:
                if __typ0(error) == "You have to pass either -u/--users or -a/--all-users.":
                    raise CommandError("You have to pass -u/--users or -a/--all-users or --entire-server.")
                raise error

        __tmp0.send(users)

    def send(__tmp0, users) :
        """Sends one-use only links for resetting password to target users

        """
        for user_profile in users:
            context = {
                'email': user_profile.email,
                'reset_url': generate_password_reset_url(user_profile, default_token_generator),
                'realm_uri': user_profile.realm.uri,
                'active_account_in_realm': True,
            }
            send_email('zerver/emails/password_reset', to_user_id=user_profile.id,
                       from_address=FromAddress.tokenized_no_reply_address(),
                       from_name="Zulip Account Security", context=context)
