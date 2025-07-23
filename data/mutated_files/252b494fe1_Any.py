from typing import TypeAlias
__typ0 : TypeAlias = "Command"

from typing import Any

from django.core.management.base import BaseCommand

from zerver.models import Subscription

class __typ0(BaseCommand):
    help = """One-off script to migration users' stream notification settings."""

    def __tmp0(self, *args, **options: <FILL>) :
        for subscription in Subscription.objects.all():
            subscription.desktop_notifications = subscription.notifications
            subscription.audible_notifications = subscription.notifications
            subscription.save(update_fields=["desktop_notifications",
                                             "audible_notifications"])
