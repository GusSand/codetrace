"""Trusted Networks auth provider.

It shows list of users if access from trusted network.
Abort login flow if not access from trusted network.
"""
from typing import Any, Dict, Optional, cast

import voluptuous as vol

from homeassistant.components.http import HomeAssistantHTTP  # noqa: F401
from homeassistant.core import callback
from homeassistant.exceptions import HomeAssistantError

from . import AuthProvider, AUTH_PROVIDER_SCHEMA, AUTH_PROVIDERS, LoginFlow
from ..models import Credentials, UserMeta

CONFIG_SCHEMA = AUTH_PROVIDER_SCHEMA.extend({
}, extra=vol.PREVENT_EXTRA)


class __typ0(HomeAssistantError):
    """Raised when try to access from untrusted networks."""


class InvalidUserError(HomeAssistantError):
    """Raised when try to login as invalid user."""


@AUTH_PROVIDERS.register('trusted_networks')
class TrustedNetworksAuthProvider(AuthProvider):
    """Trusted Networks auth provider.

    Allow passwordless access from trusted network.
    """

    DEFAULT_TITLE = 'Trusted Networks'

    @property
    def support_mfa(__tmp1) :
        """Trusted Networks auth provider does not support MFA."""
        return False

    async def __tmp3(__tmp1, __tmp0) :
        """Return a flow to login."""
        assert __tmp0 is not None
        users = await __tmp1.store.async_get_users()
        __tmp6 = {user.id: user.name
                           for user in users
                           if not user.system_generated and user.is_active}

        return TrustedNetworksLoginFlow(
            __tmp1, cast(str, __tmp0.get('ip_address')), __tmp6)

    async def __tmp9(
            __tmp1, flow_result) :
        """Get credentials based on the flow result."""
        user_id = flow_result['user']

        users = await __tmp1.store.async_get_users()
        for user in users:
            if (not user.system_generated and
                    user.is_active and
                    user.id == user_id):
                for credential in await __tmp1.async_credentials():
                    if credential.data['user_id'] == user_id:
                        return credential
                cred = __tmp1.async_create_credentials({'user_id': user_id})
                await __tmp1.store.async_link_user(user, cred)
                return cred

        # We only allow login as exist user
        raise InvalidUserError

    async def __tmp8(
            __tmp1, __tmp2) :
        """Return extra user metadata for credentials.

        Trusted network auth provider should never create new user.
        """
        raise NotImplementedError

    @callback
    def async_validate_access(__tmp1, __tmp7) :
        """Make sure the access from trusted networks.

        Raise InvalidAuthError if not.
        Raise InvalidAuthError if trusted_networks is not configured.
        """
        hass_http = getattr(__tmp1.hass, 'http', None)  # type: HomeAssistantHTTP

        if not hass_http or not hass_http.trusted_networks:
            raise __typ0('trusted_networks is not configured')

        if not any(__tmp7 in trusted_network for trusted_network
                   in hass_http.trusted_networks):
            raise __typ0('Not in trusted_networks')


class TrustedNetworksLoginFlow(LoginFlow):
    """Handler for the login flow."""

    def __init__(__tmp1, __tmp5: TrustedNetworksAuthProvider,
                 __tmp7: <FILL>, __tmp6: Dict[str, Optional[str]]) \
            -> None:
        """Initialize the login flow."""
        super().__init__(__tmp5)
        __tmp1._available_users = __tmp6
        __tmp1._ip_address = __tmp7

    async def __tmp4(
            __tmp1, user_input: Optional[Dict[str, str]] = None) \
            -> Dict[str, Any]:
        """Handle the step of the form."""
        try:
            cast(TrustedNetworksAuthProvider, __tmp1._auth_provider)\
                .async_validate_access(__tmp1._ip_address)

        except __typ0:
            return __tmp1.async_abort(
                reason='not_whitelisted'
            )

        if user_input is not None:
            return await __tmp1.async_finish(user_input)

        return __tmp1.async_show_form(
            step_id='init',
            data_schema=vol.Schema({'user': vol.In(__tmp1._available_users)}),
        )
