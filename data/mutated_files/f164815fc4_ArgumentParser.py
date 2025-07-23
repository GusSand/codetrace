from typing import TypeAlias
__typ0 : TypeAlias = "Client"
__typ1 : TypeAlias = "bool"
# Library code for use in management commands

import sys
import time

from argparse import ArgumentParser
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned
from django.core.management.base import BaseCommand, CommandError
from typing import Any, Dict, Optional, List

from zerver.models import Realm, UserProfile, Client, get_client

def __tmp8(__tmp0: str) :
    try:
        int(__tmp0)
        return True
    except ValueError:
        return False

def check_config() -> None:
    for (setting_name, default) in settings.REQUIRED_SETTINGS:
        # if required setting is the same as default OR is not found in settings,
        # throw error to add/set that setting in config
        try:
            if settings.__getattr__(setting_name) != default:
                continue
        except AttributeError:
            pass

        raise CommandError("Error: You must set %s in /etc/zulip/settings.py." % (setting_name,))

def __tmp7() -> None:
    while True:  # nocoverage
        time.sleep(10**9)

class ZulipBaseCommand(BaseCommand):
    def __tmp3(__tmp1, __tmp9: <FILL>, required: __typ1=False,
                       help: Optional[str]=None) -> None:
        if help is None:
            help = """The numeric or string ID (subdomain) of the Zulip organization to modify.
You can use the command list_realms to find ID of the realms in this server."""

        __tmp9.add_argument(
            '-r', '--realm',
            dest='realm_id',
            required=required,
            type=str,
            help=help)

    def __tmp4(__tmp1, __tmp9: ArgumentParser,
                           help: str='A comma-separated list of email addresses.',
                           all_users_help: str="All users in realm.") -> None:
        __tmp9.add_argument(
            '-u', '--users',
            dest='users',
            type=str,
            help=help)

        __tmp9.add_argument(
            '-a', '--all-users',
            dest='all_users',
            action="store_true",
            default=False,
            help=all_users_help)

    def __tmp5(__tmp1, __tmp11: Dict[str, Any]) :
        __tmp0 = __tmp11["realm_id"]
        if __tmp0 is None:
            return None

        # If they specified a realm argument, we need to ensure the
        # realm exists.  We allow two formats: the numeric ID for the
        # realm and the string ID of the realm.
        try:
            if __tmp8(__tmp0):
                return Realm.objects.get(id=__tmp0)
            return Realm.objects.get(string_id=__tmp0)
        except Realm.DoesNotExist:
            raise CommandError("There is no realm with id '%s'. Aborting." %
                               (__tmp11["realm_id"],))

    def __tmp10(__tmp1, __tmp11, __tmp6) -> List[UserProfile]:
        if "all_users" in __tmp11:
            all_users = __tmp11["all_users"]

            if not __tmp11["users"] and not all_users:
                raise CommandError("You have to pass either -u/--users or -a/--all-users.")

            if __tmp11["users"] and all_users:
                raise CommandError("You can't use both -u/--users and -a/--all-users.")

            if all_users and __tmp6 is None:
                raise CommandError("The --all-users option requires a realm; please pass --realm.")

            if all_users:
                return UserProfile.objects.filter(__tmp6=__tmp6)

        if __tmp11["users"] is None:
            return []
        emails = set([__tmp2.strip() for __tmp2 in __tmp11["users"].split(",")])
        user_profiles = []
        for __tmp2 in emails:
            user_profiles.append(__tmp1.get_user(__tmp2, __tmp6))
        return user_profiles

    def get_user(__tmp1, __tmp2: str, __tmp6: Optional[Realm]) :

        # If a realm is specified, try to find the user there, and
        # throw an error if they don't exist.
        if __tmp6 is not None:
            try:
                return UserProfile.objects.select_related().get(email__iexact=__tmp2.strip(), __tmp6=__tmp6)
            except UserProfile.DoesNotExist:
                raise CommandError("The realm '%s' does not contain a user with email '%s'" % (__tmp6, __tmp2))

        # Realm is None in the remaining code path.  Here, we
        # optimistically try to see if there is exactly one user with
        # that email; if so, we'll return it.
        try:
            return UserProfile.objects.select_related().get(email__iexact=__tmp2.strip())
        except MultipleObjectsReturned:
            raise CommandError("This Zulip server contains multiple users with that email " +
                               "(in different realms); please pass `--realm` "
                               "to specify which one to modify.")
        except UserProfile.DoesNotExist:
            raise CommandError("This Zulip server does not contain a user with email '%s'" % (__tmp2,))

    def get_client(__tmp1) :
        """Returns a Zulip Client object to be used for things done in management commands"""
        return get_client("ZulipServer")
