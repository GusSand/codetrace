from typing import TypeAlias
__typ0 : TypeAlias = "SocialAccountAdapter"
from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest


class AccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(__tmp1, __tmp0: <FILL>):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


class __typ0(DefaultSocialAccountAdapter):

    def is_open_for_signup(__tmp1, __tmp0: HttpRequest, __tmp2):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
