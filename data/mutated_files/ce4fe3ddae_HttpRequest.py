from typing import TypeAlias
__typ0 : TypeAlias = "AccountAdapter"
from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest


class __typ0(DefaultAccountAdapter):

    def __tmp3(__tmp2, __tmp0: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def __tmp3(__tmp2, __tmp0: <FILL>, __tmp1: Any):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
