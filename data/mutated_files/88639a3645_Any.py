from typing import TypeAlias
__typ0 : TypeAlias = "Command"

from typing import Any, Iterable, Tuple

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Count

from zerver.lib.onboarding import create_if_missing_realm_internal_bots
from zerver.models import Realm, UserProfile

class __typ0(BaseCommand):
    help = """\
Create realm internal bots if absent, in all realms.

These are normally created when the realm is, so this should be a no-op
except when upgrading to a version that adds a new realm internal bot.
"""

    def __tmp1(__tmp0, *args: Any, **options: <FILL>) :
        create_if_missing_realm_internal_bots()
        # create_users is idempotent -- it's a no-op when a given email
        # already has a user in a given realm.
