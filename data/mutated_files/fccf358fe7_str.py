from typing import TypeAlias
__typ0 : TypeAlias = "Client"
# Library code for use in management commands

import sys
import time

from argparse import ArgumentParser
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned
from django.core.management.base import BaseCommand, CommandError
from typing import Any, Dict, Optional, List

from zerver.models import Realm, UserProfile, Client, get_client

def is_integer_string(val: str) -> bool:
    try:
        int(val)
        return True
    except ValueError:
        return False

def __tmp8() -> None:
    for (setting_name, default) in settings.REQUIRED_SETTINGS:
        # if required setting is the same as default OR is not found in settings,
        # throw error to add/set that setting in config
        try:
            if settings.__getattr__(setting_name) != default:
                continue
        except AttributeError:
            pass

        raise CommandError("Error: You must set %s in /etc/zulip/settings.py." % (setting_name,))

def __tmp5() -> None:
    while True:  # nocoverage
        time.sleep(10**9)

class ZulipBaseCommand(BaseCommand):
    def __tmp1(__tmp0, __tmp6: ArgumentParser, required: bool=False,
                       help: Optional[str]=None) -> None:
        if help is None:
            help = """The numeric or string ID (subdomain) of the Zulip organization to modify.
You can use the command list_realms to find ID of the realms in this server."""

        __tmp6.add_argument(
            '-r', '--realm',
            dest='realm_id',
            required=required,
            type=str,
            help=help)

    def __tmp2(__tmp0, __tmp6: ArgumentParser,
                           help: str='A comma-separated list of email addresses.',
                           all_users_help: str="All users in realm.") -> None:
        __tmp6.add_argument(
            '-u', '--users',
            dest='users',
            type=str,
            help=help)

        __tmp6.add_argument(
            '-a', '--all-users',
            dest='all_users',
            action="store_true",
            default=False,
            help=all_users_help)

    def __tmp3(__tmp0, __tmp9: Dict[str, Any]) -> Optional[Realm]:
        val = __tmp9["realm_id"]
        if val is None:
            return None

        # If they specified a realm argument, we need to ensure the
        # realm exists.  We allow two formats: the numeric ID for the
        # realm and the string ID of the realm.
        try:
            if is_integer_string(val):
                return Realm.objects.get(id=val)
            return Realm.objects.get(string_id=val)
        except Realm.DoesNotExist:
            raise CommandError("There is no realm with id '%s'. Aborting." %
                               (__tmp9["realm_id"],))

    def __tmp7(__tmp0, __tmp9: Dict[str, Any], __tmp4: Optional[Realm]) -> List[UserProfile]:
        if "all_users" in __tmp9:
            all_users = __tmp9["all_users"]

            if not __tmp9["users"] and not all_users:
                raise CommandError("You have to pass either -u/--users or -a/--all-users.")

            if __tmp9["users"] and all_users:
                raise CommandError("You can't use both -u/--users and -a/--all-users.")

            if all_users and __tmp4 is None:
                raise CommandError("The --all-users option requires a realm; please pass --realm.")

            if all_users:
                return UserProfile.objects.filter(__tmp4=__tmp4)

        if __tmp9["users"] is None:
            return []
        emails = set([email.strip() for email in __tmp9["users"].split(",")])
        user_profiles = []
        for email in emails:
            user_profiles.append(__tmp0.get_user(email, __tmp4))
        return user_profiles

    def get_user(__tmp0, email: <FILL>, __tmp4: Optional[Realm]) -> UserProfile:

        # If a realm is specified, try to find the user there, and
        # throw an error if they don't exist.
        if __tmp4 is not None:
            try:
                return UserProfile.objects.select_related().get(email__iexact=email.strip(), __tmp4=__tmp4)
            except UserProfile.DoesNotExist:
                raise CommandError("The realm '%s' does not contain a user with email '%s'" % (__tmp4, email))

        # Realm is None in the remaining code path.  Here, we
        # optimistically try to see if there is exactly one user with
        # that email; if so, we'll return it.
        try:
            return UserProfile.objects.select_related().get(email__iexact=email.strip())
        except MultipleObjectsReturned:
            raise CommandError("This Zulip server contains multiple users with that email " +
                               "(in different realms); please pass `--realm` "
                               "to specify which one to modify.")
        except UserProfile.DoesNotExist:
            raise CommandError("This Zulip server does not contain a user with email '%s'" % (email,))

    def get_client(__tmp0) -> __typ0:
        """Returns a Zulip Client object to be used for things done in management commands"""
        return get_client("ZulipServer")
