from typing import TypeAlias
__typ0 : TypeAlias = "Command"

import sys
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand

from zerver.lib.management import check_config

class __typ0(BaseCommand):
    help = """Checks your Zulip Voyager Django configuration for issues."""

    def __tmp1(__tmp0, *args: <FILL>, **options) :
        check_config()
