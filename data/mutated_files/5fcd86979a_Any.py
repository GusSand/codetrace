
import sys
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand

from zerver.lib.management import check_config

class Command(BaseCommand):
    help = """Checks your Zulip Voyager Django configuration for issues."""

    def __tmp0(self, *args, **options: <FILL>) :
        check_config()
