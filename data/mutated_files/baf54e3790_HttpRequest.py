from typing import TypeAlias
__typ1 : TypeAlias = "AccountAdapter"
__typ2 : TypeAlias = "Any"
__typ0 : TypeAlias = "SocialAccountAdapter"
from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest


class __typ1(DefaultAccountAdapter):
    def is_open_for_signup(self, __tmp0: <FILL>):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


class __typ0(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, __tmp0: HttpRequest, sociallogin):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
