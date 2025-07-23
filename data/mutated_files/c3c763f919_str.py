from typing import TypeAlias
__typ1 : TypeAlias = "Any"
__typ0 : TypeAlias = "bool"
"""Example auth module."""
import logging
from typing import Any, Dict

import voluptuous as vol

from homeassistant.core import HomeAssistant

from . import MultiFactorAuthModule, MULTI_FACTOR_AUTH_MODULES, \
    MULTI_FACTOR_AUTH_MODULE_SCHEMA, SetupFlow

CONFIG_SCHEMA = MULTI_FACTOR_AUTH_MODULE_SCHEMA.extend({
    vol.Required('data'): [vol.Schema({
        vol.Required('user_id'): str,
        vol.Required('pin'): str,
    })]
}, extra=vol.PREVENT_EXTRA)

_LOGGER = logging.getLogger(__name__)


@MULTI_FACTOR_AUTH_MODULES.register('insecure_example')
class InsecureExampleModule(MultiFactorAuthModule):
    """Example auth module validate pin."""

    DEFAULT_TITLE = 'Insecure Personal Identify Number'

    def __init__(__tmp1, __tmp8, __tmp7: Dict[str, __typ1]) -> None:
        """Initialize the user data store."""
        super().__init__(__tmp8, __tmp7)
        __tmp1._data = __tmp7['data']

    @property
    def __tmp6(__tmp1) :
        """Validate login flow input data."""
        return vol.Schema({'pin': str})

    @property
    def setup_schema(__tmp1) :
        """Validate async_setup_user input data."""
        return vol.Schema({'pin': str})

    async def __tmp11(__tmp1, __tmp9) -> SetupFlow:
        """Return a data entry flow handler for setup module.

        Mfa module should extend SetupFlow
        """
        return SetupFlow(__tmp1, __tmp1.setup_schema, __tmp9)

    async def __tmp5(__tmp1, __tmp9, __tmp4: __typ1) -> __typ1:
        """Set up user to use mfa module."""
        # data shall has been validate in caller
        pin = __tmp4['pin']

        for data in __tmp1._data:
            if data['user_id'] == __tmp9:
                # already setup, override
                data['pin'] = pin
                return

        __tmp1._data.append({'user_id': __tmp9, 'pin': pin})

    async def __tmp0(__tmp1, __tmp9) :
        """Remove user from mfa module."""
        found = None
        for data in __tmp1._data:
            if data['user_id'] == __tmp9:
                found = data
                break
        if found:
            __tmp1._data.remove(found)

    async def __tmp2(__tmp1, __tmp9: <FILL>) -> __typ0:
        """Return whether user is setup."""
        for data in __tmp1._data:
            if data['user_id'] == __tmp9:
                return True
        return False

    async def __tmp3(
            __tmp1, __tmp9, __tmp10) :
        """Return True if validation passed."""
        for data in __tmp1._data:
            if data['user_id'] == __tmp9:
                # user_input has been validate in caller
                if data['pin'] == __tmp10['pin']:
                    return True

        return False
