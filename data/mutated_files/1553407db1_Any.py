from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest


class AccountAdapter(DefaultAccountAdapter):

    def __tmp3(__tmp1, __tmp0):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def __tmp3(__tmp1, __tmp0: HttpRequest, __tmp2: <FILL>):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
