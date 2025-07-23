from typing import TypeAlias
__typ1 : TypeAlias = "HttpRequest"
__typ2 : TypeAlias = "AccountAdapter"
__typ0 : TypeAlias = "SocialAccountAdapter"
from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest


class __typ2(DefaultAccountAdapter):
    def __tmp0(self, request: __typ1):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


class __typ0(DefaultSocialAccountAdapter):
    def __tmp0(self, request, sociallogin: <FILL>):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
