from typing import TypeAlias
__typ0 : TypeAlias = "HttpRequest"
from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest


class AccountAdapter(DefaultAccountAdapter):
    def __tmp1(self, __tmp0: __typ0):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def __tmp1(self, __tmp0, sociallogin: <FILL>):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
