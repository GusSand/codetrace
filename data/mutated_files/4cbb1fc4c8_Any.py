from typing import TypeAlias
__typ0 : TypeAlias = "Command"

from typing import Any

from django.conf import settings
from django.core.cache import cache
from django.core.management.base import BaseCommand
from django.db.models import F

from zerver.models import UserMessage, UserProfile

class __typ0(BaseCommand):
    help = """Script to mark all messages as unread."""

    def __tmp1(__tmp0, *args, **options: <FILL>) :
        assert settings.DEVELOPMENT
        UserMessage.objects.all().update(flags=F('flags').bitand(~UserMessage.flags.read))
        UserProfile.objects.all().update(pointer=0)
        cache._cache.flush_all()
