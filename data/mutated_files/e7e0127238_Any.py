from typing import TypeAlias
__typ0 : TypeAlias = "Command"
import datetime
import logging
from typing import Any, List

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import now as timezone_now

from zerver.lib.digest import DIGEST_CUTOFF, enqueue_emails
from zerver.lib.logging_util import log_to_file

## Logging setup ##
logger = logging.getLogger(__name__)
log_to_file(logger, settings.DIGEST_LOG_PATH)

class __typ0(BaseCommand):
    help = """Enqueue digest emails for users that haven't checked the app
in a while.
"""

    def __tmp1(__tmp0, *args: <FILL>, **options) -> None:
        cutoff = timezone_now() - datetime.timedelta(days=DIGEST_CUTOFF)
        enqueue_emails(cutoff)
