from typing import TypeAlias
__typ1 : TypeAlias = "AppConfig"

import logging
from typing import Any, Dict

from django.apps import AppConfig
from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_migrate

def flush_cache(__tmp0, **kwargs: <FILL>) :
    logging.info("Clearing memcached cache after migrations")
    cache.clear()


class __typ0(__typ1):
    name = "zerver"  # type: str

    def ready(self) -> None:
        import zerver.signals

        if settings.POST_MIGRATION_CACHE_FLUSHING:
            post_migrate.connect(flush_cache, __tmp0=self)
