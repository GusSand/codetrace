from typing import TypeAlias
__typ1 : TypeAlias = "Any"
__typ0 : TypeAlias = "SocialAccountAdapter"
from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest


class AccountAdapter(DefaultAccountAdapter):

    def __tmp2(self, __tmp0: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


class __typ0(DefaultSocialAccountAdapter):

    def __tmp2(self, __tmp0: <FILL>, __tmp1):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
