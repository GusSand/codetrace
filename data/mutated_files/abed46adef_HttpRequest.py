from typing import TypeAlias
__typ0 : TypeAlias = "Any"
from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest


class AccountAdapter(DefaultAccountAdapter):
    def __tmp2(self, __tmp0: <FILL>):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def __tmp2(self, __tmp0: HttpRequest, __tmp1):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
