"""Example auth provider."""
from collections import OrderedDict
import hmac
from typing import Any, Dict, Optional, cast

import voluptuous as vol

from homeassistant.exceptions import HomeAssistantError
from homeassistant.core import callback

from . import AuthProvider, AUTH_PROVIDER_SCHEMA, AUTH_PROVIDERS, LoginFlow
from ..models import Credentials, UserMeta


USER_SCHEMA = vol.Schema({
    vol.Required('username'): str,
    vol.Required('password'): str,
    vol.Optional('name'): str,
})


CONFIG_SCHEMA = AUTH_PROVIDER_SCHEMA.extend({
    vol.Required('users'): [USER_SCHEMA]
}, extra=vol.PREVENT_EXTRA)


class InvalidAuthError(HomeAssistantError):
    """Raised when submitting invalid authentication."""


@AUTH_PROVIDERS.register('insecure_example')
class __typ0(AuthProvider):
    """Example auth provider based on hardcoded usernames and passwords."""

    async def __tmp2(__tmp1, context) :
        """Return a flow to login."""
        return ExampleLoginFlow(__tmp1)

    @callback
    def async_validate_login(__tmp1, username, password: str) :
        """Validate a username and password."""
        user = None

        # Compare all users to avoid timing attacks.
        for usr in __tmp1.config['users']:
            if hmac.compare_digest(username.encode('utf-8'),
                                   usr['username'].encode('utf-8')):
                user = usr

        if user is None:
            # Do one more compare to make timing the same as if user was found.
            hmac.compare_digest(password.encode('utf-8'),
                                password.encode('utf-8'))
            raise InvalidAuthError

        if not hmac.compare_digest(user['password'].encode('utf-8'),
                                   password.encode('utf-8')):
            raise InvalidAuthError

    async def async_get_or_create_credentials(
            __tmp1, __tmp0: Dict[str, str]) -> Credentials:
        """Get credentials based on the flow result."""
        username = __tmp0['username']

        for credential in await __tmp1.async_credentials():
            if credential.data['username'] == username:
                return credential

        # Create new credentials.
        return __tmp1.async_create_credentials({
            'username': username
        })

    async def async_user_meta_for_credentials(
            __tmp1, credentials: <FILL>) -> UserMeta:
        """Return extra user metadata for credentials.

        Will be used to populate info when creating a new user.
        """
        username = credentials.data['username']
        name = None

        for user in __tmp1.config['users']:
            if user['username'] == username:
                name = user.get('name')
                break

        return UserMeta(name=name, is_active=True)


class ExampleLoginFlow(LoginFlow):
    """Handler for the login flow."""

    async def __tmp3(
            __tmp1, user_input: Optional[Dict[str, str]] = None) \
            -> Dict[str, Any]:
        """Handle the step of the form."""
        errors = {}

        if user_input is not None:
            try:
                cast(__typ0, __tmp1._auth_provider)\
                    .async_validate_login(user_input['username'],
                                          user_input['password'])
            except InvalidAuthError:
                errors['base'] = 'invalid_auth'

            if not errors:
                user_input.pop('password')
                return await __tmp1.async_finish(user_input)

        schema = OrderedDict()  # type: Dict[str, type]
        schema['username'] = str
        schema['password'] = str

        return __tmp1.async_show_form(
            step_id='init',
            data_schema=vol.Schema(schema),
            errors=errors,
        )
