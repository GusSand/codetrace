from typing import TypeAlias
__typ0 : TypeAlias = "AccountAdapter"
from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest


class __typ0(DefaultAccountAdapter):

    def is_open_for_signup(__tmp0, request):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def is_open_for_signup(__tmp0, request: <FILL>, __tmp1):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
