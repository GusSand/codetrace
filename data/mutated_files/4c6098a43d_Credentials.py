from typing import TypeAlias
__typ5 : TypeAlias = "LoginFlow"
__typ7 : TypeAlias = "UserMeta"
__typ4 : TypeAlias = "str"
__typ6 : TypeAlias = "bool"
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


class __typ1(HomeAssistantError):
    """Raised when try to login as invalid user."""


@AUTH_PROVIDERS.register('trusted_networks')
class __typ2(AuthProvider):
    """Trusted Networks auth provider.

    Allow passwordless access from trusted network.
    """

    DEFAULT_TITLE = 'Trusted Networks'

    @property
    def support_mfa(__tmp0) :
        """Trusted Networks auth provider does not support MFA."""
        return False

    async def async_login_flow(__tmp0, context) -> __typ5:
        """Return a flow to login."""
        assert context is not None
        users = await __tmp0.store.async_get_users()
        available_users = {user.id: user.name
                           for user in users
                           if not user.system_generated and user.is_active}

        return __typ3(
            __tmp0, cast(__typ4, context.get('ip_address')), available_users)

    async def async_get_or_create_credentials(
            __tmp0, flow_result) :
        """Get credentials based on the flow result."""
        user_id = flow_result['user']

        users = await __tmp0.store.async_get_users()
        for user in users:
            if (not user.system_generated and
                    user.is_active and
                    user.id == user_id):
                for credential in await __tmp0.async_credentials():
                    if credential.data['user_id'] == user_id:
                        return credential
                cred = __tmp0.async_create_credentials({'user_id': user_id})
                await __tmp0.store.async_link_user(user, cred)
                return cred

        # We only allow login as exist user
        raise __typ1

    async def async_user_meta_for_credentials(
            __tmp0, credentials: <FILL>) -> __typ7:
        """Return extra user metadata for credentials.

        Trusted network auth provider should never create new user.
        """
        raise NotImplementedError

    @callback
    def async_validate_access(__tmp0, ip_address: __typ4) :
        """Make sure the access from trusted networks.

        Raise InvalidAuthError if not.
        Raise InvalidAuthError if trusted_networks is not configured.
        """
        hass_http = getattr(__tmp0.hass, 'http', None)  # type: HomeAssistantHTTP

        if not hass_http or not hass_http.trusted_networks:
            raise __typ0('trusted_networks is not configured')

        if not any(ip_address in trusted_network for trusted_network
                   in hass_http.trusted_networks):
            raise __typ0('Not in trusted_networks')


class __typ3(__typ5):
    """Handler for the login flow."""

    def __init__(__tmp0, auth_provider: __typ2,
                 ip_address, available_users: Dict[__typ4, Optional[__typ4]]) \
            :
        """Initialize the login flow."""
        super().__init__(auth_provider)
        __tmp0._available_users = available_users
        __tmp0._ip_address = ip_address

    async def async_step_init(
            __tmp0, user_input: Optional[Dict[__typ4, __typ4]] = None) \
            -> Dict[__typ4, Any]:
        """Handle the step of the form."""
        try:
            cast(__typ2, __tmp0._auth_provider)\
                .async_validate_access(__tmp0._ip_address)

        except __typ0:
            return __tmp0.async_abort(
                reason='not_whitelisted'
            )

        if user_input is not None:
            return await __tmp0.async_finish(user_input)

        return __tmp0.async_show_form(
            step_id='init',
            data_schema=vol.Schema({'user': vol.In(__tmp0._available_users)}),
        )
