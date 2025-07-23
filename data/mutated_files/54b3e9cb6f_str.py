from typing import TypeAlias
__typ0 : TypeAlias = "HttpRequest"
import logging
import time
from typing import Dict, Any, Optional
import requests
import jwt
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.conf import settings
from django.http.request import HttpRequest

from .compat import reverse


logger = logging.getLogger("uaa_client")


def __tmp9(request) -> str:
    if settings.DEBUG and settings.UAA_AUTH_URL == "fake:":
        return request.build_absolute_uri(reverse("uaa_client:fake_auth"))
    return settings.UAA_AUTH_URL


def __tmp6(request: __typ0) -> str:
    if settings.DEBUG and settings.UAA_TOKEN_URL == "fake:":
        return request.build_absolute_uri(reverse("uaa_client:fake_token"))
    return settings.UAA_TOKEN_URL


def __tmp7(request: __typ0, payload: Dict[str, Any]) -> Optional[str]:
    token_url = __tmp6(request)
    token_req = requests.post(token_url, data=payload)
    if token_req.status_code != 200:
        logger.warning(
            "POST %s returned %s "
            "w/ content %s"
            % (token_url, token_req.status_code, repr(token_req.content))
        )
        return None

    response = token_req.json()
    request.session["uaa_expiry"] = int(time.time()) + response["expires_in"]
    request.session["uaa_refresh_token"] = response["refresh_token"]

    return response["access_token"]


def __tmp0(request: __typ0) -> Optional[str]:
    return __tmp7(
        request,
        {
            "grant_type": "refresh_token",
            "refresh_token": request.session["uaa_refresh_token"],
            "client_id": settings.UAA_CLIENT_ID,
            "client_secret": settings.UAA_CLIENT_SECRET,
        },
    )


def __tmp4(request: __typ0, __tmp8: <FILL>) -> Optional[str]:
    redirect_uri = request.build_absolute_uri(reverse("uaa_client:callback"))

    return __tmp7(
        request,
        {
            "grant_type": "authorization_code",
            "code": __tmp8,
            "redirect_uri": redirect_uri,
            "response_type": "token",
            "client_id": settings.UAA_CLIENT_ID,
            "client_secret": settings.UAA_CLIENT_SECRET,
        },
    )


class UaaBackend(ModelBackend):
    """
    Custom auth backend for Cloud Foundry / cloud.gov User Account and
    Authentication (UAA) servers.

    This inherits from :class:`django.contrib.auth.backends.ModelBackend`
    so that the superclass can provide all authorization methods.
    """

    @classmethod
    def get_user_by_email(__tmp3, __tmp2):
        """
        Return a :class:`django.contrib.auth.models.User` with the given
        email address. If no user can be found, return ``None``.

        The default implementation attempts to find an existing user with
        the given case-insensitive email address. If no such user exists,
        :meth:`should_create_user_for_email` is consulted to determine
        whether the user should be auto-created; if so,
        :meth:`create_user_with_email` is used to auto-create the user.
        Otherwise, ``None`` is returned.

        Subclasses may override this method to account for different kinds
        of security policies for logins.
        """

        try:
            return User.objects.get(email__iexact=__tmp2)
        except User.DoesNotExist:
            if __tmp3.should_create_user_for_email(__tmp2):
                return __tmp3.create_user_with_email(__tmp2)
            logger.info(
                "User with email {} does not exist and is not "
                "approved for auto-creation".format(__tmp2)
            )
            return None
        except MultipleObjectsReturned:
            logger.warning("Multiple users with email {} exist".format(__tmp2))
            return None

    @classmethod
    def should_create_user_for_email(__tmp3, __tmp2):
        """
        Returns whether or not a new user with the given email
        can be created.

        The default implementation consults whether the domain
        of the email address is in the
        :ref:`list of approved domains <domains>`, but subclasses may
        override this method if needed.
        """

        APPROVED_DOMAINS = getattr(settings, "UAA_APPROVED_DOMAINS", [])

        email_pieces = __tmp2.split("@")
        return email_pieces[1] in APPROVED_DOMAINS

    @classmethod
    def create_user_with_email(__tmp3, __tmp2):
        """
        Create and return a new :class:`~django.contrib.auth.models.User`
        with the given email.

        Assumes the given email address has already been approved
        for auto-creation.

        By default, the new user has a username set to the email address,
        but subclasses may override this method if needed.
        """

        User.objects.create_user(__tmp2, __tmp2)
        return User.objects.get(email__iexact=__tmp2)

    def __tmp5(__tmp1, request, uaa_oauth2_code=None, **kwargs):
        if uaa_oauth2_code is None or request is None:
            return None

        access_token = __tmp4(request, uaa_oauth2_code)
        if access_token is None:
            return None

        user_info = jwt.decode(
            access_token,
            options={"verify_signature": False},
            algorithms=["HS256", "RS256"],
        )
        __tmp2 = user_info["email"]

        logger.info("Authenticating user with email {}".format(__tmp2))

        return __tmp1.get_user_by_email(__tmp2)
