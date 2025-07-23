from typing import TypeAlias
__typ1 : TypeAlias = "AccountAdapter"
__typ0 : TypeAlias = "SocialAccountAdapter"
from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest


class __typ1(DefaultAccountAdapter):
    def __tmp3(__tmp1, __tmp0):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


class __typ0(DefaultSocialAccountAdapter):
    def __tmp3(__tmp1, __tmp0: <FILL>, __tmp2: Any):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
