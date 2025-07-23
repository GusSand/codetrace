from typing import TypeAlias
__typ1 : TypeAlias = "HttpRequest"
__typ0 : TypeAlias = "SocialAccountAdapter"
from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest


class AccountAdapter(DefaultAccountAdapter):

    def __tmp3(__tmp2, __tmp0):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


class __typ0(DefaultSocialAccountAdapter):

    def __tmp3(__tmp2, __tmp0, __tmp1: <FILL>):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
